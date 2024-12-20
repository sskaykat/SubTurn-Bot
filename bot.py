import telebot
import yaml
import os
from datetime import datetime

# 从 token.txt 中读取 BOT_TOKEN
def get_bot_token(config_file="token.txt"):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            if not token or ":" not in token:
                raise ValueError("Token 格式无效或为空，请检查 token.txt 文件")
            return token
    except Exception as e:
        print(f"读取 Bot Token 时发生错误: {e}")
        return None

# 获取 Bot Token
BOT_TOKEN = get_bot_token()

if not BOT_TOKEN:
    print("未找到有效的 Bot Token，脚本无法启动！")
    exit()

bot = telebot.TeleBot(BOT_TOKEN)

# 默认配置文件名和路径
DEFAULT_CONFIG_FILE = "config.yaml"

# 生成当前时间戳命名的文件名
def generate_time_based_filename(prefix="Clash_Meta", extension=".yaml"):
    now = datetime.now()
    return now.strftime(f"{prefix}_%Y%m%d_%H%M%S{extension}")

# 更新配置文件中的 URL 和 path
def update_proxy_url_and_path(config_file_path, new_url):
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 更新 `proxy-providers` 中的 URL 和 path
        if 'proxy-providers' in config:
            for provider in config['proxy-providers'].values():
                if 'url' in provider:
                    provider['url'] = new_url
                    print(f"URL 已更新为: {new_url}")
                if 'path' in provider:
                    new_path = generate_time_based_filename(prefix="clashmeta")
                    provider['path'] = f"./{new_path}"
                    print(f"path 已更新为: {new_path}")
        
        # 生成更新后的配置文件名
        updated_config_file = generate_time_based_filename()
        
        # 保存更新后的配置文件
        with open(updated_config_file, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, allow_unicode=True, sort_keys=False)
        
        return updated_config_file
    except Exception as e:
        print(f"发生错误: {e}")
        return None


# 当用户发送消息时触发
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "欢迎使用配置更新 Bot！\n发送新的 URL 链接即可更新配置文件。")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # 获取用户输入的新 URL
    new_url = message.text.strip()
    
    if not new_url.startswith("http"):
        bot.reply_to(message, "请发送一个有效的 URL 链接，例如：https://example.com")
        return
    
    # 检查默认配置文件是否存在
    if not os.path.exists(DEFAULT_CONFIG_FILE):
        bot.reply_to(message, f"未找到默认配置文件 {DEFAULT_CONFIG_FILE}，请确保它与脚本在同一目录中。")
        return
    
    # 更新配置文件
    updated_file_path = update_proxy_url_and_path(DEFAULT_CONFIG_FILE, new_url)
    if updated_file_path:
        bot.reply_to(message, "配置文件已更新！正在发送新文件...")
        
        try:
            # 发送更新后的文件
            with open(updated_file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)
            
            # 删除文件
            os.remove(updated_file_path)
            print(f"文件 {updated_file_path} 已成功删除。")
        except Exception as e:
            bot.reply_to(message, f"发送或删除文件时发生错误：{e}")
    else:
        bot.reply_to(message, "更新配置文件时发生错误，请检查日志。")


# 启动 Bot
if __name__ == "__main__":
    print("Bot 正在运行...")
    bot.infinity_polling()
