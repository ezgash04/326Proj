import argparse
import random
import time
import pandas as pd


class Player:
    """
    Represents a player in the racing game.

    Attributes:
        name (str): Player's name.
        items (list): List of items held by the player.
        car (any): Placeholder for car object (currently unused).
        stopped_timer (int): Number of seconds the player is stopped due to item effects.
        points (int): Points accumulated based on race progress.
        completed_time (float): Final time after race and penalties.
    """
    def __init__(self, name):
        self.name = name
        self.items = []
        self.car = None
        self.stopped_timer = 0
        self.points = 0
        self.completed_time = None


class Map:
    """
    Represents a map or track for the race.

    Attributes:
        name (str): Name of the map.
        duration (int): Duration of the race in seconds.
    """
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __str__(self):
        return f"{self.name} ({self.duration} seconds)"


class Game:
    """
    Manages the racing game, including players, maps, item interactions, and race simulation.

    Attributes:
        players (list): List of Player objects.
        item_file (str): Path to the text file containing item names.
        maps (list): Predefined list of Map objects.
        selected_map (Map): Map selected for the current race.
        itemList (list): List of items loaded from the item file.
    """
#sifene fufa
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

#sifene fufa
    def items(self, text_file):
        """
        Loads item names from a given text file.

        Args:
            text_file (str): Path to the item list file.

        Returns:
            list: Cleaned list of item strings.
        """
        try:
            with open(text_file, "r", encoding="utf-8") as f:
                item = [line.strip() for line in f if line.strip()]
                if not item:
                    print(f"There aren't any items to choose from in {text_file}")
                return item
        except FileNotFoundError:
            print(f"We can't find {text_file}!")
            return []

#rena drabovsky
    def function_throw_item(self, item, thrower):
        """
        Allows a player to throw an item at a random opponent.

        Args:
            item (str): The item being thrown.
            thrower (Player): The player using the item.
        """
        remaining = [p for p in self.players if p != thrower]
        if not remaining:
            print(f"{thrower.name} tried to throw {item}, but there's no one to throw it at!")
            return

        target_player = random.choice(remaining)
        target_player.stopped_timer = 3

        print(f"{thrower.name} threw {item} at {target_player.name}\n")
        print(f"{target_player.name} was hit!\n")
        print(f"\n{thrower.name} is in the lead!!!\n")

#rena drabovsky
    def keep_throw(self, item, player):
        """
        Prompts a player to decide whether to use or save an item.

        Args:
            item (str): The item in question.
            player (Player): The player holding the item.
        """
        while True:
            answer = input(f"{player.name}, would you like to use your {item}? ").strip().lower()
            if answer == "yes":
                self.function_throw_item(item, player)
                break
            elif answer == "no":
                print(f"{player.name} saved the {item} for later.")
                break
            else:
                print("Please type 'yes' or 'no'")

#danu nuressa
    def generate_event(self, track_length):
        """
        Randomly generates an event on the track (obstacle or speed boost).

        Args:
            track_length (int): Length of the track.

        Returns:
            dict: Event properties (location, type, time impact).
        """
        point = random.uniform(0, track_length)
        event_type = random.choice(['speed boost', 'obstacle'])
        effect = random.uniform(1.0, 5.0)
        time_impact = effect if event_type == 'obstacle' else -effect

        return {
            'point': point,
            'type': event_type,
            'time impact': time_impact
        }

#danu nuressa
    def calculate_average_time(self, track_length, seconds_per_unit=0.5):
        """
        Calculates the average base time for a given track length.

        Args:
            track_length (int): Length of the track.
            seconds_per_unit (float): Time per track unit.

        Returns:
            float: Average expected time.
        """
        return seconds_per_unit * track_length

#danu nuressa 
    def generate_map(self, track_length, seconds_per_unit=0.5, num_events=15):
        """
        Simulates a race map with events and calculates final race time.

        Args:
            track_length (int): Track length.
            seconds_per_unit (float): Time per unit.
            num_events (int): Number of events to generate.

        Returns:
            dict: Race properties including final time and events.
        """
        events = [self.generate_event(track_length) for _ in range(num_events)]
        normal_time = self.calculate_average_time(track_length, seconds_per_unit)
        total_time_change = sum(event['time impact'] for event in events)
        final_time = normal_time + total_time_change

        return {
            'length': track_length,
            'events': events,
            'final_time': final_time
        }

#ezra gashaw
    def update_ranking(self, points_dict):
        """
        Converts completion times to a ranked DataFrame.

        Args:
            points_dict (dict): Player names mapped to completion times.

        Returns:
            DataFrame: Players ranked by time.
        """
        update_df = pd.DataFrame(list(points_dict.items()), columns=['Player', 'Time Completed']) 
        update_df = update_df.groupby('Player', as_index=False).min()
        update_df = update_df.sort_values(by='Time Completed', ascending=True).reset_index(drop=True)
        print(update_df)
        return update_df

#rena drabovsky 
    def choose_map(self):
        """
        Prompts the user to select a map from available options.
        """
        print("Choose a map:")
        for index, map in enumerate(self.maps, start=1):
            print(f"{index}. {map}")

        while True:
            map_choice = input("30, 60 or 90: ").strip()
            if map_choice in ['30', '60', '90']:
                self.selected_map = next((m for m in self.maps if str(m.duration) == map_choice), None)
                if self.selected_map:
                    print(f"You selected {self.selected_map.name} ({self.selected_map.duration} seconds)")
                    break
            else:
                print("Please enter '30', '60', or '90' to select a map duration.")

#ezra gashaw, rena drabovsky
    def start_game(self):
        """
        Runs the game simulation, handles item logic and player progress, and announces the winner.
        """
        race_duration = self.selected_map.duration
        print(f"\nMap selected: {self.selected_map.name} --- Race length: {race_duration} seconds")
        print("3, 2, 1... START!\n")

        start_time = time.time()
        elapsed = 0
        next_item_time = random.randint(7, 10)

        while elapsed < race_duration:
            elapsed = int(time.time() - start_time)
            print(f"Time: {elapsed} seconds")

            if elapsed >= next_item_time:
                for player in self.players:
                    if self.itemList:
                        item = random.choice(self.itemList)
                        player.items.append(item)
                        print(f"\nPlayer {player.name} received the {item}! \n")
                        self.keep_throw(item, player)
                next_item_time = elapsed + random.randint(5, 9)

            for player in self.players:
                if player.stopped_timer > 0:
                    print(f"{player.name} hit an obstacle! Recovering...\n")
                    player.stopped_timer -= 1
                else:
                    player.points += 1  

            time.sleep(1)

        for player in self.players:
            penalty = (max([p.points for p in self.players]) - player.points) * 0.5
            player.completed_time = race_duration + penalty + random.uniform(-5, 5)

        results = {player.name: player.completed_time for player in self.players}
        winners_df = self.update_ranking(results)
        print(f"\nWinner: {winners_df.iloc[0]['Player']} with a time of {winners_df.iloc[0]['Time Completed']}!")

#ezra gashaw
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the racing game simulation.")
    parser.add_argument("players", nargs='+', help="List of player names")
    parser.add_argument("--itemfile", default="item_list.txt", help="Path to the item list text file")

    args = parser.parse_args()
    game = Game(args.players, args.itemfile)
    game.choose_map()
    game.start_game()
