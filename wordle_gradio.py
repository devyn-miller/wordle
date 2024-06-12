import gradio as gr
import random


# Load words from file
with open('words.txt', 'r') as file:
    words = [line.strip() for line in file.readlines()]

class WordleGame:
    def __init__(self):
        self.word_length = 5  # Default word length
        self.max_guesses = 6  # Default number of guesses
        self.target_word = random.choice([word for word in words if len(word) == self.word_length])
        self.current_attempt = 0
        self.guesses = []

    def update_settings(self, word_length=None, max_guesses=None):
        if word_length is not None:
            self.word_length = word_length
        if max_guesses is not None:
            self.max_guesses = max_guesses
        self.target_word = random.choice([word for word in words if len(word) == self.word_length])
        self.current_attempt = 0
        self.guesses = []

    def check_word(self, guess):
        if len(guess) != self.word_length:
            return "Invalid guess length. Please enter a word with the correct length."

        self.guesses.append(guess)
        feedback = []
        for idx, char in enumerate(guess):
            if char == self.target_word[idx]:
                feedback.append('green')
            elif char in self.target_word:
                feedback.append('yellow')
            else:
                feedback.append('gray')

        if guess == self.target_word:
            return f"Congratulations! You've guessed the word: {self.target_word}"

        if self.current_attempt >= self.max_guesses - 1:
            return f"Game Over! The correct word was: {self.target_word}"

        self.current_attempt += 1
        return feedback

    def display_keyboard(self):
        keyboard_layout = 'QWERTYUIOPASDFGHJKLZXCVBNM'
        key_status = {key: 'gray' for key in keyboard_layout}

        for guess in self.guesses:
            for idx, char in enumerate(guess.upper()):
                if char in keyboard_layout:  # Ensure the character is a valid key
                    if char in self.target_word:
                        if self.target_word[idx] == char:
                            key_status[char] = 'green'
                        elif key_status[char] != 'green':
                            key_status[char] = 'yellow'
                    else:
                        if key_status.get(char) != 'yellow':  # Use .get() to avoid KeyError
                            key_status[char] = 'gray'

        return key_status

# Initialize the game
game = WordleGame()

def wordle_interface(guess, word_length, max_guesses):
    game.update_settings(word_length, max_guesses)
    feedback = game.check_word(guess)
    keyboard_status = game.display_keyboard()
    return feedback, keyboard_status

iface = gr.Interface(
    fn=wordle_interface,
    inputs=[
        gr.Textbox(lines=1, placeholder="Enter your guess here..."),
        gr.Slider(4, 12, step=1, value=5, label="Word Length"),
        gr.Slider(1, 10, step=1, value=6, label="Max Guesses")
    ],
    outputs=[
        gr.Textbox(label="Feedback"),
        gr.JSON(label="Keyboard Status")
    ],
    title="Wordle Game"
)

if __name__ == "__main__":
    iface.launch()