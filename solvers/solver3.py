import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
DICT_PATH = os.getenv('DICT_PATH')


class Agent:
    def __init__(self, game, sort_by_ascending=True) -> None:
        self.game = game
        self.word_dict, self.letter_count = self.build_frame()
        self.green_letters = ['' for _ in range(self.game.letters)]
        self.yellow_letters = {}
        self.red_letters = []
        self.sort_by_ascending = sort_by_ascending

    def build_frame(self):
        word_dict = pd.read_csv(DICT_PATH)
        word_dict = word_dict[word_dict['words'].str.len() == self.game.letters]
        word_dict['words'] = word_dict['words'].str.upper()
        word_list = word_dict['words'].tolist()
        letter_counts = []
        for i in range(self.game.letters):
            let_cont_i = {}
            for word in word_list:
                if word[i] not in let_cont_i:
                    let_cont_i[word[i]] = 0
                let_cont_i[word[i]] += 1
            letter_counts.append(let_cont_i)

        word_dict['cf'] = word_dict['words'].apply(
            lambda curr_word: sum(letter_counts[idx][curr_word[idx]] for idx in range(self.game.letters)))
        word_dict = word_dict.sort_values('cf', ascending=True)
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
    