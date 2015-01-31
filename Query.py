#!/usr/bin/python
import shelve
import AutoGamble
from AutoGamble import *
import matplotlib.pyplot as plt
import numpy as np

graphing_indiv_graphs = False


def mean(number_list):
    if len(number_list) == 0:
        return float('nan')
 
    float_nums = [float(x) for x in number_list]
    return sum(float_nums) / len(number_list)


def get_standard_deviation(number_list):
    floats = [float(x) for x in number_list]
    number_mean = mean(number_list)
    return math.sqrt (sum([(i - number_mean)**2 for i in floats]) / len(floats))

def main():
    max_amounts = {}
    average_max_amounts = {}
    averages_of_turns_lasted = {}
    average_end_amounts = {}

    for strategy in strategies:

        datafile = shelve.open("data/" + strategy + "/data.db")
        rounds = datafile['rounds']
        max_money = 0
        moneys = [round.max_amount for round in rounds]
        max_money = max(moneys)
        average_max = mean(moneys)
        max_money_standard_deviation = get_standard_deviation(moneys)
        average_turns_lasted = mean([round.turns_lasted for round in rounds])
        end_amounts = [round.end_amount for round in rounds]
        mean_end_amount = mean(end_amounts)
        end_amount_standard_deviation = get_standard_deviation(end_amounts)
        max_end_amount = max(end_amounts)
        round_number = len(rounds)

        max_amounts[strategy] = max_money
        average_max_amounts[strategy] = average_max
        averages_of_turns_lasted[strategy] = average_turns_lasted
        average_end_amounts[strategy] = mean_end_amount

        print '' # newline
        print strategy, 'stats:'
        print 'max money overall:', max_money
        print 'average maxmimum money:', average_max
        print 'maximum money standard deviation', max_money_standard_deviation
        print 'average turns lasted', average_turns_lasted
        print 'number of rounds:', round_number
        print 'mean end amount:', mean_end_amount
        print 'max end amount:', max_end_amount
        print 'end amount standard deviation', end_amount_standard_deviation

        if graphing_indiv_graphs:
            print 'graphing histogram of end amounts...'
            plt.hist(end_amounts, 50)
            plt.title('Distribution of End Amounts of Sessions')
            plt.ylabel('Frequency')
            plt.xlabel('End Amounts of Money')
            plt.xlim(0, max_end_amount)
            plt.savefig('histogram_' + str(strategy))
            plt.clf()
            print 'graphing histogram of maximum amounts...'
            plt.hist(moneys, 50)
            plt.title('Distribution of Maximum Amounts Achieved of Sessions')
            plt.ylabel('Frequency')
            plt.xlabel('Maximum Amounts of Money')
            plt.savefig('histogram_maxes_' + str(strategy))
            plt.clf()
            datafile.close()

    print 'plotting average turns lasted per strategy'
    n = len(strategies)
    ind = np.arange(n)
    width = 0.7
    fig = plt.figure()
    ax = fig.add_subplot(111)
    averages = [averages_of_turns_lasted[strategy] for strategy in strategies]
    rects = ax.bar(ind+width, averages, width, color='r')
    ax.set_xticklabels([strategy.capitalize() for strategy in strategies])
    ax.set_title('Average Turns Lasted Per Strategy')
    ax.set_ylabel('Average Turns Lasted')
    ax.set_xlabel('Strategies')
    autolabel(rects)
    plt.savefig('turns_lasted')
    plt.clf()

    print 'plotting average max amounts per strategy'
    n = len(strategies)
    ind = np.arange(n)
    width = 0.7
    fig = plt.figure()
    ax = fig.add_subplot(111)
    averages = [averages_of_turns_lasted[strategy] for strategy in strategies]
    rects = ax.bar(ind+width, averages, width, color='g')
    ax.set_xticklabels([strategy.capitalize() for strategy in strategies])
    ax.set_title('Average Max Amounts Achieved Per Strategy')
    ax.set_ylabel('Average Max Amounts Achieved')
    ax.set_xlabel('Strategies')
    autolabel(rects)
    plt.savefig('max_amounts')
    plt.clf()

    print 'plotting average end amounts per strategy'
    n = len(strategies)
    ind = np.arange(n)
    width = 0.7
    fig = plt.figure()
    ax = fig.add_subplot(111)
    averages = [averages_of_turns_lasted[strategy] for strategy in strategies]
    rects = ax.bar(ind+width, averages, width, color='b')
    ax.set_xticklabels([strategy.capitalize() for strategy in strategies])
    ax.set_title('Average End Amounts Per Strategy')
    ax.set_ylabel('Average End Amounts')
    ax.set_xlabel('Strategies')
    autolabel(rects)
    plt.savefig('end_amounts')
    plt.clf()

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

if __name__ == '__main__':
    main()
