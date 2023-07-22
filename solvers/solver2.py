import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
DICT_PATH = os.getenv('DICT_PATH')


class Agent:
    def __init__(self, game) -> None:
        self.game = game
        self.word_dict, self.letter_count = self.build_frame()
        self.green_letters = ['' for _ in range(game.letters)]
        self.yellow_letters = {}
        self.red_letters = []

    def build_frame(self):
        word_dict = pd.read_csv(DICT_PATH)
        word_dict = word_dict[word_dict['words'].str.len() == self.game.letters]
        word_dict['words'] = word_dict['words'].str.upper()
        letter_counts = {j: word_dict['words'].str.count(j).sum() for j in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
        word_dict['sum'] = word_dict['words'].apply(lambda word: sum(letter_counts[letter] for letter in word))
        word_dict['uniq'] = word_dict['words'].apply(lambda word: len(set(word)))
        word_dict['cf'] = word_dict.apply(lambda row: row['uniq'] * row['sum'], axis=1)
        word_dict = word_dict.sort_values('cf', ascending=False)
        return word_dict, letter_counts

    def get_board_state(self):
        if self.game.attempts < 6:
            word = self.game.guessed_words[-1][1].upper()
            colors = self.game.guessed_words[-1][2]
            for i in range(self.game.letters):
                letter, color = word[i], colors[i]
                if color == 'y':
                    if letter not in self.yellow_letters:
                        self.yellow_letters[letter] = [i]
                    else:
                        if i not in self.yellow_letters[letter]:
                            self.yellow_letters[letter].append(i)
                elif color == 'g':
                    self.green_letters[i] = letter
                else:
                    if letter in self.green_letters:
                        if letter not in self.yellow_letters:
                            self.yellow_letters[letter] = i
                        else:
                            self.yellow_letters[letter].append(i)
                    elif letter not in self.red_letters:
                        self.red_letters.append(letter)
            self.red_letters = [ch for ch in self.red_letters
                                if ch not in self.yellow_letters and ch not in self.green_letters]

    def delete_red_letters(self):
        self.word_dict = self.word_dict[~self.word_dict['words'].str.contains('|'.join(self.red_letters))]
        self.red_letters = []

    def delete_yellow_letters(self):
        yellow_str = '^' + ''.join(fr'(?=.*{ch})' for ch in self.yellow_letters)
        self.word_dict = self.word_dict[self.word_dict['words'].str.contains(yellow_str)]
        for s, p in self.yellow_letters.items():
            for i in p:
                self.word_dict = self.word_dict[self.word_dict['words'].str[i] != s]
        self.yellow_letters = {}

    def select_green_letters(self):
        for i, ch in enumerate(self.green_letters):
            if ch != '':
                self.word_dict = self.word_dict[self.word_dict['words'].str[i] == ch]

    def make_guess(self):
        self.get_board_state()
        if len(self.red_letters) > 0:
            self.delete_red_letters()
        if len(self.yellow_letters) > 0:
            self.delete_yellow_letters()
        self.select_green_letters()
        return self.word_dict['words'].tolist()[0]
