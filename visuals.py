import io
import os
from PIL import Image, ImageDraw, ImageFont

# Define Color Palette (Sci-fi Cyberpunk / Academic Dark Mode)
BG_DARK = (10, 11, 19)       # #0a0b13
CARD_BG = (22, 25, 43, 200)  # Transparent dark blue
ACCENT_VIOLET = (147, 51, 234) # #9333ea
ACCENT_CYAN = (6, 182, 212)   # #06b6d4
ACCENT_AMBER = (245, 158, 11)  # #f59e0b
TEXT_WHITE = (255, 255, 255)
TEXT_GRAY = (156, 163, 175)

def get_font(size, bold=False):
    """Find and load a TTF font on the host OS. Falls back to default font if missing."""
    # List of candidate font paths across Windows and Linux
    font_names = []
    if bold:
        font_names = [
            "arialbd.ttf", "segoeuib.ttf", "calibrib.ttf", "DejaVuSans-Bold.ttf",
            "LiberationSans-Bold.ttf", "Ubuntu-B.ttf"
        ]
    else:
        font_names = [
            "arial.ttf", "segoeui.ttf", "calibri.ttf", "DejaVuSans.ttf",
            "LiberationSans-Regular.ttf", "Ubuntu-R.ttf"
        ]
        
    system_paths = [
        "C:\\Windows\\Fonts\\",
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/truetype/liberation/",
        "/usr/share/fonts/truetype/ubuntu/",
        "/usr/share/fonts/dejavu/",
        "/usr/share/fonts/liberation/",
        "" # Current directory fallback
    ]
    
    for path in system_paths:
        for name in font_names:
            full_path = os.path.join(path, name)
            if os.path.exists(full_path):
                try:
                    return ImageFont.truetype(full_path, size)
                except Exception:
                    pass
    
    # Ultimate fallback
    return ImageFont.load_default()

def draw_gradient_background(draw, width, height, start_color, end_color):
    """Fills the canvas with a vertical linear gradient."""
    for y in range(height):
        # Calculate interpolation factor
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def draw_rounded_card(draw, box, radius, fill, outline=None, width=1):
    """Helper to draw a rounded card with optional border."""
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def wrap_text(text, font, max_width):
    """Wraps text into lines that fit within a maximum pixel width."""
    # Fallback if load_default() is used (which does not support getbbox)
    if not hasattr(font, 'getbbox'):
        return [text[i:i+40] for i in range(0, len(text), 40)]
        
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_str = ' '.join(current_line)
        # get size of line_str
        bbox = font.getbbox(line_str)
        w = bbox[2] - bbox[0]
        if w > max_width:
            if len(current_line) == 1:
                lines.append(line_str)
                current_line = []
            else:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# --- Profile Card Generator ---
def generate_profile_card(username, level, xp, streak, tier) -> io.BytesIO:
    width, height = 800, 450
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    
    # 1. Background Gradient
    draw_gradient_background(draw, width, height, (12, 14, 28), (22, 16, 45))
    
    # Decorative Neon Lines
    draw.line([(0, 0), (width, 0)], fill=ACCENT_CYAN, width=4)
    draw.line([(0, height-1), (width, height-1)], fill=ACCENT_VIOLET, width=4)
    
    # Load fonts
    font_title = get_font(32, bold=True)
    font_subtitle = get_font(18, bold=False)
    font_bold = get_font(24, bold=True)
    font_stat_val = get_font(42, bold=True)
    font_stat_lbl = get_font(14, bold=False)
    
    # 2. Draw Header
    draw.text((40, 35), "ASTRAAI STUDENT ECOSYSTEM", fill=ACCENT_CYAN, font=font_subtitle)
    draw.text((40, 60), f"ACADEMIC VITALS // {username.upper()}", fill=TEXT_WHITE, font=font_title)
    
    # 3. Glassmorphic main statistics box
    draw_rounded_card(draw, (40, 125, 760, 325), radius=16, fill=CARD_BG, outline=ACCENT_VIOLET, width=2)
    
    # Left Avatar Circle
    avatar_center = (130, 225)
    avatar_radius = 60
    draw.ellipse(
        [(avatar_center[0]-avatar_radius, avatar_center[1]-avatar_radius), 
         (avatar_center[0]+avatar_radius, avatar_center[1]+avatar_radius)],
        fill=(31, 38, 68), outline=ACCENT_CYAN, width=3
    )
    
    # Initials
    initials = username[:2].upper() if username else "ST"
    draw.text((avatar_center[0] - 22, avatar_center[1] - 20), initials, fill=TEXT_WHITE, font=font_bold)
    
    # Stats columns (Level, XP, Streak)
    col_x_start = 240
    
    # Column 1: Level
    draw.text((col_x_start, 155), "LEVEL", fill=TEXT_GRAY, font=font_stat_lbl)
    draw.text((col_x_start, 180), f"{level:02d}", fill=ACCENT_CYAN, font=font_stat_val)
    
    # Column 2: XP
    draw.text((col_x_start + 140, 155), "EXPERIENCE", fill=TEXT_GRAY, font=font_stat_lbl)
    draw.text((col_x_start + 140, 180), f"{xp}", fill=TEXT_WHITE, font=font_stat_val)
    
    # Column 3: Streak
    draw.text((col_x_start + 320, 155), "FOCUS STREAK", fill=TEXT_GRAY, font=font_stat_lbl)
    draw.text((col_x_start + 320, 180), f"{streak}d 🔥", fill=ACCENT_AMBER, font=font_stat_val)
    
    # Progress Bar to next level (next 100 XP)
    progress_val = xp % 100
    bar_x = 240
    bar_y = 270
    bar_w = 480
    bar_h = 16
    
    # Draw Background bar
    draw_rounded_card(draw, (bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=8, fill=(15, 23, 42))
    # Draw Filled bar (XP %)
    filled_w = int(bar_w * (progress_val / 100.0))
    if filled_w > 4:
        draw_rounded_card(draw, (bar_x, bar_y, bar_x + filled_w, bar_y + bar_h), radius=8, fill=ACCENT_CYAN)
        
    progress_lbl = f"{progress_val} / 100 XP to Level Up"
    draw.text((bar_x + 310, 290), progress_lbl, fill=TEXT_GRAY, font=font_subtitle)
    
    # Rank Tier badge (Lower left footer)
    draw.text((40, 360), f"🏅 TIER PROGRESSION:", fill=TEXT_GRAY, font=font_subtitle)
    draw.text((220, 360), f"{tier.upper()}", fill=ACCENT_AMBER, font=font_bold)
    
    # Save image to bytes stream
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# --- Leaderboard Card Generator ---
def generate_leaderboard_card(board) -> io.BytesIO:
    width, height = 800, 600
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Background
    draw_gradient_background(draw, width, height, (9, 10, 20), (25, 18, 48))
    
    # Neon Headers
    draw.line([(0, 0), (width, 0)], fill=ACCENT_AMBER, width=4)
    
    font_title = get_font(30, bold=True)
    font_subtitle = get_font(16, bold=False)
    font_bold = get_font(20, bold=True)
    font_regular = get_font(16, bold=False)
    
    # Title
    draw.text((40, 35), "ASTRAAI HUB GLOBAL BENCHMARK", fill=ACCENT_AMBER, font=font_subtitle)
    draw.text((40, 55), "LEADERBOARD // TOP 10 FOCUS ELITE", fill=TEXT_WHITE, font=font_title)
    
    # Draw leaderboard matrix table
    start_y = 120
    row_h = 42
    
    # Table Header
    draw_rounded_card(draw, (40, start_y, 760, start_y + 36), radius=6, fill=(30, 41, 59))
    draw.text((60, start_y + 8), "RANK", fill=TEXT_GRAY, font=font_bold)
    draw.text((160, start_y + 8), "USER PROFILE", fill=TEXT_GRAY, font=font_bold)
    draw.text((420, start_y + 8), "ACADEMIC TIER", fill=TEXT_GRAY, font=font_bold)
    draw.text((650, start_y + 8), "XP SCORE", fill=TEXT_GRAY, font=font_bold)
    
    for idx, player in enumerate(board):
        curr_y = start_y + 45 + (idx * row_h)
        
        # Color coding for Top 3
        bg_color = CARD_BG
        border_color = (31, 41, 55)
        text_color = TEXT_WHITE
        medal = f"{idx + 1}"
        
        if idx == 0:
            bg_color = (251, 191, 36, 30) # Gold transparency
            border_color = ACCENT_AMBER
            medal = "🥇 1"
        elif idx == 1:
            bg_color = (209, 213, 219, 30) # Silver transparency
            border_color = (156, 163, 175)
            medal = "🥈 2"
        elif idx == 2:
            bg_color = (180, 83, 9, 30) # Bronze transparency
            border_color = (180, 83, 9)
            medal = "🥉 3"
            
        draw_rounded_card(draw, (40, curr_y, 760, curr_y + row_h - 4), radius=6, fill=bg_color, outline=border_color, width=1)
        
        # Draw columns
        draw.text((60, curr_y + 8), medal, fill=text_color, font=font_bold)
        draw.text((160, curr_y + 8), player['username'], fill=text_color, font=font_bold)
        draw.text((420, curr_y + 8), player['tier'].split(" (")[0], fill=TEXT_GRAY, font=font_regular)
        draw.text((650, curr_y + 8), f"{player['xp']} XP", fill=ACCENT_CYAN, font=font_bold)
        
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# --- Schedule Infographic Card ---
def generate_schedule_card(framework_name, schedule_data) -> io.BytesIO:
    """Generates an aesthetic layout diagram of the requested productivity protocol."""
    width, height = 800, 600
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    
    draw_gradient_background(draw, width, height, (10, 11, 20), (16, 24, 48))
    
    draw.line([(0, 0), (width, 0)], fill=ACCENT_CYAN, width=4)
    
    font_title = get_font(28, bold=True)
    font_subtitle = get_font(16, bold=False)
    font_bold = get_font(20, bold=True)
    font_regular = get_font(15, bold=False)
    
    draw.text((40, 35), "ASTRA TIME & FOCUS ENGINE", fill=ACCENT_CYAN, font=font_subtitle)
    draw.text((40, 55), f"FRAMEWORK // {framework_name.upper()}", fill=TEXT_WHITE, font=font_title)
    
    # Route according to framework
    if "eisenhower" in framework_name.lower():
        # Render a 2x2 grid representing the Eisenhower Matrix
        box_w, box_h = 330, 200
        coords = [
            ((50, 130, 380, 330), "1. URGENT & IMPORTANT", "DO FIRST", "• Immediate mock review\n• Weak area topic resolution\n• Impending deadline study", (220, 38, 38, 40), (220, 38, 38)), # Red
            ((420, 130, 750, 330), "2. IMPORTANT NOT URGENT", "SCHEDULE", "• Editorial analysis\n• Regular standard readings\n• Weak subject restructuring", (37, 99, 235, 40), (37, 99, 235)), # Blue
            ((50, 350, 380, 550), "3. URGENT NOT IMPORTANT", "DELEGATE / REDUCE", "• Arranging study logs\n• Resolving admin issues\n• Printing test keys", (217, 119, 6, 40), (217, 119, 6)), # Amber
            ((420, 350, 750, 550), "4. ELIMINATE / VOID", "VOID", "• Doomscrolling prep forums\n• Uncalibrated group chats\n• Passive reading loops", (75, 85, 99, 40), (75, 85, 99)) # Gray
        ]
        
        for box, title, action, bullet_points, fill_col, border_col in coords:
            draw_rounded_card(draw, box, radius=10, fill=fill_col, outline=border_col, width=2)
            draw.text((box[0] + 15, box[1] + 15), title, fill=TEXT_WHITE, font=font_bold)
            draw.text((box[0] + 15, box[1] + 40), f"ACTION: {action}", fill=ACCENT_CYAN, font=font_subtitle)
            
            # Bullet points draw
            y_offset = 80
            for pt in bullet_points.split('\n'):
                draw.text((box[0] + 15, box[1] + y_offset), pt, fill=TEXT_WHITE, font=font_regular)
                y_offset += 25
                
    elif "pomodoro" in framework_name.lower():
        # Renders the Pomodoro timeline
        draw_rounded_card(draw, (40, 130, 760, 550), radius=16, fill=CARD_BG, outline=ACCENT_VIOLET, width=2)
        
        draw.text((80, 160), "THE ASTRA 50/10 ELITE FOCUS TIMELINE", fill=ACCENT_CYAN, font=font_bold)
        
        # Draw Timeline Blocks
        # Block 1: Deep Work (50 mins)
        draw_rounded_card(draw, (80, 220, 500, 350), radius=10, fill=(147, 51, 234, 40), outline=ACCENT_VIOLET, width=2)
        draw.text((100, 240), "PHASE 1: DEEP WORK BLOCK", fill=TEXT_WHITE, font=font_bold)
        draw.text((100, 270), "Duration: 50 Minutes\n• All notifications silenced.\n• Single-task focus parameters enforced.\n• Complete a dedicated study item (e.g. 1 DPSP section).", fill=TEXT_WHITE, font=font_regular)
        
        # Block 2: Break (10 mins)
        draw_rounded_card(draw, (520, 220, 720, 350), radius=10, fill=(6, 182, 212, 40), outline=ACCENT_CYAN, width=2)
        draw.text((540, 240), "PHASE 2: RESET", fill=TEXT_WHITE, font=font_bold)
        draw.text((540, 270), "Duration: 10 Min\n• Complete reset.\n• No screen stimulus.\n• Stand, stretch, hydrate.", fill=TEXT_WHITE, font=font_regular)
        
        # Rationale section
        draw_rounded_card(draw, (80, 380, 720, 520), radius=10, fill=(15, 23, 42))
        draw.text((100, 400), "SYSTEM DESIGN ADVANTAGE // WHY 50/10 OVER 25/5?", fill=ACCENT_AMBER, font=font_bold)
        draw.text((100, 430), "1. Deep study requires cognitive momentum. 25 minutes is too brief to entering flow state.\n"
                              "2. A full 50-minute block triggers robust neural consolidation during revision cycles.\n"
                              "3. Completing one Pomodoro blocks awards you +10 XP.", fill=TEXT_WHITE, font=font_regular)
    
    elif "frog" in framework_name.lower():
        # Renders Eat the Frog concept card
        draw_rounded_card(draw, (40, 130, 760, 550), radius=16, fill=CARD_BG, outline=ACCENT_AMBER, width=2)
        draw.text((80, 170), "EAT THE FROG: MORNING COGNITIVE ATTACK", fill=ACCENT_AMBER, font=font_bold)
        
        draw.text((80, 220), "CORE PROTOCOL SPECIFICATIONS:", fill=TEXT_WHITE, font=font_bold)
        draw.text((80, 260), "⏰ Target Execution Time: 08:00 AM Daily\n\n"
                             "🐸 Define 'The Frog': The single most challenging, conceptually heavy, or\n"
                             "   stress-inducing task in your academic queue.\n\n"
                             "🎯 Execution Standard: Tackle this task first, before any administrative study,\n"
                             "   reading news, or doing light revisions.\n\n"
                             "⚡ Psychological Advantage: Willpower, focus, and energy are at maximum parameters\n"
                             "   at the start of the day. Accomplishing the hardest task first establishes\n"
                             "   intense positive momentum.", fill=TEXT_WHITE, font=font_regular)
        
        # Visual diagram
        draw_rounded_card(draw, (80, 440, 720, 510), radius=8, fill=(15, 23, 42))
        draw.text((100, 460), "08:00 AM (Max Energy) ──🐸 Eat Frog ──> 11:00 AM (High Momentum) ──> Easy Tasks", fill=ACCENT_CYAN, font=font_bold)
        
    else:
        # Daylight strategy layout timeline
        draw_rounded_card(draw, (40, 130, 760, 550), radius=16, fill=CARD_BG, outline=ACCENT_CYAN, width=2)
        draw.text((80, 150), "THE DAYLIGHT STRATEGY: PROFESSIONAL 9-to-5", fill=ACCENT_CYAN, font=font_bold)
        
        timeline_items = [
            ("08:00 - 13:00", "DEEP WORK SLOTS", "Execute morning blocks. Focus on 'Eat the Frog' modules.", ACCENT_VIOLET),
            ("13:00 - 14:00", "LUNCH & RESET", "Power nap or physical rest. Zero cognitive load.", ACCENT_AMBER),
            ("14:00 - 18:00", "SECONDARY STUDY MODULES", "Solve Reasoning papers, practice calculation, clarify doubt logs.", ACCENT_CYAN),
            ("18:00 - 22:00", "CONSOLIDATION & NIGHT RULES", "Lighter reading, daily editorial reviews, early screens off for recovery.", TEXT_GRAY)
        ]
        
        y_offset = 200
        for time_span, title, description, color in timeline_items:
            # Bullet/Time Block
            draw_rounded_card(draw, (80, y_offset, 220, y_offset + 50), radius=6, fill=(15, 23, 42), outline=color, width=1)
            draw.text((95, y_offset + 15), time_span, fill=color, font=font_bold)
            
            # Content details
            draw.text((250, y_offset + 5), title, fill=TEXT_WHITE, font=font_bold)
            draw.text((250, y_offset + 28), description, fill=TEXT_GRAY, font=font_regular)
            y_offset += 75
            
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output

# --- Scholastic Battle MCQ Duel Card ---
def generate_duel_card(arena_name, question_num, question_text, options, score) -> io.BytesIO:
    width, height = 800, 500
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    
    draw_gradient_background(draw, width, height, (12, 10, 24), (24, 16, 42))
    
    draw.line([(0, 0), (width, 0)], fill=ACCENT_VIOLET, width=4)
    
    font_title = get_font(24, bold=True)
    font_subtitle = get_font(14, bold=False)
    font_bold = get_font(18, bold=True)
    font_regular = get_font(15, bold=False)
    
    draw.text((40, 30), f"SCHOLASTIC DUEL // ARENA: {arena_name.upper()}", fill=ACCENT_CYAN, font=font_subtitle)
    draw.text((40, 48), f"QUESTION {question_num} OF 5", fill=TEXT_WHITE, font=font_title)
    
    # Show active score in upper right
    draw.text((640, 35), f"SCORE: {score}/5", fill=ACCENT_AMBER, font=font_bold)
    
    # 1. Question Box
    draw_rounded_card(draw, (40, 100, 760, 230), radius=12, fill=CARD_BG, outline=ACCENT_VIOLET, width=1)
    
    # Wrap and print question text
    wrapped_lines = wrap_text(question_text, font_bold, 680)
    y_offset = 120
    for line in wrapped_lines:
        draw.text((60, y_offset), line, fill=TEXT_WHITE, font=font_bold)
        y_offset += 25
        
    # 2. Options Grid
    # Option coordinates in 2x2 grid
    opt_boxes = [
        ((40, 250, 390, 350), options[0]),
        ((410, 250, 760, 350), options[1]),
        ((40, 370, 390, 470), options[2]),
        ((410, 370, 760, 470), options[3])
    ]
    
    for box, text in opt_boxes:
        draw_rounded_card(draw, box, radius=8, fill=(15, 23, 42), outline=TEXT_GRAY, width=1)
        # Wrap option text to fit within individual boxes
        wrapped_opt = wrap_text(text, font_regular, 320)
        opt_y = box[1] + 15
        for line in wrapped_opt:
            draw.text((box[0] + 15, opt_y), line, fill=TEXT_WHITE, font=font_regular)
            opt_y += 20
            
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)
    return output
