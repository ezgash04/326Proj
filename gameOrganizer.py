import pandas as pd

#init dataframe
players_df = pd.DataFrame(columns=['Player', 'Points'])

def update_ranking(points_dict):
    global players_df

    #convert dict to dataframe
    update_df = pd.DataFrame(list(points_dict.items()), columns=['Player', 'Points'])

    #merge with existing data, summing points
    players_df = pd.concat([players_df, update_df]).groupby('Player', as_index=False).sum()

    #organize by points in descending order
    players_df = players_df.sort_values(by='Points', ascending=False).reset_index(drop=True)

    print(players_df)

#ex
update_ranking({'Alice': 10, 'Bob': 5, 'Charlie': 7})
update_ranking({'Bob': 6, 'Alice': 4})