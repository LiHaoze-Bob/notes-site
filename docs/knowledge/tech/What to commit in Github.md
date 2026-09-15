---
title: What to commit in Github
---
**commit message（提交信息）** Git 本身不强制格式，但团队项目通常使用 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)：

```
<type>(<scope>): <description>
```

例如：

```
docs: redesign repository README
chore: add repository gitignore
feat(lab1-1): add PM2.5 regression notebook
fix(lab1-1): handle missing submission template
refactor(lab2-1): simplify data preprocessing
```

常用类型：

|类型|用途|
|---|---|
|`feat`|新增功能或实验|
|`fix`|修复错误|
|`docs`|README、报告或注释|
|`chore`|`.gitignore`、依赖、配置等维护工作|
|`refactor`|重构代码，但不改变功能|
|`test`|新增或修改测试|
|`style`|代码格式调整，不改变逻辑|
|`perf`|性能优化|
|`ci`|GitHub Actions 等持续集成配置|

建议遵守以下原则：

- 一个 commit 只完成一件逻辑上完整的事情。
- 标题简短明确，Git 官方建议首行尽量不超过 50 个字符。[Git commit 文档](https://git-scm.com/docs/git-commit)
- 使用动词描述“这次提交做了什么”，避免 `update files`、`修改代码` 之类模糊信息。
- 类型通常使用小写，标题末尾不加句号。
- 中文或英文都可以，但整个仓库应保持一致；公开技术仓库通常使用英文。
- 修改较复杂时，在空一行后补充正文，重点解释“为什么这样改”。
- 关联 Issue 时可在正文末尾写 `Closes #12`。
