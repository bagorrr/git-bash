import asyncio
from dotenv import load_dotenv
import os
from aiogram import Bot

load_dotenv()

async def test_bot():
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        print("❌ BOT_TOKEN не найден")
        return
    
    bot = Bot(token=bot_token)
    
    try:
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"✅ Бот подключен: @{bot_info.username} (ID: {bot_info.id})")
        print(f"📝 Имя: {bot_info.first_name}")
        
        # Проверяем webhook
        webhook_info = await bot.get_webhook_info()
        print(f"🔗 Webhook URL: {webhook_info.url}")
        
        if webhook_info.url:
            print("⚠️  Webhook активен! Это может мешать polling.")
            # Удаляем webhook
            await bot.delete_webhook()
            print("✅ Webhook удален")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(test_bot()) 