"""
Template for implementing QLearner
"""
import numpy as np
import random as rand

class QLearner(object):

    def author(self):
        return 'sbaek47'

    def __init__(self, \
        num_states = 100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):
        """
        @param num_states: integer, the number of states to consider
        @param num_actions: integer, the number of actions available.

        @param alpha: the learning rate
        @param gamma: the discount rate (value of future rewards)

        @param rar: random action rate: the probability of selecting a random action at each step. 0.0 (no random actions) to 1.0 (always random action)

        @param radr: random action decay rate, after each update, rar = rar * radr.
        0.0 (immediate decay to 0) and 1.0 (no decay)

        @param dyna: integer, conduct this number of dyna updates for each regular update.
        When Dyna is used, 200 is a typical value.
        """
        self.num_states = num_states
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.verbose = verbose

        self.Q = np.zeros((num_states, num_actions))

        if self.dyna > 0:
            self.R = -1 * np.ones((self.num_states, self.num_actions))
            self.Tc = np.ones((self.num_states, self.num_actions, self.num_states)) / 1000000
            self.T = self.Tc / self.Tc.sum(axis = 2, keepdims = True)

        self.count = 0
        self.s = 0
        self.a = 0

    def querysetstate(self, s):
        """
        @summary: Update the state without updating the Q-table
        @param s: The new state
        @returns: The selected action
        """
        self.s = s
        self.a = self.random_action()

        if self.verbose:
            print "s =", s,"a =", self.a

        return self.a

    def query(self, s_prime, r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: a real valued immediate reward
        @returns: The selected action
        """
        self.count += 1
        a_prime = np.argmax(self.Q[s_prime, :])

        self.Q[self.s, self.a] = (1 - self.alpha) * self.Q[self.s, self.a] + self.alpha * (r + self.gamma * self.Q[s_prime, a_prime])

#####################################################################
        #DYNA:
        if self.dyna > 0:
            self.Tc[self.s, self.a, s_prime] += 1
            self.T = self.Tc / self.Tc.sum(axis = 2, keepdims = True)
            self.R[self.s, self.a] = (1 - self.alpha) * self.R[self.s, self.a] + (self.alpha * r)
            dyna_state = np.random.random_integers(0, self.num_states - 1, self.dyna)
            dyna_action = np.random.random_integers(0, self.num_actions - 1, self.dyna)

        if self.dyna > 0 and self.count > 10:
            for i in range(self.dyna):
                new_state = np.random.multinomial(1, self.T[dyna_state[i],dyna_action[i],:]).argmax()
                reward = self.R[dyna_state[i], dyna_action[i]]
                a_prime = (self.Q[new_state, :]).argmax()

                self.Q[dyna_state[i], dyna_action[i]] = (1 - self.alpha) * self.Q[dyna_state[i], dyna_action[i]] + self.alpha * (reward + self.gamma * self.Q[new_state, a_prime])

#####################################################################
        self.s = s_prime
        self.a = self.random_action()

        if self.verbose:
            print "s =", s_prime,"a =",self.a,"r =",r

        self.rar = self.rar * self.radr

        return self.a
#####################################################################

    def random_action(self):
        randomAction = np.random.uniform(0,1) < self.rar

        if randomAction:
            self.a = np.random.randint(0, self.num_actions - 1)
        else:
            self.a = np.argmax(self.Q[self.s, :])
        return self.a

if __name__=="__main__":
    print "hi"
