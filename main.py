from game.wordle import WordlyGame
from solvers.solver1 import Agent

if __name__ == "__main__":
    WordlyGame.game_instruction()
    print("P - Play Wordle")
    print("H - Help you to solve wordle")
    print("T - Test Wordle")
    ch = input("Choose option: ").upper()
    if ch == "T":
        game_count = int(input("Enter test count: "))
        cnt, wins, attempts = 0, 0, 0
        while cnt != game_count:
            print("GAME -", cnt + 1)
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
    elif ch == "P":
        wordly_game = WordlyGame()
        wordly_game.play()
    elif ch == "H":
        wordly_game = WordlyGame()
        wordly_solver = Agent(wordly_game)
        wordly_game.play(player_input=wordly_solver.make_guess, helper=True)
