import sys
import gym
from os import environ
# Only works with POSIX-style paths
environ["PRISMATA_INIT_AI_JSON_PATH"] = f"{'/'.join(__file__.split('/')[:-1])}/AI_config.txt"
import prismataengine
import random
import numpy as np


class PythonRandomPlayer(object):
    def getAction(self, gamestate):
        state = gamestate.toVector()
        actions = gamestate.getAbstractActions()
        # print(gamestate.getAbstractActionsVector())
        # print(actions)
        # print([action.json() for action in gamestate._actions])
        # print([str(p.ConcreteAction(gamestate, action)) for action in gamestate._actions])
        action = random.choice(actions)
        return action

"""Currently only works for SteelSplitterOnly set and BaseSet"""
class PrismataEnv(gym.Env):

    def __init__(self):
        if __debug__:
            print('Environment initialized')
            # print(f"Starting: {self.gamestate}")
        
    def step(self, actionOffset):
        action = self.gamestate.getAction(int(actionOffset))
        if __debug__:
            print(f'Action: {actionOffset} ({action})')
        self.gamestate.doAction(int(actionOffset))
        obs, legal, done = self.gamestate.toVector(), self.gamestate.getAbstractActionsVector(), self.gamestate.isGameOver()
        obs, legal, done = self.playOpponent(obs, legal, done)
        reward = self.getReward(obs, done)
        winner=self.gamestate.winner()
        return obs, legal, reward, done, winner
    
    def getReward(self, obs, done): 
        if __debug__:
            print('Calculating reward...')
        reward = np.dot(self.reward_hyper, obs)#Coefficient is an adjustable hyper
        winner=self.gamestate.winner()
        if done and winner == prismataengine.Players.One:
            reward+=1 #another arbitrary hyper
        elif done and winner == prismataengine.Players.Two:
            reward-=1 
        if __debug__:
            print(f'Reward calc successful ({reward})!')
        return reward
    
    def playOpponent(self, obs, legal, done):
        if self.gamestate.activePlayer == prismataengine.Players.Two:
            self.gamestate.step()
        return self.gamestate.toVector(), self.gamestate.getAbstractActionsVector(), self.gamestate.isGameOver()
    
    def reset(self, policy = 'Random', cards='4'):
        self.policy = policy
        self.cards = cards
        
        if policy == 'Random':
            self.player2 = PythonRandomPlayer()
        elif type(policy) == object and hasattr(policy, 'getAction'):
            self.player2 = self.policy
        else:
            self.player2 = self.policy
        if cards == '4':
            self.gamestate = prismataengine.GameState('''{
                 "whiteMana":"0HH",
                 "blackMana":"0HH",
                 "phase":"action",
                 "table":
                 [
                     {"cardName":"Drone", "color":0, "amount":6},
                     {"cardName":"Engineer", "color":0, "amount":2},
                     {"cardName":"Drone", "color":1, "amount":7},
                     {"cardName":"Engineer", "color":1, "amount":2}
                 ],
                 "cards":["Drone","Engineer","Blastforge","Steelsplitter"]
             }''',cards=4, player2=self.player2)
            #self.reward_hyper=np.array([0, 0,
            #                         1,  0,  1,  2,
            #                         3,  3,  3,  2,  1,  2,  4,  5,  5,  6,
            #                        -1,  0, -1, -2,
            #                        -3, -3, -3, -2, -1, -2, -4, -5, -5, -6])
            self.reward_hyper=np.zeros(30) #Add more hypers if you want, this is sparse
            self.observation_space = np.ndarray(30)
            self.action_space_dim = 14
        elif cards =='11':
            self.gamestate = prismataengine.GameState('''{
                 "whiteMana":"0HH",
                 "blackMana":"0HH",
                 "phase":"action",
                 "table":
                 [
                     {"cardName":"Drone", "color":0, "amount":6},
                     {"cardName":"Engineer", "color":0, "amount":2},
                     {"cardName":"Drone", "color":1, "amount":7},
                     {"cardName":"Engineer", "color":1, "amount":2}
                 ],
                 "cards":["Drone","Engineer","Blastforge","Animus", "Conduit", "Steelsplitter", "Wall", "Rhino", "Tarsier", "Forcefield", "Gauss Cannon"]
             }''',cards=11, player2=self.player2)
            self.reward_hyper=np.zeros(82) #Same as above
            self.observation_space = np.ndarray(82)
            self.action_space_dim = 32
        else:
            raise Error('Unknown Card Set')
        if __debug__:
            print(f"Starting: {self.gamestate}")
        return self.gamestate.toVector(), self.gamestate.getAbstractActionsVector()
