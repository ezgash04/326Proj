import random
import time



class player_class:
    def __init__(self, name):
        self.name = name


#item list
itemList = []

def items(text_file, players):
    
    #opens and reads the file (strips any whitespace)
    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            #strips whitespace off of each line
            a = line.strip()
            #appends line to list as an object if it's not empty
            if not (a.isEmpty):
                itemList.append(a)
            
            
    #picks a random item (makes sure the list isn't empty first)
    if not (itemList.isEmpty):
        item = random.choice(itemList)
    else:
        #what it returns if there aren't any items to choose from
        return "There aren't any items to choose from"
    
    #chooses from the list of player names in args (non hardcoded)
    player = random.choice(players)
    
    #will skip a couple of seconds after an item is chosen from the list
    print(f"Let's see what item you got!")
    time.sleep(random.randint(3,4))
    
    #return statement 
    return f"Player {player.name} has recieved the {item}!"

if __name__ == "main":
    
    players = [player_class("Sif"), player_class("Rena"), player_class("Ezra"),
               player_class("Danu")]
    
    filename = input("Item_List.txt")
    
    print(items(filename, players))
    
    
                