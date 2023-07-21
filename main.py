from game.wordle import WordlyGame
from solvers.solver import Agent

if __name__ == "__main__":
    game_count = 100
    cnt = 0
    wins = 0
    attempts = 0
    while cnt != game_count:
        wordly_game = WordlyGame()
        wordly_solver = Agent(wordly_game)
        wordly_game.play(player_input=wordly_solver.make_guess)
        cnt += 1
        wins += wordly_game.win
        attempts += 6 - wordly_game.attempts
    
    win_percentage = (wins / cnt) * 100
    average_attempts = attempts / cnt
    print(f"Total games played: {cnt}")
    print(f"Total wins: {wins}")
    print(f"Win percentage: {win_percentage:.2f}%")
    print(f"Average number of guessing attempts: {average_attempts:.2f}")
