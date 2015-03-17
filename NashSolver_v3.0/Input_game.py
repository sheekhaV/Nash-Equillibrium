# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 10:00:59 2014

@author: Sheekha
"""
import sympy as sp
import numpy as np
import scipy as sc
import itertools as it
import gambit as gm
import PureStrategyNash as PN
#import MixedNashSolver_v3.0


###Reading from external file in gambit format
#g_external = gm.Game.read_game("/Users/Sheekha/Documents/Python/Project-Nash-Equlibrium/nfg_files/Prisoners_Dilemma-gambit")

#Adding a Prisoner's dilemma game
#=============================================================================
g_pd = gm.Game.new_table([3,3])

g_pd.title = "A prisoner's dilemma game"
g_pd.players[0].label = "P1"
g_pd.players[1].label = "P2"

#______________ Printing the game so far


#______________Printing the strategies
#g_pd.players[0].strategies

#Adding the payoffs
g_pd[0,0][0] = 1 #Payoff od P1 when action by both P1 and P2 are cooperate (0)
g_pd[0,0][1] = -1

g_pd[0,1][0] = -1 #Payoff when P2 defects
g_pd[0,1][1] = 1

g_pd[1,0][0] = -1 #Payoff when P1 defects
g_pd[1,0][1] = 1

g_pd[1,1][0] = 1 #Payoff when both defects
g_pd[1,1][1] = -1

g_pd[0,2][0]= -2
g_pd[0,2][1]= -2

g_pd[1,2][0]= -2
g_pd[1,2][1]= -2

g_pd[2,2][0]= -2
g_pd[2,2][1]= -2

g_pd[2,0][0]= -2
g_pd[2,0][1]= -2

g_pd[2,1][0]= -2
g_pd[2,1][1]= -2

#==============================================================================

game = len(g_pd.players[1].strategies)

print game
print g_pd

