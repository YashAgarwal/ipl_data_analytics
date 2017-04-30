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

def get_player_performance_for_match(match_file_name):

    with open(match_file_name, 'r') as stream:
        try:
            data = (yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    #print data

    #for key in data.keys():
    #    print key

    '''
    for key in data["innings"][0]["1st innings"].keys():
        print key

    for key in data["innings"][0]["1st innings"]["deliveries"][0][0.1].keys():
        print key
    '''

    player_performance = dict()

    '''
    unit = {'batting':
                    {'runs' : 0, 'balls' : 0, '4s': 0, '6s': 0},
            'bowling':
                    {'runs' : 0, 'balls' : 0, 'wickets':0, 'extras':0, '4s': 0, '6s': 0},
            'fielding':
                    {'catches' : 0, 'stumping' : 0, 'runout_throw': 0, 'runout_catch': 0, 'runout_direct': 0}
            }
    '''

    innings1_balls = data["innings"][0]["1st innings"]["deliveries"]
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

    player_points = dict()
    import operator

    for key in player_performance.keys():
        p = points.player_points(key, player_performance)
        print key, p
        player_points.update({key:p})
        #print player_performance[key]

    player_points_sorted = sorted(player_points.items(), key=operator.itemgetter(1))
    player_points_sorted.reverse()

    print player_points_sorted

    with open('player_performance.yaml', 'w') as outfile:
        yaml.dump(player_performance, outfile, default_flow_style=False)

match_number = 335982
match_file_name = "data/%d.yaml" % (match_number)
get_player_performance_for_match(match_file_name)
