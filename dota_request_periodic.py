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

def create_dota_dataframe(matchDetailsList):
    
    '''
    Takes in list of match detail json strings and converts
    into a pandas dataframe for easier statistical manipulation
    '''

    playerID = []                 #initialize lists for stats of interest
    playerSlot = []
    playerKills = []
    playerDeaths = []
    playerAssists = []
    playerGPM = []
    playerXPM = []
    playerHeroDamage = []
    playerTowerDamage = []
    playerLevel = []
    playerHeroID = []
    gameWonStatus = []
    matchID = []
    matchLength = []
    matchCounter = []
    gameStartTime = []

    for match in matchDetailsList:    #construct lists
        for player in match['result']['players']:
            playerID.append(player['account_id'])
            playerSlot.append(player['player_slot'])
            playerKills.append(player['kills'])
            playerDeaths.append(player['deaths'])
            playerAssists.append(player['assists'])
            playerGPM.append(player['gold_per_min'])
            playerXPM.append(player['xp_per_min'])
            playerHeroDamage.append(player['hero_damage'])
            playerTowerDamage.append(player['tower_damage'])
            playerLevel.append(player['level'])
            playerHeroID.append(player['hero_id'])
            if player['player_slot'] <= 0 and match['result']['radiant_win'] == True:
                gameWonStatus.append(1)
            elif player['player_slot'] >= 128 and match['result']['radiant_win'] == False:
                gameWonStatus.append(1)
            else:
                gameWonStatus.append(0)
            matchID.append(match['result']['match_id'])
            matchLength.append(match['result']['duration'])
            matchCounter.append(1)
            gameStartTime.append(match['result']['start_time'])

    #construct dictionary to build data frame
    referenceDict = {'Player ID': playerID, 'Player Slot': playerSlot, 'Kills': playerKills, 'Deaths': playerDeaths, 'Assists': playerAssists, 'GPM': playerGPM, 'XPM': playerXPM, 'Hero Damage': playerHeroDamage, 'Tower Damage': playerTowerDamage, 'Level': playerLevel, 'Hero ID': playerHeroID, 'Win Y/N': gameWonStatus, 'Match ID': matchID, 'Match Length (s)': matchLength, 'Match Counter': matchCounter, 'Game Start Time': gameStartTime}
    dataFrameSummary = pd.DataFrame(data=referenceDict)

    return dataFrameSummary

def get_stats(interestedPlayer, dataSummary):
    '''
    Reads in a dataframe and pumps out interesting/funny statistics about a player
    
    Parameters
    ----------
    interestedPlayer (str): numerical player ID as stored by steam API information
    dataSummary (dataframe): dataframe of data compiled from match history information
    
    Returns nothing, but prints out:
        Average deaths per minute in losses
        Average deaths per minute in wins
        Win-loss record when playing with me
        Average game length of wins (with me)
        Average game length of losses (with me)
        Average KDA over all games as Blue player (player slot 0)
        Total number of deaths over all games as Pink player (player slot 128)
    
    '''
    
    tempDF = dataSummary.groupby(['Player ID', 'Win Y/N']).aggregate(sum)
    averageDPMinWin = float(tempDF.loc[interestedPlayer, 1]['Deaths'])/tempDF.loc[interestedPlayer, 1]['Match Length (s)'] * 60.0
    averageDPMinLoss = float(tempDF.loc[interestedPlayer, 0]['Deaths'])/tempDF.loc[interestedPlayer, 0]['Match Length (s)'] * 60.0
    averageWinLength = tempDF.loc[interestedPlayer, 1]['Match Length (s)']/tempDF.loc[interestedPlayer, 1]['Match Counter']
    averageLossLength = tempDF.loc[interestedPlayer, 0]['Match Length (s)']/tempDF.loc[interestedPlayer, 0]['Match Counter']
    
    tempDF2 = dataSummary.groupby(['Player ID', 'Player Slot']).aggregate(sum)
    blueKDA = (tempDF2.loc[interestedPlayer, 0]['Kills']+tempDF2.loc[interestedPlayer, 0]['Assists'])/tempDF2.loc[interestedPlayer, 0]['Deaths']
    pinkTotalDeaths = tempDF2.loc[interestedPlayer, 0]['Deaths']
    
    print('Player\'s ID: %s' % interestedPlayer)
    print('Player\'s win-loss when playing with you: ' + str(tempDF.loc[interestedPlayer,1]['Match Counter']) + '-' + str(tempDF.loc[interestedPlayer,0]['Match Counter']) + ' (' + str(tempDF.loc[interestedPlayer,1]['Match Counter']/(tempDF.loc[interestedPlayer,1]['Match Counter']+tempDF.loc[interestedPlayer,0]['Match Counter'])) + ')')
    print('Player\'s average deaths per minute in wins is %s over %s matches' % (averageDPMinWin, tempDF.loc[interestedPlayer, 1]['Match Counter']))
    print('Player\'s average deaths per minute in losses is %s over %s matches' % (averageDPMinLoss, tempDF.loc[interestedPlayer, 0]['Match Counter']))
    print('Player\'s average game length when winning with you: %s seconds' %averageWinLength)
    print('Player\'s average game length when losing with you: %s seconds' %averageLossLength)
    print('Player\'s average KDA as Blue: %s' % blueKDA)
    print('Player\'s total deaths as Pink: %s' % pinkTotalDeaths)

    return None

highestMatchPrior = 0
lowestMatchCurrent = 0

for x in range(0, 35):

    print "Loop # %d started" %(x)

    matchIDList = retrieve_match_IDs_by_game_type(key,22,3,0)
    matchIDListClone = matchIDList    #clone for iteration to remove duplicate games
    
    lowestMatchCurrent = int(matchIDList[-1])
    for matchNumber in matchIDListClone:
        if int(matchNumber) >= lowestMatchCurrent:
            if int(matchNumber) <= highestMatchPrior:
                matchIDList.remove(matchNumber)

    time.sleep(1)

    matchDetails = []
    for match in matchIDList:
        rTemp = requests.get('https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?match_id=%s&key=%s' % (match, key))
        if len(rTemp.text)>4000:         #sometimes API will fail and won't get the match, so no json to load and would unnecessarily stop the loop
            matchDetails.append(json.loads(rTemp.text))
        time.sleep(1.5)

    matchDetails[:] = [match for match in matchDetails if ('result' in match)]             #removes erroneous matches as some are special matches
    matchDetails[:] = [match for match in matchDetails if ('players' in match['result'])]  #without the same dictionary entrie

    with open('automatchdetails.txt', 'a') as text:                 #save raw json data so we don't have to call the API again for same data
        json.dump(matchDetails, text)

    with open('matchidlist.csv', 'a') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(matchIDList)
    
    highestMatchPrior = int(matchIDList[0])
    
    print "Loop # %d done, now sleeping" %(x)
    time.sleep(600)
