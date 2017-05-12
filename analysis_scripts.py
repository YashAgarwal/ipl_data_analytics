import player_stats as ps
import operator
import matplotlib.pyplot as plt
import pandas as pd
import pickle
from operator import itemgetter
import numpy as np
import copy
import os
import yaml

#### CHANGED: Moved from player_stats.py undet tag
#### ****** time_series ******
def player_performance_over_time():
    time_series = dict()

## TODO: change constant range to reading as list of files from data/0_filelist.txt
## TODO: time data should be added
## TODO: merge players with (sub) in their
    for match_number in range(335982,1082626):
        #print match_number, "\r"
        match_file_name = "data/match_data/%d.yaml" % (match_number)
        #save_all_player_points_for_match(match_file_name)

        points_data = ps.get_all_player_points_for_match(ps.get_all_player_performance_for_match(match_file_name))
        if points_data != -1:
            for i,v in enumerate(points_data):
                if v[0] in time_series.keys():
                    time_series[v[0]].append(v[1])
                else:
                    time_series[v[0]] = list([v[1]])

        if match_number % 1000 == 0:
            print match_number

        print "Done, Yay!"
        return time_series
    #with open('output/all_player_points_time_series.yaml', 'w') as outfile:
    #p    yaml.dump(time_series, outfile, default_flow_style=False)


def some_plotting():
    time_srs = ps.get_match_data("output/all_player_points_time_series.yaml")
    #print type(time_srs)
    print len(time_srs.keys())
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    freq = ax.hist(time_srs['R Dravid'], bins = 20)
    #plt.show()
    #for key in time_srs.keys():
        #print key
        #print time_srs[key]

    print freq
    return time_srs

''' Just write the one function that is being executed here
'''

def average_ppg():
    time_srs = ps.get_match_data("output/all_player_points_time_series.yaml")
    averages = list()
    for key in time_srs.keys():
        averages.append([key, sum(time_srs[key])/len(time_srs[key])])
    averages_sorted = sorted(averages, key=operator.itemgetter(1))
    averages_sorted.reverse()
    return averages_sorted

#df = some_plotting()
#time_series = player_performance_over_time()
#print time_series

#df = average_ppg()
def average_ppg_playerlist(list):
    df = average_ppg()
    for i in df:
        print i
'''
Recursive code to merge a list of nested dictionaries with numerical values
dicts: a list of dictionaries to merge
merged_dict: a dictionary to store the merged dictionaries
'''
def add_dict(merged_dict, dicts):
    for d in dicts:
        for k in d.keys():
            if k not in merged_dict.keys():
                merged_dict[k] = d[k]
            else:
                if type(d[k]) == dict:
                    add_dict(merged_dict[k], [d[k]])
                else:
                    merged_dict[k] += d[k]

'''
Find Stadium wise perfomance for all players
This is a time consuming function
preferrential usage is to run it once for a dataset and save the generated file which will then be used for further analysis
'''
def get_all_player_performance_for_all_stadium():
    # Get the Player Performance as defined in the function get_all_player_performance_for_match() for each stadium
    # The name of the stadium is given in the info -> venue

    #The file name for all the match data
    match_file_list = os.listdir('./data/match_data/')
    player_performance = dict()
    print("Calculating Stadium wise performance for all players..")
    number_of_matches = len(match_file_list)
    for i,match_file in enumerate(match_file_list):
        #Progress check
        if i%50 == 0:
            print round(float(i)/number_of_matches * 100,2), " %"
        match_file_name = "data/match_data/%s" % (match_file)
        #get the stadium name
        stadium = ps.get_match_venue(match_file_name)
        #check if there is a key named "stadium" in the player_performance dictionary
        if stadium not in player_performance.keys():
            player_performance[stadium] = dict()
        add_dict(player_performance[stadium], [ps.get_all_player_performance_for_match(match_file_name)])

    #Save the data in a file
    output_file = 'output/all_player_performance_all_stadium.yaml'
    print "Saving the data in file ", output_file
    with open(output_file, 'w') as outfile:
        yaml.dump(player_performance, outfile, default_flow_style=False)

'''
########################################################################################
Testing Area:
Create all the prototypes here before writing the actual function
########################################################################################
'''

'''
a = pd.read_csv('data/iplRoster2017/DD.txt')
a = list(a.values.flatten())
b = list()
df = average_ppg()

for str in a:
    for sublist in df:
        if sublist[0] == str:
            b.append(sublist)
b = sorted(b, key=operator.itemgetter(1))
b.reverse()
print b
with open('test_data/DD_2017.txt', 'w') as fp:
    pickle.dump(b, fp)
'''

if __name__ =="__main__":
    time_srs = ps.get_match_data("output/all_player_points_time_series.yaml")
    #print time_srs
    count = 0
    h = list()
    for key in time_srs.keys():
        #print ps.hIndex_player(time_srs[key])
        #print time_srs[key]
        try:
            a = ps.hIndex_player(time_srs[key])
            a.insert(0, key)
            h.append(a)
        except:
            continue

    h = sorted(h, key=itemgetter(2))
    h_i = list()
    ings = list()
    for s in h:
        h_i.append(s[1])
        ings.append(s[2])

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.scatter(ings, h_i)

    m,b = np.polyfit(ings, h_i, 1)
    x = range(0, max(ings))
    y = list()
    for k in x:
        y.append(m*k+b)

    ax.plot(x,y)
    plt.show()

'''
# Correct the Player names in the team roster for this season by linearly traversing through the player name list

team_file = 'data/iplRoster2017/KXIP.yaml'
with open(team_file, 'r') as stream:
    try:
        data = (yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)

with open('output/all_player_points_time_series.yaml', 'r') as stream:
    try:
        stats = (yaml.load(stream))
    except yaml.YAMLError as exc:
        print(exc)

player_list = stats.keys()

new_list = list()

for batsman in data['Batsman']:
    surname = batsman.split()[-1].lower()
    print batsman, ':'
    for p in player_list:
        if p.split()[-1].lower() == surname:
            print p
            ans = raw_input('y/n: ')
            if ans == 'y':
                new_list.append(p)
                break

print new_list
data['Batsman'] = copy.copy(new_list)

new_list = list()

for all_rounder in data['All']:
    surname = all_rounder.split()[-1].lower()
    print all_rounder, ':'
    for p in player_list:
        if p.split()[-1].lower() == surname:
            print p
            ans = raw_input('y/n: ')
            if ans == 'y':
                new_list.append(p)
                break

print new_list
data['All'] = copy.copy(new_list)

new_list = list()

for bowler in data['Bowler']:
    surname = bowler.split()[-1].lower()
    print bowler, ':'
    for p in player_list:
        if p.split()[-1].lower() == surname:
            print p
            ans = raw_input('y/n: ')            if ans == 'y':
                new_list.append(p)
                break

print new_list
data['Bowler'] = copy.copy(new_list(team_file, 'w') as outfile
'''
