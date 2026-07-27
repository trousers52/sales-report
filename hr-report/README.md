# 人事日报 · 自动发送系统

人事同事每天填一个网页表单，提交后**自动**把日报发到 `zhongtaibu@flipped-hz.com.cn`，零人工复制粘贴。

---

## 🎯 三种使用方式（推荐第 1 种）

### ✅ 方式 1：一键网页版（最推荐，0 配置）

直接把 `index.html` 部署到任何一个静态网站托管平台：

| 平台 | 难度 | 说明 |
|------|------|------|
| **GitHub Pages** | ⭐ 免费 | 推到 GitHub 仓库，Settings → Pages 一键开启 |
| **Vercel** | ⭐ 免费 | 拖拽文件夹到 vercel.com 即可 |
| **内网 Nginx** | ⭐⭐ 公司服务器 | 放到 `/usr/share/nginx/html/hr-report/` |
| **本地双击** | ⭐ 临时用 | 直接双击 `index.html` 在浏览器打开（部分功能可能受浏览器限制） |

> 人事每天打开网址 → 填表 → 点「一键发送」→ 完事 ✨

**首次使用**：第一次点发送时，FormSubmit 会发一封激活邮件到 `zhongtaibu@flipped-hz.com.cn`，那边点确认链接后，以后就全自动了。

---

### 📧 方式 2：邮件客户端兜底（最稳，但多一步）

填完点「唤起邮件客户端」按钮，会自动打开本地邮件软件（Outlook / Foxmail / 网易邮箱大师等），主题和正文都填好，**点发送**就完事。

适合：不想搞任何部署的公司，兼容性 100%。

---

### 🐍 方式 3：Python 脚本直发（最自动，但要配 SMTP）

把网页表单内容导出为 `.txt`，跑一个 Python 脚本自动发到企业邮箱。

#### 配置 SMTP（只需做一次）

1. 登录 `https://mail.flipped-hz.com.cn`（或公司邮箱 Web 端）
2. 设置 → 账户 → 开启 **SMTP 服务** / 获取 **授权码**
3. 把授权码填到 `send_email.py` 顶部的配置区，或用环境变量：

```bash
export SMTP_HOST="smtp.flipped-hz.com.cn"
export SMTP_PORT="465"
export SMTP_USER="hr@flipped-hz.com.cn"
export SMTP_PASS="你的授权码"
```

#### 每天手动跑

```bash
python3 send_email.py < today_report.txt
```

#### 🚀 想全自动？加个定时任务

Linux/macOS 编辑 crontab（每天 18:30 自动发）：

```bash
crontab -e
# 加一行：
30 18 * * * cd /path/to/hr-daily-report && python3 send_email.py < today_report.txt >> send.log 2>&1
```

Windows 用「任务计划程序」触发 `pythonw.exe send_email.py`。

---

## 📂 文件清单

```
hr-daily-report/
├── index.html       # 📋 日报填写页面（核心）
├── send_email.py    # 🐍 备选 SMTP 发送脚本
└── README.md        # 📖 本说明
```

---

## 🛠 自定义字段

打开 `index.html`，搜以下位置就能改字段：

- **新增字段**：复制一段 `<div class="field">` 改 `name` 和 `label`
- **修改日报格式**：改 `formatReport()` 函数
- **改收件邮箱**：搜 `zhongtaibu@flipped-hz.com.cn` 替换即可

---

## ❓ 常见问题

**Q：FormSubmit 安全吗？**
A：FormSubmit 是老牌免费服务（2019 年至今），只做表单→邮件中转，不存数据。激活一次后别人也用不了你的地址。

**Q：邮件没收到？**
A：① 查垃圾邮件 ② 让收件方把 formsubmit.co 加白名单 ③ 切到方式 2 或 3。

**Q：手机能用吗？**
A：能，HTML 自带响应式，浏览器打开直接填。

**Q：能多个人用吗？**
A：能，大家打开同一个网页地址即可。各填各的不冲突。
