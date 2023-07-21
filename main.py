from wordle import WordlyGame
from solver import Agent

if __name__ == "__main__":
    wordly_game = WordlyGame()
    wordly_solver = Agent(wordly_game)
    wordly_game.play(player_input=wordly_solver.make_guess)