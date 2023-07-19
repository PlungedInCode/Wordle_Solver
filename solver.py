import random
import pandas
from wordle import HiddenWordGenerator

class Solver:
    def __init__(self, game, dict_path='wordleDict.csv'):
        self.game = game
        self.vowels = ['A', 'E', 'I', 'O', 'U', 'Y']
        word_dict_df = pandas.read_csv(dict_path)
        word_dict_df = word_dict_df[word_dict_df['words'].str.len() == self.game.letters]
        word_dict_df['words'] = word_dict_df['words'].str.upper()
        word_dict_df['v-count'] = word_dict_df['words'].apply(lambda x: ''.join(set(x))).str.count(
            '|'.join(self.vowels))
        self.word_dict = word_dict_df
        self.yellow_letters = {}
        self.red_letters = []
        self.prediction = ['' for _ in range(game.letters)]

    def calculate_letter_prob(self):
        for i in range(self.game.letters):
            counts = self.word_dict['words'].str[i].value_counts(normalize=True).to_dict()
            self.word_dict[f'p-{i}'] = self.word_dict['words'].str[i].map(counts)

    def get_board_state(self):
        if self.game.attempts < 6:
            word = self.game.guessed_words[-1][1]
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
                    self.prediction[i] = letter
                else:
                    if letter in self.prediction:
                        if letter not in self.yellow_letters:
                            self.yellow_letters[letter] = i
                        else:
                            self.yellow_letters[letter].append(i)
                    elif letter not in self.red_letters:
                        self.red_letters.append(letter)
            self.red_letters = [ch for ch in self.red_letters
                                if ch not in self.yellow_letters and ch not in self.prediction]

    def solver_action(self):
        self.get_board_state()
        if len(self.red_letters) > 0:
            self.word_dict = self.word_dict[~self.word_dict['words'].str.contains('|'.join(self.red_letters))]
            self.red_letters = []
        if len(self.yellow_letters) > 0:
            yellow_str = '^' + ''.join(fr'(?=.*{ch})' for ch in self.yellow_letters)
            self.word_dict = self.word_dict[self.word_dict['words'].str.contains(yellow_str)]
            for s, p in self.yellow_letters.items():
                for i in p:
                    self.word_dict = self.word_dict[self.word_dict['words'].str[i] != s]
            self.yellow_letters = {}

        for i, ch in enumerate(self.prediction):
            if ch != '':
                self.word_dict = self.word_dict[self.word_dict['words'].str[i]==s]

        self.word_dict['w-score'] = [0] * len(self.word_dict)
        if len(self.word_dict) > 5:
            self.calculate_letter_prob()

        for i in range(self.game.letters):
            if self.prediction[i] == '':
                self.word_dict['w-score'] += self.word_dict[f"p-{i}"]

        if True not in [True for ch in self.prediction if ch in self.vowels]:
            self.word_dict['w-score'] += self.word_dict['v-count'] / self.game.letters

        mv_dic = self.word_dict[self.word_dict['w-score'] == self.word_dict['w-score'].max()]
        if len(mv_dic):
            result = random.choice(mv_dic['words'].tolist())
        else:
            result = HiddenWordGenerator.get_random_word_from_dict()
            print("Random", end=" - ")
        return result


