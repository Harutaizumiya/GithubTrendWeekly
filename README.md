<div align="center">

# GitHub Trend Weekly

</div>

<div align="center">

**每周 GitHub 热门项目智能分析报告**

自动获取上周 GitHub 热门趋势，AI 深度分析，邮件送达

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 🌟 项目简介

GitHub Trend Weekly 是一个自动化工具，每周为你智能分析 GitHub 上最受欢迎的新项目。它通过 GitHub API 获取最近 7 天内创建的热门仓库，利用 AI 技术进行深度分析，并生成 HTML 格式报告，直接发送到你的邮箱。

### ✨ 核心功能

- 🔍 **检索** - 自动获取上周 GitHub 热门项目（按星标排序）
- 🤖 **AI 分析** - 使用通义千问深度分析项目技术亮点和核心价值
- 📧 **邮件推送** - 每周自动发送 HTML 格式报告


---

## 🚀 快速开始

### 环境要求

- Python 3.11+
- 一台电脑（最好是服务器）

### 克隆代码
```bash
git clone https://github.com/Harutaizumiya/GithubTrendWeekly.git
```

### 安装依赖

```bash
pip install -r requirement.txt
```

### 获取SMTP授权码
https://zhuanlan.zhihu.com/p/1933936404255191138

### 配置环境变量

在项目根目录创建 `.env` 文件，配置以下变量：

```env
# 阿里云通义千问 API 密钥
API_KEY=your_api_key_here

# 邮箱配置
EMAIL_SENDER=your_email@qq.com
EMAIL_RECEIVER=receiver_email@example.com
SMTP_PASSWORD=your_smtp_password
```

### 运行程序

```bash
python main.py
```

### 定时任务
十分推荐在自己的服务器上部署，然后定时执行
```bash
crontab -e

#在尾行写入，每周一上午8：30执行，根据实际文件位置替换
30 8 * * 1 /usr/bin/python3 /code/python/GithubTrendWeekly/main.py >> /code/python/GithubTrendWeekly/cron_log.log 2>&1
```

---

## 📋 功能详情

### 1. 数据获取

- 使用 GitHub API 搜索最近 7 天创建的项目
- 按星标数量降序排列
- 获取前 10 个热门项目

### 2. AI 分析

- 分析项目的技术亮点
- 总结核心价值和推荐理由
- 生成中文简报
- 输出 HTML 格式

### 3. 邮件发送

- 支持 163 邮箱 SMTP 服务
- 自动将 HTML 内容嵌入邮件
- 每周定时推送趋势报告

---

## 🔧 配置说明

### 邮箱服务

默认使用 163 邮箱 SMTP：
- 服务器：`smtp.163.com`
- 端口：`994`

如需使用其他邮箱服务，请修改 `send_email()` 函数中的 `smtp_server` 变量：

```python
# Gmail
smtp_server = "smtp.gmail.com"

# Outlook
smtp_server = "smtp.office365.com"
```

### AI 模型

默认使用通义千问 `qwen-flash` 模型，可根据需要在 `ai_analyze()` 函数中调整。

### 遗憾
本来这个程序应该跑在GithubAction上实现方便的完全自动化，
可能是因为阿里api拒绝GitHub发出的请求，本人尝试了很多次都没成功，
目前只能在本机或者服务器上使用