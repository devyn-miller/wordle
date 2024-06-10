import tkinter as tk
from tkinter import messagebox
import random

# Load words from file
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.word_length = 5  # Default word length
        self.max_guesses = 6  # Default number of guesses
        self.create_widgets()  # First create all widgets
        self.set_word_length()  # Then set the word length

    def update_settings(self, word_length=None, max_guesses=None):
        if word_length is not None:
            self.word_length = word_length
        if max_guesses is not None:
            self.max_guesses = max_guesses

    def create_widgets(self):
        self.length_var = tk.IntVar(value=5)
        length_frame = tk.Frame(self.root)
        length_frame.grid(row=0, column=0, columnspan=12, pady=10)
        tk.Label(length_frame, text="Select word length:").pack(side=tk.LEFT)
        for i in range(4, 13):
            tk.Radiobutton(length_frame, text=str(i), variable=self.length_var, value=i, command=self.set_word_length).pack(side=tk.LEFT)

        self.entries = []
        self.labels = []

        for i in range(self.max_guesses):
            row_entries = []
            for j in range(self.word_length):
                entry = tk.Entry(self.root, width=2, font=('Helvetica', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)  # Add padding to avoid overlap
                entry.bind("<KeyRelease>", lambda event, e=entry: self.on_type(event, e))
                row_entries.append(entry)

            self.entries.append(row_entries)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_word)
        self.submit_button.grid(row=self.max_guesses + 1, column=0, columnspan=12, pady=10)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.give_hint)
        self.hint_button.grid(row=self.max_guesses + 1, column=13, columnspan=12, pady=10)

    def set_word_length(self):
        for i in range(len(self.entries)):
            for j in range(len(self.entries[i])):
                self.entries[i][j].delete(0, tk.END)  # Clear the entry widget

    def check_word(self):
        if self.current_attempt >= self.max_guesses:
            messagebox.showinfo("Game Over", "No more attempts left!")
            return

        guess = ''.join([self.entries[self.current_attempt][i].get().lower() for i in range(self.word_length)])
        if len(guess) != self.word_length or guess not in words:
            messagebox.showwarning("Invalid Word", "Please enter a valid word.")
            return

        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                self.labels[self.current_attempt][i].config(text=guess[i], bg='green')
            elif guess[i] in self.target_word:
                self.labels[self.current_attempt][i].config(text=guess[i], bg='gold')
            else:
                self.labels[self.current_attempt][i].config(text=guess[i], bg='grey')

        if guess == self.target_word:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            self.root.quit()
        else:
            self.current_attempt += 1
            if self.current_attempt >= self.max_guesses:
                messagebox.showinfo("Game Over", f"The word was: {self.target_word}")
                self.root.quit()
            self.display_keyboard([entry.get().lower() for entry_row in self.entries for entry in entry_row if entry.get() != ''], self.target_word)

    def give_hint(self):
        if self.current_attempt >= self.max_guesses:
            messagebox.showinfo("Game Over", "No more attempts left!")
            return

        hint = f"Contains {len(set(self.target_word))} distinct letters"
        messagebox.showinfo("Hint", hint)
        self.current_attempt += 1

    def display_keyboard(self, guesses, solution):
        keyboard_layout = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        key_status = {key: 'gray' for key in keyboard_layout}

        for guess in guesses:
            for idx, char in enumerate(guess.upper()):
                if char in keyboard_layout:  # Ensure the character is a valid key
                    if char in solution:
                        if solution[idx] == char:
                            key_status[char] = 'green'
                        elif key_status[char] != 'green':
                            key_status[char] = 'yellow'
                    else:
                        if key_status.get(char) != 'yellow':  # Use .get() to avoid KeyError
                            key_status[char] = 'gray'

        # Create a frame for the keyboard
        keyboard_frame = tk.Frame(self.root)
        keyboard_frame.grid(row=self.max_guesses + 2, column=0, columnspan=12, pady=20)

        # Display the keyboard
        for i, key in enumerate(keyboard_layout):
            key_button = tk.Button(keyboard_frame, text=key, bg=key_status[key], width=2, font=('Helvetica', 18))
            key_button.grid(row=i // 10, column=i % 10)

    def on_type(self, event, entry):
        try:
            next_index = self.entries[self.current_attempt].index(entry) + 1
            if next_index < self.word_length:
                self.entries[self.current_attempt][next_index].focus()
        except ValueError:
            pass  # Handle the case where the entry is not found in the list

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()