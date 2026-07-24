# 芯动未来销售战报

销售战报 · 7月夏战 · 24日新签达成

## 数据更新流程

1. 编辑 `data.json`
2. 运行生成脚本（可选，已生成的 `index.html` 也可直接用）：
   ```bash
   python3 ../.skills/sales-war-report/scripts/generate_report.py \
     --data data.json --output index.html
   ```
3. `git add . && git commit -m "更新 7月24日数据" && git push`

## 部署

GitHub Pages 部署，URL 形如：`https://<username>.github.io/sales-report/`

开启方法：Settings → Pages → Source: Deploy from a branch → Branch: `main` / `(root)`

## 文件说明

- `index.html` — 最终展示的战报 HTML（自包含、可离线打开）
- `data.json` — 战报数据源（销售名单 + 数字）
- `../.skills/sales-war-report/` — 生成器 skill 源码（template.html + generate_report.py）
