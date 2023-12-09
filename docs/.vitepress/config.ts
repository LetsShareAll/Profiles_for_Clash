export default {
  appearance: true, // Whether to enable "Dark Mode" or not.
  base: "/", // The base URL the site will be deployed at.
  description: "适用于 Clash 的配置文件的文档。", // Description for the site.
  head: [
    // Additional elements to render in the <head> tag in the page HTML.
    [
      "link",
      {
        rel: "stylesheet",
        href: "https://file.lssa.fun/others/styles/genshin-font.css",
        type: "text/css",
      },
    ],
    [
      "link",
      {
        rel: "icon",
        href: "https://file.lssa.fun/pictures/clash-light.png",
      },
    ],
  ],
  ignoreDeadLinks: true, // VitePress will not fail builds due to dead links.
  lang: "zh-CN", // The lang attribute for the site.
  lastUpdated: true, // Use git commit to get the timestamp.
  markdown: {
    // Configure Markdown parser options.
    theme: {
      // https://github.com/shikijs/shiki/blob/main/docs/themes.md#all-themes
      light: "material-lighter",
      dark: "material-darker",
    },
    lineNumbers: true,
    anchor: {
      // https://github.com/valeriangalliat/markdown-it-anchor#usage
      level: 1, // Minimum level to apply anchors, or array of selected levels.
      // permalink: {
      //   // https://github.com/valeriangalliat/markdown-it-anchor#permalinks
      //   class: "header-anchor", // The class of the permalink anchor.
      //   symbol: "#", // The symbol in the permalink anchor.
      //   renderHref: "", // A custom permalink href rendering function.
      //   renderAttrs: "", // A custom permalink attributes rendering function.
      //   headerLink: {
      //     // This style wraps the header itself in an anchor link.
      //     safariReaderFix: false, // Add a span inside the link so Safari shows headings in reader view.
      //   },
      //   linkAfterHeader: {
      //     // Customize further the screen reader experience of your permalinks.
      //     style: "visually-hidden", // The (sub) style of link, one of visually-hidden, aria-label, aria-describedby or aria-labelledby.
      //     assistiveText: (title) => `Permalink to “${title}”`, // A function that takes the title and returns the assistive text.
      //     visuallyHiddenClass: "visually-hidden", // The class you use to make an element visually hidden.
      //     space: true, // Add a space between the assistive text and the permalink symbol.
      //     placement: "after", // Placement of the permalink symbol relative to the assistive text.
      //     wrapper: ['<div class="wrapper">', "</div>"], // Opening and closing wrapper string.
      //   },
      //   linkInsideHeader: {
      //     // This is the equivalent of the default permalink in previous versions.
      //     space: "&nbsp;", // Add a space between the header text and the permalink symbol.
      //     placement: "after", // Placement of the permalink.
      //     ariaHidden: true, // Makes the permalink explicitly inaccessible.
      //   },
      //   ariaHidden: {
      //     placement: "before",
      //   },
      // },
    },
    attrs: {
      //https://github.com/arve0/markdown-it-attrs
      leftDelimiter: "{",
      rightDelimiter: "}",
      allowedAttributes: [""], // Empty array means all attributes are allowed.
      disable: false,
    },
    frontmatter: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-frontmatter#options
      grayMatterOptions: {
        // https://github.com/jonschlinkert/gray-matter
        excerpt: true, // Extract an excerpt that directly follows front-matter, or is the first thing in the string if no front-matter exists.
        excerpt_separator: "<!-- end -->", // Define a custom separator to use for excerpts.
        engines: {}, // Engines may either be an object with parse and (optionally) stringify methods, or a function that will be used for parsing only.
        language: "", // Define the engine to use for parsing front-matter.
        delimiters: ["---", "---"], // Open and close delimiters can be passed in as an array of strings.
      },
      renderExcerpt: true, // Render the excerpt with markdown-it or not.
    },
    headers: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-headers#options
      // format: "", // A function for formatting header title.
      level: [2, 3], // Heading level that going to be extracted.
      // slugify: "@mdit-vue/shared", // A custom slugification function.
    },
    sfc: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-sfc#options
      customBlocks: [""], // SFC custom blocks to be extracted.
    },
    toc: {
      // https://github.com/mdit-vue/mdit-vue/tree/main/packages/plugin-toc#options
      pattern: /^[[toc]]$/i, // The pattern serving as the TOC placeholder in your markdown.
      slugify: "@mdit-vue/shared", // A custom slugification function.
      // format: "", // A function for formatting headings.
      level: [2, 3], // Heading level that going to be included in the TOC.
      containerTag: "nav", // HTML tag of the TOC container.
      containerClass: "table-of-contents", // The class for the TOC container.
      listTag: "ul", // HTML tag of the TOC list.
      listClass: "", // The class for the TOC list.
      itemClass: "", // The class for the <li> tag.
      linkTag: "router-link", // The tag of the link inside the <li> tag.
      linkClass: "", // The class for the link inside the <li> tag.
    },
    config: "", // Configure the Markdown-it instance.
  },
  outDir: "", // The build output location for the site.
  title: "Profiles for Clash", // Title for the site.
  titleTemplate: "适用于 Clash 的配置文件", // The suffix for the title.
  cleanUrls: "without-subfolders", // Allows removing trailing .html from URLs and, optionally, generating clean directory structure.
  async transformHead(ctx) {
    // A build hook to transform the head before generating each page.
  },
  async transformHtml(code, id, context) {
    // A build hook to transform the content of each page before saving to disk.
  },
  async buildEnd(siteConfig) {
    // It will run after build (SSG) finish but before VitePress CLI process exits.
  },
  themeConfig: {
    // Theme configs let you customize your theme.
    logo: {
      // Logo file to display in nav bar, right before the site title.
      light: {
        src: "https://file.lssa.fun/pictures/clash-light.png",
        alt: "Clash",
      },
      dark: {
        src: "https://file.lssa.fun/pictures/clash-dark.png",
        alt: "Clash",
      },
    },
    siteTitle: "Profiles for Clash", // You can customize this item to replace the default site title (title in app config) in nav.
    nav: [
      // The configuration for the nav menu item.
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
      // The configuration for the sidebar menu item.
      {
        text: "项目指引",
        collapsible: true,
        collapsed: false,
        items: [
          // This shows `/guide/index.md` page.
          { text: "项目介绍", link: "/introduction" },
          { text: "指引目录", link: "/guide/" },
        ],
      },
      {
        text: "脚本使用",
        collapsible: true,
        collapsed: true,
        items: [
          { text: "使用教程", link: "/guide/script/usage" },
          { text: "脚本配置", link: "/guide/script/config" },
        ],
      },
      {
        text: "Clash 教程",
        collapsible: true,
        collapsed: true,
        items: [{ text: "配置使用", link: "/guide/clash/profile" }],
      },
    ],
    outline: [2, 3], // The levels of header to display in the outline.
    outlineTitle: "此页目录", // Can be used to customize the title of the right sidebar (on the top of outline links).
    socialLinks: [
      // You may define this option to show your social account links with icons in nav.
      {
        icon: "github",
        link: "https://github.com/LetsShareAll/Profiles_for_Clash",
      },
      // You can also add custom icons by passing SVG as string:
      {
        icon: {
          svg: '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>QQ</title><path d="M12.003 2c-2.265 0-6.29 1.364-6.29 7.325v1.195S3.55 14.96 3.55 17.474c0 .665.17 1.025.281 1.025.114 0 .902-.484 1.748-2.072 0 0-.18 2.197 1.904 3.967 0 0-1.77.495-1.77 1.182 0 .686 4.078.43 6.29 0 2.239.425 6.287.687 6.287 0 0-.688-1.768-1.182-1.768-1.182 2.085-1.77 1.905-3.967 1.905-3.967.845 1.588 1.634 2.072 1.746 2.072.111 0 .283-.36.283-1.025 0-2.514-2.166-6.954-2.166-6.954V9.325C18.29 3.364 14.268 2 12.003 2z" fill-rule="evenodd" /></svg>',
        },
        link: "https://jq.qq.com/?_wv=1027&k=8JXp7Rs4",
      },
    ],
    footer: {
      // Footer configuration.
      message: "在 MIT 许可证下发布。",
      copyright: "版权所有 © 2022 - 今 Shuery",
    },
    editLink: {
      // Edit Link lets you display a link to edit the page on Git management services such as GitHub, or GitLab.
      pattern:
        "https://github.com/LetsShareAll/Profiles_for_Clash/edit/gh-pages/docs/:path",
      text: "在 GitHub 上编辑此页",
    },
    lastUpdatedText: "最后更新时间", // The prefix text showing right before the last updated time.
    // carbonAds: {
    //   // A option to display Carbon Ads.
    //   code: 'your-carbon-code',
    //   placement: 'your-carbon-placement'
    // }
    docFooter: {
      // Can be used to customize text appearing above previous and next links.
      prev: "上一页",
      next: "下一页",
    },
  },
};
