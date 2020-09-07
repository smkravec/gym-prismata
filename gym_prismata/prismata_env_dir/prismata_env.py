import sys
import gym
import prismataengine


class PrismataEnv(gym.Env):

    def __init__(self):
        self.gamestate = prismataengine.GameState()
        self.actions = prismataengine.Actions()
        self.randomcards = 0
        self.move = prismataengine.Move() 
        if __debug__:
            print('Environment initialized')
        
    def step(self, act_label): #Eats an integer labelling which of the actions to take
        action=self.take_action(act_label)
        if action.type() == prismataengine.ActionType.END_PHASE:
            self.move.clear()
            self.move.append(action)
            self.gamestate.doMove(self.move)
            if __debug__:
                print(f"Move Complete! Current State: {self.gamestate}")
        else:
            self.gamestate.doAction(action)
        self.actions.clear()
        self.gamestate.generateLegalActions(self.actions)
        if __debug__:
            print('Step successful!')
        return self.gamestate, self.actions
    
    def take_action(self, act_label): #Right now just checks legality, but can be extended
        action = self.actions[act_label]
        if not self.gamestate.isLegal(action):
            if __debug__:
                print(f"Action is illegal! Exiting")
            sys.exit(1)
        return action
    
    def reset(self):
        self.gamestate = prismataengine.GameState()
        self.gamestate.setStartingState(prismataengine.Players.Player_One, self.randomcards)
        self.gamestate.generateLegalActions(self.actions)
        if __debug__:
            print(f"Starting: {self.gamestate}")
        return self.gamestate, self.actions
