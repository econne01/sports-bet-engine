from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    print('Begin scraping scoresAndOdds.com')
    get_response = requests.get('http://www.scoresandodds.com/grid_20180602.html')
    soup = BeautifulSoup(get_response.content, 'html.parser')
    mlb_section = soup.find('div', id='mlb')
    print(mlb_section)
    mlb_table = mlb_section.find_next('table')
    mlb_rows = mlb_table.find_next('tbody')
    row_count = 0
    game_details = {}
    for row in mlb_rows.children:
        row_count += 1
        if row_count % 5 == 1:
            print(game_details)
            # this is FIRST row of a game, so it is just the Time of the game
            cols = ['time']
            game_details = {}
            game_details['time'] = row.find('td').text
        elif row_count % 5 == 2 or row_count % 5 == 3:
            if row_count % 5 == 2:
                home_or_away = 'away'
            elif row_count % 5 == 3:
                home_or_away = 'home'
            # this is SECOND or THIRD row of a game, which contains Away/Home team details
            tds = row('td')
            cols = ['team_name', 'pitcher', 'open', 'line_movement', 'current', 'run_line', 'scores']

            # TEAM NAME
            game_details[home_or_away + '_' + cols[0]] = tds[0].find('a').string
            # TEAM PITCHER
            game_details[home_or_away + '_' + cols[1]] = tds[1].string
            # ODDS (either Money Line favorite, eg '-120', or O/U, eg '9u20')
            open_odds = tds[2].string
            if open_odds[0] == '-':
                # This is the Money Line
                if home_or_away == 'away':
                    game_details['away_money_line_open'] = open_odds
                    game_details['home_money_line_open'] = str(100 + abs(int(open_odds)) - 110)
                elif home_or_away == 'home':
                    game_details['away_money_line_open'] = str(100 + abs(int(open_odds)) - 110)
                    game_details['home_money_line_open'] = open_odds
            else:
                # This is the O/U line
                game_details['o/u_open'] = open_odds
            # LINE MOVEMENTS
            line_movements = tds[3].string
            if line_movements[0] == '-':
                game_details['money_line_movement'] = line_movements
            else:
                game_details['o/u_movement'] = line_movements
            # ODDS (either Money Line favorite, eg '-120', or O/U, eg '9u20')
            current_odds = tds[4].string
            if current_odds[0] == '-':
                # This is the Money Line
                if home_or_away == 'away':
                    game_details['away_money_line_current'] = current_odds
                    game_details['home_money_line_current'] = str(100 + abs(int(current_odds)) - 110)
                elif home_or_away == 'home':
                    game_details['away_money_line_current'] = str(100 + abs(int(current_odds)) - 110)
                    game_details['home_money_line_current'] = current_odds
            else:
                # This is the O/U line
                game_details['o/u_current'] = current_odds
            # RUN LINE
            game_details[home_or_away + '_run_line'] = tds[5].string



            for idx, col in enumerate(cols):
                if tds[idx].find('a'):
                    col_text = tds[idx].find('a').string
                elif tds[idx].find('span'):
                    col_text = ''
                    for span in tds[idx].find_all('span'):
                        col_text += ' ' + span.string
                else:
                    col_text = tds[idx].string
                print(col, col_text.strip())
        
    print('Complete')
