from tabulate import tabulate
from sqlalchemy import create_engine, Column, Integer, String, desc, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = 0

    def get_choice(self):
        valid_choices = ['rock', 'paper', 'scissors']
        choice = input(f"{self.name}, enter your choice (rock, paper, scissors): ").lower()
        while choice not in valid_choices:
            print("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.")
            choice = input(f"{self.name}, enter your choice (rock, paper, scissors): ").lower()
        return choice


class Game:
    def __init__(self, player1: Player, player2: Player, sets: int):
        self.player1 = player1
        self.player2 = player2
        self.sets = sets
        self.player1.wins = 0
        self.player2.wins = 0

    wins_mode = {
        "rock": "scissors",
        "paper": "rock",
        "scissors": "paper"
    }

    def play(self):
        print(f"\n{self.player1.name} vs {self.player2.name}")
        for i in range(self.sets):
            choice1 = self.player1.get_choice()
            choice2 = self.player2.get_choice()
            winner = self.specify_winner(choice1, choice2)
            if not winner:
                print("No one won!")
            else:
                print(f"{self.player1.name if winner == 1 else self.player2.name} wins this set!")
                if winner == 1:
                    self.player1.wins += 1
                else:
                    self.player2.wins += 1
        return self.player1.wins, self.player2.wins

    def specify_winner(self, choice1: str, choice2: str):
        if choice1 == choice2:
            return 0
        elif choice2 == self.wins_mode[choice1]:
            return 1
        else:
            return 2


class Leaderboard:
    def __init__(self):
        self.scores = {}

    def update_scores(self, player: Player):
        if player.name not in self.scores:
            self.scores[player.name] = 0
        self.scores[player.name] += 1

    def print_leaderboard(self):
        print("--- Leaderboard ---")
        sorted_players = sorted(self.scores.items(), key=lambda item: item[1], reverse=True)
        table = [['Player', 'Score']] + [[player, score] for player, score in sorted_players]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))


class Manager:
    leaderboard = Leaderboard()

    def main(self):
        while True:
            print("Please choose an option:\n 1-Start Game\n 2-Show Leaderboard\n 3-Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                while True:
                    player1_name = input("Enter the name of the first player: ").strip()
                    player2_name = input("Enter the name of the second player: ").strip()
                    if player1_name and player2_name:
                        break  # Exit the inner loop if both names are valid
                    else:
                        print("Names cannot be empty. Please try again.")
                while True:
                    try:
                        sets = int(input("Enter the number of sets you want to play: "))
                        break  # Exit the loop if the input is valid
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")

                player_one = Player(player1_name)
                player_two = Player(player2_name)
                game = Game(player_one, player_two, sets)
                wins1, wins2 = game.play()
                if wins1 > wins2:
                    self.leaderboard.update_scores(player_one)
                    player_one.score += 1
                elif wins2 > wins1:
                    self.leaderboard.update_scores(player_two)
                    player_two.score += 1
            elif choice == 2:
                self.leaderboard.print_leaderboard()
            elif choice == 3:
                break
            else:
                print("Invalid choice. Please try again ")


game_manager = Manager()
game_manager.main()
