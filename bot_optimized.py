import asyncio
import logging
import re
from decimal import Decimal
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

# Load env and setup
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
BOT_TOKEN = os.getenv('BOT_TOKEN')
TONAPI_KEY = os.getenv('TONAPI_KEY')
TONAPI_BASE_URL = "https://tonapi.io/v2"

if not all([BOT_TOKEN, TONAPI_KEY]):
    raise ValueError("Missing required environment variables")

bot = Bot(token=BOT_TOKEN)  # type: ignore
dp = Dispatcher()

# Address validation patterns
ADDRESS_PATTERNS = [
    r'^[EU]Q[a-zA-Z0-9_-]{46}$',  # User-friendly
    r'^-?\d+:[a-fA-F0-9]{64}$',   # Raw
    r'https?://tonviewer\.com/[a-zA-Z0-9_-]+',
    r'https?://tonscan\.org/address/[a-zA-Z0-9_-]+'
]

def normalize_address(address: str) -> str:
    """Extract and normalize TON address"""
    # Extract from URL if needed
    if 'tonviewer.com' in address or 'tonscan.org' in address:
        address = address.split('/')[-1]
    
    # Validate format
    if any(re.match(pattern, address) for pattern in ADDRESS_PATTERNS[:2]):
        return address
    
    raise ValueError("Invalid address format")

async def get_transactions(account_id: str, limit: int = 1000) -> list:
    """Fetch transactions from TON API"""
    headers = {'Authorization': f'Bearer {TONAPI_KEY}'}
    params = {'limit': limit, 'archival': True}
    
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{TONAPI_BASE_URL}/blockchain/accounts/{account_id}/transactions",
            headers=headers, params=params
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('transactions', [])
            logger.error(f"API error: {response.status}")
            return []

async def calculate_volume(token_address: str) -> dict:
    """Calculate trading volume for token"""
    try:
        address = normalize_address(token_address)
        transactions = await get_transactions(address)
        
        if not transactions:
            return {'success': False, 'error': 'No transactions found'}
        
        total = incoming = outgoing = Decimal('0')
        
        for tx in transactions:
            # Process incoming messages
            if tx.get('in_msg') and tx['in_msg'].get('value'):
                amount = Decimal(str(tx['in_msg']['value'])) / Decimal('1000000000')
                incoming += amount
                total += amount
            
            # Process outgoing messages
            for out_msg in tx.get('out_msgs', []):
                if out_msg.get('value'):
                    amount = Decimal(str(out_msg['value'])) / Decimal('1000000000')
                    outgoing += amount
                    total += amount
        
        return {
            'success': True,
            'total_volume': float(total),
            'incoming_volume': float(incoming),
            'outgoing_volume': float(outgoing),
            'transaction_count': len(transactions),
            'address': address
        }
        
    except Exception as e:
        logger.error(f"Volume calculation error: {e}")
        return {'success': False, 'error': str(e)}

# Message handlers
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("""
🤖 **TON Volume Bot**

Анализирую торговый объем токенов в сети TON.

**Команды:**
• `/volume <адрес>` - Анализ объема
• `/help` - Справка

**Пример:** `/volume EQD4FPq-PRDieyQKkizFTRtSDyucUIqrj0v_zXJmqaDp6_0t`
    """, parse_mode="Markdown")

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("""
📖 **Справка**

**Команды:**
• `/start` - Начать
• `/volume <адрес>` - Анализ объема
• `/help` - Эта справка

**Поддерживаются:** Jetton, NFT, кошельки
    """, parse_mode="Markdown")

@dp.message(Command("volume"))
async def cmd_volume(message: Message):
    text = message.text
    if not text:
        await message.answer("❌ Неверный формат сообщения")
        return
        
    try:
        address = text.split(maxsplit=1)[1].strip()
    except IndexError:
        await message.answer("❌ Укажите адрес: `/volume EQ...`", parse_mode="Markdown")
        return
    
    processing_msg = await message.answer("⏳ Анализирую...")
    result = await calculate_volume(address)
    
    if result['success']:
        response = f"""
📊 **Анализ объема**

`{result['address']}`

• 💰 **Общий:** {result['total_volume']:.2f} TON
• 📥 **Входящий:** {result['incoming_volume']:.2f} TON  
• 📤 **Исходящий:** {result['outgoing_volume']:.2f} TON
• 🔢 **Транзакций:** {result['transaction_count']:,}

[TonViewer](https://tonviewer.com/{result['address']}) | [TonScan](https://tonscan.org/address/{result['address']})
        """
        await processing_msg.edit_text(response, parse_mode="Markdown")
    else:
        await processing_msg.edit_text(f"❌ Ошибка: {result['error']}")

@dp.message()
async def handle_text(message: Message):
    text = message.text
    if not text:
        await message.answer("🤖 Отправьте адрес или `/volume <адрес>`")
        return
        
    text = text.strip()
    
    # Check if it looks like an address
    if any(re.match(pattern, text) for pattern in ADDRESS_PATTERNS):
        address = text.split('/')[-1] if '/' in text else text
        await message.answer(
            f"🔍 Адрес: `{address}`\n\nИспользуйте: `/volume {address}`",
            parse_mode="Markdown"
        )
    else:
        await message.answer("🤖 Отправьте адрес или `/volume <адрес>`")

async def main():
    logger.info("Starting TON Volume Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 