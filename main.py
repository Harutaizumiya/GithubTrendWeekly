import datetime
import requests
from datetime import datetime, timedelta
import os
import smtplib
from email.mime.text import MIMEText
import dotenv

# 加载环境变量
dotenv.load_dotenv()

# --- 配置區 ---
AI_API_KEY = os.getenv("API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def get_trending_json():
    # GitHub API URL
    GITHUB_API_URL = "https://api.github.com/search/repositories"

    # 上周日期
    today = datetime.utcnow()
    one_week_ago = today - timedelta(days=7)
    one_week_ago_str = one_week_ago.strftime("%Y-%m-%d")

    # 查询参数
    query_params = {
        "q": f"created:>{one_week_ago_str}",
        "sort": "stars",
        "order": "desc",
        "per_page": 10
    }

    response = requests.get(GITHUB_API_URL, params=query_params)

    if response.status_code == 200:
        data = response.json()
        # 直接打印原始 JSON 数据
        # print(json.dumps(data, indent=2))
        return data
    else:
        return f"请求失败: {response.status_code}, {response.text}"


def ai_analyze(content):
    # 确保 URL 包含具体端点
    api_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    # 使用多行字符串構建 Prompt，避免轉義困擾
    prompt = f"""以下是上周 GitHub 热门项目，请帮我分析它们的技术亮点，
并整理成一份专业的中文简报（包含项目动态、核心价值、推荐理由），并转成美观，现代化的html格式。
开头写这样一句话“你好！这是上周GitHub的热门项目，来看看世界发生了什么变化。”
不要添加“当然可以，以下是...”的报头，也不要在结尾写任何额外帮助的话语）：

{content}"""

    data = {
        "model": "qwen-flash",
        "messages": [
            {"role": "system", "content": "你是一个专业的技术分析师，擅长总结开源项目。"},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 分析失敗: {str(e)}"


def send_email(report_content):
    """將 AI 生成的 Markdown 轉為 HTML 並發送"""
    # 适配 Python 3.11：在外部处理换行符转换
    html_body = report_content.replace('\n', '<br>')
    full_html = f"<html><body>{html_body}</body></html>"

    msg = MIMEText(full_html, 'html', 'utf-8')
    msg['Subject'] = '[GitHubWeekly] GitHub 每週熱門項目趨勢分析'
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER

    # 注意：如果你使用的是 Outlook 或 Gmail，請確認 SMTP 地址和端口
    # Gmail: smtp.gmail.com | Outlook: smtp.office365.com
    smtp_server = "smtp.163.com"

    try:
        with smtplib.SMTP_SSL(smtp_server, 994) as server:
            server.login(EMAIL_SENDER, SMTP_PASSWORD)
            server.send_message(msg)
        print("簡報已成功發送至郵箱！")
    except Exception as e:
        print(f"郵件發送失敗: {e}")


# --- 主程序 ---
if __name__ == "__main__":
    print("正在獲取 GitHub 熱門數據...")
    raw_data = get_trending_json()

    print("正在調用 AI 進行深度分析...")
    ai_report = ai_analyze(raw_data)

    print("正在發送郵件...")
    send_email(ai_report)