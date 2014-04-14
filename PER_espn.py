'''
Created on 22/02/2014

'''
from bs4 import BeautifulSoup
import urllib2
import re
import time
import pickle

teams_chart = {}   #  {"Team": [Players]}

title = []         #  ["stat headers"]
totalStats = []    #  [[page1[players], [page[2][players]], ...]

def loadTeams():
    """
    Adds team key: list of players to dictionary teams_chart
    """
    name_index = 1
    for pageStats in totalStats:
        for player in pageStats:
            p = player[name_index].split(", ")
            name = p[0]
            if "/" in p[1]:
                team  = p[1].split("/")[1]
            else:
                team = p[1]
            if team not in teams_chart:
                teams_chart[team] = [name]
            else:
                teams_chart[team].append(name)
                
def sumPERteam(team):
    """
    Input the team name as string and returns 
    the sum of PER team and PER avg of players on the team
    
    sumerPERteam(String) -> list float[team PER sum, team PER avg   per player]
    """
    totalsum = 0
    for player in teams_chart[team]:
        for pg in totalStats:
            for stats in pg:
                if player in stats[1]:
                    totalsum += float(stats[11])
    return [totalsum, totalsum/len(teams_chart[team])]
        
for pgNum in range(1, 8):
    """ 
    Scrapes the PER table data from each page
    The data is stored as a nested list of each list being the table row
    
    e.g.['1', 'Kevin  Durant, OKC', '77', '38.5', '.639', '16.3', '10.4',
        '31.1', '2.2', '18.9', '11.0', '30.17', '869.3', '29.0']
    """
    
    #URL Table of NBA Players' PER
    targetURL = "http://insider.espn.go.com/nba/hollinger/statistics/_/page/{0}"
    targetURL = targetURL.format(pgNum)
         
    #HTML display
    page = urllib2.urlopen(targetURL)
    pageHTML = page.read()
    soup = BeautifulSoup(pageHTML)
    
    stats = []              #  [TD]
    stats_split = []        #  [[Row TD1], [Row TD2], ...]
    
    if pgNum == 1:
        for t_row in soup.findAll("tr", {"class":"colhead"}):
            for col in t_row:
                title.append(col.get_text())
        print title
            
    for pgData in soup.findAll("tr", {"class": re.compile(r"player")}):
        for d in pgData:
            stats.append(d.get_text())
    
    for i in range(0, len(stats), 14):
        stats_split.append(stats[i:i+14])
    print stats_split
    
    totalStats.append(stats_split)
    
    time.sleep(1)

print totalStats

f = open("PER_file.txt", "w")
pickle.dump(totalStats, f)
f.close()

loadTeams()
print teams_chart
print "OKC - PER", sumPERteam("OKC")
print "SA - PER", sumPERteam("SA")
