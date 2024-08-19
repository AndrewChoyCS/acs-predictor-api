from bs4 import BeautifulSoup
import requests
import re
import csv

# url = 'https://www.vlr.gg/360909/naos-vs-zol-esports-challengers-league-2024-philippines-split-2-ubsf/?game=all&tab=overview'
# response = requests.get(url)
# data = response.text

# soup = BeautifulSoup(data, 'html.parser')
finalData = []
index = 1
while index < 50: 
    url = f'https://www.vlr.gg/matches/results/?page={index}'
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser') 
    links = []
    divTags = soup.findAll('div', class_='wf-card')
    for tag in divTags:
        aTags = tag.findAll('a')
        for aTag in aTags:
            if aTag:
                link = aTag['href']
                links.append(link)
    links = links[2:]       
    for currLink in links:
        url = 'https://vlr.gg' + currLink 
        response = requests.get(url)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser') 
        gameIds = []
        div = soup.findAll('div', class_="vm-stats-gamesnav-item js-map-switch")
        for item in div:
            if item:
                gameId = item['data-game-id']
                gameIds.append(gameId)

        all_stats = []  # Initialize an empty list to store all stats

        for gameId in gameIds:
            currGame = soup.find('div', class_='vm-stats-game', attrs={'data-game-id': gameId})
            map = currGame.find('div', class_='map').text.strip().split()[0]
            rows = currGame.find_all('tr')
            
            for row in rows:       
                # Find the player name element
                name_tag = row.find('a', href=lambda x: x and '/player' in x)
                
                if name_tag:
                    player = name_tag.find('div', class_='text-of')
                    team = name_tag.find('div', class_='ge-text-light')
                    newPlayer = re.sub(r'[\n\t]+', ' ', player.text)  # Replace newlines and tabs with a space
                    newTeam = re.sub(r'[\n\t]+', ' ', team.text)  # Replace newlines and tabs with a space
                    newPlayer = newPlayer.strip()
                    newTeam = newTeam.strip()
                
                stats = row.find_all('span', class_='side mod-side mod-both')
                cleaned_stats = [stat.text.strip() for stat in stats]  # Clean the stats
                
                if cleaned_stats:  # Check if cleaned_stats is not empty
                    tup = (gameId, newPlayer, newTeam, map, cleaned_stats)
                    all_stats.append(tup)  # Append the cleaned stats to the main list
                    print(tup)
        finalData.extend(all_stats)
    index += 1
csv_file_path = 'player_stats.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Writing the header
    csvwriter.writerow(['Game ID', 'Player', 'Team', 'Map', 'K/D Ratio', 'ACS', 'Kills'])
    
    # Writing the data rows
    for stat in finalData:
        gameId, player, team, map, stats = stat
        csvwriter.writerow([gameId, player, team, map] + stats)