
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

#All questions and printed messages to the players, including the seconds, 
# what item they receive, whether they want to use the item in question, 
# what map they wish to play, etc. This will need player input and information
# from other classes/functions used in the program. Any errors while the 
# program runs will be handled using the classes and functions existing in 
# the program. Requires a player and game class to store attributes shown in 
# terminal, and the length of the map the player chooses as well.

def start_game(self):
    print(f"\n Map selected: {self.map_choice} ---" 
          f" Race length: {self.race_duration} seconds")
    print("3, 2, 1, \n START!")
    
    for player in self.players:
        if player.stopped_timer > 0:
            player.stopped_timer -= 1
            print(f"{player.name} is stopped! Recovering now...")
            continue
  
