import sys
import gym
import prismataengine


class PrismataEnv(gym.Env):

    def __init__(self):
        self.reset()
        if __debug__:
            print('Environment initialized')
        
    def step(self, act_label): #Eats an integer labelling which of the actions to take
        action = self.gamestate.do_action(act_label)
        if __debug__:
            print('Step successful!')
        return self.toVector(), self.gamestate.getAbstractActions()
    
    def reset(self):
        self.gamestate = prismataengine.GameState('''{
             "whiteMana":"0HH",
             "blackMana":"0",
             "phase":"action",
             "table":
             [
                 {"cardName":"Drone", "color":0, "amount":6},
                 {"cardName":"Engineer", "color":0, "amount":2},
                 {"cardName":"Drone", "color":1, "amount":7},
                 {"cardName":"Engineer", "color":1, "amount":2}
             ],
             "cards":["Drone","Engineer","Blastforge","Steelsplitter"]
         }''')
        if __debug__:
            print(f"Starting: {self.gamestate}")
