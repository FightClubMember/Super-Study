import os
import sys
import json
from database import (
    get_user, add_xp, process_daily_checkin, get_leaderboard,
    get_resume_state, save_resume_step, clear_resume_state,
    get_duel_state, save_duel_state, clear_duel_state
)
from mentor import diagnose_language, solve_academic_doubt
from duels_data import DUEL_ARENAS, DUEL_QUESTIONS

SIM_USER_ID = 9999
SIM_USERNAME = "AstraStudent_CLI"

def clean_html(text: str) -> str:
    """Simplify HTML markup tags to make them clean in CLI terminal."""
    text = text.replace("<b>", "").replace("</b>", "")
    text = text.replace("<i>", "").replace("</i>", "")
    text = text.replace("<code>", "`").replace("</code>", "`")
    text = text.replace("<pre>", "\n---\n").replace("</pre>", "\n---\n")
    return text

def print_help():
    print("\n" + "="*50)
    print("🛰️  ASTRAAI HUB - LOCAL CLI COMMAND LIST")
    print("="*50)
    print("/start          - Welcome screen & profile setup")
    print("/profile        - View Level, XP, Streak, and Rank Tier")
    print("/dailycheckin   - Claim daily consistency XP & log check-in")
    print("/leaderboard    - View the Top 10 global peer matrix")
    print("/duel           - Initiate a 5-MCQ study battle arena")
    print("/schedule       - Deploy productivity routines & matrices")
    print("/makeresume     - Begin the 6-stage ATS Resume Compiler")
    print("/diagnose <txt> - Test the Zero-Error Language Lab on text")
    print("help            - Show this command map")
    print("exit            - Exit the simulator")
    print("="*50 + "\n")

def handle_schedule(option=""):
    schedules = {
        "1": (
            "### 📌 EISENHOWER PRODUCTIVITY MATRIX\n\n"
            "Sort your chaotic daily academic backlog into four distinct quadrants:\n"
            "1. **Urgent & Important (Do First):** Solve current day mock test errors, study high-weightage topics.\n"
            "2. **Important but Not Urgent (Schedule):** Read daily editorial, revise weak subjects.\n"
            "3. **Urgent but Not Important (Delegate/Streamline):** Sorting study materials, printing PDFs.\n"
            "4. **Neither (Eliminate):** Social media browsing, uncalibrated discussions."
        ),
        "2": (
            "### ⏱️ POMODORO FOCUS PROTOCOL (50/10 RULE)\n\n"
            "Avoid short 25-minute blocks which are insufficient for deep academic study.\n"
            "* **Deep Work Block:** 50 minutes of uninterrupted study (phone silenced, zero tabs open).\n"
            "* **Cognitive Reset:** 10 minutes of complete rest (no screen, stand up, stretch, drink water).\n"
            "* **Award:** Completing one block earns **+10 XP**."
        ),
        "3": (
            "### 🐸 'EAT THE FROG' MANDATE\n\n"
            "Tackle your hardest, most cognitively taxing academic topic first thing in the morning.\n"
            "* **Execution:** At **8:00 AM**, start with the subject you dread the most (e.g., Algebra or Laxmikanth amendments).\n"
            "* **Rationale:** Cognitive capacity and willpower are at their peak. Clearing this first guarantees daily success."
        ),
        "4": (
            "### ☀️ DAYLIGHT STRATEGY LAYOUT (For At-Home Aspirants)\n\n"
            "Treat full-time study at home like a professional 9-to-5 desk job:\n"
            "- **08:00 - 13:00:** Deep study blocks (Split into 50/10 sets). Tackle the 'Frog' here.\n"
            "- **13:00 - 14:00:** Lunch & Power Reset.\n"
            "- **14:00 - 18:00:** Secondary study modules, reasoning practice, and doubt clearance.\n"
            "- **18:00 onwards:** Revision, light reading, and physical activity.\n"
            "- **Night Rule:** Unplug early. Preserve night hours for mental recovery and deep sleep."
        )
    }
    
    if option in schedules:
        print("\n" + clean_html(schedules[option]) + "\n")
        return
        
    print("\n--- 📅 Productivity Block Engine ---")
    print("Choose a productivity protocol:")
    print("1. Eisenhower Matrix (Urgent vs Important)")
    print("2. Pomodoro Protocol (50/10 focus resetting)")
    print("3. Eat the Frog (Morning hardest task first)")
    print("4. Daylight Strategy Layout (9-to-5 study day model)")
    choice = input("Enter option number (1-4): ").strip()
    if choice in schedules:
        print("\n" + clean_html(schedules[choice]) + "\n")
    else:
        print("[ERROR] Invalid choice. Returning to console.")

def run_simulator():
    print("\n" + "!"*60)
    print("  ASTRAAI HUB ENTERPRISE TELEGRAM BOT - CLI SIMULATION SYSTEM  ")
    print("!"*60)
    print(f"Logged in as: ID: {SIM_USER_ID} | Username: {SIM_USERNAME}")
    print("Type 'help' to list commands, 'exit' to terminate.")
    
    # Initialize user profile
    get_user(SIM_USER_ID, SIM_USERNAME)
    
    while True:
        try:
            # Check current states
            resume_state = get_resume_state(SIM_USER_ID)
            duel_state = get_duel_state(SIM_USER_ID)
            
            prompt_prefix = "astraai"
            if resume_state.get('current_step', 0) > 0:
                step = resume_state['current_step']
                prompt_prefix = f"resume_step_{step}"
            elif duel_state.get('active', 0) == 1:
                q_num = duel_state['current_question'] + 1
                prompt_prefix = f"duel_q_{q_num}"
                
            user_input = input(f"\n{prompt_prefix}> ").strip()
            
            if not user_input:
                continue
                
            # Intercept exits
            if user_input.lower() == 'exit':
                print("[SYSTEM] CLI Session Terminated.")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
                
            # --- Active Duel Processing ---
            if duel_state.get('active', 0) == 1:
                q_idx = duel_state['current_question']
                questions = duel_state['questions']
                current_q = questions[q_idx]
                
                ans = user_input.upper()
                if ans not in ['A', 'B', 'C', 'D']:
                    print("[WARNING] Invalid option. Answer must be A, B, C, or D.")
                    continue
                
                correct_ans = current_q['correct']
                score = duel_state['score']
                
                print("\n" + "-"*30)
                if ans == correct_ans:
                    score += 1
                    print("✅ CORRECT ANSWER!")
                else:
                    print(f"❌ INCORRECT. Your answer: {ans} | Correct answer: {correct_ans}")
                
                print(f"Explanation:\n{current_q['explanation']}")
                print("-"*30)
                
                if q_idx == 4: # Last question completed
                    print("\n🏆 DUEL COMPLETED!")
                    print(f"Your final score: {score}/5")
                    
                    if score >= 4:
                        print("🔥 VICTORY! You won the Study Duel!")
                        user, leveled_up = add_xp(SIM_USER_ID, 50, SIM_USERNAME)
                        print("XP Awarded: **+50 XP**.")
                        if leveled_up:
                            print(f"🎉 LEVEL UP! You reached **Level {user['level']}** ({user['tier']})!")
                    else:
                        print("⚡ Defeat/Participation. Keep practicing to build speed!")
                        user, leveled_up = add_xp(SIM_USER_ID, 10, SIM_USERNAME)
                        print("XP Awarded: **+10 XP**.")
                        if leveled_up:
                            print(f"🎉 LEVEL UP! You reached **Level {user['level']}** ({user['tier']})!")
                    
                    clear_duel_state(SIM_USER_ID)
                else:
                    save_duel_state(
                        SIM_USER_ID,
                        duel_state['arena'],
                        score,
                        q_idx + 1,
                        questions,
                        active=1
                    )
                    # Show next question immediately
                    next_q = questions[q_idx + 1]
                    print(f"\nQuestion {q_idx + 2}: {next_q['question']}")
                    for opt in next_q['options']:
                        print(opt)
                continue
                
            # --- Active Resume Builder Processing ---
            if resume_state.get('current_step', 0) > 0:
                current_step = resume_state['current_step']
                save_resume_step(SIM_USER_ID, current_step, user_input)
                
                next_step = current_step + 1
                if next_step > 6:
                    # Final compilation
                    print("\n" + "="*60)
                    print("⚙️ COMPILED ATS-FRIENDLY RESUME")
                    print("="*60)
                    
                    latest_state = get_resume_state(SIM_USER_ID)
                    
                    # Generate Markdown Output
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
                    
                    print(resume_md)
                    print("="*60)
                    print("Copy the Markdown text above. You can paste it into standard compilers or converters.")
                    
                    # Award XP
                    add_xp(SIM_USER_ID, 30, SIM_USERNAME)
                    print("\nXP Awarded: **+30 XP** for Resume construction completion!")
                    clear_resume_state(SIM_USER_ID)
                else:
                    save_resume_step(SIM_USER_ID, next_step, "") # Initialize next step
                    
                    steps_prompts = {
                        2: "Phase 2: Enter your Core Professional/Academic Summary (Action-verb heavy).",
                        3: "Phase 3: Enter your Academic Pedigree (Degrees, Institutions, Scores).",
                        4: "Phase 4: Enter your Core Competencies & Technical Skills (Categorized).",
                        5: "Phase 5: Enter your Projects, Research Papers, or Competitive Exam achievements.",
                        6: "Phase 6: Enter your Professional Experience or Leadership positions."
                    }
                    print(f"\n[{next_step}/6] {steps_prompts[next_step]}")
                continue
                
            # --- Standard Commands Routing ---
            if user_input.startswith('/'):
                cmd_parts = user_input.split(maxsplit=1)
                cmd = cmd_parts[0].lower()
                cmd_args = cmd_parts[1] if len(cmd_parts) > 1 else ""
                
                if cmd == '/start':
                    print("\n--- 🛰️ AstraAI Hub initialized ---")
                    print("AstraAI Hub is active and calibrated. You are rank: Aspirant Cadet.")
                    print("Type /profile to check stats, or /duel to battle.")
                    
                elif cmd in ['/profile', '/dailycheckin']:
                    if cmd == '/profile':
                        user = get_user(SIM_USER_ID, SIM_USERNAME)
                        print(f"\n👤 **USER PROFILE PROFILE**")
                        print(f"- Username: {user['username']}")
                        print(f"- Current Level: {user['level']}")
                        print(f"- Total XP: {user['xp']} XP")
                        print(f"- Active Daily Streak: {user['streak']} Days")
                        print(f"- Current Rank Tier: {user['tier']}")
                        
                        # Show a neat text progress bar to next level
                        progress = user['xp'] % 100
                        bar = "█" * (progress // 10) + "░" * (10 - (progress // 10))
                        print(f"- Level Progress: [{bar}] {progress}/100 XP to next level")
                        
                    elif cmd == '/dailycheckin':
                        user, xp_gained, msg = process_daily_checkin(SIM_USER_ID, SIM_USERNAME)
                        print(f"\n📅 {clean_html(msg)}")
                        
                elif cmd == '/leaderboard':
                    board = get_leaderboard()
                    print("\n🥇 **GLOBAL ACADEMIC LEADERBOARD (TOP 10)**")
                    print("-" * 55)
                    for i, player in enumerate(board):
                        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f" {i+1}."
                        print(f"{medal} {player['username']:<15} | Lvl {player['level']:<2} | {player['xp']:<4} XP | {player['tier']}")
                    print("-" * 55)
                    
                elif cmd in ['/schedule', '/pomodoro']:
                    handle_schedule()
                    
                elif cmd in ['/makeresume', '/cv']:
                    print("\n--- 📄 ATS Resume Compiler Initialized ---")
                    print("You will compile your resume iteratively across 6 distinct phases.")
                    save_resume_step(SIM_USER_ID, 1, "")
                    print("[1/6] Phase 1: Enter your Contact Details & Professional Headline.")
                    
                elif cmd in ['/duel', '/battle']:
                    print("\n--- ⚔️ Scholastic Battle Duel Engine ---")
                    print("Select your Battle Arena:")
                    for k, v in DUEL_ARENAS.items():
                        print(f"{k}. {v}")
                    arena_choice = input("Enter arena number (1-3): ").strip()
                    
                    if arena_choice not in DUEL_QUESTIONS:
                        print("[ERROR] Invalid arena selection.")
                        continue
                        
                    questions = DUEL_QUESTIONS[arena_choice]
                    # Reset score, set step, active duel
                    save_duel_state(SIM_USER_ID, DUEL_ARENAS[arena_choice], 0, 0, questions, active=1)
                    
                    # Show first question
                    print(f"\n[1/5] Question 1: {questions[0]['question']}")
                    for opt in questions[0]['options']:
                        print(opt)
                        
                elif cmd == '/diagnose':
                    if not cmd_args:
                        print("[ERROR] Please provide text to analyze: `/diagnose <text>`")
                    else:
                        diag = diagnose_language(cmd_args)
                        print("\n" + clean_html(diag) + "\n")
                else:
                    print(f"[ERROR] Command '{cmd}' not recognized.")
            else:
                # Treat general inputs as doubts
                print("\n" + "~"*40)
                print("🤔 MENTOR ANSWER ENGINE:")
                doubt_response = solve_academic_doubt(user_input)
                print(clean_html(doubt_response))
                print("~"*40)
                
        except KeyboardInterrupt:
            print("\n[SYSTEM] CLI Session Terminated.")
            break
        except Exception as e:
            print(f"[SYSTEM ERROR] {str(e)}")

if __name__ == "__main__":
    run_simulator()
