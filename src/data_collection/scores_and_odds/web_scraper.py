import re
from bs4 import BeautifulSoup
import requests

money_line_cols = [
    'date',
    'away_team_name', 'away_pitcher', 'away_pitcher_handedness',
    'home_team_name', 'home_pitcher', 'home_pitcher_handedness',
    'away_money_line_open', 'away_money_line_current',
    'home_money_line_open', 'home_money_line_current',
    'money_line_movement',
    'away_final',
    'home_final',
]

run_line_cols = [
    'date',
    'away_team_name', 'away_pitcher', 'away_pitcher_handedness',
    'home_team_name', 'home_pitcher', 'home_pitcher_handedness',
    'away_run_line',
    'home_run_line',
    'away_final',
    'home_final',
]

ou_line_cols = [
    'date',
    'away_team_name', 'away_pitcher', 'away_pitcher_handedness',
    'home_team_name', 'home_pitcher', 'home_pitcher_handedness',
    'o/u_open', 'o/u_movement', 'o/u_current',
    'total_runs_final',
]

def parse_money_line_odds(odds):
    """ Read a money line odds string and return it as (favorite_odds, underdog_odds) tuple 

        @example: parse_money_line_odds('-130') => (-130, +110)
        @example: parse_money_line_odds('+100') => (-110, +100)
    """
    is_favorite = abs(int(odds)) / int(odds) == -1
    if is_favorite:
        return odds, str(100 + abs(abs(int(odds)) - 110))
    return str(-1 * (100 + abs(abs(int(odds)) - 110))), odds

def parse_game_data_rows(date, time_row, away_team_row, home_team_row):
    """
    parse the BeautifulSoup row objects for the <tr> data in scoresandodds.com Odds history view
    """
    game_details = {'date': date}
    # the FIRST row of a game is just the Time of the game
    game_details['time'] = time_row.find('td').text

    home_tds = home_team_row.find_all('td')
    away_tds = away_team_row.find_all('td')
    # TEAM NAME
    game_details['home_team_name'] = home_tds[0].find('a').string
    game_details['away_team_name'] = away_tds[0].find('a').string
    # TEAM PITCHER, eg '(r) arrieta, j'
    home_pitcher = re.match(r"\((?P<handedness>[r,l])\) (?P<name>.*)", home_tds[1].string).groupdict()
    away_pitcher = re.match(r"\((?P<handedness>[r,l])\) (?P<name>.*)", away_tds[1].string).groupdict()

    game_details['home_pitcher'] = home_pitcher['name']
    game_details['home_pitcher_handedness'] = home_pitcher['handedness']
    game_details['away_pitcher'] = away_pitcher['name']
    game_details['away_pitcher_handedness'] = away_pitcher['handedness']

    # ODDS (either Money Line favorite, eg '-120', or O/U, eg '9u20')
    if home_tds[2].string[0] == '-':
        # This is the Money Line and HOME team is open favorite
        fav_underdog = parse_money_line_odds(home_tds[2].string)
        game_details['home_money_line_open'] = fav_underdog[0]
        game_details['away_money_line_open'] = fav_underdog[1]
        game_details['o/u_open'] = away_tds[2].string
        game_details['money_line_movement'] = home_tds[3].string
        game_details['o/u_movement'] = away_tds[3].string
    elif home_tds[2].string[0] == '+':
        # This is the Money Line and HOME team is open underdog
        fav_underdog = parse_money_line_odds(home_tds[2].string)
        game_details['away_money_line_open'] = fav_underdog[0]
        game_details['home_money_line_open'] = fav_underdog[1]
        game_details['o/u_open'] = away_tds[2].string
        game_details['money_line_movement'] = home_tds[3].string
        game_details['o/u_movement'] = away_tds[3].string
    else:
        # This is the O/U line (and AWAY team is favorite)
        fav_underdog = parse_money_line_odds(away_tds[2].string)
        game_details['away_money_line_open'] = fav_underdog[0]
        game_details['home_money_line_open'] = fav_underdog[1]
        game_details['o/u_open'] = home_tds[2].string
        game_details['money_line_movement'] = away_tds[3].string
        game_details['o/u_movement'] = home_tds[3].string

    # ODDS (either Money Line favorite, eg '-120', or O/U, eg '9u20')
    if home_tds[4].string[0] == '-':
        # This is the Money Line and HOME team is current favorite
        fav_underdog = parse_money_line_odds(home_tds[4].string)
        game_details['home_money_line_current'] = fav_underdog[0]
        game_details['away_money_line_current'] = fav_underdog[1]
        game_details['o/u_current'] = away_tds[4].string
    elif home_tds[4].string[0] == '+':
        # This is the Money Line and HOME team is current underdog
        fav_underdog = parse_money_line_odds(home_tds[4].string)
        game_details['away_money_line_current'] = fav_underdog[0]
        game_details['home_money_line_current'] = fav_underdog[1]
        game_details['o/u_current'] = away_tds[4].string
    else:
        # This is the O/U Line and AWAY team is current favorite
        fav_underdog = parse_money_line_odds(away_tds[4].string)
        game_details['away_money_line_current'] = fav_underdog[0]
        game_details['home_money_line_current'] = fav_underdog[1]
        game_details['o/u_current'] = home_tds[4].string

    # RUN LINE
    game_details['home_run_line'] = home_tds[5].string
    game_details['away_run_line'] = away_tds[5].string

    # FINAL SCORE
    game_details['home_final'] = home_tds[6].find('span').string
    game_details['away_final'] = away_tds[6].find('span').string
    if game_details['home_final'] is None or game_details['away_final'] is None:
        # Game was postponed... so we don't care about this game. Just return None
        return None
    else:
        game_details['total_runs_final'] = str(int(game_details['home_final']) + int(game_details['away_final']))

    return game_details

def print_money_line_odds(game_details):
    """
    Print information for Money Line details of a game
    """
    print('\t'.join([game_details[col] for col in money_line_cols]))

def print_run_line_odds(game_details):
    """
    Print information for Run Line details of a game
    """
    print('\t'.join([game_details[col] for col in run_line_cols]))

def print_over_under_odds(game_details):
    """
    Print information for Over/Under details of a game
    """
    print('\t'.join([game_details[col] for col in ou_line_cols]))


def scrape_data_for_date(date):
    get_response = requests.get('http://www.scoresandodds.com/grid_' + date.replace('-', '') + '.html')
    soup = BeautifulSoup(get_response.content, 'html.parser')
    mlb_section = soup.find('div', id='mlb')

    mlb_table = mlb_section.find_next('table')
    mlb_rows = mlb_table.find_next('tbody')
    row_count = 0
    game_details_list = []
    for row in mlb_rows.children:
        row_count += 1
        if row_count % 5 == 0:
            # Reset to prepare for next game's set of rows
            time_row = None
            away_team_row = None
            home_team_row = None
        elif row_count % 5 == 1:
            time_row = row
        elif row_count % 5 == 2:
            away_team_row = row
        elif row_count % 5 == 3:
            home_team_row = row
            game_details = parse_game_data_rows(date, time_row, away_team_row, home_team_row)
            if game_details is not None:
                game_details_list.append(game_details)
    return game_details_list

if __name__ == '__main__':
    print('Begin scraping scoresAndOdds.com')
    game_details_list = []
    for date in ['2018-06-01', '2018-06-02', '2018-06-03']:
        game_details_list.extend(scrape_data_for_date(date))

    # Money Line results
    print('\t'.join([col.upper() for col in money_line_cols]))
    for game_details in game_details_list:
        print_money_line_odds(game_details)
    print('\n')

    # Run Line results
    print('\t'.join([col.upper() for col in run_line_cols]))
    for game_details in game_details_list:
        print_run_line_odds(game_details)
    print('\n')

    # O/U Line results
    print('\t'.join([col.upper() for col in ou_line_cols]))
    for game_details in game_details_list:
        print_over_under_odds(game_details)
    print('\n')
    print('Complete')
