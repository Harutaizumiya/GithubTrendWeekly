import os

# 获取环境变量
# 注意：在 GitHub Actions 中，你需要手动将 Secret 映射为环境变量
smtp_pass = os.getenv("SMTP_PASSWORD")

print("--- 环境变量检测 ---")

if smtp_pass:
    print(f"✅ 成功读取到 SMTP_PASSWORD")
    print(f"字符长度: {len(smtp_pass)}")
    # 打印前两个字符用于手动核对（GitHub 可能会脱敏，取决于内容）
    print(f"首位字符预览: {smtp_pass[0]}...{smtp_pass[-1]}")
else:
    print("❌ 未能读取到 SMTP_PASSWORD，请检查 Workflow 文件配置。")

print("-------------------")