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
        if row_count % 3 == 1:
            # this is FIRST row of a game, so it is just the Time of the game
            cols = ['time']
            game_details = {}
            game_details['time'] = row.find('td').text
        else:
            # this is SECOND or THIRD row of a game, which contains Away/Home team details
            tds = row('td')
            cols = ['team_name', 'pitcher', 'open', 'line_movement', 'current', 'run_line', 'scores']
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
        if row_count > 2:
            break
    print('Complete')
