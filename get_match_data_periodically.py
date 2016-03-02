import json
import requests
import numpy as np
import pandas as pd
import argparse
import time
import csv

parser = argparse.ArgumentParser(description="Pulls Dota 2 API information on matches")
parser.add_argument("-k", "--key", help="Steam API key", required=True)
args = parser.parse_args()

key = args.key                        #personal Steam WebAPI key
playerID = '46667982'                 #enter Steam playerID to only find matches for that player

def retrieve_match_IDs_by_game_type(key,game_mode,skill,startAtMatch='0'):
    '''
    Retrieves match history information for a player in json format and then returns
    a list of matchIDs the player was involved in to be used to retrieve match details
    
    Regardless of parameters enetered, WebAPI will only return the 500 most recent matches
    (100 at a time maximum); to get around this, implement a for loop to search matches
    by hero played assuming no hero has been played more than 500 times.
    
    Parameters
    -----------

    key (str): Personal Steam WebAPI key
    startAtMatch (str): Tells API what match to start at and returns descending matches
                        Disables when 0. When non-zero, take the latest matchID found and subtract
                        one to be used in function recursion.
    game_mode (str): Game mode identifier. 1 = All Pick, 22 = Ranked All Pick.
    skill (str): Skill level identifier. 3 = Very High skill
    '''
    
    r = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=100&key=%s&game_mode=%s&skill=%s&start_at_match_id=%s&min_players=10' % (key, game_mode, skill, 0))
    resultJ = json.loads(r.text)
    matchIDList = []
    for match in resultJ['result']['matches']:
        matchIDList.append(match['match_id'])
    
    time.sleep(1)
    newStart = matchIDList[-1]-1
    r = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=100&key=%s&game_mode=%s&skill=%s&start_at_match_id=%s&min_players=10' % (key, game_mode, skill, newStart))
    resultJ = json.loads(r.text)
    for match in resultJ['result']['matches']:
        matchIDList.append(match['match_id'])

    time.sleep(1)
    newStart = matchIDList[-1]-1
    r = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=100&key=%s&game_mode=%s&skill=%s&start_at_match_id=%s&min_players=10' % (key, game_mode, skill, newStart))
    resultJ = json.loads(r.text)
    for match in resultJ['result']['matches']:
        matchIDList.append(match['match_id'])
        
    time.sleep(1)
    newStart = matchIDList[-1]-1
    r = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=100&key=%s&game_mode=%s&skill=%s&start_at_match_id=%s&min_players=10' % (key, game_mode, skill, newStart))
    resultJ = json.loads(r.text)
    for match in resultJ['result']['matches']:
        matchIDList.append(match['match_id'])
        
    time.sleep(1)
    newStart = matchIDList[-1]-1
    r = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=100&key=%s&game_mode=%s&skill=%s&start_at_match_id=%s&min_players=10' % (key, game_mode, skill, newStart))
    resultJ = json.loads(r.text)
    for match in resultJ['result']['matches']:
        matchIDList.append(match['match_id'])
    
    return matchIDList

highestMatchPrior = 0
lowestMatchCurrent = 0
matchIDListRunning = []

for x in range(0, 100):

    print "Loop # %d started" %(x)

    matchIDList = retrieve_match_IDs_by_game_type(key,22,3,0)
    matchIDListClone = matchIDList    #clone for iteration to remove duplicate games
    
    lowestMatchCurrent = int(matchIDList[-1])
    for matchNumber in matchIDListClone:
        if matchNumber in matchIDListRunning:   #remove matches already called
            matchIDList.remove(matchNumber)
    matchIDListRunning = matchIDListRunning + matchIDList   #update list of matches already called
    time.sleep(2)

    matchDetails = []
    for match in matchIDList:
        rTemp = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id=%s&key=%s' % (match, key))
        if len(rTemp.text)>4000:         #sometimes API will fail and won't get the match, so no json to load and would unnecessarily stop the loop
            matchDetails.append(json.loads(rTemp.text))
        time.sleep(2)

    matchDetails[:] = [match for match in matchDetails if ('result' in match)]             #removes erroneous matches as some are special matches
    matchDetails[:] = [match for match in matchDetails if ('players' in match['result'])]  #without the same dictionary entrie

    with open('automatchdetails.txt', 'a') as text:                 #save raw json data so we don't have to call the API again for same data
        json.dump(matchDetails, text)

    with open('matchidlist.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(matchIDList)
    
    highestMatchPrior = int(matchIDList[0])
    
    print "Loop # %d done, now sleeping" %(x)
    time.sleep(300)
