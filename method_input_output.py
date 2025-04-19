
import random

# what item they receive, whether they want to use the item in question

def random_item(filename):
    with open(filename, "r") as file:
        items = [line.strip() for line in file if line.strip()]
    return random.choice(items)


def function_throw_item(item):
    players = ["Player 1", "Player 2", "Player 3"]
    thrower = random.choice(players)
    
    remaining = [p for p in players if p != thrower]
    target_player = random.choice(remaining)
    
    not_hit = [p for p in players if p != thrower and p != target_player][0]
    print(f"{thrower} threw {item} at {target_player}")
    print(f"{target_player} got down!")
    print(f"{not_hit} and {thrower} are in the lead!!!")
        
        
def keep_throw(item):
    while True:
        answer = input(f"Would you like to use your {item}?").strip().lower()
        if answer == "yes":
            function_throw_item(item)
            break
        elif answer == "no":
            print(f"You saved the {item} for later.")
            break
        else:
            print("You did not answer correctly, please type 'yes' or 'no'")
            
powerup = random_item("item list.txt")
keep_throw(powerup)

