# -*- coding: utf-8 -*-


from __future__ import division
import numpy as np
import pandas as pd
import json
import math



def create_dota_dataframe2(matchDetailsList):
    
    '''
    Takes in list of match detail json strings and converts
    into a pandas dataframe for easier statistical manipulation
    
    This function uses 1 row for each match, recording only
    the information about the heroes on each team, the match outcome,
    the match ID number, and the length of the match. Information
    is to be used for modelling match outcomes based on drafts
    (the heroes present in the game)
    
    Inputs:
    matchDetailsList: list of JSONs
    
    Outputs:
    dataFrameSummary: a pandas dataframe
    '''

    radiant1 = []                 #initialize lists for stats of interest
    radiant2 = []
    radiant3 = []
    radiant4 = []
    radiant5 = []
    dire1 = []
    dire2 = []
    dire3 = []
    dire4 = []
    dire5 = []
    radiantWin = []
    matchID = []
    gameMode = []
    matchLength = []
    matchCounter = []
    gameStartTime = []


    for match in matchDetailsList:    #construct lists
        for player in match['result']['players']:
            
            if player['player_slot'] == 0:
                radiant1.append(player['hero_id'])
            if player['player_slot'] == 1:
                radiant2.append(player['hero_id'])    
            if player['player_slot'] == 2:
                radiant3.append(player['hero_id'])    
            if player['player_slot'] == 3:
                radiant4.append(player['hero_id'])
            if player['player_slot'] == 4:
                radiant5.append(player['hero_id'])
            if player['player_slot'] == 128:
                dire1.append(player['hero_id'])
            if player['player_slot'] == 129:
                dire2.append(player['hero_id'])    
            if player['player_slot'] == 130:
                dire3.append(player['hero_id'])                
            if player['player_slot'] == 131:
                dire4.append(player['hero_id'])                
            if player['player_slot'] == 132:
                dire5.append(player['hero_id'])                
        #endplayerloop    
        radiantWin.append(match['result']['radiant_win'])
        matchID.append(match['result']['match_id'])
        gameMode.append(match['result']['game_mode'])
        matchLength.append(match['result']['duration'])
        matchCounter.append(1)
        gameStartTime.append(match['result']['start_time'])
                
    #construct dictionary to build data frame
    referenceDict = {'Radiant 1': radiant1, 'Radiant 2': radiant2, 'Radiant 3': radiant3, 'Radiant 4': radiant4, 'Radiant 5': radiant5, 'Dire 1': dire1, 'Dire 2': dire2, 'Dire 3': dire3, 'Dire 4': dire4, 'Dire 5': dire5, 'Radiant Win Y/N': radiantWin, 'Match ID': matchID, 'Game Mode': gameMode, 'Match Length (s)': matchLength, 'Match Counter': matchCounter, 'Game Start Time': gameStartTime}
    dataFrameSummary = pd.DataFrame(data=referenceDict)
    
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Radiant 1']!=0]  #eliminate matches where a player did not pick a hero
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Radiant 2']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Radiant 3']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Radiant 4']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Radiant 5']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Dire 1']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Dire 2']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Dire 3']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Dire 4']!=0]
    dataFrameSummary = dataFrameSummary[dataFrameSummary['Dire 5']!=0]

    return dataFrameSummary


def create_dota_dataframe(matchDetailsList):
    
    '''
    Takes in list of match detail json strings and converts
    into a pandas dataframe for easier statistical manipulation
    
    1 row per player (10 rows per match); records most
    information retrievable from Steam API information, except
    item and ability information
    
    Inputs:
    matchDetailsList: list of JSONs
    
    Outputs:
    dataFrameSummary: a pandas dataframe
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
    isRadiant = []

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
            if player['player_slot'] <= 4 and match['result']['radiant_win'] == True:
                gameWonStatus.append(1)
            elif player['player_slot'] >= 128 and match['result']['radiant_win'] == False:
                gameWonStatus.append(1)
            else:
                gameWonStatus.append(0)
            matchID.append(match['result']['match_id'])
            matchLength.append(match['result']['duration'])
            matchCounter.append(1)
            gameStartTime.append(match['result']['start_time'])
            if player['player_slot'] <= 4:
                isRadiant.append(1)
            else:
                isRadiant.append(0)
                
    #construct dictionary to build data frame
    referenceDict = {'Player ID': playerID, 'Player Slot': playerSlot, 'Kills': playerKills, 'Deaths': playerDeaths, 'Assists': playerAssists, 'GPM': playerGPM, 'XPM': playerXPM, 'Hero Damage': playerHeroDamage, 'Tower Damage': playerTowerDamage, 'Level': playerLevel, 'Hero ID': playerHeroID, 'Win Y/N': gameWonStatus, 'Match ID': matchID, 'Match Length (s)': matchLength, 'Match Counter': matchCounter, 'Game Start Time': gameStartTime, 'Radiant Y/N': isRadiant}
    dataFrameSummary = pd.DataFrame(data=referenceDict)

    return dataFrameSummary


def getWinRateArray(dataFrame):
    
    '''
    From a dataframe of match information constructed using
    create_dota_dataframe2(), creates and populates two 2D
    arrays consisting of win rate information (single hero
    and pairwise) and match sample size information (single
    hero and pairwise).
    
    Inputs:
    dataFrame: a pandas dataframe with columns 'Radiant #'
    and 'Dire #', where # is in [0-4].
    
    Outputs:
    winRateArray: 2D array (technically a list of lists of floats)
    matchCountArray: 2D array (list of lists of floats)
    
    
    '''
    
    heroIDs = range(0,114)
    heroIDs.remove(24)
    heroIDs.remove(108)
    
    heroIDLength = 114
    thirdDimLength = 2
    
    numberMatchesAndWins = [[[0 for k in xrange(2)] for j in xrange(114)] for i in xrange(114)]
    winRateArray = [[0 for j in xrange(114)] for i in xrange(114)]
    matchCountArray = [[0 for j in xrange(114)] for i in xrange(114)]
    
    for index, row in dataFrame.iterrows():
        
        radiantHeroList = [row['Radiant 1'], row['Radiant 2'], row['Radiant 3'], row['Radiant 4'], row['Radiant 5']]
        direHeroList = [row['Dire 1'], row['Dire 2'], row['Dire 3'], row['Dire 4'], row['Dire 5']]
        
        for hero in radiantHeroList:
            for hero2 in radiantHeroList:            #number of matches for hero-pair
                numberMatchesAndWins[int(hero)][int(hero2)][0] = numberMatchesAndWins[int(hero)][int(hero2)][0] + 1
                if row['Radiant Win Y/N'] == True:   #number of wins for hero-pair
                    numberMatchesAndWins[int(hero)][int(hero2)][1] = numberMatchesAndWins[int(hero)][int(hero2)][1] + 1
        for hero in direHeroList:
            for hero2 in direHeroList:               #number of matches for hero-pair
                numberMatchesAndWins[int(hero)][int(hero2)][0] = numberMatchesAndWins[int(hero)][int(hero2)][0] + 1
                if row['Radiant Win Y/N'] == False:  #number of wins for hero-pair
                    numberMatchesAndWins[int(hero)][int(hero2)][1] = numberMatchesAndWins[int(hero)][int(hero2)][1] + 1
                    
    for i in heroIDs:
        for j in heroIDs:
            if numberMatchesAndWins[i][j][0] != 0:
                winRateArray[i][j] = numberMatchesAndWins[i][j][1]/numberMatchesAndWins[i][j][0]
            else:
                winRateArray[i][j] = -1             #for small sample sizes where some hero combinations aren't recorded
                                                    #record effectively no combined winrate; will not be factored in synergy
            matchCountArray[i][j] = numberMatchesAndWins[i][j][0]
                
    return winRateArray, matchCountArray

def getSynergyFactor(teamHeroArray, winRateArray, mcArray, tuning):
    
    '''
    Takes in input arrays and returns a value that quantifying the quality of the composition
    of the team based on win rates in past games of heroes individually and pairs of heroes
    on the team
    
    Inputs:
    teamHeroArray (list): List of 5 heroes on the same team
    winRateArray: 2d array of pair-wise winrates retrieved from getWinRateArray()
    mcArray: 2d array of pair-wise match counts retrieved from getWinRateArray()
    tuning: b/a factor for mathematical model determining team synergy; for same b/a, different b and a return same results
            tuning = 1 means weigh individual winrates equally with pairwise win rates
                (factor of 1/2 in calculations below is due to counting both wr_ij and wr_ji, effectively double counting)
    
    Output:
    synergyFactor (float): number between 0 and 1; higher number means better team synergy
    
    '''
    synergyNumerator = 0
    synergyDivider = 0
    
    for hero in teamHeroArray:
        for hero2 in teamHeroArray:
            if mcArray[hero][hero2] > 0:    #if no matches recorded for hero pairing, hero pair is not factored in
                if hero == hero2:
                    synergyNumerator = synergyNumerator + winRateArray[hero][hero2]*math.log(mcArray[hero][hero2])
                    synergyDivider = synergyDivider + math.log(mcArray[hero][hero2])  
                else:
                    synergyNumerator = synergyNumerator + winRateArray[hero][hero2]*(tuning/2)*math.log(mcArray[hero][hero2])
                    synergyDivider = synergyDivider + (tuning/2)*math.log(mcArray[hero][hero2])
    
    synergyFactor = synergyNumerator/synergyDivider
    
    return synergyFactor



def predictWinRate(testDataFrame, wrArray, matchCountArray, tuning):

    '''
    Takes in dataframe and input arrays, calculates synergy factors for both teams in each
    match and predicts the winner for each match in the dataframe.
    
    Inputs:
    testDataFrame (dataframe): Dataframe of matches from create_dota_dataframe2()
    winRateArray: 2d array of pair-wise winrates retrieved from getWinRateArray()
    mcArray: 2d array of pair-wise match counts retrieved from getWinRateArray()
    tuning: b/a factor for mathematical model determining team synergy; for same b/a, different b and a return same results
            tuning = 1 means weigh individual winrates equally with pairwise win rates
                (factor of 1/2 in calculations below is due to counting both wr_ij and wr_ji, effectively double counting)
    
    Output:
    percentCorrect (float): Percentage of matches predicted correctly using model
        
    '''


    numberPredictions = 0
    correctPredictions = 0
    highestSynergyFactor = 0
    highestSynergyFactorTeam = [0,0,0,0,0]
    
    for index, row in testDataFrame.iterrows():
        
        radiantHeroList = [row['Radiant 1'], row['Radiant 2'], row['Radiant 3'], row['Radiant 4'], row['Radiant 5']]
        direHeroList = [row['Dire 1'], row['Dire 2'], row['Dire 3'], row['Dire 4'], row['Dire 5']]
        
        radiantSynergy = getSynergyFactor(radiantHeroList, wrArray, matchCountArray, tuning)
        direSynergy = getSynergyFactor(direHeroList, wrArray, matchCountArray, tuning)
        
        if radiantSynergy > direSynergy:
            predictedRadiantWin = 1
            if radiantSynergy > highestSynergyFactor:
                highestSynergyFactor = radiantSynergy
                highestSynergyFactorTeam = radiantHeroList
        elif direSynergy > radiantSynergy:
            predictedRadiantWin = 0
            if direSynergy > highestSynergyFactor:
                highestSynergyFactor = radiantSynergy
                highestSynergyFactorTeam = radiantHeroList                
        else:
            predictedRadiantWin = 0.5
            print("Equal synergies???????")
    
            
        if predictedRadiantWin == 1:
            if row['Radiant Win Y/N'] == True:
                correctPredictions = correctPredictions + 1
        
        if predictedRadiantWin == 0:
            if row['Radiant Win Y/N'] == False:
                correctPredictions = correctPredictions + 1
                
        numberPredictions = numberPredictions + 1
        
    percentCorrect = correctPredictions/numberPredictions
    
    return percentCorrect


def getWinRateOpposingTeamArray(dataFrame):
    
    '''
    From a dataframe of match information constructed using
    create_dota_dataframe2(), creates and populates two 2D
    arrays consisting of win rate information when heroes are
    on opposing teams as well as match sample size information.
    
    Inputs:
    dataFrame: a pandas dataframe with columns 'Radiant #'
    and 'Dire #', where # is in [0-4].
    
    Outputs:
    winRateArray: 2D array (technically a list of lists of floats)
    matchCountArray: 2D array (list of lists of floats)
    
    
    ''' 
    
    heroIDs = range(0,114)
    heroIDs.remove(24)
    heroIDs.remove(108)
    
    heroIDLength = 114
    thirdDimLength = 2
    
    numberMatchesAndWins = [[[0 for k in xrange(2)] for j in xrange(114)] for i in xrange(114)]
    winRateArray = [[0 for j in xrange(114)] for i in xrange(114)]
    matchCountArray = [[0 for j in xrange(114)] for i in xrange(114)]
    
    for index, row in dataFrame.iterrows():
        
        radiantHeroList = [row['Radiant 1'], row['Radiant 2'], row['Radiant 3'], row['Radiant 4'], row['Radiant 5']]
        direHeroList = [row['Dire 1'], row['Dire 2'], row['Dire 3'], row['Dire 4'], row['Dire 5']]
        
        for hero in radiantHeroList:
            for hero2 in direHeroList:               #number of matches for hero-pair
                numberMatchesAndWins[int(hero)][int(hero2)][0] = numberMatchesAndWins[int(hero)][int(hero2)][0] + 1    
                if row['Radiant Win Y/N'] == True:   #number of wins for hero-pair
                    numberMatchesAndWins[int(hero)][int(hero2)][1] = numberMatchesAndWins[int(hero)][int(hero2)][1] + 1    
        for hero in direHeroList:
            for hero2 in radiantHeroList:            #number of matches for hero-pair
                numberMatchesAndWins[int(hero)][int(hero2)][0] = numberMatchesAndWins[int(hero)][int(hero2)][0] + 1    
                if row['Radiant Win Y/N'] == False:  #number of wins for hero-pair
                    numberMatchesAndWins[int(hero)][int(hero2)][1] = numberMatchesAndWins[int(hero)][int(hero2)][1] + 1   
                    
    for i in heroIDs:
        for j in heroIDs:
            if numberMatchesAndWins[i][j][0] != 0:
                winRateArray[i][j] = numberMatchesAndWins[i][j][1]/numberMatchesAndWins[i][j][0]
            else:
                winRateArray[i][j] = -1
            
            matchCountArray[i][j] = numberMatchesAndWins[i][j][0]
                
    return winRateArray, matchCountArray

def getAdvantageFactor(radHeroArray, direHeroArray, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, tuning=1):

    '''
    Takes in input arrays and returns a value that decides the advantage that the Radiant team
    has based on how their heroes have fared against Dire heroes in past games.
    
    Inputs:
    teamHeroArray (list): List of 5 heroes on the same team
    winRateArray: 2d array of pair-wise winrates retrieved from getWinRateArray()
    mcArray: 2d array of pair-wise match counts retrieved from getWinRateArray()
    wrOpposingTeamArray: 2d array of opposite team winrates from getWinRateOpposingTeamArray()
    mcOpposingTeamArray: 2d array of opposite team match counts from getWinRateOpposingTeamArray()
    tuning: Changes the amount of impact advantage factors have on results
            For tuning = 1, radiantAdvantage = 1 - DireAdvantage (e.g. 0.55, 0.45)
            For tuning = x, adjRadiantAdvantage = radiantAdvantage^x, wat if direAdv goes negative ._.
    
    '''
    advantageNumerator = 0
    advantageDivider = 0
    
    for rad in radHeroArray:
        for dire in direHeroArray:
            if mcOpposingTeamArray[rad][dire] > 0:    #if no matches recorded for hero pairing, hero pair is not factored in
                wrDiff = wrOpposingTeamArray[rad][dire] - (wrArray[rad][rad] - wrArray[dire][dire])
                advantageNumerator = advantageNumerator + wrDiff*math.log(mcOpposingTeamArray[rad][dire])
                advantageDivider = advantageDivider + math.log(mcOpposingTeamArray[rad][dire])
    
    advantageFactor = advantageNumerator/advantageDivider
    
    #Tuning factor up means advantageFactor weighs more in following prediction calculations
    advantageFactor = advantageFactor**tuning
    
    return advantageFactor



def predictWinRateRefined(testDataFrame, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, b, c):

    '''
    Takes in dataframe and input arrays, calculates synergy factors for both teams in each
    match and predicts the winner for each match in the dataframe.
    
    Inputs:
    testDataFrame (dataframe): Dataframe of matches from create_dota_dataframe2()
    winRateArray: 2d array of pair-wise winrates retrieved from getWinRateArray()
    mcArray: 2d array of pair-wise match counts retrieved from getWinRateArray()
    wrOpposingTeamArray: 2d array of opposite team winrates from getWinRateOpposingTeamArray()
    mcOpposingTeamArray: 2d array of opposite team match counts from getWinRateOpposingTeamArray()
    b: b/a factor for mathematical model determining team synergy; for same b/a, different b and a return same results
            tuning = 1 means weigh individual winrates equally with pairwise win rates
                (factor of 1/2 in calculations below is due to counting both wr_ij and wr_ji, effectively double counting)
    c: c factor for mathematical model determining team advantage
    
    Output:
    percentCorrect (float): Percentage of matches predicted correctly using model
    '''

    numberPredictions = 0
    correctPredictions = 0

    
    for index, row in testDataFrame.iterrows():
        
        radiantList = [row['Radiant 1'], row['Radiant 2'], row['Radiant 3'], row['Radiant 4'], row['Radiant 5']]
        direList = [row['Dire 1'], row['Dire 2'], row['Dire 3'], row['Dire 4'], row['Dire 5']]
     
        radiantSynergy = getSynergyFactor(radiantList, wrArray, mcArray, b)
        radiantAdvantage = getAdvantageFactor(radiantList, direList, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, c)
        direSynergy = getSynergyFactor(direList, wrArray, mcArray, b)
        direAdvantage = getAdvantageFactor(direList, radiantList, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, c)
        
        if radiantSynergy*radiantAdvantage > direSynergy*direAdvantage:
            predictedRadiantWin = 1

        elif direSynergy*direAdvantage > radiantSynergy*radiantAdvantage:
            predictedRadiantWin = 0
        
        else:
            predictedRadiantWin = 0.5
            print("Equal synergies???????")
    
            
        if predictedRadiantWin == 1:
            if row['Radiant Win Y/N'] == True:
                correctPredictions = correctPredictions + 1
        
        if predictedRadiantWin == 0:
            if row['Radiant Win Y/N'] == False:
                correctPredictions = correctPredictions + 1
                
        numberPredictions = numberPredictions + 1
        
    percentCorrect = correctPredictions/numberPredictions
    
    return percentCorrect




def suggestHero(yourTeam, enemyTeam, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, heroDict, b=1, c=1):
    
    '''
    Suggests top three potential hero choices to give your team an advantage
    against the enemy team depending on team compositions.
    
    Inputs:
    yourTeam: list of heroes currently on your team
    enemyTeam: list of heroes currently on the enemy team
    winRateArray: 2d array of pair-wise winrates retrieved from getWinRateArray()
    mcArray: 2d array of pair-wise match counts retrieved from getWinRateArray()
    wrOpposingTeamArray: 2d array of opposite team winrates from getWinRateOpposingTeamArray()
    mcOpposingTeamArray: 2d array of opposite team match counts from getWinRateOpposingTeamArray()
    b: b/a factor for mathematical model determining team synergy; for same b/a, different b and a return same results
            tuning = 1 means weigh individual winrates equally with pairwise win rates
                (factor of 1/2 in calculations below is due to counting both wr_ij and wr_ji, effectively double counting)
    c: c factor for mathematical model determining team advantage
    heroDict: dict corresponding hero IDs to hero names. 111 heroes from 1 to 113,
              excluding 24 and 108 (IDs currently unused in game)    
    
    '''
    
    
    recommendedHero = [[0,0]]
    heroIDList = range(1,114)
    heroIDList.remove(24)     #no hero by ID 24
    heroIDList.remove(108)    #no hero by ID 108
    
    for hero in heroIDList:
        
        yourPotentialTeam = yourTeam + [hero]
        yourSynergy = getSynergyFactor(yourPotentialTeam, wrArray, mcArray, b)
        yourAdvantage = getAdvantageFactor(yourPotentialTeam, enemyTeam, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, c)
        enemySynergy = getSynergyFactor(enemyTeam, wrArray, mcArray, b)
        direAdvantage = getAdvantageFactor(enemyTeam, yourPotentialTeam, wrArray, mcArray, wrOpposingTeamArray, mcOpposingTeamArray, c)
        
        recommendedHero.append([yourSynergy*yourAdvantage, hero])

    
    yourTeamNames = []
    for hero in yourTeam:
        yourTeamNames.append(heroDict[str(hero)])
    enemyTeamNames = []
    for hero in enemyTeam:
        enemyTeamNames.append(heroDict[str(hero)])
    
    recommendedHero.sort(key=lambda x: -x[0])
    topHero = heroDict[str(recommendedHero[0][1])]
    topHero2 = heroDict[str(recommendedHero[1][1])]
    topHero3 = heroDict[str(recommendedHero[2][1])]
    
    print("Your team: %s") %(", ".join(yourTeamNames))
    print("Enemy team: %s") %(", ".join(enemyTeamNames))
    print("Top 3 recommended heroes: %s, %s, %s") %(topHero, topHero2, topHero3)

    
    recommendedHeroIDs = [recommendedHero[0][1], recommendedHero[1][1], recommendedHero[2][1]]
    
    return recommendedHeroIDs

