# Quek Link Bot for Telegram

A Telegram bot that converts `x.com` / `twitter.com` links into `quekx.com` links, similar to how the Rick bot uses FixupX — this gives Telegram proper link previews (videos, images, full tweets).

**Example:**
You paste: `https://x.com/HumansNoContext/status/2045544145851126192`
Bot replies: `https://quekx.com/HumansNoContext/status/2045544145851126192`

---

## Setup

### 1. Get a bot token
- Open Telegram, message **@BotFather**
- Send `/newbot`, follow the prompts
- Copy the token it gives you

### 2. Install dependencies
```bash
pip install python-telegram-bot
```

### 3. Run the bot
Either edit `BOT_TOKEN` in `quek_bot.py`, or use an environment variable:
```bash
export BOT_TOKEN="123456:ABC-your-token"
python quek_bot.py
```

### 4. (Optional) Use in groups
By default, Telegram bots can only see commands in groups. To let the bot see regular messages (so it auto-converts x.com links anyone pastes):
- Message **@BotFather**
- Send `/setprivacy` → pick your bot → **Disable**
- Then add the bot to your group

### 5. Keep it running
For 24/7 operation, deploy to a free host:
- **Railway** or **Render** — easiest, just push the repo
- **Fly.io** — generous free tier
- **A VPS / Raspberry Pi** — use `systemd` or `screen`/`tmux`

---

## Customization

Want to convert more sites? Edit the `DOMAIN_MAP` in `quek_bot.py`:

```python
DOMAIN_MAP = {
    "x.com":          "quekx.com",
    "twitter.com":    "quekx.com",
    "instagram.com":  "ddinstagram.com",   # for Instagram previews
    "tiktok.com":     "vxtiktok.com",      # for TikTok previews
    "reddit.com":     "rxddit.com",        # for Reddit previews
}
```

The bot automatically preserves the rest of the URL (path, query params, etc.) — it only swaps the domain.
