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

`publish.toml` 限定课程、知识库、技术积累和阅读四类源目录。`local.toml` 保存本机 Vault 路径并被 Git 忽略。GitHub Actions 只构建已导出的公开内容。

可选属性 `title` 设置网页标题，`nav_order` 用数字控制同层笔记顺序。目录保留原层级、按数字自然排序；目录名称可在 `publish.toml` 的 `labels` 中设置。

## 图片、链接与撤下页面

支持标准 Markdown 链接、`[[笔记]]`、`[[笔记#标题|文字]]`、`![[图片.png]]` 和图片宽度。建议使用笔记旁的 `assets/` 目录；图片必须位于配置允许的源目录内。程序只复制引用的图片，并通过内容哈希避免同名覆盖。

提示块、折叠提示块和数学公式在导出时适配网站，原文不变；代码中的示例语法不会转换。未公开笔记的链接转为文字并提示。缺图、歧义链接、块引用、笔记嵌入、动态 Dataview 和非图片本地附件会阻止发布。

将 `publish` 改成 `false` 后再次发布，对应页面和不再使用的图片会从当前网站及搜索索引移除。已经公开的 Git 历史仍保留旧内容。笔记移动或重命名会改变网址。

## 环境与命令

使用 Python 3.12、Zensical 0.0.62，依赖由 `uv.lock` 固定。新机器在项目根目录执行：

```sh
uv sync --frozen --python 3.12
cp local.example.toml local.toml
# 编辑 local.toml，填写本机 Vault 的绝对路径
.venv/bin/python scripts/site.py check
.venv/bin/python scripts/site.py preview
.venv/bin/python scripts/site.py publish
```

发布需要 Git、已登录正确账号的 GitHub CLI。目标固定为 `LiHaoze-Bob/notes-site` 的 `main` 分支；只自动提交 `docs/` 和生成的 `mkdocs.yml`。其他分支、其他 origin、未提交的源码修改会阻止自动发布。

`check` 在临时目录导出、构建并校验内部链接与资源。`preview` 同时启动仅绑定本机的预览服务：`http://127.0.0.1:8765/notes-site/`；再次点击会更新内容并复用服务。

`publish` 完成检查后提交、推送并等待该提交的 GitHub Actions 部署结果，只有成功才提示「已上线」。重复点击受互斥锁保护，内容没变化不会生成空提交。

## 排错

- **缺失图片或歧义链接**：按报错修正引用，使用明确的相对路径。
- **源码未提交**：在网站项目中检查并提交认可的代码修改，再发布。
- **网络、认证或推送失败**：检查 GitHub 登录与连接后重试；脚本不会强制推送。
- **远端有新提交**：在网站项目中检查差异并合并，不要对 Obsidian Vault 执行这些操作。
- **部署失败或超时**：查看仓库 Actions；本地状态保存在 `.runtime/status.json`。
- **控制页无反应**：确认 Shell commands 插件已启用；初次安装后正常重启 Obsidian。
- **移动项目目录**：更新插件工作目录和三个命令中的绝对路径，并重建虚拟环境。

## 开发

```sh
uv run --frozen pytest -q
uv run --frozen zensical build --clean
uv run --frozen python scripts/site.py validate
```

`site-template/` 保存样式、公式资源和基础配置；`scripts/exporter.py` 负责筛选转换；`scripts/site.py` 负责构建发布。修改模板后，先用下列命令检查并生成导出，再提交已审阅的源码与导出变更：

```sh
.venv/bin/python -c 'from scripts.site import prepare; prepare(True)'
```

第一版不包含评论、访问统计、手机发布或自定义域名。MathJax 3.2.2 随站提供，许可证见 `site-template/assets/vendor/mathjax/LICENSE`；无需外部字体或公式 CDN。
