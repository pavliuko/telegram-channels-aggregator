# AI News Aggregator

This simple script listens to a list of Telegram channels, translates each new message into English using OpenAI and forwards the original and translated text to another channel.

## Setup
1. Install Python 3.8+ and the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Obtain Telegram `API_ID` and `API_HASH` from [https://my.telegram.org](https://my.telegram.org).
3. Generate an [OpenAI API key](https://platform.openai.com) and set `OPENAI_API_KEY`.
4. Run the script once to generate a session file and log in.

## Usage
Set the required environment variables and run the script:

```bash
export TELEGRAM_API_ID=your_api_id
export TELEGRAM_API_HASH=your_api_hash
export SOURCE_CHANNELS="channel1,channel2"
export TARGET_CHANNEL="@your_target_channel"
export OPENAI_API_KEY=your_openai_key
python app.py
```

`SOURCE_CHANNELS` should be a comma‑separated list of channel usernames or IDs. The account must have access to these channels.

The script will listen for new messages, translate them to English and post the original text with its translation to the target channel.
