import pandas as pd
import random

class Agent:
    def __init__(self, game, f_name='wordleDict.csv') -> None:
        self.game = game
        self.vowels = ['A','E','I','O','U','Y']
        word_dict = pd.read_csv(f_name)
        word_dict = word_dict[word_dict['words'].str.len()==5]
        word_dict['words'] = word_dict['words'].str.upper() #Convert all words to uppercase
        word_dict['v-count'] = word_dict['words'].apply(lambda x: ''.join(set(x))).str.count('|'.join(self.vowels)) #Count amount of vowels in words
        self.word_dict = word_dict
        self.green_letters = ['' for _ in range(game.letters)]
        self.yellow_letters = {}
        self.red_letters = []
    
    def calculate_letter_prob(self):
        for i in range(self.game.letters):
            counts = self.word_dict['words'].str[i].value_counts(normalize=True).to_dict()
            self.word_dict[f'p-{i}'] = self.word_dict['words'].str[i].map(counts)

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

        self.word_dict['w-score'] = [0] * len(self.word_dict)
        if len(self.word_dict) > 5:
            self.calculate_letter_prob()
        
        for i in range(self.game.letters):
            if self.green_letters[i] == '':
                self.word_dict['w-score'] += self.word_dict[f"p-{i}"]
        
        if True not in [True for ch in self.green_letters if ch in self.vowels]:
            self.word_dict['w-score'] += self.word_dict['v-count'] / self.game.letters

        mv_dic = self.word_dict[self.word_dict['w-score'] == self.word_dict['w-score'].max()]
        if len(mv_dic) > 0:
            return random.choice(mv_dic['words'].tolist())
        else:
            raise Exception("There's no such word in our dict")

