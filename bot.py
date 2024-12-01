import telebot
import yaml
import os

# 从 token.txt 中读取 BOT_TOKEN
def get_bot_token(config_file="token.txt"):
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            token = file.read().strip()
            if not token:
                raise ValueError("Bot Token 为空，请检查 token.txt 文件")
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
UPDATED_CONFIG_FILE = "updated_config.yaml"


# 更新配置文件中的 URL
def update_proxy_url(config_file_path, new_url, output_file_path):
    try:
        with open(config_file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
        
        # 更新 `proxy-providers` 中的 URL
        if 'proxy-providers' in config:
            for provider in config['proxy-providers'].values():
                if 'url' in provider:
                    provider['url'] = new_url
                    print(f"URL 已更新为: {new_url}")
        
        # 保存更新后的配置文件
        with open(output_file_path, 'w', encoding='utf-8') as file:
            yaml.dump(config, file, allow_unicode=True, sort_keys=False)
            return True
    except Exception as e:
        print(f"发生错误: {e}")
        return False


# 当用户发送消息时触发
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "欢迎使用订阅转换 Bot！\n发送新的 URL 链接即可更新配置文件。")


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
    if update_proxy_url(DEFAULT_CONFIG_FILE, new_url, UPDATED_CONFIG_FILE):
        bot.reply_to(message, "配置文件已更新！正在发送新文件...")
        
        # 发送更新后的文件
        with open(UPDATED_CONFIG_FILE, 'rb') as file:
            bot.send_document(message.chat.id, file)
    else:
        bot.reply_to(message, "更新配置文件时发生错误，请检查日志。")


# 启动 Bot
if __name__ == "__main__":
    print("Bot 正在运行...")
    bot.infinity_polling()
