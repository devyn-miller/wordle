import tkinter as tk
from tkinter import messagebox
import random

# Load words from file
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")
        self.attempts = 6
        self.current_attempt = 0
        self.word_length = 5
        self.target_word = ""
        self.create_widgets()

    def create_widgets(self):
        self.length_var = tk.IntVar(value=5)
        length_frame = tk.Frame(self.root)
        length_frame.grid(row=0, column=0, columnspan=12, pady=10)
        tk.Label(length_frame, text="Select word length:").pack(side=tk.LEFT)
        for i in range(4, 13):
            tk.Radiobutton(length_frame, text=str(i), variable=self.length_var, value=i, command=self.set_word_length).pack(side=tk.LEFT)

        self.entries = []
        self.labels = []

        for i in range(self.attempts):
            entry_row = []
            label_row = []
            for j in range(12):  # Maximum 12 letters
                entry = tk.Entry(self.root, width=2, font=('Helvetica', 24), justify='center')
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                entry_row.append(entry)

                label = tk.Label(self.root, width=2, font=('Helvetica', 24), justify='center')
                label.grid(row=i+1, column=j + 13, padx=5, pady=5)
                label_row.append(label)

            self.entries.append(entry_row)
            self.labels.append(label_row)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.check_word)
        self.submit_button.grid(row=self.attempts + 1, column=0, columnspan=12, pady=10)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.give_hint)
        self.hint_button.grid(row=self.attempts + 1, column=13, columnspan=12, pady=10)

    def set_word_length(self):
        self.word_length = self.length_var.get()
        self.target_word = random.choice([word for word in words if len(word) == self.word_length])
        self.current_attempt = 0
        for i in range(self.attempts):
            for j in range(12):
                self.entries[i][j].delete(0, tk.END)
                self.entries[i][j].config(state=tk.NORMAL if j < self.word_length else tk.DISABLED)
                self.labels[i][j].config(text="", bg=self.root.cget("bg"))

    def check_word(self):
        if self.current_attempt >= self.attempts:
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
                self.labels[self.current_attempt][i].config(text=guess[i], bg='yellow')
            else:
                self.labels[self.current_attempt][i].config(text=guess[i], bg='grey')

        if guess == self.target_word:
            messagebox.showinfo("Congratulations!", "You guessed the word!")
            self.root.quit()
        else:
            self.current_attempt += 1
            if self.current_attempt >= self.attempts:
                messagebox.showinfo("Game Over", f"The word was: {self.target_word}")
                self.root.quit()

    def give_hint(self):
        if self.current_attempt >= self.attempts:
            messagebox.showinfo("Game Over", "No more attempts left!")
            return

        hint = f"Contains {len(set(self.target_word))} distinct letters"
        messagebox.showinfo("Hint", hint)
        self.current_attempt += 1

if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()