import tkinter as tk
from tkinter import messagebox
import random

# Load words from file
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]

class WordleGame:
    def __init__(self, root, word_length=5, max_guesses=6):
        self.root = root
        self.root.title("Wordle Game")
        self.word_length = word_length
        self.max_guesses = max_guesses
        self.current_attempt = 0
        self.target_word = ""
        self.create_widgets()

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
            entry_row = []
            label_row = []
            for j in range(12):  # Maximum 12 letters
                entry = tk.Entry(self.root, width=2, font=('Helvetica', 24), justify='center')
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                entry.bind("<KeyRelease>", lambda event, e=entry: self.on_type(event, e))
                entry_row.append(entry)

                label = tk.Label(self.root, width=2, font=('Helvetica', 24), justify='center')
                label.grid(row=i+1, column=j + 13, padx=5, pady=5)
                label_row.append(label)

            self.entries.append(entry_row)
            self.labels.append(label_row)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_word)
        self.submit_button.grid(row=self.max_guesses + 1, column=0, columnspan=12, pady=10)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.give_hint)
        self.hint_button.grid(row=self.max_guesses + 1, column=13, columnspan=12, pady=10)

    def set_word_length(self):
        self.word_length = self.length_var.get()
        self.target_word = random.choice([word for word in words if len(word) == self.word_length])
        self.current_attempt = 0
        for i in range(self.max_guesses):
            for j in range(12):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(state=tk.NORMAL if j < self.word_length else tk.DISABLED)
                self.labels[i][j].config(text="", bg=self.root.cget("bg"))

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
            for idx, char in enumerate(guess):
                if char in solution:
                    if solution[idx] == char:
                        key_status[char] = 'green'
                    elif key_status[char] != 'green':
                        key_status[char] = 'yellow'
                else:
                    if key_status[char] == 'gray':
                        key_status[char] = 'gray'

        # Display the keyboard
        for key in keyboard_layout:
            print(f"{key}: {key_status[key]}")

    def on_type(self, event, entry):
        current_text = entry.get()
        if len(current_text) > 1:
            entry.delete(1, tk.END)
        next_index = self.entries[self.current_attempt].index(entry) + 1
        if len(current_text) == 1 and next_index < len(self.entries[self.current_attempt]):
            self.entries[self.current_attempt][next_index].focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()