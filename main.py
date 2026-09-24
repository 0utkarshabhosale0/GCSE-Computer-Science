import csv
import re
import os
import time
import random
import hashlib


class Card:
    def __init__(self, colour, value):
        self.colour = colour
        self.value = value

    def __str__(self):
        return f"{self.colour} {self.value}"


class Player:
    def __init__(self, card, card_number):
        self.card = card
        self.card_number = card_number


def starter_menu():
    print("=" * 40)
    print("CARD GAME")
    print("=" * 40)
    print()
    print("1. Register")
    print("2. Login and play")
    print("3. View Leaderboard")
    print("4. Exit")
    print()

    try:
        click = int(input("Enter choice (1-4): "))

        if click not in range(1, 5):
            print("Please enter a number between 1 and 4.")
            time.sleep(2)
            os.system("cls")
            return None

        os.system("cls")
        return click

    except ValueError:
        print("Please enter a number between 1 and 4.")
        time.sleep(2)
        os.system("cls")
        return None


def register(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    with open("users.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([username, hashed_password])


def login(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        with open("users.csv", "r", newline="") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) >= 2:
                    if row[0] == username and row[1] == hashed_password:
                        return True

    except FileNotFoundError:
        return False

    return False


def main_menu():
    print("=" * 40)
    print("MENU")
    print("=" * 40)
    print()
    print("1. Play")
    print("2. View Leaderboard")
    print("3. Exit")
    print()

    try:
        click = int(input("Enter choice (1-3): "))

        if click not in range(1, 4):
            print("Please enter a number between 1 and 3.")
            time.sleep(2)
            os.system("cls")
            return None

        os.system("cls")
        return click

    except ValueError:
        print("Please enter a number between 1 and 3.")
        time.sleep(2)
        os.system("cls")
        return None


def card_generator():
    colour = random.choice(["Red", "Yellow", "Black"])
    value = random.randint(1, 10)

    card = Card(colour, value)

    return card


def card_comparision(card1, card2, player1, player2):

    if card1.colour == card2.colour:

        if card1.value > card2.value:
            return player1

        elif card2.value > card1.value:
            return player2

        else:
            return None

    elif card1.colour == "Red" and card2.colour == "Black":
        return player1

    elif card1.colour == "Black" and card2.colour == "Red":
        return player2

    elif card1.colour == "Black" and card2.colour == "Yellow":
        return player1

    elif card1.colour == "Yellow" and card2.colour == "Black":
        return player2

    elif card1.colour == "Yellow" and card2.colour == "Red":
        return player1

    elif card1.colour == "Red" and card2.colour == "Yellow":
        return player2


def check_cardnumber(deck1, deck2):
    total_deck = deck1 + deck2

    if total_deck <= 30:
        return True
    else:
        return False


def add_score(username, score):
    leaderboard = []

    try:
        with open("leaderboard.csv", "r", newline="") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) >= 2:
                    leaderboard.append([row[0], int(row[1])])

    except FileNotFoundError:
        pass

    leaderboard.append([username, score])

    leaderboard.sort(key=lambda x: x[1], reverse=True)

    with open("leaderboard.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(leaderboard)


def view_leaderboard():
    print("=" * 40)
    print("LEADERBOARD")
    print("=" * 40)
    print()

    try:
        with open("leaderboard.csv", "r", newline="") as f:
            reader = csv.reader(f)

            leaderboard = []

            for row in reader:
                if len(row) >= 2:
                    leaderboard.append([row[0], int(row[1])])

            leaderboard.sort(key=lambda x: x[1], reverse=True)

            if not leaderboard:
                print("The leaderboard is empty.")
                return

            for position, player in enumerate(leaderboard, start=1):
                print(f"{position}. {player[0]} - {player[1]} points")

    except FileNotFoundError:
        print("The leaderboard is empty.")


def play(username):

    print("Playing against bot...")
    time.sleep(2)
    os.system("cls")

    player1 = Player(None, 0)
    player2 = Player(None, 0)

    round = 0

    while round <= 14:

        print("=" * 40)
        print(f"Round {round + 1}")
        print("=" * 40)

        player1.card = card_generator()
        print(f"{username} got {player1.card}")

        player2.card = card_generator()
        print(f"Bot got {player2.card}")

        winner = card_comparision(
            player1.card,
            player2.card,
            player1,
            player2
        )

        if winner == player1:
            player1.card_number += 2
            print(f"{username} wins the round!")

        elif winner == player2:
            player2.card_number += 2
            print("Bot wins the round!")

        else:
            print("Draw!")

        deck_total = check_cardnumber(
            player1.card_number,
            player2.card_number
        )

        if deck_total:
            round += 1
        else:
            print("Oops, something went wrong.")
            break

        print()
        print(f"{username}: {player1.card_number}")
        print(f"Bot: {player2.card_number}")

        time.sleep(5)
        os.system("cls")

    if player1.card_number > player2.card_number:

        score = player1.card_number

        print(f"Winner is {username}!")
        print(f"Score: {score}")

        add_score(username, score)

    elif player2.card_number > player1.card_number:

        print("You lost!")
        print(f"Your score: {player1.card_number}")

    else:

        score = player1.card_number

        print("It was a draw!")
        print(f"Score: {score}")

        add_score(username, score)

    time.sleep(5)
    os.system("cls")



# START OF PROGRAM


while True:

    choice = starter_menu()

    if choice == 1:

        print("=" * 40)
        print("REGISTRATION")
        print("=" * 40)

        while True:

            username = input("USERNAME (3-15 characters): ")

            if len(username) < 3 or len(username) > 15:
                print("Username has to be between 3-15 characters")
                time.sleep(3)
                os.system("cls")
                continue

            else:
                print("Username accepted")
                break

        while True:

            password = input("PASSWORD (min. 8 characters): ")

            if len(password) < 8:
                print("Password has to be at least 8 characters")
                time.sleep(3)
                os.system("cls")
                continue

            else:
                print("Password accepted")
                break

        print("We are making your account")
        time.sleep(3)

        register(username, password)

        print("Account created!")
        time.sleep(3)
        os.system("cls")

        # Go to main menu after registering
        logged_in = True


    elif choice == 2:

        print("=" * 40)
        print("LOGIN")
        print("=" * 40)
        print()

        check_username = input("USERNAME: ")
        check_password = input("PASSWORD: ")

        if login(check_username, check_password):

            print("Welcome...")
            time.sleep(2)
            os.system("cls")

            username = check_username
            logged_in = True

        else:

            print("Credentials don't match")
            time.sleep(3)
            os.system("cls")
            logged_in = False


    elif choice == 3:

        view_leaderboard()

        print()
        input("Press Enter to return to the menu...")
        os.system("cls")


    elif choice == 4:

        print("Goodbye!")
        time.sleep(3)
        os.system("cls")
        break


    if choice == 1 or (choice == 2 and logged_in):

        while True:

            main_choice = main_menu()

            if main_choice == 1:

                play(username)

            elif main_choice == 2:

                view_leaderboard()

                print()
                input("Press Enter to return to the main menu...")
                os.system("cls")

            elif main_choice == 3:

                print("Goodbye!")
                time.sleep(3)
                os.system("cls")
                exit()

