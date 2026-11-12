from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#f27d85"
RED = "#e7305b"
GREEN = "#00aa00"
GREY = "#555555"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 35
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
reps = 0
flag = False
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, flag

    reps = 0
    flag = False
    title_label.config(text="Timer", fg=GREY)
    if timer is not None:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text="00:00")
        check_mark.config(text="")

# ---------------------------- TIMER STATUS CHECK ------------------------------- #
def is_timer_running():
    global flag

    if not flag:
        flag = True
        start_timer()

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, flag

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
    global timer

    count_min = count // 60
    count_sec = count % 60
    if count_min < 10:
        count_min = f"0{count_min}"
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
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
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="Timer", fg=GREY, bg=YELLOW, font=(FONT_NAME, 48))
title_label.grid(column=1, row=0)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="res/tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", command=is_timer_running, width=10, bg=YELLOW, fg="#000", highlightthickness=0)
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer, width=10, bg=YELLOW, fg=RED, highlightthickness=0)
reset_button.grid(column=2, row=2)

check_mark = Label(fg=GREEN, bg=YELLOW, highlightthickness=0)
check_mark.grid(column=1, row=3)

window.mainloop()