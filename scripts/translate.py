import os
import re
import argparse
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def load_model(model_name="facebook/nllb-200-distilled-600M"):
    """Load NLLB translation model for English to Chinese translation."""
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return model, tokenizer

def translate_batch(texts, model, tokenizer):
    """Translate English texts to Chinese using NLLB model."""
    if not texts:
        return []
    
    # NLLB uses language codes: eng_Latn for English, zho_Hans for Simplified Chinese
    tokenizer.src_lang = "eng_Latn"
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    translated = model.generate(
        **inputs, 
        forced_bos_token_id=tokenizer.convert_tokens_to_ids("zho_Hans"),
        max_length=512
    )
    result = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
    return result

def protect_content(content):
    protected = []
    
    def make_placeholder(match):
        protected.append(match.group(0))
        # Use special Unicode brackets that won't be translated
        return f"⟦KEEP⟧{len(protected)-1}⟦/KEEP⟧"
    
    patterns = [
        (r'```[\s\S]*?```', 'code_block'),
        (r'`[^`\n]+?`', 'inline_code'),
        (r'<[^>]+>', 'html_tag'),
        (r'!\[([^\]]*)\]\([^\)]+\)', 'image'),
        (r'\[([^\]]+)\]\(([^\)]+)\)', 'link'),
        (r'https?://[^\s\)]+', 'bare_url'),
    ]
    
    for pattern, _ in patterns:
        content = re.sub(pattern, make_placeholder, content)
    
    return content, protected

def restore_content(content, protected):
    for i, item in enumerate(protected):
        content = content.replace(f"⟦KEEP⟧{i}⟦/KEEP⟧", item)
    return content

def extract_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return f"---{parts[1]}---", parts[2]
    return "", content

def translate_markdown_file(file_path, model, tokenizer):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    frontmatter, main_content = extract_frontmatter(content)
    
    protected_content, protected_items = protect_content(main_content)
    
    lines = protected_content.split('\n')
    translated_lines = []
    
    batch_lines = []
    batch_indices = []
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        
        if not stripped or re.match(r'^⟦KEEP⟧\d+⟦/KEEP⟧$', stripped) or re.match(r'^[\*\-]{3,}$', stripped):
            translated_lines.append(line)
            continue
        
        if re.match(r'^#+\s+', line):
            header_match = re.match(r'^(#+\s+)(.+)$', line)
            if header_match:
                prefix, text = header_match.groups()
                protected_text, text_protected = protect_content(text)
                batch_lines.append(protected_text)
                batch_indices.append((idx, 'header', prefix, text_protected))
                translated_lines.append("")
            else:
                translated_lines.append(line)
            continue
        
        if re.match(r'^[\*\-\+]\s+', line) or re.match(r'^\d+\.\s+', line):
            list_match = re.match(r'^([\*\-\+]\s+|\d+\.\s+)(.+)$', line)
            if list_match:
                prefix, text = list_match.groups()
                protected_text, text_protected = protect_content(text)
                batch_lines.append(protected_text)
                batch_indices.append((idx, 'list', prefix, text_protected))
                translated_lines.append("")
            else:
                translated_lines.append(line)
            continue
        
        protected_line, line_protected = protect_content(line)
        batch_lines.append(protected_line)
        batch_indices.append((idx, 'plain', None, line_protected))
        translated_lines.append("")
    
    if batch_lines:
        sub_batch_size = 8
        results = []
        for i in range(0, len(batch_lines), sub_batch_size):
            sub_batch = batch_lines[i:i+sub_batch_size]
            results.extend(translate_batch(sub_batch, model, tokenizer))
        
        for i, batch_item in enumerate(batch_indices):
            idx, item_type, prefix, line_protected = batch_item
            translated_text = results[i]
            restored_text = restore_content(translated_text, line_protected)
            
            if item_type == 'header':
                translated_lines[idx] = prefix + restored_text
            elif item_type == 'list':
                translated_lines[idx] = prefix + restored_text
            else:
                translated_lines[idx] = restored_text
    
    result_content = "\n".join(translated_lines)
    result_content = restore_content(result_content, protected_items)
    
    final_output = frontmatter
    if frontmatter and not frontmatter.endswith('\n'):
        final_output += '\n'
    final_output += result_content
    
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
    
    all_files.sort()
    
    total_files = len(all_files)
    
    # Use round-robin distribution for better load balancing
    # Shard 1 gets files [0, total_shards, 2*total_shards, ...]
    # Shard 2 gets files [1, total_shards+1, 2*total_shards+1, ...]
    # This ensures even distribution even when files vary in size
    files_to_process = [
        all_files[i] for i in range(args.shard_index - 1, total_files, args.total_shards)
    ]
    
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
