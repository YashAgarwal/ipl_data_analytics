import player_stats as ps
import operator
import matplotlib.pyplot as plt

#### CHANGED: Moved from player_stats.py undet tag
#### ****** time_series ******
def player_performance_over_time():
    time_series = dict()

## TODO: change constant range to reading as list of files from data/0_filelist.txt
## TODO: time data should be added
## TODO: merge players with (sub) in their
    for match_number in range(335982,1082626):
        #print match_number, "\r"
        match_file_name = "data/%d.yaml" % (match_number)
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

df = average_ppg()
