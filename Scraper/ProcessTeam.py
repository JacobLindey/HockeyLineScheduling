from src.PlayerParser import PlayerParser
import pandas as pd


def process_team(team_file):
    f = open(team_file, 'r')  # open file

    team_id = f.readline().rstrip('\n')  # read off teamID from first line
    season_year = f.readline().rstrip('\n')  # read off year from second line

    players = []  # container for player names
    for line in f:
        players.append(line)

    player_data_frames = []  # container for scraper output
    for player in players:
        first_name = player.split()[0]
        last_name = player.split()[1]
        player_parser = PlayerParser()
        player_parser.set_inputs(first_name, last_name, season_year)
        player_data_frames.append(player_parser.create_player_data())

    # prepare to write to excel file
    writer = pd.ExcelWriter('playerstats' + team_id + season_year + '.xlsx', options={'strings_to_numbers': True})
    for player in player_data_frames:
        player_name, data_frame, keys = player
        # if no data, don't write
        if data_frame is not None:
            data_frame.to_excel(writer, player_name, columns=keys)
        else:
            pd.DataFrame().to_excel(writer, player_name)
    writer.save()
    print("Successfully saved as " + 'playerstats' + team_id + season_year + '.xlsx')
    writer.close()
