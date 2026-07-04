import os
import logging
import html
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Determine Web App URL
# Render sets RENDER_EXTERNAL_URL to the public https address of the web service
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
WEB_APP_URL = os.getenv("WEB_APP_URL")

if RENDER_URL:
    # Ensure it ends with a slash
    if not RENDER_URL.endswith('/'):
        RENDER_URL += '/'
    BASE_URL = RENDER_URL
elif WEB_APP_URL:
    BASE_URL = WEB_APP_URL
else:
    # Fallback default (users can configure this in .env or Render variables)
    BASE_URL = "https://super-study.onrender.com/"

logger.info(f"Using Web App Base URL: {BASE_URL}")

def get_webapp_keyboard(tab="dashboard"):
    url = f"{BASE_URL}?tab={tab}"
    keyboard = [
        [InlineKeyboardButton("Launch AstraAI Hub 🚀", web_app=WebAppInfo(url=url))]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Start Command ---
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"🛰️ <b>ASTRAAI HUB | Web Ecosystem Active</b>\n\n"
        f"Welcome, cadet. Your student ecosystem, gamified productivity engine, "
        f"and career accelerator has been upgraded to a **Telegram Mini App (TMA)**.\n\n"
        f"Click the button below to launch the next-level, interactive dashboard. "
        f"Access Pomodoro focus timers, drag-and-drop Eisenhower matrices, real-time MCQs, "
        f"ATS Resume compiler wizard, and the AI doubts resolver."
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_webapp_keyboard("dashboard"),
        parse_mode="HTML"
    )

# --- Profile Command ---
async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👤 Click below to access your **Astra Academic Profile** and daily consistency status:",
        reply_markup=get_webapp_keyboard("profile"),
        parse_mode="Markdown"
    )

# --- Leaderboard Command ---
async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🥇 Click below to launch the **Global Peer Scoreboard** and benchmark your academic standing:",
        reply_markup=get_webapp_keyboard("leaderboard"),
        parse_mode="Markdown"
    )

# --- Schedule Command ---
async def schedule_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 Click below to open the **Productivity Hub** (Pomodoro Timer, Eisenhower Quadrants, Day Timelines):",
        reply_markup=get_webapp_keyboard("schedule"),
        parse_mode="Markdown"
    )

# --- Duel Command ---
async def duel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚔️ Click below to enter the **Scholastic MCQ Duel Arena** and battle for XP scores:",
        reply_markup=get_webapp_keyboard("duel"),
        parse_mode="Markdown"
    )

# --- Resume Command ---
async def makeresume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Click below to initialize the 6-stage **ATS Professional Resume Compiler Wizard**:",
        reply_markup=get_webapp_keyboard("resume"),
        parse_mode="Markdown"
    )

# --- Language Diagnostic ---
async def diagnose_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 Click below to open the **Linguistic Correction & Doubt Solver Lab**:",
        reply_markup=get_webapp_keyboard("mentor"),
        parse_mode="Markdown"
    )

# --- Setup Application helper (called by main.py) ---
def setup_bot(application: Application):
    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("profile", profile_cmd))
    application.add_handler(CommandHandler("dailycheckin", profile_cmd)) # redirect checkin to profile tab
    application.add_handler(CommandHandler("leaderboard", leaderboard_cmd))
    application.add_handler(CommandHandler("schedule", schedule_cmd))
    application.add_handler(CommandHandler("pomodoro", schedule_cmd))
    application.add_handler(CommandHandler("makeresume", makeresume_cmd))
    application.add_handler(CommandHandler("cv", makeresume_cmd))
    application.add_handler(CommandHandler("duel", duel_cmd))
    application.add_handler(CommandHandler("battle", duel_cmd))
    application.add_handler(CommandHandler("diagnose", diagnose_cmd))
