#!/usr/bin/env python3
"""
人事日报发送脚本
================
从 stdin 读取日报内容，通过 SMTP 发送到 zhongtaibu@flipped-hz.com.cn

使用方法：
  1. 配置下方 SMTP_* 常量（或用环境变量覆盖）
  2. 把日报内容 pipe 给这个脚本：
     python3 send_email.py < report.txt
"""

import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from datetime import datetime

# ============== SMTP 配置 ==============
# 推荐用环境变量，避免把密码写进代码
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.flipped-hz.com.cn")  # 公司 SMTP 服务器
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))                # 465=SSL, 587=TLS
SMTP_USER = os.getenv("SMTP_USER", "")                        # 发件邮箱（一般是人事本人）
SMTP_PASS = os.getenv("SMTP_PASS", "")                        # 邮箱授权码（非登录密码）
TO_EMAIL  = "zhongtaibu@flipped-hz.com.cn"
# ========================================


def send_email(subject: str, body: str) -> bool:
    if not SMTP_USER or not SMTP_PASS:
        print("❌ 错误：请先设置 SMTP_USER 和 SMTP_PASS 环境变量", file=sys.stderr)
        print("   例子：", file=sys.stderr)
        print("   export SMTP_USER='hr@flipped-hz.com.cn'", file=sys.stderr)
        print("   export SMTP_PASS='你的邮箱授权码'", file=sys.stderr)
        return False

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Date"] = formatdate(localtime=True)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, [TO_EMAIL], msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(SMTP_USER, [TO_EMAIL], msg.as_string())
        print(f"✅ 发送成功 → {TO_EMAIL}")
        return True
    except Exception as e:
        print(f"❌ 发送失败：{e}", file=sys.stderr)
        return False


def main():
    # 主题：第一行；正文：剩余行
    content = sys.stdin.read()
    lines = content.strip().split("\n", 1)
    if len(lines) == 2 and not lines[0].startswith("═"):
        subject = lines[0].strip()
        body = lines[1]
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"【人事日报】{today}"
        body = content

    ok = send_email(subject, body)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
