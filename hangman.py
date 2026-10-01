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
    
def play_game(secret_word, display, penalty, attempts, answer_org):
    penalty = 0
    display = ['_'] * len(secret_word)
    attempts = 0

    while penalty < 12:
        answer = answer_org.upper()
        attempts += 1

        if len(answer) == 1:
            if answer in secret_word:
                for i in range(len(secret_word)):
                    if answer == secret_word[i]:
                        display[i] = answer
                       
            else:
                penalty += 1
        else:
            if answer == secret_word:
                for i in range(len(secret_word)):
                    display[i] = secret_word[i]
            else:
                penalty += 5

    return display, penalty, attempts

def check_high_score(secret_word, final_score, attempts):
    try:
        with open("score.txt", 'r', encoding='utf-8') as file:
            old_word, old_attempts, old_date = file.read().split()
            today = datetime.date.today().strftime("%Y-%m-%d")
      
        if attempts < int(old_attempts):
            with open("score.txt", 'w', encoding='utf-8') as file:
                file.write(f"{secret_word} {attempts} {today}")
                print(f"Best ever ! You guessed '{secret_word}' in {attempts} attempts.")
        else:
                print(f"You guessed '{secret_word}' in {attempts} attempts, but the record from {old_date} is {old_attempts} attempts.")

    except FileNotFoundError:
        sys.stderr.write(f"Error: can't find the score.txt\n")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Error: missing argument\n")
        sys.exit(1)

    filename = sys.argv[1]
    word = get_word_from_file(filename)
    secret_word = random.choice(word).upper()
    print(f"Secret word: {secret_word}") # (테스트용)
        
    final_score, attempts = play_game(secret_word)
        
    display = ['_'] * len(secret_word)
    penalty = 0
    attempts = 0

    # 밖으로 빠져나온 while문과 input!
    while penalty < 12 and '_' in display:
        answer_org = input("$> ")
        if not answer_org: continue
        
        # 입력값을 백엔드 함수(play_game)로 던져주고 결과를 받음
        display, penalty, attempts = play_game(secret_word, display, penalty, attempts, answer_org)
        
        print(f"{display} / {penalty} penalty")

    if penalty >= 12:
        print("You lose")
    else:
        print("You win!")
        check_high_score(secret_word, penalty, attempts)