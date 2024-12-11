from tkinter import *
import pandas as pd
import random as rd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_to_learn = {}

try:
    # Create Pandas DataFrame from CSV file
    # If file does not exist, create a new one from the original file
    df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
        original_data = pd.read_csv("data/french_words.csv")
        words_to_learn = original_data.to_dict(orient="records")
else:    
    words_to_learn = df.to_dict(orient="records")

  

# Generate random French word
def generate_next_word():
    """Generate a new French word"""
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card = rd.choice(words_to_learn)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], font=("Ariel", 40, "bold"), fill="black")
    canvas.itemconfig(card_background, image=front_img)

    # Reveal translation after 3 seconds
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    """Flips the card based on time."""
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_img)

def is_known():
    """Removes the current card from the list and saves the updated list to a CSV file."""
    words_to_learn.remove(current_card)
    data = pd.DataFrame(words_to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    generate_next_word()



# -------------------------- GUI Setup --------------------------------------

# Window
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# Images
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
unknown_img = PhotoImage(file="images/wrong.png")
correct_img = PhotoImage(file="images/right.png")


# Canvas
canvas = Canvas(width=800, height=526)
card_background = canvas.create_image(400, 263, image=front_img)
title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill="black")
word = canvas.create_text(400, 263, text="word", font=("Ariel", 40, "bold"), fill="black")
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
unknown_btn = Button(image=unknown_img, command=generate_next_word, highlightthickness=0)
unknown_btn.grid(row=1, column=0)

correct_btn = Button(image=correct_img,command=is_known, highlightthickness=0)
correct_btn.grid(row=1, column=1)


# Generate the first card
generate_next_word()

# Start event listener
window.mainloop()




