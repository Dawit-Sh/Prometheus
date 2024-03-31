import time
import sys
import random

# ASCII art
intro_art = """
  _____________________________________________________________
 /                                                             \\
|  _________________________________________________________    |
| |                                                         |   |
| |                      Welcome to                         |   |
| |                 Prometheus : Galactic Infiltration      |   |
| |                                                         |   |
| |     _______  __   __  _______    _______  __   __      |   |
| |    |       ||  | |  ||       |  |       ||  | |  |     |   |
| |    |    ___||  |_|  ||    ___|  |_     _||  |_|  |     |   |
| |    |   |___ |       ||   |___     |   |  |       |     |   |
| |    |    ___||       ||    ___|    |   |  |       |     |   |
| |    |   |___  |     | |   |___     |   |  |     | |     |   |
| |    |_______|  |___|  |_______|    |___|  |___|  |     |   |
| |_______________________________________________________|   |
|_____________________________________________________________|
"""

# Function to print text with delay
def print_with_delay(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Free will
def make_choice(question, options):
    print_with_delay(question)
    for i, option in enumerate(options, 1):
        print_with_delay(f"{i}. {option}")
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice) - 1
        else:
            print_with_delay("Invalid choice. Please enter a number corresponding to the options.")

# hackerman
def hacking_scenario():
    print_with_delay("You are a skilled space hacker tasked with infiltrating a military starship.")
    time.sleep(1)
    print_with_delay("Your mission: Hack into the starship's system to obtain classified information.")
    time.sleep(1)
    print_with_delay("You find yourself outside the starship's main terminal.")
    time.sleep(1)
    print_with_delay("You need to make a decision quickly:")
    choice = make_choice("1. Hack into the mainframe directly.", ["2. Find a hidden backdoor into the system."])
    if choice == 0:
        print_with_delay("You attempt to hack into the mainframe directly.")
        time.sleep(1)
        print_with_delay("The security protocols are strong, but you manage to bypass them.")
        time.sleep(1)
        mainframe_scenario()
    else:
        print_with_delay("You search for a hidden backdoor into the system.")
        time.sleep(1)
        print_with_delay("After some time, you find a vulnerability and exploit it to gain access.")
        time.sleep(1)
        mainframe_scenario()

# mainframe hacking
def mainframe_scenario():
    print_with_delay("You've gained access to the starship's mainframe.")
    time.sleep(1)
    print_with_delay("Now you need to navigate through the system to find the classified information.")
    time.sleep(1)
    print_with_delay("You encounter a series of security checkpoints.")
    time.sleep(1)
    print_with_delay("You must choose how to proceed:")
    choice = make_choice("1. Attempt to bypass the security checkpoints.", ["2. Create a distraction to divert attention."])
    if choice == 0:
        print_with_delay("You try to bypass the security checkpoints, but the system detects your intrusion.")
        time.sleep(1)
        print_with_delay("The security forces are alerted, and they start hunting you down.")
        time.sleep(1)
        hunt_scenario()
    else:
        print_with_delay("You create a distraction, causing chaos and confusion among the security personnel.")
        time.sleep(1)
        print_with_delay("You use the opportunity to slip past the security checkpoints unnoticed.")
        time.sleep(1)
        find_information_scenario()

# the hunt 
def hunt_scenario():
    print_with_delay("You're now being hunted by the starship's security forces.")
    time.sleep(1)
    print_with_delay("You need to think fast and make a decision:")
    choice = make_choice("1. Hide in the maintenance tunnels.", ["2. Try to blend in with the crew."])
    if choice == 0:
        print_with_delay("You quickly duck into the maintenance tunnels, evading detection for now.")
        time.sleep(1)
        print_with_delay("You hear security personnel passing by, but they don't spot you.")
        time.sleep(1)
        find_information_scenario()
    else:
        print_with_delay("You attempt to blend in with the crew, but your disguise doesn't fool the security forces.")
        time.sleep(1)
        print_with_delay("They recognize you as an intruder and apprehend you.")
        time.sleep(1)
        game_over()

# finding the information 
def find_information_scenario():
    print_with_delay("You've successfully bypassed the security checkpoints and are now searching for the classified information.")
    time.sleep(1)
    print_with_delay("You encounter a heavily encrypted file.")
    time.sleep(1)
    print_with_delay("You must decrypt the file to access the information:")
    choice = make_choice("1. Use brute force to crack the encryption.", ["2. Search for a decryption key."])
    if choice == 0:
        print_with_delay("You attempt to brute force the encryption, but it triggers an alarm.")
        time.sleep(1)
        print_with_delay("The security forces are alerted, and they converge on your location.")
        time.sleep(1)
        game_over()
    else:
        print_with_delay("You search for a decryption key and manage to find one hidden in a secure database.")
        time.sleep(1)
        print_with_delay("With the key, you successfully decrypt the file and access the classified information.")
        time.sleep(1)
        print_with_delay("Mission accomplished! You've obtained the valuable intel.")
        time.sleep(1)
        win()

# win
def win():
    print_with_delay("Congratulations! You successfully hacked into the starship's system and obtained the classified information.")
    print_with_delay("You're a master space hacker!")
    print_with_delay("Be Aware this is not the end, but the beginning of your Journey")

# game over
def game_over():
    print_with_delay("Game Over. Better luck next time!")
    print_with_delay("Thanks for playing!")


def main():
    print_with_delay(intro_art)
    time.sleep(1)
    print_with_delay("Welcome Prometheus")
    time.sleep(1)
    print_with_delay("Your mission: Hack into the military starship's system to obtain classified information.")
    time.sleep(1)
    hacking_scenario()

if __name__ == "__main__":
    main()
