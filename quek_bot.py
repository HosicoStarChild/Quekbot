"""
Quek Link Preview Bot for Telegram
-----------------------------------
Transforms x.com / twitter.com links into quekx.com links
so Telegram shows proper previews (videos, images, etc.)

Usage:
    1. Install dependencies: pip install python-telegram-bot
    2. Get a bot token from @BotFather on Telegram
    3. Set the BOT_TOKEN below (or use env var)
    4. Run: python quek_bot.py
"""

import os
import re
import logging
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters,
)

# ---- CONFIG -----------------------------------------------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN", "PASTE_YOUR_TOKEN_HERE")

# Domains to rewrite:  original -> replacement
# Add more here if you want (e.g. "instagram.com": "ddinstagram.com")
DOMAIN_MAP = {
    "x.com":          "quekx.com",
    "twitter.com":    "quekx.com",
    "www.x.com":      "quekx.com",
    "www.twitter.com": "quekx.com",
}

# ---- LOGGING ----------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---- URL MATCHING -----------------------------------------------------------
# Finds http(s) URLs in a message
URL_REGEX = re.compile(r"https?://[^\s]+", re.IGNORECASE)


def transform_url(url: str) -> str | None:
    """Return rewritten URL if its domain is in DOMAIN_MAP, else None."""
    # Match scheme://host/rest-of-path
    m = re.match(r"(https?://)([^/]+)(/.*)?", url, re.IGNORECASE)
    if not m:
        return None

    scheme, host, rest = m.group(1), m.group(2).lower(), m.group(3) or ""

    if host in DOMAIN_MAP:
        return f"{scheme}{DOMAIN_MAP[host]}{rest}"
    return None


def transform_message(text: str) -> list[str]:
    """Find all URLs in text and return a list of transformed URLs."""
    urls = URL_REGEX.findall(text)
    transformed = []
    for url in urls:
        # Strip trailing punctuation that commonly sticks to URLs
        url = url.rstrip(".,!?);:]")
        new_url = transform_url(url)
        if new_url:
            transformed.append(new_url)
    return transformed


# ---- HANDLERS ---------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Hi! 👋\n\n"
        "Send or forward me any x.com / twitter.com link and I'll reply "
        "with a quekx.com version so Telegram shows a proper preview.\n\n"
        "You can also add me to a group — I'll auto-convert any x.com "
        "links people paste.\n\n"
        "(Make sure to disable Group Privacy in @BotFather if using in groups.)"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main handler: look for x.com links and reply with quekx.com versions."""
    if not update.message or not update.message.text:
        return

    text = update.message.text
    new_urls = transform_message(text)

    if not new_urls:
        return  # Nothing to do

    # One URL -> send it directly; multiple -> send them on separate lines
    reply = "\n".join(new_urls)

    await update.message.reply_text(
        reply,
        disable_web_page_preview=False,  # we want the preview!
    )


# ---- MAIN -------------------------------------------------------------------
def main() -> None:
    if BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        raise SystemExit(
            "ERROR: Set BOT_TOKEN env var or edit the file. "
            "Get a token from @BotFather on Telegram."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Quek bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
