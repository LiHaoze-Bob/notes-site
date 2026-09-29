# Astro Theme Pure attribution

This site uses the published `astro-pure` 1.4.9 package and Astro 6.4.8.

The following files derive from [cworld1/astro-theme-pure](https://github.com/cworld1/astro-theme-pure), commit `4ecd4762e1e750daf7a51978092d7cea8e14c0d6`, under the Apache License 2.0 (retained in `PURE-LICENSE`):

- `src/components/Header.astro`: imports refer to the package; brand/search links honor the GitHub Pages base path.
- `src/layouts/ContentLayout.astro`: local configuration import and back link adjusted; passes the page's math requirement through to the base layout.
- `src/styles/app.css`: original theme colors.
- `uno.config.ts`: original typography and utility configuration.

Pure's footer, theme provider, table of contents, back-to-top control, button and Pagefind search components come directly from the pinned package.

Site-specific layouts, note listings, public snapshot adapter, code-copy controls, and Obsidian compatibility styles are maintained in this repository. Fonts, icons, and MathJax retain the notices listed in `site-template/THIRD_PARTY.md`.
