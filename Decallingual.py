import tkinter as tk
from tkinter import messagebox
import symspellpy
from symspellpy.symspellpy import SymSpell, Verbosity

sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dictionary_path = "frequency_dictionary_en_82_765.txt"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

manual_corrections = {
    "lets": "let's",
    "letus": "let us",
    "dont": "don't",
    "wont": "won't",
    "its": "it's",
    "youre": "you're",
    "theres": "there's",
    "im": "I'm",
    "ive": "I've",
    "supercede": "supersede",
    "pneumonoultramicroscopicsilicovolcanoconiosis": "pneumonoultramicroscopicsilicovolcanoconiosis",
    "bibilos": "bibilous",
    "manageriel": "managerial",
    "dekracinate": "decracinate",
    "funambullist": "funambulist",
    "ambission": "ambition",
    "enormitee": "enormity",
    "arant": "arrant",
    "bellie": "belie",
    "abchure": "abjure"
}

def correct_text():
    input_word = text_entry.get().strip()
    if not input_word:
        messagebox.showerror("Input Error", "Please enter a word.")
        return
    
    corrected_word = manual_corrections.get(input_word.lower(), input_word)
    
    if corrected_word.lower() == input_word.lower():
        suggestions = sym_spell.lookup(input_word, Verbosity.CLOSEST, max_edit_distance=2)
        if suggestions and suggestions[0].term != input_word:
            corrected_word = suggestions[0].term
            
    if corrected_word.lower() == input_word.lower():
        result_label.config(text="No errors found.")
    else:
        result_label.config(text=f"Corrected word: {corrected_word}")

# Zoom control variables
zoom_factor = 1.0

def zoom_in():
    global zoom_factor
    zoom_factor += 0.1
    update_zoom()

def zoom_out():
    global zoom_factor
    zoom_factor -= 0.1
    update_zoom()

def update_zoom():
    global zoom_factor
    
    font_size = int(14 * zoom_factor)
    title_label.config(font=("Arial", int(24 * zoom_factor)))
    input_label.config(font=("Arial", font_size))
    text_entry.config(font=("Arial", font_size), width=int(30 * zoom_factor))
    correct_button.config(font=("Arial", font_size))
    result_label.config(font=("Arial", font_size), wraplength=400)
    
    # Update button sizes on the keyboard
    for button in keyboard_buttons:
        button.config(font=("Arial", int(10 * zoom_factor)), width=int(3 * zoom_factor))

# Create the virtual keyboard with upper and lower case
def on_key_press(key):
    current_text = text_entry.get()
    text_entry.delete(0, tk.END)
    text_entry.insert(0, current_text + key)

def toggle_case():
    global is_upper_case
    is_upper_case = not is_upper_case
    update_keyboard_case()

def update_keyboard_case():
    for button, label in zip(keyboard_buttons, keyboard_labels):
        button.config(text=label.upper() if is_upper_case else label.lower())

def create_keyboard():
    global keyboard_labels
    keys = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
    ]
    
    keyboard_labels = [key for row in keys for key in row]  # Flatten the keys
    buttons = []
    
    for row in keys:
        row_frame = tk.Frame(window)
        for key in row:
            button = tk.Button(row_frame, text=key, width=3, height=2, font=("Arial", 10), command=lambda key=key: on_key_press(key))
            button.pack(side="left", padx=1)
            buttons.append(button)
        row_frame.pack(pady=3)

    return buttons

# Tkinter window setup
window = tk.Tk()
window.title("Decallingual")
window.geometry("500x600")

# Title label
title_label = tk.Label(window, text="Decallingual", font=("Arial", 24))
title_label.pack(pady=10)

# Zoom buttons
zoom_buttons_frame = tk.Frame(window)
zoom_in_button = tk.Button(zoom_buttons_frame, text="Zoom In", font=("Arial", 14), command=zoom_in)
zoom_out_button = tk.Button(zoom_buttons_frame, text="Zoom Out", font=("Arial", 14), command=zoom_out)
zoom_in_button.pack(side="left", padx=5)
zoom_out_button.pack(side="right", padx=5)
zoom_buttons_frame.pack(pady=10)

# Input label and entry
input_label = tk.Label(window, text="Enter a word to check:")
input_label.pack(pady=5)

text_entry = tk.Entry(window, font=("Arial", 14), width=30)
text_entry.pack(pady=5)

# Correct button
correct_button = tk.Button(window, text="Correct", font=("Arial", 14), command=correct_text)
correct_button.pack(pady=10)

# Result label
result_label = tk.Label(window, text="", font=("Arial", 14), wraplength=400)
result_label.pack(pady=5)

# Create virtual keyboard buttons
keyboard_buttons_frame = tk.Frame(window)
keyboard_buttons = create_keyboard()

# Initially, show the keyboard
for button in keyboard_buttons_frame.winfo_children():
    button.pack(side="left", padx=1)

# Attribution text positioned on the right corner
attribution_label = tk.Label(window, text="A project by Arrjuneshwar", font=("Arial", 12))
attribution_label.pack(side="right", pady=10, padx=20)

# Start the Tkinter event loop
window.mainloop()
