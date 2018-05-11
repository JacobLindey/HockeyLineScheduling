from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import sys


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class PlayerParser:

    def __init__(self):

        # field keys for data
        self.goalie_keys = ["Date", "Season Game", "Age", "Team", "Home/Away", "Opponent", "Win/Loss", "Decision",
                            "Goals Against", "Shots Against", "Saves", "Save Percentage", "Shutouts", "Penalties",
                            "TOI"]
        self.non_goalie_keys = ["Date", "Season Game", "Age", "Team", "Home/Away", "Opponent", "Win/Loss", "Goals",
                                "Assists", "Points", "+/-", "PIM", "EV Goals", "PP Goals", "SH Goals", "GW Goals",
                                "EV Assists", "PP Assists", "SH Assists", "Shots", "Shot%", "Shifts", "TOI", "Hits",
                                "Blocks", "Face-off Wins", "Face-off Losses", "Face-off Win%"]
        self.keys = []
        # player stats
        self.player_first = ""
        self.player_last = ""
        self.short_first = ""
        self.short_last = ""
        self.season_year = ""
        self.name_num = ""
        self.position = ""
        self.combined_name = ""
        self.data_frame = None

    def set_inputs(self, player_first, player_last, season_year):
        self.player_first = player_first
        self.player_last = player_last
        self.season_year = season_year
        self.name_num = "01"
        self.format_name()

    def format_name(self):
        """
        pulls name bits
        :return: None
        """
        # Format input names
        if len(self.player_last) >= 5:
            self.short_last = self.player_last[:5].lower()
        else:
            self.short_last = self.player_last.lower()

        self.short_first = self.player_first[:2].lower()

    def set_combined_name(self):
        """
        combines first and last name for unique identifier
        :return: None
        """
        self.combined_name = self.short_last + self.short_first + self.name_num

    def check_name(self, game_log_soup):
        """
        determines if fetched page matches queried name
        :param game_log_soup: html soup from hockey-reference
        :return: boolean or exit
        """
        parsed_name = game_log_soup.find('h1', attrs={'itemprop': 'name'}).text
        # print(parsed_name)

        if parsed_name.replace('.', "") == self.player_first + ' ' + self.player_last:
            return True
        else:
            self.name_num = '0' + str(int(self.name_num) + 1)
            if self.name_num == '05':
                print("Exceeded Depth on Search")
                sys.exit(1)

    def get_position(self, game_log_soup):
        parsed_person = game_log_soup.find('div', attrs={'itemtype': 'https://schema.org/Person'})
        parsed_position = parsed_person.find('p').text[10]  # grabs the 11 character in the line, the position id
        self.position = parsed_position

    def get_game_log_soup(self):
        """
        fetches page soup from hockey-reference
        :return: returns some beautiful soup
        """
        while True:

            self.set_combined_name()
            # print(self.combined_name)  # useful for catching errors

            # assemble the url that needs to be queried
            url = 'https://www.hockey-reference.com/players/c/' + self.combined_name + \
                  '/gamelog/' + self.season_year + '/'

            # query hockey-reference.com
            try:
                response = requests.get(url)
            except requests.ConnectionError:
                print("No such page ", self.combined_name)
                sys.exit(1)

            # create some soup
            game_log_soup = BeautifulSoup(response.text, 'html.parser')

            if self.check_name(game_log_soup):
                self.get_position(game_log_soup)
                self.keys = self.goalie_keys if self.position is 'G' else self.non_goalie_keys
                return game_log_soup

    def get_game_log_table_body(self, game_log_soup):
        """
        pulls table body from html soup
        :param game_log_soup: html soup from hockey-reference.com
        :return: soup for table body
        """
        try:
            table = game_log_soup.find('table', attrs={'id': "gamelog"})  # the table object on hockey-reference
            table_body = table.find('tbody')  # grab the body of the table
        except RuntimeError:
            print(game_log_soup.find('table', attrs={'id': 'gamelog'}))
            return [self.combined_name, None, None]
        return table_body

    @ staticmethod
    def fetch_data_from_table(table_body):
        """
        pulls data from table and places it into a numpy array stratified by record
        :param table_body: soup for tbody
        :return: numpy array stratified by record
        """
        # split the table body into rows
        rows = table_body.find_all('tr')
        data = []  # container for the data scraped
        # iterate through the rows, grabbing the contents of each cell
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]  # strip the text
            data.append(cols)
        data = np.array(data)  # convert the data list to an array for ease of use
        return data

    @ staticmethod
    def remove_empty_data(data):
        # remove empty data rows
        del_arr = []  # index collection for deletion
        for i, d in enumerate(data):
            if len(d) == 0:
                del_arr.append(i)
        if len(del_arr) > 0:
            data = np.delete(data, del_arr)  # delete them

        return data

    def reshape_data(self, data):
        """
        stratifies data by field rather than record
        :param data: numpy array stratified by record
        :return: numpy array stratified by field
        """
        # we reshape the data, placing it into rows of common data
        reshaped_data = []
        for i, key in enumerate(self.keys):
            temp = []
            for record in data:
                if i < len(record):
                    temp.append(record[i])
                else:
                    temp.append('NULL')
            reshaped_data.append(temp)
        reshaped_data = np.array(reshaped_data)
        return reshaped_data

    @ staticmethod
    def format_time(time_data):
        for i, time in enumerate(time_data):
            t = time.split(':')
            t = int(t[0])*60 + int(t[1])
            time_data[i] = t
        return time_data

    def create_data_frame(self, reshaped_data):
        """
        creates a data from given data
        :param reshaped_data: numpy array containing data stratified by field
        :return: pandas data frame
        """
        data_dict = {}  # dictionary for data frame construction
        for i, key in enumerate(self.keys):
            data_dict[key] = reshaped_data[i]  # assign data to key
        data_dict['Position'] = [self.position]*len(reshaped_data[0])  # Set position info
        data_dict['TOI'] = self.format_time(data_dict['TOI'])
        df = pd.DataFrame(data_dict)  # data frame construct

        return df

    def create_player_data(self):
        """
        creates data frame player data fetched from hockey-reference.com
        :return: pandas data frame
        """

        # fetch game log beautiful soup
        game_log_soup = self.get_game_log_soup()

        # fetch table body
        table_body = self.get_game_log_table_body(game_log_soup)

        # fetch data from table body
        data = self.fetch_data_from_table(table_body)

        # remove empty data rows
        data = self.remove_empty_data(data)

        # reshape by field
        reshaped_data = self.reshape_data(data)

        # create the player data from data
        df = self.create_data_frame(reshaped_data)

        self.keys[4:4] = ["Position"]
        return [self.combined_name, df, self.keys]
