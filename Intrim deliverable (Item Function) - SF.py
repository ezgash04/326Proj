import random

#player and item list (I am not making a whole class for this deliverable)
players = ["Sif", "Rena", "Danu", "Ezra"]
itemList = []

def items(text_file):
    text_file = "item_list.txt"
    #opens and reads the file (strips any whitespace)
    with open(text_file, "r", encoding="utf-8") as f:
        for line in f:
            #strips whitespace off of each line
            a = line.strip()
            #appends line to list as an object
            itemList.append(a)
            
    #picks a random player (hardcoded, will actually use a class in the future)         
    player = random.choice(players)
    
    #picks a random item (makes sure the list isn't empty first)
    if not itemList.isEmpty:
        item = random.choice(itemList)
    else:
        #what it returns if there aren't any items to choose from
        return "There aren't any items to choose from"
    
    #will skip a couple of seconds(time?) in final function
    
    #return statement 
    return f"Player {player} has recieved an item!"
    
                