# AstraAI Hub - Premium Visual AI Student Ecosystem & Career Accelerator

AstraAI Hub is an elite academic and professional bot engineered for competitive exam aspirants, global university students, and career-driven professionals. It provides systemic study duels, pomodoro and scheduler engines, an ATS-friendly resume compiler, and high-precision language diagnostics, all powered by Groq (Llama 3) and gamified with XP, levels, and global leaderboards.

This version is the **Premium Visual Edition**, which dynamically renders stunning, dark-mode infographic cards for profile metrics, leaderboards, study duels, and schedules, delivering a next-level, immersive Telegram experience.

---

## 🎨 Visual Engine (`visuals.py`)
Rather than standard text dashboards, the bot uses the Python `Pillow` library to dynamically generate beautiful, graphic infographics:
* **Academic Identity Card (`/profile`):** Renders a personalized student card showing username, avatar icon, XP metrics, active daily streaks, and a level progress bar.
* **Scoreboard Dashboard (`/leaderboard`):** Outputs a digital matrix display highlighting the Top 10 users, complete with custom medals.
* **Productivity Infographics (`/schedule`):** Outputs visual diagrams of the Eisenhower Matrix grid, Pomodoro 50/10 timeline, or Daylight 9-to-5 schedules.
* **Scholastic Battle Board (`/duel`):** Displays MCQ questions and choices styled like a premium digital card game.

---

## Setup & Local Testing

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configuration
Open the `.env` file in the project folder:
* Place your Telegram token in `TELEGRAM_BOT_TOKEN`.
* Place your Groq API key in `GROQ_API_KEY`.

### 4. CLI Simulator (Offline Mode)
Test the core database operations, resume compiler steps, schedules, and MCQ duels directly in your console:
```powershell
python simulator.py
```

### 5. Start the Telegram Bot (Local Run)
```powershell
python bot.py
```

---

## 🚀 GitHub & Render Deployment Guide

Follow these steps to deploy your bot 24/7 on Render using the pre-configured Render Blueprint.

### Step 1: Create a GitHub Repository
1. Log in to your [GitHub](https://github.com) account.
2. Click **New** to create a new repository. Name it `astraai-hub-bot` (or similar).
3. Leave "Initialize this repository with..." options **unchecked** (no README, no .gitignore).

### Step 2: Push your Local Git Repository to GitHub
Since a local Git repository has already been initialized and committed in this directory, run the following commands in your terminal to link and push your code:
```powershell
# Add your remote GitHub URL
git remote add origin https://github.com/<your-github-username>/astraai-hub-bot.git

# Rename default branch to main
git branch -M main

# Push to your GitHub repo
git push -u origin main
```
*(Replace `<your-github-username>` with your actual GitHub username).*

### Step 3: Deploy to Render using Blueprints
Render's Blueprint service automatically parses the `render.yaml` file in the repository to launch the bot as a 24/7 Background Worker.
1. Log in to [Render](https://dashboard.render.com/).
2. Click **New** (top right) and select **Blueprint**.
3. Connect your GitHub account and select your `astraai-hub-bot` repository.
4. Render will read the `render.yaml` configuration. Under the variables prompt, enter your keys:
   * `TELEGRAM_BOT_TOKEN`
   * `GROQ_API_KEY`
5. Click **Apply**. Render will automatically build and start the bot!

---

## 🛠️ Project Structure
* `bot.py` - Core Telegram bot handlers and message routing.
* `visuals.py` - PIL canvas drawing for dark-mode infographic cards.
* `mentor.py` - Groq Llama-3 integrations (spelling correction, isolation safeguards, context preservation).
* `database.py` - SQLite DB state management.
* `duels_data.py` - Question pool.
* `render.yaml` - Render Blueprint setup.
* `simulator.py` - CLI simulator.
