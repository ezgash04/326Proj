import argparse
import random
import time
import pandas as pd


class Player:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.car = None
        self.stopped_timer = 0
        self.points = 0
        self.completed_time = None


class Map:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __str__(self):
        return f"{self.name} ({self.duration} seconds)"




class Game:
    def __init__(self, players, item_file):
        self.players = [Player(name) for name in players]
        self.item_file = item_file
        self.maps = [
            Map("Short Race", 30),
            Map("Medium Race", 60),
            Map("Long Race", 90)
            ]
        self.selected_map = None
        self.itemList = self.items(self.item_file)
        

    def items(self, text_file):
        try: 
        # Opens and reads the file (strips any whitespace)
            with open(text_file, "r", encoding="utf-8") as f:
                for line in f:
                # Strips whitespace off of each line
                    item = line.strip()
                        
                if not item:
                    #if the file is empty
                    print(f"There aren't any items to choose from in {text_file}")
                
                #returns the list of items if everything checks out
                return item
            
        except FileNotFoundError:
            #returns an error if the file is empty (it shouldn't)
            print(f"We can't find {text_file}!")
            return
    
    def function_throw_item(item, players):
        #picks a random person to throw an item
        thrower = random.choice(players)
        
        #sections off all non-chosen players
        remaining = [p for p in players if p != thrower]
        
        #chooses who the player targets
        target_player = random.choice(remaining)
        target_player.stopped_timer = 3
        
        #puts those who arent hit in a seprate space
        not_hit = [p for p in players if p != thrower and p != target_player]
        not_hit_names = ", ".join([p.name for p in not_hit])
        
        #output
        print(f"{thrower.name} threw {item} at {target_player.name}")
        print(f"{target_player.name} got down!")
        print(f"{not_hit_names} and {thrower.name} are in the lead!!!")

    def keep_throw(self, item, player):
        while True:
            #checks to see if person wants to use item
            answer = input(f"{player.name}, would you like to use your {item}? ").strip().lower()
            if answer == "yes":
                #runs throw item if yes
                self.function_throw_item(item)
                break
            elif answer == "no":
                #saves item if no
                print(f"{player.name} saved the {item} for later.")
                break
            else:
                print("Please type 'yes' or 'no'")


    def generate_event(track_length):

        #This is where the event happens
        point = random.uniform(0, track_length)

        #This decides the event type
        event_type = random.choice(['speed boost', 'obstacle'])

        #This determines the magnitude of the effect
        effect = random.uniform(1.0, 5.0)

        #This will determine whether time is taken away or added to your time
        time_impact = effect if event_type == 'obstacle' else -effect

        #Return dictionary
        return {
            'point': point,
            'type': event_type,
            'time impact': time_impact
            }

    def calculate_average_time(track_length, seconds_per_unit=0.5):
        return seconds_per_unit * track_length

    def generate_map(self, track_length, seconds_per_unit=0.5, num_events=15):
        #generates track length, what events might happen, etc.
        events = [self.generate_event(track_length) for _ in range(num_events)]
        normal_time = self.calculate_average_time(track_length, seconds_per_unit)
        total_time_change = sum(event['time impact'] for event in events)
        final_time = normal_time + total_time_change
        
        #output
        return {
            'length': track_length,
            'events': events,
            'final_time': final_time
            }



    def update_ranking(self, points_dict):
    #convert dict to dataframe
        update_df = pd.DataFrame(list(points_dict.items()), columns=['Player', 'Time Completed']) #THIS SAYS POINTS RIGHT NOW BUT SHOULD BE CHANGED TO TIME, OR SOME OTHER WAY OF RANKING PLAYERS
        update_df = update_df.groupby('Player', as_index=False).min()

    #organize by time in descending order (updated!)
        update_df = update_df.sort_values(by='Time Completed', ascending=True).reset_index(drop=True)
        print(update_df)
        return update_df

    def choose_map(self):
        print("Choose a map:")
        index = 1
        for map in self.maps:
            print(f"{index}. {map}")
            index += 1
            while True:
                map_choice = input("30, 60 or 90: ").strip() # Asking for the map duration as input
                if map_choice in ['30', '60', '90']: # Check if the input is one of the valid map durations
                # Match the map duration based on the input and set the selected map
                    self.selected_map = next((m for m in self.maps if str(m.duration) == map_choice), None)
                    if self.selected_map:
                        print(f"You selected {self.selected_map.name} ({self.selected_map.duration} seconds)")
                        break
                    else:
                        print("Please enter '30', '60', or '90' to select a map duration.")




    def start_game(self):
        race_duration = self.selected_map.duration
        print(f"\nMap selected: {self.selected_map.name} --- Race length: {race_duration} seconds")
        print("3, 2, 1... START!\n")
        
        #variables
        start_time = time.time()
        elapsed = 0
        item_interval = random.randint(7, 10)
        last_item_time = 0

        while elapsed < race_duration:
            elapsed = int(time.time() - start_time)
            print(f"Time: {elapsed} seconds")

        if elapsed - last_item_time >= item_interval:
            for player in self.players:
                if self.itemList:
                    item = random.choice(self.itemList)
                    player.items.append(item)
                    
                    print("Let's see what item you got")
                    time.sleep(random.randint(3,4))
                    print(f"Player {player.name} has recieved the {item}!")
                    self.keep_throw(item, player)
                    last_item_time = elapsed
                    
                else:
                    print("Can't assign any items!")
                    break
                

        for player in self.players:
            if player.stopped_timer > 0:
                player.stopped_timer -= 1
                print(f"{player.name} is stopped! Recovering now...")
            time.sleep(1)
            
            #end of race
            for player in self.players: 
                player.completed_time = random.uniform(25.0, race_duration + 10)
            
            results = {player.name: player.completed_time for player in self.players}
            winners_df = self.update_ranking(results)
            print(f"Winner: {winners_df.iloc[0]['Player']} with a time of {winners_df.iloc[0]['Time Completed']}!")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the racing game simulation.")
    parser.add_argument("players", nargs='+', help="List of player names")
    parser.add_argument("--itemfile", default="item_list.txt", help="Path to the item list text file")

    args = parser.parse_args()
    game = Game(args.players, args.itemfile)
    game.choose_map()
    game.start_game()
