#!/usr/bin/env python

import yaml
import points

def add_player(player_name, player_performance):

    if player_name not in player_performance:
        player_performance[player_name] = dict()
        player_performance[player_name].update(dict({'batting':{'runs' : 0, 'balls' : 0, '4s': 0, '6s': 0},
                'bowling':{'runs' : 0, 'balls' : 0, 'wickets':0, 'extras':0, '4s': 0, '6s': 0},
                'fielding':{'catches' : 0, 'stumping' : 0, 'runout_throw': 0, 'runout_catch': 0, 'runout_direct': 0}
                }))

def get_all_player_performance_for_match(match_file_name):

    data = get_match_data(match_file_name)
    if data == -1:
        return -1

    player_performance = dict()
    innings1_balls = data["innings"][0]["1st innings"]["deliveries"]
    if len(data["innings"]) > 1:
        innings2_balls = data["innings"][1]["2nd innings"]["deliveries"]
        innings1_balls.extend(innings2_balls)

    for ball in innings1_balls:

        ball_data = ball[ball.keys()[0]]

        #Batsman Data
        player_name = ball_data["batsman"]

        add_player(player_name, player_performance)
        player_performance[player_name]["batting"]["runs"] +=  ball_data["runs"]["batsman"]

        if ball_data["runs"]["batsman"] == 4:
            player_performance[player_name]["batting"]["4s"] += 1
        elif ball_data["runs"]["batsman"] == 6:
            player_performance[player_name]["batting"]["6s"] += 1

        player_performance[player_name]["batting"]["balls"] += 1

        #Bowling and Fielding data
        player_name = ball_data["bowler"]

        add_player(player_name, player_performance)

        player_performance[player_name]["bowling"]["runs"] +=  ball_data["runs"]["total"]

        if "wicket" in ball_data:
            if ball_data['wicket']['kind'] != "run out":
                player_performance[player_name]["bowling"]["wickets"] +=  1
                if ball_data['wicket']['kind'] == "caught":
                    add_player(ball_data['wicket']['fielders'][0], player_performance)
                    #print ball_data['wicket']['fielders'][0]
                    player_performance[ball_data['wicket']['fielders'][0]]['fielding']['catches'] += 1
                elif ball_data['wicket']['kind'] == "caught and bowled":
                    #print player_name
                    player_performance[player_name]['fielding']['catches'] += 1
                elif ball_data['wicket']['kind'] == "stumped":
                    add_player(ball_data['wicket']['fielders'][0], player_performance)
                    #print ball_data['wicket']['fielders'][0]
                    player_performance[ball_data['wicket']['fielders'][0]]['fielding']['stumping'] += 1
            else :
                p1 = ball_data['wicket']['fielders'][0]
                add_player(p1, player_performance)
                if len(ball_data['wicket']['fielders']) == 2:
                    add_player(ball_data['wicket']['fielders'][1], player_performance)
                    p2 = ball_data['wicket']['fielders'][1]
                    player_performance[p1]['fielding']['runout_throw'] += 1
                    player_performance[p2]['fielding']['runout_catch'] += 1
                else :
                    player_performance[p1]['fielding']['runout_direct'] += 1

        player_performance[player_name]["bowling"]["extras"] +=  ball_data["runs"]["extras"]

        if ball_data["runs"]["batsman"] == 4:
            player_performance[player_name]["bowling"]["4s"] += 1
        elif ball_data["runs"]["batsman"] == 6:
            player_performance[player_name]["bowling"]["6s"] += 1

        player_performance[player_name]["bowling"]["balls"] += 1

    return player_performance

def get_all_player_points_for_match(player_performance):

    if player_performance == -1:
        return -1

    player_points = dict()
    import operator

    for key in player_performance.keys():
        p = points.player_points(key, player_performance)
        #print key, p
        player_points.update({key:p})
        #print player_performance[key]

    player_points_sorted = sorted(player_points.items(), key=operator.itemgetter(1))
    player_points_sorted.reverse()
    return player_points_sorted
    #print player_points_sorted

def save_all_player_points_for_match(match_file_name):

    player_performance = get_all_player_performance_for_match(match_file_name)
    if player_performance == -1:
        return

    player_points_sorted = get_all_player_points_for_match(player_performance)
    match_date = get_match_date(match_file_name)

    with open('output/all_player_points_%s.yaml' % (match_date), 'w') as outfile:
        yaml.dump(player_points_sorted, outfile, default_flow_style=False)

def get_match_date(match_file_name):

    data = get_match_data(match_file_name)
    if data != -1:
        return data["info"]["dates"][0]
    return ""

def get_match_data(match_file_name):

    try:
        with open(match_file_name, 'r') as stream:
            try:
                data = (yaml.load(stream))
            except yaml.YAMLError as exc:
                print(exc)
    except:
        data = -1
        print('Unable to open file %s' % (match_file_name))
    finally:
        return data

"""Time series of Points for every player in the last 10 seasons of IPL"""
time_series = dict()

for match_number in range(335982,1082626):
    #print match_number, "\r"
    match_file_name = "data/%d.yaml" % (match_number)
    #save_all_player_points_for_match(match_file_name)

    points_data = get_all_player_points_for_match(get_all_player_performance_for_match(match_file_name))
    if points_data != -1:
        for i,v in enumerate(points_data):
            if v[0] in time_series.keys():
                time_series[v[0]].append(v[1])
            else:
                time_series[v[0]] = list([v[1]])

    if match_number % 1000 == 0:
        print match_number

print "Done, Yay!"
with open('output/all_player_points_time_series.yaml', 'w') as outfile:
    yaml.dump(time_series, outfile, default_flow_style=False)