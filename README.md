# TON Volume Bot 🤖

Telegram бот для анализа торгового объема токенов в сети TON blockchain.

## 🚀 Возможности

- 📊 Анализ торгового объема по адресу контракта токена
- 💰 Подсчет входящих и исходящих транзакций в TON
- 🔢 Статистика количества транзакций
- 🔄 Поддержка различных форматов адресов TON
- 🔗 Интеграция с TonAPI для получения данных
- 📱 Удобный Telegram интерфейс

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- TON API Key (от [tonconsole.com](https://tonconsole.com/tonapi/api-keys))

## 🛠 Установка

### 1. Клонирование и настройка

```bash
cd /Users/aleksejaleksej/Documents/gasbot
```

### 2. Установка зависимостей

```bash
make install
```

Или вручную:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Файл `.env` уже создан с вашими токенами:
```
BOT_TOKEN=7103687787:AAHqvGjMLa5EbHhIPWqYmyzX7MQQSflyPxQ
TONAPI_KEY=AHGHOL2PO5KWW2QAAAADJA4D5OGV22B4GTWAJXFWZJCVUE3SU2QWX445UGHC5DPLWSS5LNA
```

## 🚀 Запуск

### Быстрый запуск
```bash
make start
```

### Альтернативные способы запуска

1. **Через скрипт:**
```bash
./start_bot.sh
```

2. **Вручную:**
```bash
source venv/bin/activate
python bot.py
```

## 📱 Использование

### Команды бота

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/volume <адрес>` - Анализ торгового объема

### Примеры использования

```
/volume EQD4FPq-PRDieyQKkizFTRtSDyucUIqrj0v_zXJmqaDp6_0t
```

### Поддерживаемые форматы адресов

- **User-friendly:** `EQ...`, `UQ...`
- **Raw:** `0:1234567890abcdef...`
- **Ссылки:** `https://tonviewer.com/...`

## 🛠 Управление

### Команды Makefile

```bash
make start    # Запустить бота
make stop     # Остановить бота
make restart  # Перезапустить бота
make status   # Проверить статус
make install  # Установить зависимости
make clean    # Очистить процессы и кэш
make help     # Показать справку
```

### Проверка статуса

```bash
make status
```

### Остановка бота

```bash
make stop
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `BOT_TOKEN` | Telegram Bot Token | `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz` |
| `TONAPI_KEY` | TON API Key | `AHGHOL2PO5KWW2QAAAADJA4D5OGV22B4GTWAJXFWZJCVUE3SU2QWX445UGHC5DPLWSS5LNA` |

### Получение токенов

1. **Telegram Bot Token:**
   - Создайте бота через [@BotFather](https://t.me/BotFather)
   - Получите токен из сообщения

2. **TON API Key:**
   - Зарегистрируйтесь на [tonconsole.com](https://tonconsole.com/tonapi/api-keys)
   - Создайте новый API ключ

## 📊 API Endpoints

Бот использует следующие эндпоинты TonAPI:

- `GET /v2/blockchain/accounts/{account_id}/transactions` - Получение транзакций аккаунта

## 🔍 Анализ данных

Бот анализирует:

- **Общий объем:** Сумма всех входящих и исходящих транзакций
- **Входящий объем:** Сумма входящих транзакций
- **Исходящий объем:** Сумма исходящих транзакций
- **Количество транзакций:** Общее число обработанных транзакций

## 🐛 Устранение неполадок

### Ошибка "BOT_TOKEN not found"
```bash
# Проверьте наличие файла .env
ls -la .env

# Проверьте содержимое файла
cat .env
```

### Ошибка "TONAPI_KEY not found"
```bash
# Убедитесь, что API ключ правильный
# Получите новый ключ на https://tonconsole.com/tonapi/api-keys
```

### Ошибка "Request timeout"
- Проверьте интернет-соединение
- Возможно, требуется VPN для доступа к Telegram API

### Ошибка "TelegramConflictError"
```bash
# Остановите все процессы бота
make stop

# Запустите заново
make start
```

## 📁 Структура проекта

```
gasbot/
├── bot.py              # Основной код бота
├── .env                # Переменные окружения
├── requirements.txt    # Зависимости Python
├── start_bot.sh       # Скрипт запуска
├── Makefile           # Команды управления
├── README.md          # Документация
└── venv/              # Виртуальное окружение
```

## 🤝 Поддержка

При возникновении проблем:

1. Проверьте логи бота
2. Убедитесь в правильности токенов
3. Проверьте интернет-соединение
4. Обратитесь к документации TonAPI

## 📄 Лицензия

Этот проект создан для анализа торгового объема в сети TON blockchain.

---

**Создано с ❤️ для TON Community** 
