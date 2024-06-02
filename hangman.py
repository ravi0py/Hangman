import random
import sqlite3

# Hangman graphics
HANGMAN_PICS = [
    '''
  +---+
      |
      |
      |
     ===''',
    '''
  +---+
  O   |
      |
      |
     ===''',
    '''
  +---+
  O   |
  |   |
      |
     ===''',
    '''
  +---+
  O   |
 /|   |
      |
     ===''',
    '''
  +---+
  O   |
 /|\  |
      |
     ===''',
    '''
  +---+
  O   |
 /|\  |
 /    |
     ===''',
    '''
  +---+
  O   |
 /|\  |
 / \  |
     ==='''
]

# Word categories
word_categories = {
    'Animal': 'ant baboon badger bat bear beaver camel cat clam cobra cougar coyote crow deer dog donkey duck eagle ferret fox frog goat goose hawk lion lizard llama mole monkey moose mouse mule newt otter owl panda parrot pigeon python rabbit ram rat raven rhino salmon seal shark sheep skunk sloth snake spider stork swan tiger toad trout turkey turtle weasel whale wolf wombat zebra'.split(),
    'Shape': 'square triangle rectangle circle ellipse rhombus trapezoid'.split(),
    'Place': 'Cairo London Paris Baghdad Istanbul Riyadh'.split()
}

# Database setup
def setup_database():
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            level TEXT NOT NULL,
            remaining_lives INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Get random word
def get_random_word(word_list):
    word_index = random.randint(0, len(word_list) - 1)
    return word_list[word_index]

# Display the current game state
def display_board(missed_letters, correct_letters, secret_word):
    print(HANGMAN_PICS[len(missed_letters)])
    print()

    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter, end=' ')
    print()

    blanks = '_' * len(secret_word)

    for i in range(len(secret_word)):
        if secret_word[i] in correct_letters:
            blanks = blanks[:i] + secret_word[i] + blanks[i+1:]

    for letter in blanks:
        print(letter, end=' ')
    print()

# Get user guess
def get_guess(already_guessed):
    while True:
        print('Guess a letter.')
        guess = input().lower()
        if len(guess) != 1:
            print('Please enter a single letter.')
        elif guess in already_guessed:
            print('You have already guessed that letter. Choose again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please enter a LETTER.')
        else:
            return guess

# Ask if player wants to play again
def play_again():
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')

# Save score to database
def save_score(name, level, remaining_lives):
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scores (name, level, remaining_lives)
        VALUES (?, ?, ?)
    ''', (name, level, remaining_lives))
    conn.commit()
    conn.close()

# Show Hall of Fame
def show_hall_of_fame():
    conn = sqlite3.connect('hangman_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT level, name, MAX(remaining_lives) as lives
        FROM scores
        GROUP BY level
        ORDER BY lives DESC
    ''')
    rows = cursor.fetchall()
    conn.close()

    print("\nHALL OF FAME")
    print(f"{'Level':<10}{'Winner Name':<20}{'Remaining Lives':<10}")
    for row in rows:
        print(f"{row[0]:<10}{row[1]:<20}{row[2]:<10}")

# Main game function
def play_game(level, category):
    missed_letters = ''
    correct_letters = ''
    secret_word = get_random_word(word_categories[category])
    game_is_done = False

    if level == 'Easy':
        max_misses = 8
    else:
        max_misses = 6

    while True:
        display_board(missed_letters, correct_letters, secret_word)
        guess = get_guess(missed_letters + correct_letters)

        if guess in secret_word:
            correct_letters += guess

            if all(letter in correct_letters for letter in secret_word):
                print(f'Yes The secret word is "{secret_word}" You have won!')
                remaining_lives = max_misses - len(missed_letters)
                save_score(player_name, level, remaining_lives)
                game_is_done = True
        else:
            missed_letters += guess

            if len(missed_letters) == max_misses:
                display_board(missed_letters, correct_letters, secret_word)
                print(f'You have run out of guesses!\nAfter {len(missed_letters)} missed guesses and {len(correct_letters)} correct guesses, the word was "{secret_word}".')
                game_is_done = True

        if game_is_done:
            if play_again():
                play_game(level, category)
            else:
                break

# Introductory menu
def show_intro_menu():
    print(f"Hi {player_name}.")
    print("Welcome to HANGMAN")
    print("1. Play the Game")
    print("2. Hall of Fame")
    print("3. About the Game")
    print("4. Exit")

    choice = input("Choose an option: ")
    if choice == '1':
        show_level_menu()
    elif choice == '2':
        show_hall_of_fame()
    elif choice == '3':
        show_about_game()
    elif choice == '4':
        exit()
    else:
        print('Choice is not valid')

# Level selection menu
def show_level_menu():
    print("Choose the level of challenge:")
    print("1. Easy")
    print("2. Moderate")
    print("3. Hard")

    choice = input("Choose a level: ")
    if choice == '1':
        show_category_menu('Easy')
    elif choice == '2':
        show_category_menu('Moderate')
    elif choice == '3':
        play_game('Hard', random.choice(list(word_categories.keys())))
    else:
        print('Choice is not valid')

# Category selection menu
def show_category_menu(level):
    print("Select from the following sets of secret words:")
    print("1. Animals")
    print("2. Shapes")
    print("3. Places")

    choice = input("Choose a category: ")
    if choice == '1':
        play_game(level, 'Animal')
    elif choice == '2':
        play_game(level, 'Shape')
    elif choice == '3':
        play_game(level, 'Place')
    else:
        print('Choice is not valid')

# About the game
def show_about_game():
    print("ABOUT THE GAME")
    print("Easy: Select from Animals, Shapes, or Places. 8 lives.")
    print("Moderate: Select from Animals, Shapes, or Places. 6 lives.")
    print("Hard: Random category. 6 lives.")

# Main program
setup_database()
print("Enter your name:")
player_name = input()

while True:
    show_intro_menu()
