import asyncio
import os
import sqlite3

from telethon import TelegramClient, events
import openai
from dotenv import load_dotenv

load_dotenv()

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

def init_db(db_path='processed_messages.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS processed_messages (
                    channel TEXT,
                    message_id INTEGER,
                    PRIMARY KEY (channel, message_id)
                )''')
    conn.commit()
    return conn

def is_processed(conn, channel, message_id):
    c = conn.cursor()
    c.execute('SELECT 1 FROM processed_messages WHERE channel=? AND message_id=?', (channel, message_id))
    return c.fetchone() is not None

def mark_processed(conn, channel, message_id):
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO processed_messages (channel, message_id) VALUES (?, ?)', (channel, message_id))
    conn.commit()

async def translate_to_english(text: str) -> str:
    if not text.strip():
        return text
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate the following text to English."},
            {"role": "user", "content": text},
        ],
    )
    content = response.choices[0].message.content
    return content.strip() if content else text

async def forward_message_with_media(client, original_message, translated_text, target_channel):
    """Forward a message with its media content and translated text"""
    author_info = get_author_info(original_message)
    formatted_text = f"{translated_text}\n\nAuthor: {author_info}"
    
    # Check if the message has media
    if original_message.media:
        try:
            # Forward the media with the translated caption
            await client.send_file(
                target_channel,
                original_message.media,
                caption=formatted_text
            )
        except Exception as e:
            print(f"Error forwarding media: {e}")
            # Fallback: send text only if media forwarding fails
            await client.send_message(target_channel, formatted_text)
    else:
        # No media, just send the text
        await client.send_message(target_channel, formatted_text)

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    db_conn = init_db()
    await fetch_latest_messages(client, SOURCE_CHANNELS[0], db_conn)

    @client.on(events.NewMessage(chats=SOURCE_CHANNELS))
    async def handler(event):
        channel = event.chat.username if event.chat and event.chat.username else str(event.chat_id)
        message_id = event.message.id
        if is_processed(db_conn, channel, message_id):
            return
        original_text = event.message.message
        if not original_text:
            return
        # Translate to English
        translation = await translate_to_english(original_text)
        # Forward message with media
        await forward_message_with_media(client, event.message, translation, TARGET_CHANNEL)
        mark_processed(db_conn, channel, message_id)

    print('Aggregator started. Listening for new messages...')
    await client.run_until_disconnected()


async def fetch_latest_messages(client, channel, db_conn, limit=10):
    async for message in client.iter_messages(channel, limit=limit):
        if message.message:
            channel_id = message.chat.username if message.chat and message.chat.username else str(message.chat_id)
            if db_conn:
                if is_processed(db_conn, channel_id, message.id):
                    continue
            print(f"Message: {message.message}")
            # Optionally: translate and forward
            translation = await translate_to_english(message.message)
            # Forward message with media
            await forward_message_with_media(client, message, translation, TARGET_CHANNEL)
            if db_conn:
                mark_processed(db_conn, channel_id, message.id)

def get_author_info(message):
    # Handle author information properly for Telethon
    author_info = "Unknown"
    if hasattr(message, 'sender') and message.sender:
        if hasattr(message.sender, 'username') and message.sender.username:
            author_info = f"https://t.me/{message.sender.username}"
        elif hasattr(message.sender, 'first_name'):
            author_info = message.sender.first_name
    elif hasattr(message, 'author') and message.author:
        if hasattr(message.author, 'username') and message.author.username:
            author_info = f"https://t.me/{message.author.username}"
        elif hasattr(message.author, 'first_name'):
            author_info = message.author.first_name

    return author_info


if __name__ == '__main__':
    asyncio.run(main())
