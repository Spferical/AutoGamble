#!/usr/bin/python
import random
import math
import shelve
import os

#initialize constants
STARTING_AMOUNT = 1000
MAX_BETS = 10000
#ROUND_LIMIT = 500000
ROUND_LIMIT = 5000
#whether or not to give verbose terminal output for each round of gambling
#note: with short rounds, terminal output becomes a significant bottleneck
# also, with short rounds, the information flashes on the screen too quickly
# to be of use.
VERBOSE = False
#whether or not to graph each round
#note: this can use up a lot of memory if MAX_BETS is a very high number
GRAPHING = False

#matplotlib is needed only if we are graphing each round
if GRAPHING:
    import matplotlib.pyplot as plt

#the fibonacci strategy uses the fibonacci sequence, so calculate it
if VERBOSE:
    print 'calculating fibonacci sequence'
#the first two numbers are both ones
fibonacci_sequence = [1, 1]
for i in range(500): #500 should be a safe place which no gambler will reach
    #each term is the two previous terms added together, a + b
    a = fibonacci_sequence[-2]
    b = fibonacci_sequence[-1]
    fibonacci_sequence.append(a + b)
if VERBOSE:
    print 'done calculating fibonacci sequence'

class Round:
    """Stores the variables of a round of gambling"""
    def __init__(self, strategy, max_amount, wins, losses, turns_lasted,
                losing_streaks, starting_bet, starting_amount,
                end_amount):
        self.strategy = strategy
        self.max_amount = max_amount
        self.wins = wins
        self.losses = losses
        self.turns_lasted = turns_lasted
        self.losing_streaks = losing_streaks
        self.starting_bet = starting_bet
        self.starting_amount = starting_amount
        self.end_amount = end_amount

class Gambler:
    """Simulates one round of gambling.
    The update_bet method is overriden by different strategies"""
    money = STARTING_AMOUNT
    starting_amount = money
    bet = 1 # 1 betting unit
    starting_bet = 1 # used by some strategies
    strategy = 'flat' # the default update_bet strategy is flat betting

    def update_bet(self, win):
        #in flat betting, bet does not change
        pass

    def gamble(self):
        #output to terminal the strategy used and the round number
        print 'gambling, using ' + self.strategy + ', round number ' + \
                str(len(rounds_list) + 1)
        bet_number = 0
        max_money = 0
        wins = 0
        losses = 0
        #this class also handles graphing and updating the graph's index
        if GRAPHING:
            global figindex
            #if graphing, the money the gambler has is stored in this list
            #after each bet, which is graphed at the end
            moneyovertime = []
        unfortunate_losing_streaks = 0
        i = 0
        while i < MAX_BETS:
            i += 1
            if GRAPHING:
                #append current money amount to moneyovertime
                #this is used only for graphing
                moneyovertime.append(self.money)
            #if gambler is out of money, end early
            if self.money == 0:
                break
            #track the maximum money achieved
            #if current money is higher, increase the max_money accordingly
            if self.money > max_money:
                max_money = self.money
            #gambler can't bet more than he has, can he?
            if self.bet > self.money:
                #if he is trying to, just make him bet all of his money
                self.bet = self.money
                #unfortunate losing streak: each time gambler bets all money
                unfortunate_losing_streaks += 1
            #there is 50% chance of winning; flip a coin
            win = random.getrandbits(1)
            if win:
                #gambler has won! track the number of wins
                wins += 1
                #and give him his money
                self.money += self.bet
            else:
                #gambler has lost! track the number of losses
                losses += 1
                #and take money from him
                self.money -= self.bet
            #finally, update the gambler's bet based on if he won
            self.update_bet(win)
            #bet must always be over 0, if not, there is an error
            assert self.bet > 0
        if VERBOSE:
            #lots of terminal output of verbose mode is on
            print "WINS=", wins
            print "LOSSES=", losses
            print "MAX=", max_money
            print "TURNS LASTED=", i
            print "UNFORTUNATE LOSING STREAKS=", unfortunate_losing_streaks
            print 'END AMOUNT=', self.money
        #add the tracked data to the rounds list
        rounds_list.append(
            Round(self.strategy, max_money, wins, losses, i, 
                  unfortunate_losing_streaks,
                  gambler.starting_bet, self.starting_amount, self.money)
            )
        if GRAPHING:
            #if graphing, plot the graph of moneyovertime
            print 'plotting the graph...'
            plt.plot(moneyovertime)
            #money is the Y variable
            plt.ylabel("Money")
            #number of gambles is the X variable
            plt.xlabel("Gambles")
            #the graph goes from 0 to the maximum money achieved
            plt.ylim(0,max_money)
            #finally, save the graph
            plt.savefig(graph_dir + str(figindex))
            #increase the index of the graph
            figindex += 1
            #clear the current figure
            plt.clf()
            print 'done\n'


class FibonacciGambler(Gambler):
    fib_position = 0
    strategy = 'fibonacci'
    def update_bet(self, win):
        if win:
            self.fib_position = max(self.fib_position - 2, 0)
        else:
            self.fib_position += 1
        self.bet = fibonacci_sequence[self.fib_position]


class ProgressiveFibonacciGambler(Gambler):
    fib_position = 0
    strategy = 'progressive fibonacci'
    def update_bet(self, win):
        if win:
            self.fib_position += 1
        else:
            self.fib_position = max(self.fib_position - 2, 0)
        self.bet = fibonacci_sequence[self.fib_position]


class Doubler(Gambler):
    strategy = 'doubling'
    def update_bet(self, win):
        if win:
            self.bet = self.starting_bet
        else:
            self.bet = self.bet * 2


class ProgressiveDoubler(Gambler):
    strategy = 'progressive doubling'
    def update_bet(self, win):
        if win:
            self.bet = self.bet * 2
        else:
            self.bet = self.starting_bet


class Tripler(Gambler):
    strategy = 'tripling'
    def update_bet(self, win):
        if win:
            self.bet = self.starting_bet
        else:
            self.bet = self.bet * 3


class ProgressiveTripler(Gambler):
    strategy = 'progressive tripling'
    def update_bet(self, win):
        if win:
            self.bet = self.bet * 3
        else:
            self.bet = self.starting_bet


class OscarGrinder(Gambler):
    strategy = 'Oscar\'s Grind'
    goal = STARTING_AMOUNT + 1
    def update_bet(self, win):
        if self.money == self.goal:
            self.goal = self.money + 1
        if win:
            self.bet = self.bet + 1
        if self.bet + self.money > self.goal:
            #rule 1: always drop bet just large enough to gain one unit
            self.bet = self.goal - self.money

#dictionary with strategies as keys and their respective gamblers as values
gamblers = {
    'flat' : Gambler,
    'fibonacci' : FibonacciGambler,
    'progressive fibonacci' : ProgressiveFibonacciGambler,
    'doubling' : Doubler,
    'progressive doubling' : ProgressiveDoubler,
    'tripling' : Tripler,
    'progressive tripling' : ProgressiveTripler,
    'Oscar\'s Grind' : OscarGrinder,
    }

strategies = [
    'flat',
    'fibonacci',
    'progressive fibonacci',
    'doubling',
    'progressive doubling',
    'tripling',
    'progressive tripling',
    "Oscar's Grind",
    ]

if __name__ == '__main__':
    #the keys of gamblers contain each strategy, so use them
    for strategy in strategies:
        print '\n', 'preparing to gamble using', strategy
        #if graphing, get the directory to store the graphs in
        #this is in data/[strategy]/graphs
        if GRAPHING:
            graph_dir = "data/" + strategy + "/graphs/"
            figindex = 0
            #don't overwrite graphs already in the graph directory
            figindex += len(os.listdir(graph_dir))

        #load the shelve databases with previous experimentation data
        try:
            print 'loading data file...'
            data_file = shelve.open("data/" + strategy + "/data.db")
        except:
            #if we can't load the file, make a new one
            print 'cannot load data file: creating new one'
            data_file = shelve.open("data/" + strategy + "/data.db", 'n')
            break
        try:
            #try to load the rounds from the shelve database
            rounds_list = data_file['rounds']
        except KeyError:
            #if the database has no data, create a new rounds list
            #and add it in later
            print 'unable to load data'
            rounds_list = []
        print 'done loading data file'
        #only simulate and save rounds if we need to
        if len(rounds_list) < ROUND_LIMIT:
            #now, simulate gambling rounds until we get to ROUND_LIMIT
            while len(rounds_list) < ROUND_LIMIT:
                #initialize a new gambler from the class for the strategy
                gambler = gamblers[strategy]()
                try:
                    gambler.gamble()
                except KeyboardInterrupt:
                    #if the user hits Ctrl+C, quit gambling with this strategy
                    print 'stopping'
                    break
            #finally, put all of the experiment data into the shelve database
            print 'saving data...'
            data_file['rounds'] = rounds_list
        data_file.close()
        print 'data saved'
