
import os
import re
import argparse
from transformers import MarianMTModel, MarianTokenizer

def load_model(model_name="liam168/trans-opus-mt-en-zh"):
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return model, tokenizer

def translate_batch(texts, model, tokenizer):
    if not texts:
        return []
    
    # MarianMT handles batch translation
    # Use standard generate parameters
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(**inputs)
    result = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return result

def replace_code_blocks(content):
    # Placeholders for code blocks to prevent translation
    code_blocks = []
    
    def replacer(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"

    # Regex for fenced code blocks
    pattern = r"```[\s\S]*?```"
    content = re.sub(pattern, replacer, content)
    
    # Regex for inline code
    pattern_inline = r"`[^`]+`"
    content = re.sub(pattern_inline, replacer, content)
    
    return content, code_blocks

def restore_code_blocks(content, code_blocks):
    for i, block in enumerate(code_blocks):
        content = content.replace(f"__CODE_BLOCK_{i}__", block)
    return content

def split_text_preserve_formatting(text):
    # Simple semantic splitting by newlines to preserve paragraph structure
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    
    for line in lines:
        if line.strip() == "":
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []
            chunks.append("")  # Preserve empty line
        elif line.startswith("#") or line.startswith("-") or line.startswith("*") or line.startswith(">"):
             # Structural lines handled separately or as single chunk
             if current_chunk:
                 chunks.append("\n".join(current_chunk))
                 current_chunk = []
             chunks.append(line)
        else:
            current_chunk.append(line)
            
    if current_chunk:
        chunks.append("\n".join(current_chunk))
        
    return chunks

def translate_markdown_file(file_path, model, tokenizer):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Frontmatter handling (basic)
    frontmatter = ""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---\n"
            content = parts[2]
            
    # Protect code blocks
    safe_content, code_blocks = replace_code_blocks(content)
    
    # Split into translatable chunks
    # We split by double newlines to keep paragraphs together roughly
    # For a robust implementation, we'd need a full parser, but splitting by lines/paragraphs acts as a good heuristic
    
    lines = safe_content.split('\n')
    translated_lines = []
    
    batch_lines = []
    batch_indices = []
    
    for idx, line in enumerate(lines):
        if not line.strip():
            translated_lines.append(line)
            continue
        
        # Check if line is a placeholder
        if re.match(r"__CODE_BLOCK_\d+__", line.strip()):
            translated_lines.append(line)
            continue
            
        # Basic heuristic: Check if it's structural markdown that shouldn't be fully translated like urls
        # For simplicity, we translate everything that isn't a code block placeholder
        # Ideally we would extract text from links [text](url), but MarianMT is decent at keeping structure if simple
        
        # Add to batch
        batch_lines.append(line)
        batch_indices.append(idx)
        translated_lines.append("") # Placeholder
        
    # Translate batch
    if batch_lines:
        # Process in smaller sub-batches to avoid OOM
        sub_batch_size = 8
        results = []
        for i in range(0, len(batch_lines), sub_batch_size):
            sub_batch = batch_lines[i:i+sub_batch_size]
            results.extend(translate_batch(sub_batch, model, tokenizer))
            
        for i, original_idx in enumerate(batch_indices):
            translated_lines[original_idx] = results[i]

    # Reassemble
    result_content = "\n".join(translated_lines)
    result_content = restore_code_blocks(result_content, code_blocks)
    
    # Combine with frontmatter
    final_output = frontmatter + result_content
    
    return final_output

def main():
    parser = argparse.ArgumentParser(description="Translate Markdown files.")
    parser.add_argument("--docs_dir", default="docs", help="Directory containing markdown files")
    parser.add_argument("--output_dir", default="docs_translated", help="Output directory")
    parser.add_argument("--shard_index", type=int, default=1, help="Current shard index (1-based)")
    parser.add_argument("--total_shards", type=int, default=1, help="Total number of shards")
    args = parser.parse_args()

    print(f"Loading model...")
    model, tokenizer = load_model()
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    all_files = []
    for root, dirs, files in os.walk(args.docs_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                all_files.append(file_path)
    
    # Sort for deterministic sharding
    all_files.sort()
    
    # Calculate shard range
    total_files = len(all_files)
    chunk_size = (total_files + args.total_shards - 1) // args.total_shards
    start_idx = (args.shard_index - 1) * chunk_size
    end_idx = min(start_idx + chunk_size, total_files)
    
    files_to_process = all_files[start_idx:end_idx]
    
    print(f"Shard {args.shard_index}/{args.total_shards}: Processing {len(files_to_process)} files out of {total_files}")

    for file_path in files_to_process:
        rel_path = os.path.relpath(file_path, args.docs_dir)
        out_path = os.path.join(args.output_dir, rel_path)
        
        out_dir = os.path.dirname(out_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        
        print(f"Translating {file_path}...")
        try:
            translated = translate_markdown_file(file_path, model, tokenizer)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(translated)
        except Exception as e:
            print(f"Error translating {file_path}: {e}")

if __name__ == "__main__":
    main()
