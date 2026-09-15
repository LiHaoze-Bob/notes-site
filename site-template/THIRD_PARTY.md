# Theme assets

Chirpy layouts, styles and JavaScript are provided by the MIT-licensed `jekyll-theme-chirpy` 7.6.0 gem.

`assets/lib/` contains unmodified libraries and fonts from [chirpy-static-assets](https://github.com/cotes2020/chirpy-static-assets), commit `5cde3f0076b62e45fc68291893cf7d93e122adb7`. The bundled font licenses and repository license are retained. MathJax 3.2.2 remains self-hosted in `assets/vendor/mathjax/` with its license.

`_data/locales/en.yml` and `_data/origin/basic.yml` are from Chirpy 7.6.0; changes add the custom tab names and point MathJax to the existing local bundle.

`_includes/post-nav.html` adapts Chirpy 7.6.0's navigation component to link public notes in the same folder by filename instead of site-wide publication date.

`_layouts/home.html` adapts Chirpy 7.6.0's home cards to show section headings and complete public directory paths.

`_includes/topbar.html` adapts Chirpy 7.6.0's top bar to show the exported folder hierarchy in note and directory breadcrumbs, retaining the theme's navigation for other pages.
