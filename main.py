import os
import asyncio
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict

# Import bot and DB logic
from bot import TELEGRAM_BOT_TOKEN, setup_bot
from telegram.ext import ApplicationBuilder
import database
import mentor
from duels_data import DUEL_QUESTIONS

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AstraAI Hub Web API")

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schemas for request bodies
class UserRequest(BaseModel):
    user_id: int
    username: str

class CheckinRequest(BaseModel):
    user_id: int
    username: str

class XPRequest(BaseModel):
    user_id: int
    username: str
    xp_amount: int

class DuelCompleteRequest(BaseModel):
    user_id: int
    username: str
    score: int
    won: bool

class ResumeCompileRequest(BaseModel):
    name: str
    email: str
    phone: str
    headline: str
    summary: str
    education: str
    skills: str
    projects: str
    experience: str

class DoubtRequest(BaseModel):
    user_id: int
    text: str

class DiagnoseRequest(BaseModel):
    text: str

# --- REST API Endpoints ---

@app.get("/api/user")
async def get_user_profile(user_id: int, username: str):
    try:
        user = database.get_user(user_id, username)
        return user
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/checkin")
async def process_checkin(req: CheckinRequest):
    try:
        user, xp_gained, msg = database.process_daily_checkin(req.user_id, req.username)
        return {"user": user, "xp_gained": xp_gained, "message": msg}
    except Exception as e:
        logger.error(f"Error checking in: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/add_xp")
async def add_xp(req: XPRequest):
    try:
        user, leveled_up = database.add_xp(req.user_id, req.xp_amount, req.username)
        return {"user": user, "leveled_up": leveled_up}
    except Exception as e:
        logger.error(f"Error adding XP: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leaderboard")
async def get_leaderboard():
    try:
        board = database.get_leaderboard()
        return board
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/duel/questions")
async def get_duel_questions(arena: str):
    if arena not in DUEL_QUESTIONS:
        raise HTTPException(status_code=400, detail="Invalid Arena Selected")
    return DUEL_QUESTIONS[arena]

@app.post("/api/duel/complete")
async def complete_duel(req: DuelCompleteRequest):
    try:
        xp_reward = 50 if req.won else 10
        user, leveled_up = database.add_xp(req.user_id, xp_reward, req.username)
        return {"user": user, "xp_gained": xp_reward, "leveled_up": leveled_up}
    except Exception as e:
        logger.error(f"Error completing duel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/resume/compile")
async def compile_resume(req: ResumeCompileRequest):
    try:
        contact_line = f"{req.name} | {req.headline} | {req.email} | {req.phone}"
        
        # Compile Markdown
        markdown_output = (
            f"# RESUME: {contact_line}\n\n"
            f"## PROFESSIONAL SUMMARY\n"
            f"{req.summary}\n\n"
            f"## ACADEMIC PEDIGREE\n"
            f"{req.education}\n\n"
            f"## CORE COMPETENCIES\n"
            f"{req.skills}\n\n"
            f"## PROJECTS & ACHIEVEMENTS\n"
            f"{req.projects}\n\n"
            f"## EXPERIENCE & LEADERSHIP\n"
            f"{req.experience}\n"
        )
        
        # Compile LaTeX
        latex_output = (
            f"\\documentclass{{article}}\n"
            f"\\usepackage{{hyperref}}\n"
            f"\\begin{{document}}\n"
            f"\\title{{Resume - {req.name}}}\n"
            f"\\author{{{req.name}}}\n"
            f"\\maketitle\n\n"
            f"\\section{{Summary}}\n"
            f"{req.summary}\n\n"
            f"\\section{{Education}}\n"
            f"{req.education}\n\n"
            f"\\section{{Skills}}\n"
            f"{req.skills}\n\n"
            f"\\section{{Projects}}\n"
            f"{req.projects}\n\n"
            f"\\section{{Experience}}\n"
            f"{req.experience}\n\n"
            f"\\end{{document}}"
        )
        
        return {"markdown": markdown_output, "latex": latex_output}
    except Exception as e:
        logger.error(f"Error compiling resume: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/doubt")
async def solve_doubt(req: DoubtRequest):
    try:
        # Check academic isolation triggers
        isolation_check = mentor.check_academic_isolation(req.text)
        if isolation_check:
            return {"output": isolation_check, "isolation_activated": True}
            
        # Check query ambiguity
        ambiguity_check = mentor.check_ambiguity(req.text)
        if ambiguity_check:
            return {"output": ambiguity_check, "ambiguity_activated": True}
            
        # Solve using mentor core
        response = mentor.solve_academic_doubt(req.text)
        return {"output": response, "isolation_activated": False, "ambiguity_activated": False}
    except Exception as e:
        logger.error(f"Error solving doubt: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/diagnose")
async def diagnose_lang(req: DiagnoseRequest):
    try:
        response = mentor.diagnose_language(req.text)
        return {"output": response}
    except Exception as e:
        logger.error(f"Error running language diagnosis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- Mount Static Web App Files ---
# Mounts the 'static' folder to the root '/' path
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# We serve static folder on '/static' path or can mount at root using custom handlers.
# Mounting StaticFiles at '/static' is robust
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Redirection from root to static/index.html
@app.get("/")
async def redirect_to_index():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/index.html")


# --- Unified Startup & Shutdown handlers ---
bot_app = None

@app.on_event("startup")
async def startup_event():
    global bot_app
    if TELEGRAM_BOT_TOKEN:
        try:
            bot_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
            setup_bot(bot_app)
            
            # Start telegram bot loop asynchronously
            await bot_app.initialize()
            await bot_app.start()
            await bot_app.updater.start_polling()
            logger.info("Telegram Bot Polling successfully initialized in background.")
        except Exception as e:
            logger.error(f"Failed to start Telegram Bot background polling: {e}")
    else:
        logger.warning("TELEGRAM_BOT_TOKEN not provided in env. Running API Server only.")

@app.on_event("shutdown")
async def shutdown_event():
    global bot_app
    if bot_app:
        try:
            await bot_app.updater.stop()
            await bot_app.stop()
            await bot_app.shutdown()
            logger.info("Telegram Bot Polling successfully stopped.")
        except Exception as e:
            logger.error(f"Error shutting down Telegram Bot: {e}")
