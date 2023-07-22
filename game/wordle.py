import os
from dotenv import load_dotenv
from colorama import Fore, Style
import random
import csv

load_dotenv()
DICT_PATH = os.getenv('DICT_PATH')


class WordlyGame:
    def __init__(self: str, attempts=6, letters=5) -> None:
        self.attempts = attempts
        self.Validator = InputValidator()
        self.Generator = HiddenWordGenerator()
        self.letters = letters
        self.guessed_words = []
        self.win = False

    def play(self, player_input=input, helper=False):
        while self.attempts > 0 and not self.win:
            print(f"Attempts left {self.attempts}")
            if helper:
                print("Try: ", end=" ")
            else:
                print("Enter your guess: ")
            try:
                guess = player_input().strip().lower()
            except Exception as e:
                print(f"An Error occurred while guessing word : {e}")
                self.attempts = 6
                self.win = 1
                break

            if guess == "/show_attempts":
                for i in self.guessed_words:
                    print(i[0])
                continue

            if not self.check_guess(guess):
                continue

            if guess == self.Generator.hidden_word and not helper:
                self.win = True

            if helper:
                checked_guess = self.player_check(guess)
            else:
                checked_guess = self.check(guess)

            self.guessed_words.append(checked_guess)

            if not helper:
                print(checked_guess[0])
            self.attempts -= 1

        if not self.win:
            print("Game over. You ran out of attempts.")
            if not helper:
                print(f"The hidden word was: {self.Generator.hidden_word}")
        else:
            print("Congratulations! You guessed the word.")

    def check_guess(self, guess):
        if not self.Validator.is_valid_guess(guess, self.letters):
            print("Invalid guess. Please enter a 5-letter word in english.")
            return False
        elif not self.Validator.is_in_dict(guess):
            print("There's no such word in our Dict.")
            return False
        elif self.check(guess) in self.guessed_words:
            print("Please try new word")
            return False
        return True

    def check(self, guess): 
        checked_guess = ""
        colors = ""
        for i in range(5):
            if guess[i] == self.Generator.hidden_word[i]:
                checked_guess += (Fore.GREEN + guess[i] + Style.RESET_ALL)
                colors += 'g'
            elif guess[i] in self.Generator.hidden_word:
                checked_guess += (Fore.YELLOW + guess[i] + Style.RESET_ALL)
                colors += 'y'
            else:
                checked_guess += (Fore.RED + guess[i] + Style.RESET_ALL)
                colors += 'r'
        return checked_guess, guess, colors
    
    def player_check(self, guess):
        print(guess)
        print("Enter colors, r - red letters, y - yellow letters, g - green letters")
        checked_guess = guess
        colors = input()
        if colors == "ggggg":
            self.win = True
        return checked_guess, guess, colors

    @staticmethod
    def game_instruction():
        ramen = Fore.GREEN + "Ra" + Fore.YELLOW + "m" + Fore.RED + "en" + Style.RESET_ALL
        green = Fore.GREEN + "Green" + Style.RESET_ALL
        yellow = Fore.YELLOW + "Yellow" + Style.RESET_ALL
        red = Fore.RED + "Red" + Style.RESET_ALL
        print(f"""Wordle is a single player game
        A player has to guess a five letter hidden word
        You have six attempts
        Your Progress Guide "{ramen}"
        "{green}" - Indicates that the letter at that position was guessed correctly
        "{yellow}" - indicates that the letter at that position is in the hidden word, but in a different position
        "{red}" - indicates that the letter at that position is wrong, and isn't in the hidden word   """)


class HiddenWordGenerator:
    def __init__(self) -> None:
        self.hidden_word = self.get_random_word_from_dict()

    @staticmethod
    def get_random_word_from_dict(dict_path=DICT_PATH) -> str:
        with open(dict_path, 'r') as file:
            reader = csv.reader(file)
            words = list(reader)
            random_word = random.choice(words)[0]
        return random_word


class InputValidator:
    @staticmethod
    def is_in_dict(word, dict_path=DICT_PATH) -> bool:
        with open(dict_path, 'r') as file:
            reader = csv.reader(file)
            words = list(reader)
            return [word] in words

    @staticmethod
    def is_valid_guess(guess: str, letters) -> bool:
        return len(guess) == letters and guess.isalpha()
