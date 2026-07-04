# AstraAI Hub - Enterprise AI Student Ecosystem & Career Placement Accelerator

AstraAI Hub is an elite academic and professional bot engineered for competitive exam aspirants, global university students, and career-driven professionals. It provides systemic study duels, pomodoro and scheduler engines, an ATS-friendly resume compiler, and high-precision language diagnostics, all powered by Groq (Llama 3) and gamified with XP, levels, and global leaderboards.

---

## Features

1. **Gamification & Leaderboard (`/profile`, `/dailycheckin`, `/leaderboard`):**
   * Experience points (XP) tracking.
   * Rank progressions from `Aspirant Cadet` to `Grandmaster Strategist`.
   * Medal-based peer leaderboard system.

2. **Systemic Study Duels (`/duel`):**
   * Three distinct revision arenas: Speed Aptitude (Quant shortcuts), UPSC Concept Clash (General Studies), Spelling/Grammar Lab.
   * Interactive 5-MCQ rapid fire rounds with score evaluation and rule breakdown.

3. **ATS Professional Resume Builder (`/makeresume` or `/cv`):**
   * Guided 6-stage interactive compiler (Contact info, Summary, Education, Skills, Projects, Experience).
   * Generates clean, ready-to-use raw Markdown or standard LaTeX code blocks.

4. **Zero-Error Language Correction Lab:**
   * Analyzes spelling and orthography diagnostics (using Syllable Parsing for English and short/long vowel phonetics for Hindi).

5. **Advanced Productivity block Engine (`/schedule` or `/pomodoro`):**
   * Custom schedules implementing the Eisenhower Matrix, Pomodoro Protocol, "Eat the Frog," and the "Daylight Strategy Layout" for full-time at-home aspirants.

6. **Global Exam Mentorship & Doubt Solver:**
   * Answers General Studies, Quant, and English questions.
   * **Academic Bank Isolation Rule:** Commands university students to suspend competitive schedules 10-15 days prior to undergraduate semester exams.
   * **Context Preservation:** Offers 3 clear choices when queries are ambiguous.

---

## Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system. 

### 2. Install Dependencies
Navigate to the directory and run:
```powershell
pip install -r requirements.txt
```

### 3. Configuration
Open the `.env` file in the project folder:
* Place your Telegram token in `TELEGRAM_BOT_TOKEN`.
* Place your Groq API key in `GROQ_API_KEY`.

---

## How to Run

### Option A: Local CLI Simulator (Recommended for Testing)
Test all features, gamification, resume builders, and LLM doubts directly in your terminal, without needing a Telegram connection:
```powershell
python simulator.py
```

### Option B: Telegram Bot
Start the Telegram bot:
```powershell
python bot.py
```
*(Ensure you have filled out `TELEGRAM_BOT_TOKEN` in `.env` before running).*
