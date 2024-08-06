from tabulate import tabulate
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

base = declarative_base()


class PlayerModel(base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    score = Column(Integer, default=0)


class GameModel(base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True, autoincrement=True)
    player1_name = Column(String)
    player2_name = Column(String)
    player1_wins = Column(Integer)
    player2_wins = Column(Integer)
    sets = Column(Integer)


class Database:
    def __init__(self, db_url, Base):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    def add_record(self, model, **kwargs):
        session = self.Session()
        entry = session.query(model).filter_by(**{k: v for k, v in kwargs.items() if k != 'score'}).first()
        if entry and model == PlayerModel:
            # Update the score if the entry exists
            score = kwargs.pop('score')
            entry.score += score
        else:
            new_entry = model(**kwargs)
            session.add(new_entry)
        session.commit()
        session.close()

    def get_all_record(self, model):
        session = self.Session()
        result = session.query(model).all()
        session.close()
        return result


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
        self.db = Database('sqlite:///mydatabase.db', base)

    def update_scores(self, player: Player):
        self.db.add_record(PlayerModel, name=player.name, score=1)

    def print_leaderboard(self):
        score = {}
        print("--- Leaderboard ---")
        records = self.db.get_all_record(PlayerModel)
        for record in records:
            score[record.name] = record.score
        sorted_players = sorted(score.items(), key=lambda item: item[1], reverse=True)
        table = [['Player', 'Score']] + [[player, score] for player, score in sorted_players]
        print(tabulate(table, headers="firstrow", tablefmt="grid"))


class Manager:
    leaderboard = Leaderboard()

    def main(self):
        while True:
            print("Please choose an option:\n 1-Start Game\n 2-Show Leaderboard\n 3-Show Game log\n 4-Exit")
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
                db = Database('sqlite:///mydatabase.db', base)
                db.add_record(GameModel, player1_name=player1_name, player2_name=player2_name, player1_wins=wins1,
                              player2_wins=wins2, sets=sets)
            elif choice == 2:
                self.leaderboard.print_leaderboard()
            elif choice == 3:
                db = Database('sqlite:///mydatabase.db', base)
                records = db.get_all_record(GameModel)
                list1 = []
                for record in records:
                    list1.append([record.player1_name, record.player2_name, record.player1_wins, record.player2_wins,
                                  record.sets])
                table = [['Player1_name', 'player2_name', 'player1_wins', 'player2_wins', 'sets']] + list1
                print(tabulate(table, headers="firstrow", tablefmt="grid"))

            elif choice == 4:
                break
            else:
                print("Invalid choice. Please try again ")


game_manager = Manager()
game_manager.main()
