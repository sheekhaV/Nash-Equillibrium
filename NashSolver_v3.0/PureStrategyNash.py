# -*- coding: utf-8 -*-
"""
Created on Fri Nov  7 17:30:21 2014

@author: Sheekha
"""

import gambit as gm
import numpy as np
import itertools as it
import pandas as pd

###Reading from external file in gambit format
g_external = gm.Game.read_game("/Users/Sheekha/Documents/Python/Project-Nash-Equlibrium/nfg_files/Chicken_game")

#Adding a Prisoner's dilemma game
#=============================================================================
g_pd = gm.Game.new_table([2,2])

g_pd.title = "A prisoner's dilemma game"
g_pd.players[0].label = "P1"
g_pd.players[1].label = "P2"

#______________ Printing the game so far
#g_pd

#Adding stratgies
g_pd.players[0].strategies

g_pd.players[0].strategies[0].label = "C"
g_pd.players[0].strategies[1].label = "D"

g_pd.players[1].strategies[0].label = "C"
g_pd.players[1].strategies[1].label = "D"

#______________Printing the strategies
g_pd.players[0].strategies

#Adding the payoffs
g_pd[0,0][0] = 8 #Payoff od P1 when action by both P1 and P2 are cooperate (0)
g_pd[0,0][1] = 8

g_pd[0,1][0] = 2 #Payoff when P2 defects
g_pd[0,1][1] = 10

g_pd[1,0][0] = 10 #Payoff when P1 defects
g_pd[1,0][1] = 2

g_pd[1,1][0] = 5 #Payoff when both defects
g_pd[1,1][1] = 5

#==============================================================================

#Generate action tuples
def generate_action_combinations(actions):
    return map(list, it.product(*actions))

#Generates strategies of a player from which he has incentive to deviate
def get_non_best_strategies(action_tuple, player_actions, player_index):
    max_response = game_NE[action_tuple][player_index]
    player_current_action = action_tuple[player_index]
    
    remaining_player_actions = player_actions[:]
    remaining_player_actions.remove(player_current_action)

    tuples_to_remove = []
    current_max_tuple = action_tuple

    for player_action in remaining_player_actions:
        new_tuple = action_tuple[:]
        new_tuple[player_index] = player_action
        response = game_NE[new_tuple][player_index]
        if response > max_response:
            tuples_to_remove.append(current_max_tuple)
            max_response = response
        elif max_response > response:
            tuples_to_remove.append(new_tuple)

    return tuples_to_remove

#generate a list of all strategies which can NOT be a nash equilibrium
def reduce_tuples(action_tuples, player_index, ActionIndexes):
    tuples_to_remove = []
    player_actions = ActionIndexes[player_index]
    
    for action_tuple in action_tuples:
        if action_tuple not in tuples_to_remove:
            tuples_to_remove += get_non_best_strategies(action_tuple, player_actions, player_index)

    return [item for item in action_tuples if item not in tuples_to_remove]


def get_nash_pure(game):
    # generates all combination of responses
    print game
    Players = len(game.players)
    ActionNum = [len(game.players[i].strategies) for i in range(Players)]
    ActionSet = pd.DataFrame()
    for x in range(Players):
        ActionSet[x] = pd.Series(list(game.players[x].strategies))
    ActionIndexes = [range(ActionNum[i]) for i in range(Players)]
    action_tuples = generate_action_combinations(ActionIndexes)
 
    ####reduces the set of possible actions that can be Nash Eq
    for player_index in range(Players):
        #action_tuples give the complete combination of actions
        action_tuples = reduce_tuples(action_tuples, player_index, ActionIndexes)
        #print action_tuples
    

    print "Pure Strategy Nash Equillibria are"
    print action_tuples

#Selecting game
#game_NE = g_external

#Defining Variables
#Players = len(game_NE.players)
#ActionNum = [len(game_NE.players[i].strategies) for i in range(Players)]
#ActionSet = pd.DataFrame()
#for x in range(Players):
#    ActionSet[x] = pd.Series(list(game_NE.players[x].strategies))
#ActionIndexes = [range(ActionNum[i]) for i in range(Players)]
#   
#get_nash_pure(game_NE)