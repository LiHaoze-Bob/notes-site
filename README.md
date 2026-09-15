# sychostar

浙江大学 CS 本科生的课程笔记、知识积累与阅读记录。

[网站](https://lihaoze-bob.github.io/notes-site/) · [部署记录](https://github.com/LiHaoze-Bob/notes-site/actions)

## 日常发布

在 Obsidian 的「网站发布」控制页点击「检查内容」「预览网站」「发布网站」。三个入口由桌面版 Shell commands 插件调用项目脚本。

为要公开的笔记添加布尔属性：

```yaml
publish: true
```

只有 `publish: true` 生效，字符串 `"true"` 会报错，旧的 `published:` 属性不参与发布。正文在 Obsidian 中维护，`docs/` 是自动生成的副本，不要直接编辑。

`publish.toml` 限定课程、技术积累、Tools、Reading 和 Paper 五个源目录。`local.toml` 保存本机 Vault 路径并被 Git 忽略。GitHub Actions 只构建已导出的公开内容。

可选属性 `title` 设置网页标题，`nav_order` 用数字控制同层笔记顺序。目录保留原层级、按数字自然排序；目录名称可在 `publish.toml` 的 `labels` 中设置。

## 图片、链接与撤下页面

支持标准 Markdown 链接、`[[笔记]]`、`[[笔记#标题|文字]]`、`![[图片.png]]` 和图片宽度。建议使用笔记旁的 `assets/` 目录；图片必须位于配置允许的源目录内。程序只复制引用的图片，并通过内容哈希避免同名覆盖。

提示块、折叠提示块和数学公式在导出时适配网站，原文不变；Callout Manager 中定义的自定义类型、颜色和常用图标会一并带到网站，未知类型也保留原名称。代码中的示例语法不会转换。未公开笔记的链接转为文字并提示。缺图、歧义链接、块引用、笔记嵌入、动态 Dataview 和非图片本地附件会阻止发布。

将 `publish` 改成 `false` 后再次发布，对应页面和不再使用的图片会从当前网站及搜索索引移除。已经公开的 Git 历史仍保留旧内容。笔记移动或重命名会改变网址。

## 环境与命令

使用 **Jekyll + 官方 Chirpy 7.6.0**，Ruby 依赖由 `Gemfile.lock` 固定。Python 3.12 负责筛选并转换 Obsidian 笔记，依赖由 `uv.lock` 固定。

新机器先安装 Ruby 3.3；macOS 可用 `brew install ruby@3.3`。在项目根目录执行：

```sh
uv sync --frozen --python 3.12
# macOS Homebrew 安装的 Ruby
export PATH="$(brew --prefix ruby@3.3)/bin:$PATH"
BUNDLE_PATH=.runtime/bundle bundle install
cp local.example.toml local.toml
# 编辑 local.toml，填写本机 Vault 的绝对路径
.venv/bin/python scripts/site.py check
.venv/bin/python scripts/site.py preview
.venv/bin/python scripts/site.py publish
```

发布需要 Git、已登录正确账号的 GitHub CLI。目标固定为 `LiHaoze-Bob/notes-site` 的 `main` 分支；只自动提交 `docs/` 中的公开快照。其他分支、其他 origin、未提交的源码修改会阻止自动发布。

`check` 在临时目录导出、构建并校验内部链接与资源。`preview` 同时启动仅绑定本机的预览服务：`http://127.0.0.1:8765/notes-site/`；再次点击会更新内容并复用服务。

`publish` 完成检查后提交、推送并等待该提交的 GitHub Actions 部署结果，只有成功才提示「已上线」。重复点击受互斥锁保护，内容没变化不会生成空提交。

## 排错

- **缺失图片或歧义链接**：按报错修正引用，使用明确的相对路径。
- **源码未提交**：在网站项目中检查并提交认可的代码修改，再发布。
- **网络、认证或推送失败**：检查 GitHub 登录与连接后重试；脚本不会强制推送。
- **终端可连接、Obsidian 连接超时**：在 `local.toml` 设置 `proxy`，参考示例文件。本机已设置代理，发布时需保持代理应用运行；代理端口变更后同步更新此项。
- **远端有新提交**：在网站项目中检查差异并合并，不要对 Obsidian Vault 执行这些操作。
- **部署失败或超时**：查看仓库 Actions；本地状态保存在 `.runtime/status.json`。
- **控制页无反应或 Working directory 报错**：确认 Shell commands 插件已启用，将 Environments 中的 Working directory 留空（默认使用 Vault 目录），再正常重启 Obsidian。三个入口脚本会自行切换到网站项目目录。
- **移动项目目录**：更新三个命令中的绝对路径，并重建虚拟环境；插件 Working directory 保持留空。

## 网站与主题

完整使用 [Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy) 官方 gem 的布局、样式和脚本，包括首页文章列表、搜索、阅读目录、图片放大、代码复制、明暗切换和 RSS。侧栏依次为 **HOME / COURSE / READING / TECH / ABOUT**。

- `_config.yml`：站名、简介、头像、网址和 Chirpy 功能设置。
- `site-template/_tabs/`：栏目标题、图标、顺序与 About 正文。Course 自动生成可折叠的课程树；Tech 只显示「技术积累 / Tools」一层分组，Reading 只显示「Reading / Paper」一层分组，各组内扁平罗列所有公开文章。
- `site-template/assets/`：头像和本地字体、搜索、目录、图片预览、MathJax 等资源。
- `site-template/_data/`：社交入口、栏目英文名称，以及静态资源地址。

课程使用 `/courses/`；Tech 使用 `/knowledge/`，子目录为 `/knowledge/tech/` 和 `/knowledge/tools/`；Reading 使用 `/reading/`，子目录为 `/reading/reading/` 和 `/reading/paper/`。Course 按原目录层级显示文件夹和笔记；Tech 和 Reading 的栏目首页不继续展示深层文件夹，而是在一级分组下直接列出带文章图标的公开笔记。笔记的原有 URL 和顶部路径导航仍保留完整目录层级。

可选属性 `date` 设置文章日期（如 `2026-09-14`）。没有该属性时，已有笔记使用 Git 中首次公开的日期；新笔记使用首次导出到公开快照的时间，并保存在 `docs/publication.json`，后续构建不会改变它。公开的目录 `index.md` 优先作为该目录首页，顶层栏目索引不重复加入首页文章列表。文章页标题下不自动重复正文摘要；只有笔记显式填写 `description` 时才显示简介。

文章底部的 Older / Newer 只在同一文件夹的公开文章之间跳转，按原文件名自然排序（例如 Lecture2 在 Lecture10 前），不受文章日期、显示标题或 `nav_order` 影响，也不会进入子文件夹。Older 指向前一篇，Newer 指向后一篇；到达首尾时对应按钮禁用。

首页卡片自动提取正文最外层级的前 4 个不同章节标题，以「 · 」分隔；忽略代码和提示块内的标题、重复的文章标题及公式，没有章节标题时省略摘要。卡片底部显示完整公开目录（如 `Course / FDS-ZJU / notes`），目录名称沿用 `publish.toml` 的 `labels`，长路径允许换行。

顶部路径导航按笔记所在目录显示完整层级，例如 Home › Course › FDS-ZJU › notes › 算法分析基础，每个上级目录均可点击返回；窄窗口中保留该路径并支持横向滚动，不再显示笼统的 Post。目录名称优先使用 `labels`，其次使用公开目录首页的标题，最后使用文件夹名；顶层栏目使用侧栏名称。

`site-template/_includes/post-nav.html` 覆写主题的文章导航组件；Course 树在官方分类卡片样式上补充局部样式，使用浏览器原生折叠控件。静态资源版本及许可证见 `site-template/THIRD_PARTY.md`。当前未配置评论、访问统计与 PWA 离线缓存。

## 开发

```sh
uv run --frozen pytest -q
# 仅用已导出的公开内容构建，与 GitHub Actions 相同，不读取 Vault
uv run --frozen python scripts/site.py build
```

`scripts/exporter.py` 负责筛选公开内容、转换 Obsidian 语法和复制引用图片；`scripts/jekyll.py` 将公开 Markdown 转为 Chirpy 可直接使用的文章和目录页；`scripts/site.py` 负责构建、检查、预览和发布。临时 Jekyll 源目录位于 `.runtime/`，最终输出位于 `site/`，均不提交。

转换层保留数学公式、嵌套提示块、代码、中文锚点与既有网址。正文禁用 Liquid 展开，因此笔记里的 `{{ ... }}` 或 `{% ... %}` 示例仍作为原文展示。GitHub Actions 无需访问 Obsidian Vault。

修改源码或主题设置后，可检查并重新生成公开快照：

```sh
.venv/bin/python -c 'from scripts.site import prepare; prepare(True)'
```

审阅源码与导出变更后再提交。自动发布入口会拒绝尚未提交的源码修改。
