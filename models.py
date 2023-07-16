# from typing import List
from random import choice
from colorama import Fore, Style
# import enchant 
from random_word import Wordnik


class WordlyGame:
    def __init__(self, hidden_word : str) -> None:
        self.hidden_word = hidden_word
        self.attempts = 6
        self.guessed_words = []
        self.win = False
        # self.dict = enchant.Dict("en_US")
    
    def play(self):
        self.game_instruction()
        while self.attempts > 0 and self.win == False:
            print(f"Attempts left {self.attempts}")
            guess = input("Enter your guess: ").strip().lower()

            if guess == "/show_attempts":
                print("Guessed words : ", "\n".join(self.guessed_words))
                continue

            if not InputValidator.is_valid_guess(guess):
                print("Invalid guess. Please enter a 5-letter word in english.")
                continue
            
            if guess == self.hidden_word:
                self.win = True
            
            checked_guess = self.check(guess)
            self.guessed_words.append(checked_guess)
            print(checked_guess)

            self.attempts -= 1
        
        if not self.win:
            print("Game over. You ran out of attempts.")
            print(f"The hidden word was: {self.hidden_word}")
        else :
            print("Congratulations! You guessed the word.")
    
    def check(self, guess):
        checked_guess = ""
        for i in range(5):
            if guess[i] == self.hidden_word[i]:
                checked_guess += (Fore.GREEN + guess[i] + Style.RESET_ALL)
            elif guess[i] in self.hidden_word:
                checked_guess += (Fore.YELLOW + guess[i] + Style.RESET_ALL)
            else:
                checked_guess += (Fore.RED + guess[i] + Style.RESET_ALL)
        return checked_guess



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
    # TODO : Build Wordnik with my own API key
    def __init__(self) -> None:
        self.Generator = Wordnik()

    def generate_hidden_word(self) -> str:
        word = self.Generator.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun", 
                                              minDictionaryCount = 3, minLength=5, maxLength=5)
        while word == None or '-' in word:
            word = self.Generator.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun", 
                                              minDictionaryCount = 3, minLength=5, maxLength=5)
        return word


class InputValidator:
    @staticmethod
    def is_valid_guess(guess:str) -> bool:
        return len(guess) == 5 and guess.isalpha()

if __name__ == "__main__":
    hidden_word_generator = HiddenWordGenerator()
    hidden_word = hidden_word_generator.generate_hidden_word()
    print(hidden_word)
    wordle_game = WordlyGame(hidden_word)
    wordle_game.play()