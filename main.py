from tkinter import *
from pathlib import Path
import time

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#f27d85"
RED = "#e7305b"
DARK_RED = "#990000"
GREEN = "#00aa00"
DARK_GREEN = "#006600"
GREY = "#444444"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
BASE_DIR = Path(__file__).resolve().parent
TOMATO_IMG_DIR = BASE_DIR / "res" / "tomato.png"
reps = 0
is_active = False
is_paused = False
is_reset = True
timer = None
next_tick = None
rem_ms = 0
cnt = 0

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global timer, reps, is_active, is_paused, is_reset

    is_active = False
    is_paused = False

    if not is_reset:
        window.after_cancel(timer)
        if reps % 8 == 0:
            txt = f"{LONG_BREAK_MIN if LONG_BREAK_MIN >= 10 else f"0{LONG_BREAK_MIN}"}:00"
        elif reps % 2 == 0:
            txt = f"{SHORT_BREAK_MIN if SHORT_BREAK_MIN >= 10 else f"0{SHORT_BREAK_MIN}"}:00"
        else:
            txt = f"{WORK_MIN if WORK_MIN >= 10 else f"0{WORK_MIN}"}:00"
        canvas.itemconfig(timer_text, text=txt)
        timer_controller.configure(text="Start", command=is_timer_running, fg=DARK_GREEN)
        reset_button.configure(text="Reset")
        reps -= 1
        is_reset = True
        
        return

    reps = 0
    title_label.config(text="Timer", fg=GREY)
    if timer is not None:
        window.after_cancel(timer)
        timer = None
        timer_controller.configure(text="Start", command=is_timer_running, fg=DARK_GREEN)
        reset_button.configure(text="Reset")
        canvas.itemconfig(timer_text, text="00:00")
        check_mark.config(text="")

# ---------------------------- PAUSE MECHANISM ------------------------------- # 
def pause_resume():
    global is_paused, timer, rem_ms, next_tick

    if not is_paused:
        rem_ms = max(0, (next_tick - time.perf_counter()) * 1000)
        window.after_cancel(timer)
        is_paused = True
        timer_controller.configure(text="Resume")
    else:
        next_tick = time.perf_counter() + rem_ms / 1000
        timer = window.after(round(rem_ms), count_down, cnt - 1)
        is_paused = False
        timer_controller.configure(text="Pause")

# ---------------------------- TIMER STATUS CHECK ------------------------------- #
def is_timer_running():
    global is_active, is_reset

    if not is_active:
        is_active = True
        timer_controller.configure(text="Pause", command=pause_resume, fg=GREY)
        if is_reset:
            reset_button.configure(text="Restart")
        start_timer()

# ---------------------------- START MECHANISM ------------------------------- # 
def start_timer():
    global reps, is_reset

    is_reset = False
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    reps += 1

    if reps % 8 == 0:
        title_label.config(text="Long Break", fg=RED)
        count_down(long_break_sec)
    elif reps % 2 == 0:
        title_label.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    else:
        title_label.config(text="Work", fg=GREEN)
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global timer, cnt, next_tick

    cnt = count
    count_min = count // 60
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        next_tick = time.perf_counter() + 1
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        for _ in range(reps // 2):
            marks += "✔️"

        check_mark.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
tomato_img = PhotoImage(file=TOMATO_IMG_DIR)
window.iconphoto(True, tomato_img)
window.config(padx=100, pady=50, bg=YELLOW)


title_label = Label(text="Timer", fg=GREY, bg=YELLOW, font=(FONT_NAME, 48))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

timer_controller = Button(text="Start", command=is_timer_running, width=10, bg=YELLOW, fg=DARK_GREEN, highlightthickness=0)
timer_controller.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer, width=10, bg=YELLOW, fg=DARK_RED, highlightthickness=0)
reset_button.grid(column=2, row=2)

check_mark = Label(fg=GREEN, bg=YELLOW, highlightthickness=0)
check_mark.grid(column=1, row=3)

window.mainloop()