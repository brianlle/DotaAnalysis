import json
import requests
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Pulls Dota 2 API information on matches")
parser.add_argument("-k", "--key", help="Steam API key", required=True)
args = parser.parse_args()

key = args.key                          #personal Steam WebAPI key
playerID = '76561198006933710'          #enter Steam playerID to only find matches for that player

def retrieve_match_IDs_by_hero(playerID,key,heroID,startAtMatch='0'):
    '''
    Retrieves match history information for a player in json format and then returns
    a list of matchIDs the player was involved in to be used to retrieve match details
    
    Regardless of parameters enetered, WebAPI will only return the 500 most recent matches
    (100 at a time maximum); to get around this, implement a for loop to search matches
    by hero played assuming no hero has been played more than 500 times.
    
    Parameters
    -----------
    playerID (str): Numerical Steam playerID
    key (str): Personal Steam WebAPI key
    startAtMatch (str): Tells API what match to start at and returns descending matches
                        Disables when 0. When non-zero, take the latest matchID found and subtract
                        one to be used in function recursion.
    heroID (str): Hero numerical identifier to serach matches where playerID played heroID.
                  Default of 0 searches by any hero.
    '''
    
    r = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?matches_requested=100&account_id=%s&key=%s&start_at_match_id=%s&hero_id=%s' % (playerID, key, startAtMatch, heroID))
    resultJ = json.loads(r.text)
    matchIDList = []
    for match in resultJ['result']['matches']:
        matchIDList.append(match['match_id'])
    
    if len(resultJ['result']['matches']) != 0:
        newStart = matchIDList[-1]-1
        matchIDList = matchIDList + retrieve_match_IDs_by_hero(playerID,key,heroID,newStart)
    
    return matchIDList


def retrieve_all_match_IDs(playerID,key):
    '''
    Uses retrieve_match_IDs_by_hero and parses through every hero currently in the game
    110 heroes currently with IDs ranging from 1 to 112 as of October 2015
    '''
    
    matchIDList = []
    heroRange = list(range(1,113))   #heroIDs range from 1 to 112 currently
    heroRange.remove(24)             #no hero with ID 24... strangely
    heroRange.remove(108)            #no hero with ID 108 yet, probalby Pitlord or Arc Warden
    
    for hero in heroRange:
        matchIDList = matchIDList + retrieve_match_IDs_by_hero(playerID,key,str(hero),'0')
        
    return matchIDList

def get_stats(interestedPlayer, dataSummary):
    '''
    Reads in a dataframe and pumps out interesting/funny statistics about a player
    
    Parameters
    ----------
    interestedPlayer (str): numerical player ID as stored by steam API information
    dataSummary (dataframe): dataframe of data compiled from match history information
    
    '''
    
    tempDF = dataSummary.groupby(['Player ID', 'Win Y/N']).aggregate(sum)
    averageDPMinLoss = tempDF.loc[interestedPlayer, 0]['Deaths']/tempDF.loc[interestedPlayer, 0]['Match Length (s)'] * 60
    averageDPMinWin = tempDF.loc[interestedPlayer, 1]['Deaths']/tempDF.loc[interestedPlayer, 1]['Match Length (s)'] * 60
    
    print('Player\'s average deaths per minute in losses is %s over %s matches' % (averageDPMinLoss, tempDF.loc[interestedPlayer, 0]['Match Counter']))
    print('Player\'s average deaths per minute in wins is %s over %s matches' % (averageDPMinWin, tempDF.loc[interestedPlayer, 1]['Match Counter']))
    print('Player\'s win-loss when playing with you: ' + str(tempDF.loc[interestedPlayer,1]['Match Counter']) + '-' + str(tempDF.loc[interestedPlayer,0]['Match Counter']))
    
    return None

matchIDList = retrieve_all_match_IDs('76561198006933710',key)

matchDetails = []
for match in matchIDList:
    rTemp = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id=%s&key=%s' % (match, key))
    matchDetails.append(json.loads(rTemp.text))

matchDetails[:] = [match for match in matchDetails if ('result' in match)]             #removes erroneous matches as some are special matches
matchDetails[:] = [match for match in matchDetails if ('players' in match['result'])]  #without the same parameters

playerID = []                 #initialize lists for stats of interest
playerSlot = []
playerKills = []
playerDeaths = []
playerAssists = []
gameWonStatus = []
matchID = []
matchLength = []
matchCounter = []

for match in matchDetails:    #construct lists
    for player in match['result']['players']:
        playerID.append(player['account_id'])
        playerSlot.append(player['player_slot'])
        playerKills.append(player['kills'])
        playerDeaths.append(player['deaths'])
        playerAssists.append(player['assists'])
        matchLength.append(match['result']['duration'])
        
        if ((player['player_slot'] == 0) or (player['player_slot'] == 1) or (player['player_slot'] == 2) or (player['player_slot'] == 3) or (player['player_slot'] == 4)) and match['result']['radiant_win'] == True:
            gameWonStatus.append(1)
        elif ((player['player_slot'] == 128) or (player['player_slot'] == 129) or (player['player_slot'] == 130) or (player['player_slot'] == 131) or (player['player_slot'] == 132)) and match['result']['radiant_win'] == False:
            gameWonStatus.append(1)
        else:
            gameWonStatus.append(0)
        matchID.append(match['result']['match_id'])
        matchCounter.append(1)

#construct dictionary to build data frame
referenceDict = {'Player ID': playerID, 'Player Slot': playerSlot, 'Kills': playerKills, 'Deaths': playerDeaths, 'Assists': playerAssists, 'Win Y/N': gameWonStatus, 'Match ID': matchID, 'Match Length (s)': matchLength, 'Match Counter': matchCounter}
dataFrameSummary = pd.DataFrame(data=referenceDict)

get_stats(30999748,dataFrameSummary)    #get some fun stats about player '30999748' aka feeder