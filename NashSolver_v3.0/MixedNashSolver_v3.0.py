# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 12:24:55 2014
@author: Sheekha
"""

import sympy as sp
import numpy as np
import scipy as sc
import itertools as it
import gambit as gm
import PureStrategyNash as PN

#Generates combination of all actions from the list of action of each player
#The array actions = [[0,1], [0,1,2]] denotes player1's actions are [0,1] and player2's actions are [0,1,2]
def generate_action_combinations(actions):
    return map(list, it.product(*actions))

# Generate action conbinations for all players given a player index
def generate_remaining_player_action_combination (actions, player_index, player_action):
    temp_actions = actions[:]
    final_actions = [x for x in temp_actions if x[player_index] == player_action]
    return final_actions


#Generates support for each players
def generate_support_each_player(actions):
    support = []
    for i in xrange(1, len(actions)+1):
        support += [list(x) for x in it.combinations(actions, i)]
    return support


# Genenerate actions sets for all players given a support
def generate_action_indices_from_support(support):
    transposed = zip(*support)
    used_player_actions = [list(set(x)) for x in transposed]
    return used_player_actions

# Get all action sets not there in the support
def get_missing_action_sets(action_sets, original_action_sets):
    unused_actions = [[] for x in players]
    used_player_actions = zip(*action_sets)
    for x in range(len(original_action_sets)):
        original_action_set = original_action_sets[x]
        used_action_set = used_player_actions[x]
        unused_actions[x] = [item for item in original_action_set if item not in used_action_set]
    return unused_actions

# Generate all player payoffs given a solution
def generate_payoffs(support, solution):
    symbols = sp.symarray('p', (players_count, max(all_action_counts)))
    payoffs = [0 for x in players]

    for pindex in range(players_count):
        player_action = support[0][pindex]
        player_filtered_sets = [x for x in support if x[pindex] == player_action]
        for action_set in player_filtered_sets:
            prod = 1
            for pcount in action_set:
                if pcount != pindex:
                    prod *= solution[symbols[pcount, action_set[pcount]]]
            payoffs[pindex] += game[action_set][pindex]*prod

    return payoffs

# Generates a payoff for a player for his actions not in the support, 
# assuming the actions of all other players are S(-i) with the calculated probabilities
def generate_payoff_for_player(support, solution, pindex, action_substitute):
    payoff = 0
    player_action = support[0][pindex]
    player_filtered_sets = [x for x in support if x[pindex] == player_action]
    for action_set in player_filtered_sets:
        prod = 1
        for pcount in action_set:
            if pcount != pindex:
                prod *= solution[symbols[pcount, action_set[pcount]]]

        set_to_check = action_set[:]
        set_to_check[pindex] = action_substitute
        payoff += game[set_to_check][pindex]*prod

    return payoff

# No player should have a better stratgey outside the support
# Returns Trues if the payoff is maximum for the given support
def check_support_payoff(payoffs, support, solution):
    missing_actions = get_missing_action_sets(support, all_action_indices)

    for player_index in range(len(missing_actions)):
        missing_action_set = missing_actions[player_index]

        for action in missing_action_set:
                payoff = generate_payoff_for_player(support, solution, player_index, action)
                if payoff > payoffs[player_index]:
                    return False

    return True

# Applies the constraint 0<= probability <= 1
def is_solution_feasible(support, solution):
    for key in solution:
        if solution[key] < 0 or solution[key] > 1:
            return False
    payoffs = generate_payoffs(support, solution)
    return check_support_payoff(payoffs, support, solution)


# Find mixed startegy equillibrium for the game
def solve_mixed_nash():
    
    #generates a set of all possible combinations of actions for every player
    possible_actions_all_players= []

    for player_index in range(players_count):
        possible_actions_all_players += [generate_support_each_player(all_action_indices[player_index])]

    #generates all sets of action tuples for every support
    population_set = generate_action_combinations(possible_actions_all_players)

    # generate all combination of support that will support randomization 
    possible_support_action = []
    for i in range(len(population_set)):
        if len(generate_action_combinations(population_set[i])) > 3:
            possible_support_action.append(generate_action_combinations(population_set[i]))

    support_action_count = len(possible_support_action)

    #generate payoffs and probability set for each support
    for each_support in range(support_action_count):        
        
        #action indices defines the new possible action set for each player, given a support
        action_indices = possible_support_action[each_support]
        
        

        #number of actions over which each player is randomizing
        action_counts = [len(action_indices[i]) for i in range(len(action_indices))]

        #sympy matrix of variables that store probaility variables as "p_0_1" 
        #p_0_2 - indicates probability of player[0] and action[2]
        player_probaility_list = sp.symarray('p', (players_count, max(action_counts)))

        #To solve the sympy equation, the variables should be listed in a 1-D array and not a matrix
        list_of_variables = []

        for iterator in xrange(players_count):
            list_of_variables += [player_probaility_list[iterator, i] for i in range(max(action_counts))]

        ###initializing the set of equations
        set_of_equations = []

        ###Generating payoff equations for each player
        for player_index in range(players_count):

            generating_each_player_equations = []

            for player_action_index in range(action_counts[player_index]):

                #for every player action of each player, calculates the pay-off
                remaining_player_action_set = generate_remaining_player_action_combination(action_indices, player_index, player_action_index)

                pay_off_after_randomizing = 0

                for other_action_combination in range(len(remaining_player_action_set)):

                    #for each action tuple of the other players
                    current_action_set = remaining_player_action_set[other_action_combination]

                    payoff_current_action_set = game[current_action_set][player_index]


                    for counter in range(players_count):
                        if counter != player_index:
                            probability = player_probaility_list[counter, current_action_set[counter]]
                            payoff_current_action_set *= probability

                    pay_off_after_randomizing += payoff_current_action_set

                generating_each_player_equations.append(pay_off_after_randomizing)

            #generating equations for each player - payoff of a player will the same for all his
            # strategies if he is randomizing over all
            for i in range(action_counts[player_index] - 1):
                set_of_equations += [generating_each_player_equations[i] - generating_each_player_equations[i+1] ]

            #Adding the sum of probabilities to the set of equations
            set_of_equations += [sum(player_probaility_list[player_index, i] for i in range(action_counts[player_index])) - 1]

        #As the number of equation = number of unknowns, this gives a solution
        #We'll now check wether this solution generates the maximum payoff or not
        solution = sp.solve(set_of_equations,list_of_variables)
        is_support_feasible = is_solution_feasible(action_indices, solution)

        if is_support_feasible:
            print "Found a Mixed Strategy Nash Equillibrium"
            print solution


# Reading the game from an input file with game specified in gamut format
#game = gm.Game.read_game("/Users/Sheekha/Documents/Python/Project-Nash-Equlibrium/nfg_files/CoordinationGames_2players")
#game = gm.Game.read_game("/Users/Sheekha/Documents/Python/Project-Nash-Equlibrium/nfg_files/Prisoners_Dilemma-gambit")

game = gm.Game.read_game("/Users/Sheekha/Documents/Python/Project-Nash-Equlibrium/nfg_files/Chicken_game")

#Adding a Prisoner's dilemma game
#=============================================================================

players = game.players
players_count = len(players) #number of players

all_action_indices = [] #action set of all players
all_action_counts = [len(game.players[i].strategies) for i in range(players_count)]
all_action_indices = [range(all_action_counts[i]) for i in range(players_count)]

# Solve mixed
#solve_mixed_nash()
PN.get_nash_pure(game)
