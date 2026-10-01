import sys
import random
import datetime

def get_word_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            word = file.read().splitlines()
            return word

    except FileNotFoundError:
        sys.stderr.write(f"Error: '{filename}' I can't find the file\n")
        sys.exit(1)
    
def play_game(secret_word):
    penalty = 0
    display = ['_'] * len(secret_word)
    attempts = 0

    while penalty < 12:
        answer_org = input("$> ")
        answer = answer_org.upper()
        attempts += 1

        if len(answer) == 1:
            if answer in secret_word:
                print(f"Found one '{answer}'")
                for i in range(len(secret_word)):
                    if answer == secret_word[i]:
                        display[i] = answer
                print(f"{display} / {penalty} penalty")
            else:
                penalty += 1
                print(f"No '{answer}' found")
                print(f"{display} / {penalty} penalty")
                
        else:
            if answer == secret_word:
                print(f"{answer}: correct guess - {penalty} penalties")
                break
            else:
                penalty += 5
                print(f"{answer}: incorrect guess")
                print(f"{display} / {penalty} penalties")

    if penalty >= 12:
        print("You lose")

    return penalty, attempts

def check_high_score(secret_word, final_score, attempts):
    try:
         with open("score.txt", 'r', encoding='utf-8') as file:
            content = file.read().split()
            today = datetime.date.today().strftime("%Y-%m-%d")
        
            if not content:
                with open("score.txt", 'w', encoding='utf-8') as file:
                    file.write(f"{secret_word} {attempts} {today}")
                    print(f"Best ever ! You guessed '{secret_word}' in {attempts} attempts.")
                    
            else:
                old_word, old_score, old_date = content
                if final_score < int(old_score):
                    with open("score.txt", 'w', encoding='utf-8') as file:
                        file.write(f"{secret_word} {final_score} {today}")
                        print(f"Best ever ! You guessed '{secret_word}' in {attempts} attempts.")
                else:
                    print(f"You guessed '{secret_word}' in {attempts} attempts, but the record from {today} is {old_score} attempts.")
        
    except FileNotFoundError:
        sys.stderr.write(f"Error: can't find the score.txt\n")
        sys.exit(1)


if len(sys.argv) < 2:
    sys.stderr.write("Error: missing argument\n")
    sys.exit(1)

filename = sys.argv[1]

word = get_word_from_file(filename)
secret_word = random.choice(word).upper()
print(f"Secret word: {secret_word}") # (테스트용)
    
final_score, attempts = play_game(secret_word)
    
check_high_score(secret_word, final_score, attempts)