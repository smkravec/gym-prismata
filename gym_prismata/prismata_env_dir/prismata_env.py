import sys
import gym
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

"""Currently only works for SteelSplitterOnly set"""
class PrismataEnv(gym.Env):

    def __init__(self):
        self.reward_hyper=np.array([0, 0, 1, 0, 1, 2, 3, 3, 3, 2, 1, 2, 4, 5, 5, 6, 0, 0, -1, -2, -3, -3, -3, -2, -1, -2, -4, -5, -5, -6])
        self.observation_space = np.ndarray(30)
        self.action_space_dim = 14
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
        return obs, legal, reward, done
    
    def getReward(self, obs, done): 
        if __debug__:
            print('Calculating reward...')
        reward = (.001)*np.dot(self.reward_hyper, obs)
        if done and self.gamestate.winner() == prismataengine.Players.One:
            reward+=1000 #another arbitrary hyper
        elif done and self.gamestate.winner() == prismataengine.Players.Two:
            reward-=1000 
        if __debug__:
            print(f'Reward calc successful ({reward})!')
        return reward
    
    def playOpponent(self, obs, legal, done):
        if self.gamestate.activePlayer == prismataengine.Players.Two:
            self.gamestate.step()
        return self.gamestate.toVector(), self.gamestate.getAbstractActionsVector(), self.gamestate.isGameOver()
    
    def reset(self, policy = 'Random'):
        self.policy = policy
        if policy == 'Random':
            self.player2 = PythonRandomPlayer()
        elif type(policy) == object and hasattr(policy, 'getAction'):
            self.player2 = self.policy
        else:
            raise Error('Unknown policy provided')
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
         }''', player2=self.player2)
        if __debug__:
            print(f"Starting: {self.gamestate}")
        return self.gamestate.toVector(), self.gamestate.getAbstractActionsVector()
