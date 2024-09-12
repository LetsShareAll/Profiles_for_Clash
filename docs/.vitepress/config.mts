import { defineConfig } from "vitepress";

export default defineConfig({
  // https://vitepress.dev/reference/site-config
  title: "Profiles for Clash",
  titleTemplate: true,
  description: "适用于 Clash 的配置文件的文档。",
  head: [
    [
      "link",
      {
        rel: "icon",
        href: "/icon/clash-light.png",
      },
    ],
    [
      "script",
      { async: "", src: "https://www.googletagmanager.com/gtag/js?id=TAG_ID" },
    ],
    [
      "script",
      {},
      `window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'TAG_ID');`,
    ],
  ],
  lang: "zh-CN",
  base: "/",
  locales: {
    root: {
      label: "中文",
      lang: "zh",
    },
    en: {
      label: "English",
      lang: "en",
      link: "/en/",
    },
  },

  cleanUrls: true,
  rewrites: { "source/:page": "destination/:page" }, // https://vitepress.dev/zh/guide/routing#route-rewrites

  srcDir: ".",
  srcExclude: ["**/README.md", "**/TODO.md"], // https://github.com/mrmlnc/fast-glob#pattern-syntax
  outDir: "./.vitepress/dist",
  assetsDir: "assets",
  cacheDir: "./.vitepress/cache",
  ignoreDeadLinks: true,
  metaChunk: true,
  mpa: true,

  appearance: true,
  lastUpdated: true,

  markdown: {
    // https://github.com/vuejs/vitepress/blob/main/src/node/markdown/markdown.ts
    // preConfig: "",
    // config: "",
    cache: true,
    // externalLinks: "",

    theme: {
      // https://shiki.style/themes#bundled-themes
      light: "solarized-light",
      dark: "solarized-dark",
    },
    languages: [
      // https://shiki.style/languages#bundled-languages
    ],
    languageAlias: {
      // https://shiki.style/guide/load-lang#custom-language-aliases
    },
    lineNumbers: true,
    defaultHighlightLang: "shellscript",
    codeTransformers: [
      // https://shiki.style/guide/transformers#transformers
      {
        code(node) {
          this.addClassToHast(node, "language-js");
        },
        line(node, line) {
          node.properties["data-line"] = line;
          if ([1, 3, 4].includes(line)) this.addClassToHast(node, "highlight");
        },
        span(node, line, col) {
          node.properties["data-token"] = `token:${line}:${col}`;
        },
      },
    ],
    shikiSetup() {},
    codeCopyButtonTitle: "复制代码",

    anchor: {
      // https://github.com/valeriangalliat/markdown-it-anchor#usage
      level: 1,
      // permalink: {
      //   // https://github.com/valeriangalliat/markdown-it-anchor#permalinks
      //   class: "header-anchor",
      //   symbol: "#",
      //   renderHref: "",
      //   renderAttrs: "",
      //   headerLink: {
      //     // https://github.com/valeriangalliat/markdown-it-anchor?tab=readme-ov-file#common-options
      //     safariReaderFix: false,
      //   },
      //   linkAfterHeader: {
      //     // https://github.com/valeriangalliat/markdown-it-anchor?tab=readme-ov-file#common-options
      //     style: "visually-hidden",
      //     assistiveText: (title) => `Permalink to “${title}”`,
      //     visuallyHiddenClass: "visually-hidden",
      //     space: true,
      //     placement: "after",
      //     wrapper: ['<div class="wrapper">', "</div>"],
      //   },
      //   linkInsideHeader: {
      //     // https://github.com/valeriangalliat/markdown-it-anchor?tab=readme-ov-file#common-options
      //     space: "&nbsp;",
      //     placement: "after",
      //     ariaHidden: true,
      //   },
      //   ariaHidden: {
      //     placement: "before",
      //   },
      // },
      // slugify: "",
      callback() {},
      // getTokensText: [],
      tabIndex: -1,
      uniqueSlugStartIndex: 1,
    },
    attrs: {
      // https://github.com/arve0/markdown-it-attrs?tab=readme-ov-file#usage
      leftDelimiter: "{",
      rightDelimiter: "}",
      allowedAttributes: [""],
      disable: false,
    },
    emoji: {
      // https://github.com/markdown-it/markdown-it-emoji?tab=readme-ov-file#use
      defs: {},
      enabled: [],
      shortcuts: {},
    },
    frontmatter: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-frontmatter#options
      grayMatterOptions: {
        // https://github.com/jonschlinkert/gray-matter?tab=readme-ov-file#usage
        excerpt: true,
        excerpt_separator: "<!-- end -->",
        engines: {},
        language: "",
        delimiters: ["---", "---"],
      },
      renderExcerpt: true,
    },
    headers: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-headers#options
      // format: "",
      level: [2, 3],
      shouldAllowNested: false,
      // slugify: "@mdit-vue/shared",
    },
    sfc: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-sfc#options
      customBlocks: [""],
    },
    toc: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-toc#options
      pattern: /^[[toc]]$/i,
      // slugify: "@mdit-vue/shared",
      // format: "",
      level: [2, 3],
      shouldAllowNested: false,
      containerTag: "nav",
      containerClass: "table-of-contents",
      listTag: "ul",
      listClass: "",
      itemClass: "",
      linkTag: "router-link",
      linkClass: "",
    },
    component: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-component#options\
      blockTags: [],
      inlineTags: [],
    },
    container: {
      // https://github.com/markdown-it/markdown-it-container?tab=readme-ov-file
    },
    math: true,
    image: { lazyLoading: false },
    gfmAlerts: true,
  },
  vite: {
    // https://vitejs.dev/config/
  },
  vue: {
    // https://github.com/vitejs/vite-plugin-vue/tree/main/packages/plugin-vue#options
  },

  async buildEnd(siteConfig) {},
  async postRender(context) {},
  async transformHead(context) {},
  async transformHtml(code, id, context) {},
  async transformPageData(pageData, { siteConfig }) {},

  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    i18nRouting: true,
    logo: {
      light: "/icon/clash-light.png",
      dark: "/icon/clash-dark.png",
      alt: "Clash",
    },
    siteTitle: "PFC",
    nav: [
      { text: "项目介绍", link: "/introduction" },
      { text: "指引目录", link: "/guide/" },
      {
        text: "脚本使用",
        activeMatch: "/guide/script/usage",
        items: [
          {
            text: "基本使用",
            items: [
              {
                text: "Github Actions",
                link: "/guide/script/usage#github-actions",
              },
              { text: "本地执行", link: "/guide/script/usage#本地执行" },
            ],
          },
          { text: "高级使用", link: "/guide/script/usage#高级使用" },
        ],
      },
    ],
    sidebar: [
      {
        text: "Profiles for Clash",
        items: [
          {
            text: "项目指引",
            collapsed: false,
            items: [
              // This shows `/guide/index.md` page.
              { text: "项目介绍", link: "/introduction" },
              { text: "指引目录", link: "/guide/" },
            ],
          },
          {
            text: "脚本使用",
            collapsed: true,
            items: [
              { text: "使用教程", link: "/guide/script/usage" },
              { text: "脚本配置", link: "/guide/script/config" },
            ],
          },
          {
            text: "Clash 教程",
            collapsed: true,
            items: [{ text: "配置使用", link: "/guide/clash/profile" }],
          },
        ],
      },
    ],
    aside: true,
    outline: {
      level: [2, 3],
      label: "此页目录",
    },
    socialLinks: [
      {
        icon: "github",
        link: "https://github.com/LetsShareAll/Profiles_for_Clash",
        ariaLabel: "GitHub",
      },
      {
        icon: {
          svg: '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>QQ</title><path d="M12.003 2c-2.265 0-6.29 1.364-6.29 7.325v1.195S3.55 14.96 3.55 17.474c0 .665.17 1.025.281 1.025.114 0 .902-.484 1.748-2.072 0 0-.18 2.197 1.904 3.967 0 0-1.77.495-1.77 1.182 0 .686 4.078.43 6.29 0 2.239.425 6.287.687 6.287 0 0-.688-1.768-1.182-1.768-1.182 2.085-1.77 1.905-3.967 1.905-3.967.845 1.588 1.634 2.072 1.746 2.072.111 0 .283-.36.283-1.025 0-2.514-2.166-6.954-2.166-6.954V9.325C18.29 3.364 14.268 2 12.003 2z" fill-rule="evenodd" /></svg>',
        },
        link: "https://jq.qq.com/?_wv=1027&k=8JXp7Rs4",
        ariaLabel: "QQ",
      },
    ],
    footer: {
      message: "基于 MIT 许可发布",
      copyright: "版权所有 © 2021-今 一起分享吧",
    },
    editLink: {
      pattern:
        "https://github.com/LetsShareAll/Profiles_for_Clash/edit/gh-pages/docs/:path",
      text: "在 GitHub 上编辑",
    },
    lastUpdated: {
      text: "最后更新于",
      formatOptions: {
        dateStyle: "full",
        timeStyle: "medium",
      },
    },
    search: {
      provider: "local",
      options: {
        locales: {
          root: {
            translations: {
              button: {
                buttonText: "搜索文档",
                buttonAriaLabel: "搜索文档",
              },
              modal: {
                noResultsText: "无法找到相关结果",
                resetButtonTitle: "清除查询条件",
                footer: {
                  selectText: "选择",
                  navigateText: "切换",
                  closeText: "关闭",
                },
              },
            },
          },
        },
        miniSearch: {
          // https://lucaong.github.io/minisearch/classes/MiniSearch.MiniSearch.html
          options: {
            /* ... */
          },
          searchOptions: {
            /* ... */
          },
        },
        _render(src, env, md) {
          const html = md.render(src, env);
          if (env.frontmatter?.search === false) return "";
          if (env.relativePath.startsWith("some/path")) return "";
          if (env.frontmatter?.title)
            return md.render(`# ${env.frontmatter.title}`) + html;
          return html;
        },
      },
    },
    // carbonAds: {
    //   // https://vitepress.dev/zh/reference/default-theme-carbon-ads
    //   code: "",
    //   placement: "",
    // },
    docFooter: {
      prev: "上一页",
      next: "下一页",
    },
    darkModeSwitchLabel: "外观",
    lightModeSwitchTitle: "切换至亮色主题",
    darkModeSwitchTitle: "切换至暗色主题",
    sidebarMenuLabel: "菜单",
    returnToTopLabel: "回到顶部",
    langMenuLabel: "切换语言",
    externalLinkIcon: true,
  },
});
