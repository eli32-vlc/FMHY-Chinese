/**
 *  Copyright (c) 2025 taskylizard. Apache License 2.0.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

import type { DefaultTheme } from 'vitepress'
import consola from 'consola'
import { transform, transformGuide } from './transformer'

// @unocss-include

export const meta = {
  name: 'freemediaheckyeah',
  description: 'The largest collection of free stuff on the internet!',
  hostname: 'https://fmhy.net',
  keywords: ['stream', 'movies', 'gaming', 'reading', 'anime'],
  build: {
    api: true,
    nsfw: true
  }
}

export const excluded = [
  'readme.md',
  'single-page',
  'feedback.md',
  'index.md',
  'sandbox.md',
  'startpage.md'
]

if (process.env.FMHY_BUILD_NSFW === 'false') {
  consola.info('FMHY_BUILD_NSFW is set to false, disabling NSFW content')
  meta.build.nsfw = false
}
if (process.env.FMHY_BUILD_API === 'false') {
  consola.info('FMHY_BUILD_API is set to false, disabling API component')
  meta.build.api = false
}

const formatCommitRef = (commitRef: string) =>
  `<a href="https://github.com/fmhy/edit/commit/${commitRef}">${commitRef.slice(0, 8)}</a>`

export const commitRef =
  process.env.CF_PAGES && process.env.CF_PAGES_COMMIT_SHA
    ? formatCommitRef(process.env.CF_PAGES_COMMIT_SHA)
    : process.env.COMMIT_REF
      ? formatCommitRef(process.env.COMMIT_REF)
      : 'dev'

export const feedback = `<a href="/feedback" class="feedback-footer">Made with ❤</a>`

export const search: DefaultTheme.Config['search'] = {
  options: {
    _render(src, env, md) {
      // Check if current file should be excluded from search
      const relativePath = env.relativePath || env.path || ''
      const shouldExclude = excluded.some(excludedFile => 
        relativePath.includes(excludedFile) || 
        relativePath.endsWith(excludedFile)
      )
      
      // Return empty content for excluded files so they don't appear in search
      if (shouldExclude) {
        return ''
      }

      let contents = src
      // I do this as env.frontmatter is not available until I call `md.render`
      if (contents.includes('Beginners Guide'))
        contents = transformGuide(contents)
      contents = transform(contents)
      const html = md.render(contents, env)
      return html
    },
    miniSearch: {
      options: {
        tokenize: (text) => text.split(/[\n\r #%*,=/:;?[\]{}()&]+/u), // simplified charset: removed [-_.@] and non-english chars (diacritics etc.)
        processTerm: (term, fieldName) => {
          // biome-ignore lint/style/noParameterAssign: h
          term = term
            .trim()
            .toLowerCase()
            .replace(/^\.+/, '')
            .replace(/\.+$/, '')
          const stopWords = [
            'frontmatter',
            '$frontmatter.synopsis',
            'and',
            'about',
            'but',
            'now',
            'the',
            'with',
            'you'
          ]
          if (term.length < 2 || stopWords.includes(term)) return false

          if (fieldName === 'text') {
            const parts = term.split('.')
            if (parts.length > 1) {
              const newTerms = [term, ...parts]
                .filter((t) => t.length >= 2)
                .filter((t) => !stopWords.includes(t))
              return newTerms
            }
          }
          return term
        }
      },
      searchOptions: {
        combineWith: 'AND',
        fuzzy: false,
        // @ts-ignore
        boostDocument: (documentId, term, storedFields: Record) => {
          const titles = (storedFields?.titles as string[])
            .filter((t) => Boolean(t))
            .map((t) => t.toLowerCase())
          // Downrank posts
          if (documentId.match(/\/posts/)) return -5
          // Downrank /other
          if (documentId.match(/\/other/)) return -5

          // Uprate if term appears in titles. Add bonus for higher levels (i.e. lower index)
          const titleIndex =
            titles
              .map((t, i) => (t?.includes(term) ? i : -1))
              .find((i) => i >= 0) ?? -1
          if (titleIndex >= 0) return 10000 - titleIndex

          return 1
        }
      }
    },
    detailedView: true
  },
  provider: 'local'
}

export const socialLinks: DefaultTheme.SocialLink[] = [
  { icon: 'github', link: 'https://github.com/fmhy/edit' },
  { icon: 'discord', link: 'https://github.com/fmhy/FMHY/wiki/FMHY-Discord' },
  {
    icon: 'reddit',
    link: 'https://reddit.com/r/FREEMEDIAHECKYEAH'
  }
]

export const nav: DefaultTheme.NavItem[] = [
  { text: '📑 更新日志', link: '/posts/changelog-sites' },
  { text: '📖 词汇表', link: 'https://rentry.org/The-Piracy-Glossary' },
  {
    text: '💾 备份',
    link: '/other/backups'
  },
  {
    text: '🌱 生态系统',
    items: [
      { text: '🌐 搜索', link: '/posts/search' },
      { text: '❓ 常见问题', link: '/other/FAQ' },
      { text: '🔖 书签', link: 'https://github.com/fmhy/bookmarks' },
      { text: '✅ SafeGuard', link: 'https://github.com/fmhy/FMHY-SafeGuard' },
      { text: '🚀 起始页', link: 'https://fmhy.net/startpage' },
      { text: '📋 snowbin', link: 'https://pastes.fmhy.net' },
      { text: '🔎 SearXNG', link: 'https://searx.fmhy.net/' },
      {
        text: '💡 网站探索',
        link: 'https://www.reddit.com/r/FREEMEDIAHECKYEAH/wiki/find-new-sites/'
      },
      {
        text: '😇 SFW FMHY',
        link: 'https://rentry.org/piracy'
      },
      {
        text: '🏠 自托管',
        link: '/other/selfhosting'
      },
      { text: '🏞 壁纸', link: '/other/wallpapers' },
      { text: '💙 反馈', link: '/feedback' }
    ]
  }
]

export const sidebar: DefaultTheme.Sidebar | DefaultTheme.NavItemWithLink[] = [
  {
    text: '<span class="i-twemoji:books"></span> 新手指南',
    link: '/beginners-guide'
  },
  {
    text: '<span class="i-twemoji:newspaper"></span> 文章',
    link: '/posts'
  },
  {
    text: '<span class="i-twemoji:light-bulb"></span> 贡献',
    link: '/other/contributing'
  },
  {
    text: '维基',
    collapsed: false,
    items: [
      {
        text: '<span class="i-twemoji:name-badge"></span> 广告拦截 / 隐私',
        link: '/privacy'
      },
      {
        text: '<span class="i-twemoji:robot"></span> 人工智能',
        link: '/ai'
      },
      {
        text: '<span class="i-twemoji:television"></span> 电影 / 电视 / 动漫',
        link: '/video'
      },
      {
        text: '<span class="i-twemoji:musical-note"></span> 音乐 / 播客 / 电台',
        link: '/audio'
      },
      {
        text: '<span class="i-twemoji:video-game"></span> 游戏 / 模拟',
        link: '/gaming'
      },
      {
        text: '<span class="i-twemoji:green-book"></span> 书籍 / 漫画 / 轻小说',
        link: '/reading'
      },
      {
        text: '<span class="i-twemoji:floppy-disk"></span> 下载',
        link: '/downloading'
      },
      {
        text: '<span class="i-twemoji:cyclone"></span> 种子',
        link: '/torrenting'
      },
      {
        text: '<span class="i-twemoji:brain"></span> 教育',
        link: '/educational'
      },
      {
        text: '<span class="i-twemoji:mobile-phone"></span> Android / iOS',
        link: '/mobile'
      },
      {
        text: '<span class="i-twemoji:penguin"></span> Linux / macOS',
        link: '/linux-macos'
      },
      {
        text: '<span class="i-twemoji:globe-showing-asia-australia"></span> 非英文',
        link: '/non-english'
      },
      {
        text: '<span class="i-twemoji:file-folder"></span> 杂项',
        link: '/misc'
      }
    ]
  },
  {
    text: '工具',
    collapsed: false,
    items: [
      {
        text: '<span class="i-twemoji:laptop"></span> 系统工具',
        link: '/system-tools'
      },
      {
        text: '<span class="i-twemoji:card-file-box"></span> 文件工具',
        link: '/file-tools'
      },
      {
        text: '<span class="i-twemoji:paperclip"></span> 网络工具',
        link: '/internet-tools'
      },
      {
        text: '<span class="i-twemoji:left-speech-bubble"></span> 社交媒体工具',
        link: '/social-media-tools'
      },
      {
        text: '<span class="i-twemoji:memo"></span> 文本工具',
        link: '/text-tools'
      },
      {
        text: '<span class="i-twemoji:alien-monster"></span> 游戏工具',
        link: '/gaming-tools'
      },
      {
        text: '<span class="i-twemoji:camera"></span> 图像工具',
        link: '/image-tools'
      },
      {
        text: '<span class="i-twemoji:videocassette"></span> 视频工具',
        link: '/video-tools'
      },
      {
        text: '<span class="i-twemoji:speaker-high-volume"></span> 音频工具',
        link: '/audio#audio-tools'
      },
      {
        text: '<span class="i-twemoji:red-apple"></span> 教育工具',
        link: '/educational#educational-tools'
      },
      {
        text: '<span class="i-twemoji:man-technologist"></span> 开发工具',
        link: '/developer-tools'
      }
    ]
  },
  {
    text: '更多',
    collapsed: true,
    items: [
      meta.build.nsfw
        ? {
            text: '<span class="i-twemoji:no-one-under-eighteen"></span> NSFW',
            link: 'https://rentry.org/NSFW-Checkpoint'
          }
        : {},
      {
        text: '<span class="i-twemoji:warning"></span> 不安全网站',
        link: '/unsafe'
      },
      {
        text: '<span class="i-twemoji:package"></span> 存储',
        link: '/storage'
      }
    ]
  }
]
