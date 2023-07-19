from wordle import WordlyGame
from solver import  Solver

if __name__ == "__main__":
    wordly_game = WordlyGame()
    wordly_solver = Solver(wordly_game)
    wordly_game.play(player_input=wordly_solver.solver_action)
