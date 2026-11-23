import os
import random
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk

# QUIZ DATA: a list of dictionaries (question, four choices, answer letter)

QUESTIONS = [
    {
        "question": "Which giant, said to live in big old trees like the balete and acacia, is known for smoking an enormous cigar?",
        "choices": ["A. Tikbalang", "B. Kapre", "C. Tiyanak", "D. Santelmo"],
        "answer": "B",
    },
    {
        "question": "Which creature is said to separate its upper body from its lower half and fly into the night on bat-like wings?",
        "choices": ["A. Manananggal", "B. Diwata", "C. Sirena", "D. Bakunawa"],
        "answer": "A",
    },
    {
        "question": "Which creature has the head and hooves of a horse, very long limbs, and leads travelers astray in the mountains?",
        "choices": ["A. Kapre", "B. Sarimanok", "C. Tikbalang", "D. Dwende"],
        "answer": "C",
    },
    {
        "question": "In Philippine folklore, what is a diwata?",
        "choices": [
            "A. A flesh-eating shape-shifter",
            "B. A guardian spirit of nature",
            "C. A ghost light seen at night",
            "D. A giant sea serpent",
        ],
        "answer": "B",
    },
    {
        "question": "You pass a tall anthill at night. What do Filipinos say to ask the dwende (nuno sa punso) for permission to pass?",
        "choices": ["A. Paalam po", "B. Salamat po", "C. Mano po", "D. Tabi-tabi po"],
        "answer": "D",
    },
    {
        "question": "Which giant serpent-dragon is said to swallow the moon and cause eclipses?",
        "choices": ["A. Manananggal", "B. Kapre", "C. Bakunawa", "D. Aswang"],
        "answer": "C",
    },
    {
        "question": "Which creature imitates a crying baby to lure travelers into the forest?",
        "choices": ["A. Tiyanak", "B. Tikbalang", "C. Diwata", "D. Siyokoy"],
        "answer": "A",
    },
    {
        "question": "Which shape-shifting creature looks like an ordinary villager by day but is feared as a night-time predator?",
        "choices": ["A. Dwende", "B. Sarimanok", "C. Kapre", "D. Aswang"],
        "answer": "D",
    },
    {
        "question": "Which colorful legendary bird from Maranao folklore is shown holding a fish in its beak?",
        "choices": ["A. Bakunawa", "B. Sarimanok", "C. Tiyanak", "D. Tikbalang"],
        "answer": "B",
    },
    {
        "question": "Which mysterious floating ball of fire, often linked to restless spirits, is seen at night?",
        "choices": ["A. Kapre", "B. Diwata", "C. Santelmo", "D. Manananggal"],
        "answer": "C",
    },
]

# SETTINGS

TIME_LIMIT = 15  # seconds per question
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HIGH_SCORE_FILE = os.path.join(BASE_DIR, "high_score.txt")
HAZE_FILE = os.path.join(BASE_DIR, "assets", "haze.png")

# Every screen is designed on an 800 x 700 "design box" and then scaled up to
# fit the real window, so the game looks right when maximized or full screen.
DESIGN_W, DESIGN_H = 800, 700
CX = DESIGN_W // 2  # horizontal centre of the design box

# Colour palette: maroon / red with black
BG_FALLBACK = "#000000"   
BLACK = "#0B0305"
PANEL = "#1A0709"         # answer cards
PANEL_HOVER = "#2B0A10"
MAROON = "#5E0B15"
CRIMSON = "#B3121F"
RED_BRIGHT = "#F0283C"
CREAM = "#F5E9E4"
MUTED = "#C79DA1"
GOOD = "#4CAF7A"          # only used to mark the correct answer


# QUIZ STATE
quiz_questions = []     # shuffled copy of QUESTIONS
current_question = 0    # index of the current question
score = 0
time_left = TIME_LIMIT
wrong_answers = []      # details of incorrect answers, used for the review
timer_job = None        # id returned by root.after(), needed to cancel it
answered = False        # True once a question is submitted or time is up
player_name = ""

# Screen state (lets a screen be redrawn at a new size without losing progress)
current_screen = "start"   # "start", "question" or "results"
shown_time = TIME_LIMIT    # the number currently shown by the timer
last_result = None         # feedback of the answered question
new_record = False         # True if the finished quiz set a new high score

# Layout values, recalculated by compute_layout()
scale = 1.0
offset_x = 0.0
offset_y = 0.0
last_size = (0, 0)
resize_job = None


# WINDOW AND CANVAS
root = tk.Tk()
root.title("ALAMAT - Philippine Folklore Quiz")
root.minsize(900, 650)

selected_answer = tk.StringVar()
name_var = tk.StringVar()


def maximize_window():
    #Open the game maximized on Windows, Linux and macOS.
    try:
        root.state("zoomed")                       
    except tk.TclError:
        try:
            root.attributes("-zoomed", True)       
        except tk.TclError:
            root.geometry(f"{root.winfo_screenwidth()}x"
                          f"{root.winfo_screenheight()}+0+0")  


def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))


def leave_fullscreen(event=None):
    root.attributes("-fullscreen", False)


def pick_font(candidates, fallback):
    #Return the first installed font family from candidates.
    installed = set(tkfont.families())
    for name in candidates:
        if name in installed:
            return name
    return fallback


# Firm, bold, sharp fonts. The first one installed on the player's computer wins:)
HEAD_FAMILY = pick_font(
    ["Impact", "Haettenschweiler", "Bahnschrift", "Agency FB", "Arial Black",
     "Oswald", "Anton", "DejaVu Sans"], "Helvetica")
BODY_FAMILY = pick_font(
    ["Bahnschrift", "Franklin Gothic Demi", "Arial Black", "Arial Narrow",
     "Helvetica Neue", "DejaVu Sans"], "Helvetica")

# Base font sizes (at scale 1.0). F() scales them to the current window size.
FONT_TITLE = (HEAD_FAMILY, 54)
FONT_HEAD = (HEAD_FAMILY, 26)
FONT_BIG = (HEAD_FAMILY, 60)
FONT_QUESTION = (BODY_FAMILY, 18)
FONT_BODY = (BODY_FAMILY, 14)
FONT_SMALL = (BODY_FAMILY, 11)

canvas = tk.Canvas(root, highlightthickness=0, bg=BG_FALLBACK)
canvas.pack(fill="both", expand=True)

try:
    haze_image = tk.PhotoImage(file=HAZE_FILE)
    canvas.create_image(0, 0, image=haze_image, anchor="center", tags="bg")
except tk.TclError:
    haze_image = None  # fall back to the plain dark background

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Alamat.Horizontal.TProgressbar",
    troughcolor=BLACK, background=RED_BRIGHT, bordercolor=MAROON,
    lightcolor=RED_BRIGHT, darkcolor=CRIMSON,
)

# Items/widgets that are updated while the quiz runs
timer_item = None
feedback_item = None
timer_bar = None
submit_button = None
next_button = None
choice_buttons = []



# LAYOUT AND DRAWING HELPERS

def compute_layout():
    #Work out how much to scale the 800x700 design box for this window.
    global scale, offset_x, offset_y, last_size
    width = max(canvas.winfo_width(), 900)
    height = max(canvas.winfo_height(), 650)
    scale = max(0.8, min(width / DESIGN_W, height / DESIGN_H, 2.4))
    offset_x = (width - DESIGN_W * scale) / 2
    offset_y = (height - DESIGN_H * scale) / 2
    last_size = (canvas.winfo_width(), canvas.winfo_height())
    canvas.coords("bg", width / 2, height / 2)  # keep the haze centred


def X(x):
    return offset_x + x * scale


def Y(y):
    return offset_y + y * scale


def F(base_font):
    """Scale a (family, size) pair and make it bold."""
    return (base_font[0], max(8, round(base_font[1] * scale)), "bold")


def add_text(x, y, text, font, fill=CREAM, anchor="center", width=0,
             justify="left", shadow=False):
    """Draw text on the canvas. A black offset copy gives a sharp shadow."""
    wrap = int(width * scale) if width else 0
    if shadow:
        canvas.create_text(X(x) + 3 * scale, 
                           Y(y) + 3 * scale, 
                           text=text,
                           font=F(font), 
                           fill=BLACK, 
                           anchor=anchor, 
                           width=wrap,
                           justify=justify, 
                           tags="screen"
                        )
    return canvas.create_text(X(x), Y(y), 
                              text=text, 
                              font=F(font), 
                              fill=fill,
                              anchor=anchor, 
                              width=wrap, 
                              justify=justify,
                              tags="screen"
                            )


def add_widget(widget, x, y, anchor="center", width=None, height=None):
    kwargs = {"window": widget, "anchor": anchor, "tags": "screen"}
    if width:
        kwargs["width"] = int(width * scale)
    if height:
        kwargs["height"] = int(height * scale)
    return canvas.create_window(X(x), Y(y), **kwargs)


def make_button(text, command, color=CRIMSON, fg=CREAM, width=14):
    #A flat, square-edged button with bold capital letters.
    return tk.Button(
        canvas, 
        text=text.upper(), 
        command=command, 
        font=F(FONT_BODY),
        bg=color, 
        fg=fg, 
        activebackground=RED_BRIGHT, 
        activeforeground=CREAM,
        disabledforeground="#7A4A50", 
        relief="flat", 
        bd=0, 
        cursor="hand2",
        padx=int(14 * scale), 
        pady=int(10 * scale), 
        width=width,
    )


def clear_screen():
    #Remove every text item and widget (but keep the haze background).
    canvas.delete("screen")
    for widget in canvas.winfo_children():
        widget.destroy()


def on_resize(event=None):
    #Redraw the current screen shortly after the window size settles.
    global resize_job
    if resize_job is not None:
        root.after_cancel(resize_job)
    resize_job = root.after(150, apply_resize)


def apply_resize():
    global resize_job
    resize_job = None
    if (canvas.winfo_width(), canvas.winfo_height()) == last_size:
        return
    redraw_current_screen()


def redraw_current_screen():
   #Draw the current screen again at the new size (progress is kept).
    if current_screen == "question":
        draw_question()
    elif current_screen == "results":
        draw_results()
    else:
        draw_start_screen()



# HIGH SCORE (file handling)

def get_high_score():
    #Read the saved high score. Return 0 if the file is missing or invalid.
    if os.path.exists(HIGH_SCORE_FILE):
        try:
            with open(HIGH_SCORE_FILE, "r") as file:
                return int(file.read().strip())
        except (ValueError, OSError):
            return 0
    return 0


def save_high_score(new_score):
    #Write new_score to the file only if it beats the old one.
    if new_score > get_high_score():
        try:
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(new_score))
            return True
        except OSError:
            return False
    return False



# START SCREEN

def show_start_screen():
    global current_screen
    stop_timer()
    current_screen = "start"
    draw_start_screen()


def draw_start_screen():
    clear_screen()
    compute_layout()

    add_text(CX, 120, "ALAMAT", FONT_TITLE, RED_BRIGHT, shadow=True)
    canvas.create_line(X(250), 
                       Y(175), 
                       X(550), 
                       Y(175), 
                       fill=CRIMSON,
                       width=max(2, int(3 * scale)), 
                       tags="screen"
                    )
    add_text(CX, 205, "A QUIZ OF PHILIPPINE CREATURES", FONT_BODY, CREAM)

    add_text(CX, 290, f"{len(QUESTIONS)} QUESTIONS", FONT_HEAD, CREAM)
    add_text(CX, 335, f"{TIME_LIMIT} SECONDS EACH", FONT_HEAD, CREAM)
    add_text(CX, 395, f"HIGH SCORE: {get_high_score()} / {len(QUESTIONS)}",
             FONT_BODY, RED_BRIGHT, shadow=True)

    add_text(CX, 465, "YOUR NAME (OPTIONAL)", FONT_SMALL, MUTED)
    entry = tk.Entry(
        canvas, 
        textvariable=name_var, 
        font=F(FONT_BODY),
        justify="center", 
        bg=BLACK, 
        fg=CREAM, 
        insertbackground=CREAM,
        relief="flat", 
        highlightthickness=2,
        highlightbackground=MAROON, 
        highlightcolor=RED_BRIGHT
        )
    add_widget(entry, CX, 500, width=280, height=38)

    add_widget(make_button("Enter the forest", start_quiz, width=20), CX, 590)
    add_text(CX, 670, "F11 = FULL SCREEN    ESC = EXIT FULL SCREEN", FONT_SMALL, MUTED)



# STARTING / RESTARTING

def start_quiz():
    #Reset all variables, shuffle the questions and show the first one.
    global quiz_questions, current_question, score, wrong_answers, player_name
    player_name = name_var.get().strip()
    quiz_questions = random.sample(QUESTIONS, len(QUESTIONS))  # new shuffled list
    current_question = 0
    score = 0
    wrong_answers = []
    show_question()



# QUESTION SCREEN

def show_question():
    #Reset the per-question state, draw the screen and start the timer.
    global answered, time_left, shown_time, last_result, current_screen
    stop_timer()
    current_screen = "question"
    answered = False
    time_left = TIME_LIMIT
    shown_time = TIME_LIMIT
    last_result = None
    selected_answer.set("")  # no choice pre-selected
    draw_question()
    update_timer()


def draw_question():
    #Build the question screen from the current state (also used on resize).
    global timer_item, feedback_item, timer_bar
    global submit_button, next_button, choice_buttons

    clear_screen()
    compute_layout()
    choice_buttons = []

    question = quiz_questions[current_question]
    total = len(quiz_questions)

    # Progress (left) and score (right)
    add_text(
        50, 40, 
        f"QUESTION {current_question + 1} OF {total}", 
        FONT_BODY,
        MUTED, 
        anchor="w"
    )
    add_text(750, 40, f"SCORE: {score}", FONT_BODY, MUTED, anchor="e")

    # Timer text and bar
    timer_item = add_text(
        CX, 
        90, 
        f"TIME LEFT: {shown_time}s", 
        FONT_HEAD,
        RED_BRIGHT if shown_time <= 5 else CREAM, 
        shadow=True
    )
    timer_bar = ttk.Progressbar(
        canvas, 
        style="Alamat.Horizontal.TProgressbar",
        maximum=TIME_LIMIT, value=shown_time
    )
    add_widget(timer_bar, CX, 135, width=700, height=14)

    # Question text
    add_text(
        50, 170, 
        question["question"], 
        FONT_QUESTION, 
        CREAM, 
        anchor="nw",
        width=700, 
        shadow=True
    )

    # Four radio buttons that share one variable; the value is the letter
    for number, choice in enumerate(question["choices"]):
        letter = choice[0]
        button = tk.Radiobutton(
            canvas, 
            text=choice, 
            variable=selected_answer, 
            value=letter,
            indicatoron=0, 
            font=F(FONT_BODY), 
            bg=PANEL, 
            fg=CREAM,
            selectcolor=MAROON, 
            activebackground=PANEL_HOVER,
            activeforeground=CREAM, 
            disabledforeground=CREAM, 
            relief="flat",
            bd=0, 
            anchor="w", 
            padx=int(18 * scale), 
            cursor="hand2",
            highlightthickness=1, 
            highlightbackground=MAROON,
        )
        add_widget(
            button, 
            50, 275 + number * 62, 
            anchor="nw",
            width=700, 
            height=50
        )
        choice_buttons.append(button)

    feedback_item = add_text(
        CX, 
        535, 
        "", 
        FONT_BODY, 
        CREAM, 
        anchor="n",
        width=700, 
        justify="center"
    )

    submit_button = make_button("Submit", submit_answer)
    add_widget(submit_button, 300, 625)
    next_button = make_button("Next", next_question, color=PANEL, fg=MUTED)
    next_button.config(state="disabled")
    add_widget(next_button, 500, 625)

    if answered:  # redrawn after the question was already answered
        lock_choices()
        submit_button.config(state="disabled")
        canvas.itemconfig(
            feedback_item, 
            text=last_result["text"],
            fill=last_result["color"]
        )
        highlight_choices(question, last_result["chosen"])
        enable_next()



# TIMER

def update_timer():
    #Show the time left, then call itself again after one second.
    global time_left, timer_job, shown_time
    if answered:
        return
    shown_time = time_left
    canvas.itemconfig(
        timer_item, 
        text=f"TIME LEFT: {time_left}s",
        fill=RED_BRIGHT if time_left <= 5 else CREAM
    )
    timer_bar.config(value=time_left)
    if time_left == 0:
        time_up()
        return
    time_left -= 1
    timer_job = root.after(1000, update_timer)


def stop_timer():
    #Cancel the scheduled timer call, if there is one.
    global timer_job
    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None



# ANSWER CHECKING

def lock_choices():
    for button in choice_buttons:
        button.config(state="disabled")


def choice_text(question, letter):
    """Return the full choice text (e.g. 'B. Kapre') for a letter."""
    for choice in question["choices"]:
        if choice[0] == letter:
            return choice
    return "No answer (time is up)"


def highlight_choices(question, chosen_letter):
    #Colour the correct choice green and a wrong choice red.
    for button, choice in zip(choice_buttons, question["choices"]):
        letter = choice[0]
        if letter == question["answer"]:
            button.config(bg=GOOD, fg=BLACK, disabledforeground=BLACK)
        elif letter == chosen_letter:
            button.config(bg=RED_BRIGHT, fg=CREAM, disabledforeground=CREAM)


def submit_answer():
    #Check the selected answer. Does nothing if already submitted.
    global score, answered, last_result
    if answered:  # blocks double submission
        return

    choice = selected_answer.get()
    if choice == "":
        messagebox.showwarning("No answer", "Please select an answer first.")
        return  # timer keeps running

    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct = choice_text(question, question["answer"])
    if choice == question["answer"]:
        score += 1
        text, color = "CORRECT! +1 POINT", GOOD
    else:
        wrong_answers.append({
            "question": question["question"],
            "your_answer": choice_text(question, choice),
            "correct_answer": correct,
        })
        text, color = f"WRONG. CORRECT ANSWER: {correct}", RED_BRIGHT
    last_result = {"chosen": choice, "text": text, "color": color}
    canvas.itemconfig(feedback_item, text=text, fill=color)
    highlight_choices(question, choice)
    enable_next()


def time_up():
    #Same as a wrong submission, but the player gave no answer.
    global answered, last_result
    if answered:
        return
    answered = True
    stop_timer()
    lock_choices()
    submit_button.config(state="disabled")

    question = quiz_questions[current_question]
    correct = choice_text(question, question["answer"])
    wrong_answers.append({
        "question": question["question"],
        "your_answer": "No answer (time is up)",
        "correct_answer": correct,
    })
    text = f"TIME IS UP! CORRECT ANSWER: {correct}"
    last_result = {"chosen": "", "text": text, "color": RED_BRIGHT}
    canvas.itemconfig(feedback_item, text=text, fill=RED_BRIGHT)
    highlight_choices(question, "")
    enable_next()


def enable_next():
    # On the last question the button leads to the results
    if current_question == len(quiz_questions) - 1:
        next_button.config(text="SEE RESULTS")
    next_button.config(state="normal", bg=CRIMSON, fg=CREAM)


def next_question():
    #Go to the next question, or to the results after the last one.
    global current_question
    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        show_results()



# RESULTS SCREEN

def performance_message(percentage):
    if percentage >= 90:
        return "Albularyo-level wisdom! Even the spirits bow to you."
    elif percentage >= 70:
        return "You walked the forest and lived to tell the tale."
    elif percentage >= 50:
        return "The tikbalang nearly got you. Study the lore!"
    else:
        return "Lost in the woods... follow the trail and try again."


def show_results():
   #Save the high score once, then draw the results screen.
    global current_screen, new_record
    stop_timer()
    current_screen = "results"
    new_record = save_high_score(score)
    draw_results()


def draw_results():
    clear_screen()
    compute_layout()
    total = len(quiz_questions)
    percentage = (score / total) * 100

    heading = f"THE HUNT ENDS, {player_name.upper()}!" if player_name else "THE HUNT ENDS!"
    add_text(CX, 45, heading, FONT_HEAD, RED_BRIGHT, shadow=True)
    add_text(CX, 120, f"{score} / {total}", FONT_BIG, CREAM, shadow=True)
    add_text(CX, 185, f"{percentage:.0f}%  -  {performance_message(percentage)}",
             FONT_SMALL, CREAM, width=700, justify="center")

    if new_record:
        add_text(CX, 220, "NEW HIGH SCORE!", FONT_BODY, GOOD, shadow=True)
    else:
        add_text(CX, 220, f"HIGH SCORE: {get_high_score()} / {total}",
                 FONT_BODY, MUTED)

    # Answer review: scrollable, read-only text box
    add_text(50, 255, "ANSWER REVIEW", FONT_SMALL, MUTED, anchor="w")
    box_frame = tk.Frame(
        canvas, 
        bg=BLACK, 
        highlightthickness=1,
        highlightbackground=MAROON
    )
    scrollbar = tk.Scrollbar(box_frame)
    scrollbar.pack(side="right", fill="y")
    review_box = tk.Text(
        box_frame, 
        font=F(FONT_SMALL), 
        bg=BLACK, 
        fg=CREAM,
        relief="flat", 
        wrap="word", 
        padx=14, 
        pady=10,
        yscrollcommand=scrollbar.set
    )
    review_box.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=review_box.yview)
    add_widget(box_frame, 50, 275, anchor="nw", width=700, height=300)

    review_box.tag_configure("q", foreground=CREAM)
    review_box.tag_configure("bad", foreground=RED_BRIGHT)
    review_box.tag_configure("good", foreground=GOOD)

    if not wrong_answers:
        review_box.insert("end", "Perfect score! Nothing to review.", "good")
    else:
        for number, item in enumerate(wrong_answers, start=1):
            review_box.insert("end", f"{number}. {item['question']}\n", "q")
            review_box.insert("end", f"    Your answer: {item['your_answer']}\n", "bad")
            review_box.insert("end", f"    Correct answer: {item['correct_answer']}\n\n", "good")
    review_box.config(state="disabled")  # read-only

    add_widget(make_button("Restart", start_quiz, width=12), 230, 640)
    add_widget(make_button("Home", show_start_screen, color=PANEL, fg=CREAM,
                           width=12), 400, 640)
    add_widget(make_button("Exit", on_close, color=PANEL, fg=CREAM, width=12),
               570, 640)



# CLOSING AND START-UP

def on_close():
    #Cancel the timer before destroying the window to avoid errors.
    stop_timer()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", leave_fullscreen)

maximize_window()
root.update()          # let the window reach its maximized size before drawing
canvas.bind("<Configure>", on_resize)
show_start_screen()
root.mainloop()
