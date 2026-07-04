import sqlite3
import json
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'astraai.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # User Profile Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            last_checkin TEXT,
            tier TEXT DEFAULT 'Aspirant Cadet'
        )
    ''')
    
    # Resume Builder State Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resume_builder (
            user_id INTEGER PRIMARY KEY,
            current_step INTEGER DEFAULT 0,
            step1_data TEXT,
            step2_data TEXT,
            step3_data TEXT,
            step4_data TEXT,
            step5_data TEXT,
            step6_data TEXT
        )
    ''')
    
    # Duel State Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS duels (
            user_id INTEGER PRIMARY KEY,
            arena TEXT,
            current_question INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            questions_json TEXT,
            active INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def calculate_tier(level):
    if level >= 13:
        return "Grandmaster Strategist (Top 1%)"
    elif level >= 8:
        return "Elite Focus Master"
    elif level >= 4:
        return "Novice Scholar"
    else:
        return "Aspirant Cadet"

def get_user(user_id, username="Aspirant"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row is None:
        # Create user
        cursor.execute(
            "INSERT INTO users (user_id, username, xp, level, streak, tier) VALUES (?, ?, 0, 1, 0, 'Aspirant Cadet')",
            (user_id, username)
        )
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
    user_dict = dict(row)
    conn.close()
    return user_dict

def update_user(user_id, username, xp, level, streak, last_checkin, tier):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users 
        SET username = ?, xp = ?, level = ?, streak = ?, last_checkin = ?, tier = ? 
        WHERE user_id = ?
    ''', (username, xp, level, streak, last_checkin, tier, user_id))
    conn.commit()
    conn.close()

def add_xp(user_id, xp_amount, username="Aspirant"):
    user = get_user(user_id, username)
    new_xp = max(0, user['xp'] + xp_amount)
    
    # Level progression formula: Level = 1 + floor(XP / 100)
    new_level = 1 + (new_xp // 100)
    new_tier = calculate_tier(new_level)
    
    # Check if level up occurred
    leveled_up = new_level > user['level']
    
    update_user(
        user_id=user_id,
        username=username if username else user['username'],
        xp=new_xp,
        level=new_level,
        streak=user['streak'],
        last_checkin=user['last_checkin'],
        tier=new_tier
    )
    
    updated_user = get_user(user_id, username)
    return updated_user, leveled_up

def process_daily_checkin(user_id, username="Aspirant"):
    user = get_user(user_id, username)
    today_str = date.today().isoformat()
    last_checkin_str = user['last_checkin']
    
    xp_gained = 0
    message = ""
    streak = user['streak']
    
    if last_checkin_str == today_str:
        return user, 0, "Already checked in today. Keep maintaining focus!"
    
    if last_checkin_str:
        last_checkin_date = date.fromisoformat(last_checkin_str)
        delta_days = (date.today() - last_checkin_date).days
        if delta_days == 1:
            streak += 1
            xp_gained = 20 + min(streak * 2, 30) # base 20 XP + streak bonus (capped at 50 XP total)
            message = f"Check-in successful! Streak maintained. Streak: **{streak} Days**. XP Awarded: **+{xp_gained} XP**."
        elif delta_days > 1:
            streak = 1
            xp_gained = 20
            message = f"Check-in successful! Streak reset. Active Streak: **1 Day** (Gap: {delta_days} days). XP Awarded: **+20 XP**."
    else:
        streak = 1
        xp_gained = 20
        message = f"First daily check-in logged! Streak initiated: **1 Day**. XP Awarded: **+20 XP**."
        
    new_xp = user['xp'] + xp_gained
    new_level = 1 + (new_xp // 100)
    new_tier = calculate_tier(new_level)
    
    update_user(
        user_id=user_id,
        username=username if username else user['username'],
        xp=new_xp,
        level=new_level,
        streak=streak,
        last_checkin=today_str,
        tier=new_tier
    )
    
    updated_user = get_user(user_id, username)
    return updated_user, xp_gained, message

def get_leaderboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, xp, level, tier FROM users ORDER BY xp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    
    leaderboard = []
    for row in rows:
        leaderboard.append(dict(row))
        
    # Fill in mock data if less than 10 users to look professional
    mocks = [
        {"username": "Aditya_UPSC", "xp": 1450, "level": 15, "tier": "Grandmaster Strategist (Top 1%)"},
        {"username": "Priya_Focus", "xp": 1280, "level": 13, "tier": "Grandmaster Strategist (Top 1%)"},
        {"username": "Rohan_CGL", "xp": 950, "level": 10, "tier": "Elite Focus Master"},
        {"username": "Neha_Scholar", "xp": 820, "level": 9, "tier": "Elite Focus Master"},
        {"username": "Siddharth_CDS", "xp": 640, "level": 7, "tier": "Novice Scholar"},
        {"username": "Ananya_Polity", "xp": 590, "level": 6, "tier": "Novice Scholar"},
        {"username": "Vikram_Frog", "xp": 410, "level": 5, "tier": "Novice Scholar"},
    ]
    
    for mock in mocks:
        if len(leaderboard) >= 10:
            break
        # Avoid duplicating usernames that actually exist
        if not any(u['username'].lower() == mock['username'].lower() for u in leaderboard):
            leaderboard.append(mock)
            
    # Sort again in case user data inserts between mock data
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)
    return leaderboard[:10]

# --- Resume State Management ---
def get_resume_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM resume_builder WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return {"current_step": 0}
    return dict(row)

def save_resume_step(user_id, step, data_str):
    conn = get_connection()
    cursor = conn.cursor()
    # Check if user exists in table
    cursor.execute("SELECT current_step FROM resume_builder WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    if row is None:
        cursor.execute("INSERT INTO resume_builder (user_id, current_step) VALUES (?, ?)", (user_id, step))
    
    step_col = f"step{step}_data"
    cursor.execute(f"UPDATE resume_builder SET current_step = ?, {step_col} = ? WHERE user_id = ?", (step, data_str, user_id))
    conn.commit()
    conn.close()

def clear_resume_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resume_builder WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# --- Duel State Management ---
def get_duel_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM duels WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        return {"active": 0}
    
    res = dict(row)
    if res['questions_json']:
        res['questions'] = json.loads(res['questions_json'])
    else:
        res['questions'] = []
    return res

def save_duel_state(user_id, arena, score, current_question, questions_list, active=1):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT active FROM duels WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    
    questions_json = json.dumps(questions_list)
    if row is None:
        cursor.execute('''
            INSERT INTO duels (user_id, arena, score, current_question, questions_json, active) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, arena, score, current_question, questions_json, active))
    else:
        cursor.execute('''
            UPDATE duels 
            SET arena = ?, score = ?, current_question = ?, questions_json = ?, active = ? 
            WHERE user_id = ?
        ''', (arena, score, current_question, questions_json, active, user_id))
    conn.commit()
    conn.close()

def clear_duel_state(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM duels WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# Initialize tables immediately on import
init_db()
