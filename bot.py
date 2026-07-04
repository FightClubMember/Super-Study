import os
import logging
import html
import json
import re
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# Import local modules
from database import (
    get_user, add_xp, process_daily_checkin, get_leaderboard,
    get_resume_state, save_resume_step, clear_resume_state,
    get_duel_state, save_duel_state, clear_duel_state
)
from mentor import diagnose_language, solve_academic_doubt
from duels_data import DUEL_ARENAS, DUEL_QUESTIONS

# Import visuals generators
from visuals import (
    generate_profile_card,
    generate_leaderboard_card,
    generate_schedule_card,
    generate_duel_card
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

# Helper to escape HTML tags
def esc(text: str) -> str:
    if not text:
        return ""
    return html.escape(text)

# --- Start Command ---
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or user.first_name or f"User_{user.id}"
    
    # Init user in DB
    get_user(user.id, username)
    
    welcome_text = (
        f"🛰️ <b>ASTRAAI HUB | System Online</b>\n\n"
        f"Welcome, cadet. Your student ecosystem, gamified productivity engine, "
        f"and career accelerator is fully calibrated.\n\n"
        f"<b>🤖 Tier:</b> Aspirant Cadet\n"
        f"<b>📋 Core Commands:</b>\n"
        f"• /profile - View academic vitals, XP, and streaks.\n"
        f"• /dailycheckin - Claim daily focus XP.\n"
        f"• /leaderboard - Benchmark against global top peers.\n"
        f"• /schedule - Deploy high-efficiency time protocols.\n"
        f"• /duel - Launch rapid MCQ scholastic battles.\n"
        f"• /makeresume - Create ATS-friendly Resume/CV.\n"
        f"• /diagnose &lt;text&gt; - Run orthography and spelling analysis.\n\n"
        f"<i>Enter a command or type an academic doubt directly to begin.</i>"
    )
    await update.message.reply_text(welcome_text, parse_mode="HTML")

# --- Profile Command ---
async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or user.first_name or f"User_{user.id}"
    
    db_user = get_user(user.id, username)
    
    # Generate visual profile card
    photo_stream = generate_profile_card(
        username=db_user['username'],
        level=db_user['level'],
        xp=db_user['xp'],
        streak=db_user['streak'],
        tier=db_user['tier']
    )
    
    caption_text = (
        f"👤 <b>ASTRA ACADEMIC IDENTITY CARD</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Profile details parsed. XP and level records synchronized successfully."
    )
    
    await update.message.reply_photo(
        photo=photo_stream,
        caption=caption_text,
        parse_mode="HTML"
    )

# --- Daily Check-in ---
async def daily_checkin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username or user.first_name or f"User_{user.id}"
    
    db_user, xp_gained, msg = process_daily_checkin(user.id, username)
    
    # Format message for HTML
    formatted_msg = msg.replace("**", "<b>").replace("**", "</b>")
    
    checkin_text = (
        f"📅 <b>DAILY FOCUS CHECK-IN</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{formatted_msg}\n\n"
        f"👤 <b>Total XP:</b> {db_user['xp']} XP | <b>Streak:</b> {db_user['streak']} Days"
    )
    await update.message.reply_text(checkin_text, parse_mode="HTML")

# --- Leaderboard ---
async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    board = get_leaderboard()
    
    # Generate visual leaderboard card
    photo_stream = generate_leaderboard_card(board)
    
    caption_text = (
        f"🥇 <b>ASTRAAI HUB GLOBAL BENCHMARK</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Current rankings based on global focus hours and study challenges completed."
    )
    
    await update.message.reply_photo(
        photo=photo_stream,
        caption=caption_text,
        parse_mode="HTML"
    )

# --- Schedule Command ---
async def schedule_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📌 Eisenhower Matrix", callback_data="sched_eisenhower"),
            InlineKeyboardButton("⏱️ Pomodoro (50/10)", callback_data="sched_pomodoro")
        ],
        [
            InlineKeyboardButton("🐸 Eat the Frog", callback_data="sched_frog"),
            InlineKeyboardButton("☀️ Daylight Layout", callback_data="sched_daylight")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    schedule_text = (
        f"📅 <b>PRODUCTIVITY & TIME-MANAGEMENT ENGINE</b>\n\n"
        f"Deploy advanced organizational protocols to maximize study efficiency and focus parameters. "
        f"Select a framework below to access layout specifications:"
    )
    await update.message.reply_text(schedule_text, reply_markup=reply_markup, parse_mode="HTML")

# --- Resume Builder ---
async def makeresume_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Initialize State
    save_resume_step(user.id, 1, "")
    
    start_text = (
        f"📄 <b>ATS-FRIENDLY PROFESSIONAL RESUME ENGINE</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"You will compile your credentials across 6 distinct information phases. "
        f"This design prevents cognitive overload and maintains data integrity.\n\n"
        f"👉 <b>[Phase 1 of 6] Contact Details & Headline:</b>\n"
        f"Submit your full name, professional email, phone number, and a sharp, target career headline.\n"
        f"<i>e.g., 'Amit Sharma | UPSC Aspirant & Polity Specialist | amit@email.com | +91-9999999999'</i>"
    )
    await update.message.reply_text(start_text, parse_mode="HTML")

# --- Study Duels ---
async def duel_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Check if user already in active duel
    d_state = get_duel_state(user.id)
    if d_state.get('active', 0) == 1:
        await update.message.reply_text(
            "⚠️ You are currently in an active Scholastic Duel. Complete your current run first!",
            parse_mode="HTML"
        )
        return

    keyboard = [
        [InlineKeyboardButton("🧮 Speed Aptitude Arena", callback_data="duel_arena_1")],
        [InlineKeyboardButton("🏛️ UPSC Concept Clash", callback_data="duel_arena_2")],
        [InlineKeyboardButton("🔤 Spelling & Grammar Lab", callback_data="duel_arena_3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    duel_text = (
        f"⚔️ <b>SCHOLASTIC BATTLES & DUEL ARENA</b>\n\n"
        f"Revision through intensive, high-stakes competition. "
        f"Select your arena. You will face 5 rapid-fire MCQs. "
        f"Success awards <b>+50 XP</b>. Defeat/Participation awards <b>+10 XP</b>."
    )
    await update.message.reply_text(duel_text, reply_markup=reply_markup, parse_mode="HTML")

# --- Language correction Command ---
async def diagnose_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_to_check = " ".join(context.args)
    if not text_to_check:
        await update.message.reply_text(
            "⚠️ <b>Usage:</b> <code>/diagnose [your English or Hindi text here]</code>",
            parse_mode="HTML"
        )
        return
        
    await update.message.reply_text("<i>Running linguistic orthography diagnostics...</i>", parse_mode="HTML")
    diag_res = diagnose_language(text_to_check)
    await update.message.reply_text(diag_res, parse_mode="HTML")

# --- Callback Queries Handler ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name or f"User_{user_id}"
    data = query.data
    
    # 1. Handle Productivity Schedules
    if data.startswith("sched_"):
        sched_type = data.split("_")[1]
        
        if sched_type == "menu":
            # Revert back to text menu
            keyboard = [
                [
                    InlineKeyboardButton("📌 Eisenhower Matrix", callback_data="sched_eisenhower"),
                    InlineKeyboardButton("⏱️ Pomodoro (50/10)", callback_data="sched_pomodoro")
                ],
                [
                    InlineKeyboardButton("🐸 Eat the Frog", callback_data="sched_frog"),
                    InlineKeyboardButton("☀️ Daylight Layout", callback_data="sched_daylight")
                ]
            ]
            schedule_text = (
                f"📅 <b>PRODUCTIVITY & TIME-MANAGEMENT ENGINE</b>\n\n"
                f"Deploy advanced organizational protocols to maximize study efficiency and focus parameters. "
                f"Select a framework below to access layout specifications:"
            )
            # Delete previous visual if it exists and write text menu
            try:
                await query.message.delete()
            except Exception:
                pass
            await query.message.reply_text(
                schedule_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )
            return
            
        # Draw Visual Schedule
        photo_stream = generate_schedule_card(sched_type, None)
        
        caption_text = (
            f"📅 <b>{sched_type.upper()} FOCUS MATRIX</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Review framework quadrants and timelines above. Optimize study blocks accordingly."
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="sched_menu")]]
        
        # Delete text query and reply with visual card
        try:
            await query.message.delete()
        except Exception:
            pass
            
        await query.message.reply_photo(
            photo=photo_stream,
            caption=caption_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        
    # 2. Handle Duel Arena Selection
    elif data.startswith("duel_arena_"):
        arena_num = data.split("_")[2]
        arena_name = DUEL_ARENAS[arena_num]
        questions = DUEL_QUESTIONS[arena_num]
        
        # Save state in DB
        save_duel_state(user_id, arena_name, 0, 0, questions, active=1)
        
        # Generate visual card for question 1
        first_q = questions[0]
        photo_stream = generate_duel_card(
            arena_name=arena_name,
            question_num=1,
            question_text=first_q['question'],
            options=first_q['options'],
            score=0
        )
        
        keyboard = [
            [
                InlineKeyboardButton("A", callback_data="duel_ans_A"),
                InlineKeyboardButton("B", callback_data="duel_ans_B"),
                InlineKeyboardButton("C", callback_data="duel_ans_C"),
                InlineKeyboardButton("D", callback_data="duel_ans_D")
            ]
        ]
        
        try:
            await query.message.delete()
        except Exception:
            pass
            
        await query.message.reply_photo(
            photo=photo_stream,
            caption=f"⚔️ <b>{esc(arena_name)} // Question 1</b>\nSelect your option below:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML"
        )
        
    # 3. Handle Duel Answers
    elif data.startswith("duel_ans_"):
        user_ans = data.split("_")[2]
        
        d_state = get_duel_state(user_id)
        if d_state.get('active', 0) != 1:
            await query.message.reply_text("⚠️ Duel session expired or invalid.")
            return
            
        q_idx = d_state['current_question']
        questions = d_state['questions']
        current_q = questions[q_idx]
        
        correct_ans = current_q['correct']
        score = d_state['score']
        
        is_correct = (user_ans == correct_ans)
        if is_correct:
            score += 1
            result_header = "✅ <b>CORRECT ANSWER!</b>"
        else:
            result_header = f"❌ <b>INCORRECT ANSWER</b> (You: {user_ans} | Correct: {correct_ans})"
            
        explanation_msg = (
            f"{result_header}\n\n"
            f"<b>Explanation:</b>\n{esc(current_q['explanation'])}"
        )
        
        # Delete old question photo
        try:
            await query.message.delete()
        except Exception:
            pass
            
        # Prepare next action
        if q_idx == 4: # End of duel
            # Final scoring and XP award
            victory = (score >= 4)
            xp_reward = 50 if victory else 10
            
            user_db, leveled_up = add_xp(user_id, xp_reward, username)
            
            final_text = (
                f"{explanation_msg}\n\n"
                f"🏆 <b>DUEL COMPLETE</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 <b>Aspirant:</b> {esc(username)}\n"
                f"🎯 <b>Final Score:</b> {score}/5\n"
                f"🎁 <b>XP Awarded:</b> +{xp_reward} XP\n"
                f"🔥 <b>Status:</b> {'VICTORY!' if victory else 'DEFEAT / PRACTICE COMPLETE'}\n"
            )
            if leveled_up:
                final_text += f"\n🎉 <b>LEVEL UP!</b> You reached <b>Level {user_db['level']}</b> ({user_db['tier']})!"
                
            clear_duel_state(user_id)
            await query.message.reply_text(final_text, parse_mode="HTML")
        else:
            # Advance to next question
            save_duel_state(user_id, d_state['arena'], score, q_idx + 1, questions, active=1)
            
            next_q = questions[q_idx + 1]
            next_caption = (
                f"{explanation_msg}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"⚔️ <b>{esc(d_state['arena'])} // Question {q_idx + 2}</b>\n"
                f"Select your option below:"
            )
            
            photo_stream = generate_duel_card(
                arena_name=d_state['arena'],
                question_num=q_idx + 2,
                question_text=next_q['question'],
                options=next_q['options'],
                score=score
            )
            
            keyboard = [
                [
                    InlineKeyboardButton("A", callback_data="duel_ans_A"),
                    InlineKeyboardButton("B", callback_data="duel_ans_B"),
                    InlineKeyboardButton("C", callback_data="duel_ans_C"),
                    InlineKeyboardButton("D", callback_data="duel_ans_D")
                ]
            ]
            await query.message.reply_photo(
                photo=photo_stream,
                caption=next_caption,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )

# --- General Message Text Handler ---
async def handle_message_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name or f"User_{user_id}"
    user_text = update.message.text.strip()
    
    # 1. Handle Active Resume Steps
    resume_state = get_resume_state(user_id)
    if resume_state.get('current_step', 0) > 0:
        current_step = resume_state['current_step']
        save_resume_step(user_id, current_step, user_text)
        
        next_step = current_step + 1
        if next_step > 6:
            # Final Compilation
            latest_state = get_resume_state(user_id)
            
            # Markdown Block
            resume_md = (
                f"# RESUME: {latest_state['step1_data']}\n\n"
                f"## PROFESSIONAL SUMMARY\n"
                f"{latest_state['step2_data']}\n\n"
                f"## ACADEMIC PEDIGREE\n"
                f"{latest_state['step3_data']}\n\n"
                f"## CORE COMPETENCIES\n"
                f"{latest_state['step4_data']}\n\n"
                f"## PROJECTS & ACHIEVEMENTS\n"
                f"{latest_state['step5_data']}\n\n"
                f"## EXPERIENCE & LEADERSHIP\n"
                f"{latest_state['step6_data']}\n"
            )
            
            # LaTeX Block
            resume_latex = (
                f"\\documentclass{{article}}\n"
                f"\\usepackage{{hyperref}}\n"
                f"\\begin{{document}}\n"
                f"\\title{{Resume - {latest_state['step1_data'].split('|')[0].strip()}}}\n"
                f"\\author{{{latest_state['step1_data'].split('|')[0].strip()}}}\n"
                f"\\maketitle\n\n"
                f"\\section{{Summary}}\n"
                f"{latest_state['step2_data']}\n\n"
                f"\\section{{Education}}\n"
                f"{latest_state['step3_data']}\n\n"
                f"\\section{{Skills}}\n"
                f"{latest_state['step4_data']}\n\n"
                f"\\section{{Projects}}\n"
                f"{latest_state['step5_data']}\n\n"
                f"\\section{{Experience}}\n"
                f"{latest_state['step6_data']}\n\n"
                f"\\end{{document}}"
            )
            
            # Award XP
            add_xp(user_id, 30, username)
            
            compilation_text = (
                f"🎉 <b>RESUME GENERATION COMPLETED</b>\n"
                f"XP Awarded: <b>+30 XP</b>\n\n"
                f"Below is your ATS-friendly Markdown template and standard LaTeX code. "
                f"Tap to copy and paste directly into standard compilers or Overleaf:\n\n"
                f"📋 <b>MARKDOWN FORMAT:</b>\n"
                f"<pre>{esc(resume_md)}</pre>\n\n"
                f"📋 <b>LATEX FORMAT:</b>\n"
                f"<pre>{esc(resume_latex)}</pre>"
            )
            
            clear_resume_state(user_id)
            await update.message.reply_text(compilation_text, parse_mode="HTML")
        else:
            save_resume_step(user_id, next_step, "")
            
            steps_prompts = {
                2: "<b>[Phase 2 of 6] Professional Summary:</b>\nSubmit a brief, action-verb heavy profile summary summarizing your academic focus and strengths.",
                3: "<b>[Phase 3 of 6] Academic Pedigree:</b>\nList your degrees, institutions, graduation years, and GPAs/scores.",
                4: "<b>[Phase 4 of 6] Core Competencies & Skills:</b>\nList technical skills, soft skills, or domain expertise areas (separated by commas).",
                5: "<b>[Phase 5 of 6] Projects & achievements:</b>\nDetail academic projects, publications, or competitive exam milestones (e.g. cleared Prelims).",
                6: "<b>[Phase 6 of 6] Professional Experience:</b>\nDetail previous internships, work experience, or leadership responsibilities in clubs/committees."
            }
            await update.message.reply_text(
                f"👉 {steps_prompts[next_step]}",
                parse_mode="HTML"
            )
        return
        
    # 2. General doubt clearing or input checks
    await update.message.reply_chat_action("typing")
    doubt_response = solve_academic_doubt(user_text)
    
    # Replace markdown syntax headers/bold with standard HTML formatting
    clean_res = doubt_response.replace("**", "<b>").replace("**", "</b>")
    clean_res = re.sub(r'### (.*?)\n', r'<b>\1</b>\n', clean_res)
    
    await update.message.reply_text(clean_res, parse_mode="HTML")

# --- Main Bot Execution ---
def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set. Exiting.")
        return
        
    # Build bot application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_cmd))
    application.add_handler(CommandHandler("profile", profile_cmd))
    application.add_handler(CommandHandler("dailycheckin", daily_checkin_cmd))
    application.add_handler(CommandHandler("leaderboard", leaderboard_cmd))
    application.add_handler(CommandHandler("schedule", schedule_cmd))
    application.add_handler(CommandHandler("pomodoro", schedule_cmd))
    application.add_handler(CommandHandler("makeresume", makeresume_cmd))
    application.add_handler(CommandHandler("cv", makeresume_cmd))
    application.add_handler(CommandHandler("duel", duel_cmd))
    application.add_handler(CommandHandler("battle", duel_cmd))
    application.add_handler(CommandHandler("diagnose", diagnose_cmd))
    
    # Callback queries (for inline button routing)
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Fallback to general text parsing
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_text))
    
    # Run bot
    logger.info("AstraAI Hub Telegram Bot started successfully (Visual Edition).")
    application.run_polling()

if __name__ == '__main__':
    main()
