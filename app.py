import asyncio
import os

from telethon import TelegramClient, events
import openai

# Environment variables:
# TELEGRAM_API_ID: Telegram API ID
# TELEGRAM_API_HASH: Telegram API hash
# SOURCE_CHANNELS: comma separated list of channel usernames or IDs
# TARGET_CHANNEL: username or ID of the channel to post translations
# OPENAI_API_KEY: key for OpenAI API
# SESSION_NAME (optional): session name or path for Telethon

API_ID = int(os.environ['TELEGRAM_API_ID'])
API_HASH = os.environ['TELEGRAM_API_HASH']
SOURCE_CHANNELS = [ch.strip() for ch in os.environ['SOURCE_CHANNELS'].split(',') if ch.strip()]
TARGET_CHANNEL = os.environ['TARGET_CHANNEL']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
SESSION_NAME = os.environ.get('SESSION_NAME', 'aggregator')

openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

async def translate_to_english(text: str) -> str:
    if not text.strip():
        return text
    response = await openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Translate the following text to English."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        original_text = event.message.message
        if not original_text:
            return
        # Translate to English
        translation = await translate_to_english(original_text)
        message = f"Original:\n{original_text}\n\nTranslated:\n{translation}"
        await client.send_message(TARGET_CHANNEL, message)

    print('Aggregator started. Listening for new messages...')
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
