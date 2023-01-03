from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
JAPANESE_WORDS = "data/japanese_words.csv"

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv(JAPANESE_WORDS)
to_learn = data.to_dict(orient="records")
current_card = {}


# ---------------------------- FLIP CARDS ------------------------------- #

def card_flip():
    english_word = current_card["English"]
    if len(english_word) > 15:
        canvas.itemconfig(word, text=english_word, fill="white", font=("arial", 50, "bold"))
    canvas.itemconfig(card_bg, image=card_back)
    canvas.itemconfig(word, text=english_word, fill="white")
    canvas.itemconfig(lang, text="English", fill="white")


# ---------------------------- NEW FLASH CARDS ------------------------------- #

def new_card():
    global current_card, timer
    window.after_cancel(timer)

    current_card = random.choice(to_learn)
    foreign_word = current_card["Japanese"]
    canvas.itemconfig(card_bg, image=card_front)
    canvas.itemconfig(lang, text="Japanese", fill="black")
    canvas.itemconfig(word, text=foreign_word, fill="black")

    timer = window.after(3000, card_flip)


# ---------------------------- NEW LIST ------------------------------- #

def known_card():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Card")
window.config(padx=80, pady=50, bg=BACKGROUND_COLOR)
timer = window.after(3000, card_flip)

# Images
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
wrong_button = PhotoImage(file="images/wrong.png")
right_button = PhotoImage(file="images/right.png")

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)
canvas.config()
card_bg = canvas.create_image(400, 263, image=card_front)
lang = canvas.create_text(400, 150, text="Language", font=("arial", 40, "italic"))
word = canvas.create_text(400, 300, text="Word", font=("arial", 60, "bold"))

# Buttons
save_btn = Button(image=wrong_button, highlightthickness=0, command=new_card)
save_btn.grid(row=1, column=0)
check_btn = Button(image=right_button, highlightthickness=0, command=known_card)
check_btn.grid(row=1, column=1)

new_card()

window.mainloop()
