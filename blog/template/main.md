# Post Title

> 可选：一句话摘要或引用

正文从这里开始。你可以用 Markdown 写草稿，再整理到 `main.html` 发布。

## 小节标题

- 要点一
- 要点二

## 常用标签（写入 blogs.json）

- `paper-reading` — 论文阅读
- `tutorial` — 教程
- `notes` — 笔记

## 发布新文章

1. 复制 `blog/template/` 文件夹，重命名为文章 slug（如 `my-first-post`）
2. 编辑 `main.html`（及可选的 `main.md`）
3. 在 `blog/blogs.json` 中添加条目：

```json
{
  "id": "my-first-post",
  "title": "Post Title",
  "description": "Brief description shown on the blog list.",
  "tags": ["notes"]
}
```

`id` 必须与文件夹名一致，列表页会链接到 `{id}/main.html`。
