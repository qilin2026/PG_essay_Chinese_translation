# PG Essay 中文翻译镜像 — 项目快照

## 项目目标

构建 paulgraham.com 的中文翻译镜像网站。用户可以像浏览 PG 原站一样直接阅读中文翻译后的 essay。目标读者不是技术人员，关注的是 PG 的思想和写作，而非编程技术。

## 当前状态

- **基础设施已完成**：提取、分类、站点生成管线可用
- **221 篇文章已提取**（来自 ofou/graham-essays EPUB 存档）
- **26 篇纯技术文章已排除**（Lisp、垃圾邮件过滤、编程语言）
- **195 篇待翻译**（其中 188 篇有英文正文内容）
- **所有翻译已清除**，需要从头开始逐段忠实翻译
- **站点输出到 `docs/`**，用于 GitHub Pages 部署（需要仓库设为 Public）

## 翻译质量要求（极其重要）

1. **逐段忠实翻译** — 必须先读取 JSON 中的英文原文（paragraphs_en），逐段翻译，不可凭记忆概括
2. **保留所有细节** — PG 的具体例子、比喻、数据、人名、故事都必须完整保留
3. **注释和致谢必须翻译** — 原文中的 [1] [2] 等脚注和 "Thanks to..." 致谢部分都是正文的一部分，必须包含在翻译中
4. **保持 PG 的文风** — 对话式、深刻洞察、有时幽默，避免翻译腔
5. **每批只翻译 2-3 篇** — 质量优先于数量
6. **专有名词** — 首次出现时中英对照，如：Y Combinator（Y Combinator）

## 翻译工作流（核心）

采用"用户发原文 → Claude 翻译 → 用户验证 → 写入 JSON"的方式：

1. **用户发送原文** — 用户从 paulgraham.com 复制一篇文章的完整英文原文（包括注释和致谢），发送到对话中
2. **Claude 逐段翻译** — Claude 在对话中返回逐段中文翻译，用户可以直接对照原文检查质量
3. **用户确认满意后** — Claude 将翻译写入 `data/essays/{slug}.json`（更新 title_zh、paragraphs_zh、translation_status）
4. **定期生成站点** — 每完成几篇后运行 `python scripts/generate.py` 生成 HTML 到 `docs/`
5. **提交并推送** — `git add -A && git commit && git push`

## 项目结构
PG_essay_Chinese_translation/
├── CLAUDE.md # 本文件 — 项目上下文快照
├── requirements.txt # Python 依赖：Jinja2
├── .gitignore
├── scripts/
│ ├── config.py # 路径配置、站点生成配置
│ └── generate.py # 从翻译好的 JSON 生成静态 HTML 到 docs/
├── templates/
│ ├── index.html # 文章列表页 Jinja2 模板
│ └── essay.html # 单篇文章页 Jinja2 模板（含注释和致谢区域）
├── data/
│ └── essays/ # 每篇文章的 JSON，格式见下
└── docs/ # 生成的静态网站（GitHub Pages 部署目录）

## 单篇文章 JSON 格式
```json
{
"slug": "vb",
"title": "Life is Short",
"title_zh": "人生苦短",
"date": "January 2016",
"url": "https://paulgraham.com/vb.html",
"paragraphs_zh": [
"人生苦短，这谁都知道。...",
"..."
],
"notes_zh": [
"[1] 我一开始不喜欢...",
"[2] 我选择这个例子..."
],
"thanks_zh": "感谢 Jessica Livingston 和 Geoff Ralston 阅读本文草稿。",
"translation_status": "complete"
}

字段说明：
- `slug` — 文章标识符，和 paulgraham.com URL 中的文件名一致（如 vb.html → slug 为 vb）
- `title` — 英文原标题
- `title_zh` — 中文标题
- `date` — 发表日期（保留英文原格式如 "January 2016"）
- `url` — 原文链接
- `paragraphs_zh` — 正文逐段翻译
- `notes_zh` — 注释翻译（如 [1]、[2] 等脚注），没有则为空数组
- `thanks_zh` — 致谢翻译（"Thanks to..." 部分），没有则为空字符串
- `translation_status` — "complete" 表示已翻译
## 写入翻译的方式
可以用 Python 脚本直接更新 JSON 文件：
```python
import json
filepath = "data/essays/{slug}.json"
with open(filepath) as f:
data = json.load(f)
data["title_zh"] = "中文标题"
data["paragraphs_zh"] = ["第一段翻译...", "第二段翻译...", ...]
data["translation_status"] = "complete"
with open(filepath, "w", encoding="utf-8") as f:
json.dump(data, f, ensure_ascii=False, indent=2)

## Git 信息
- 仓库：`qilin2026/PG_essay_Chinese_translation`
- 分支：`main`
- GitHub Pages 配置：Source = main 分支 /docs 目录
## 注意事项
- paulgraham.com 返回 403，无法直接抓取，用户手动从网站复制原文
- 不需要 API Key — 翻译在对话中直接完成
