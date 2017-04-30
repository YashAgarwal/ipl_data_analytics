def player_points(player_name, player_performance):
    points = 0
    player_data = player_performance[player_name]

    #batting runs
    points +=  player_data["batting"]["runs"]*0.5

    #4s and 6s
    points +=  player_data["batting"]["4s"]*0.5 + player_data["batting"]["6s"]*1

    #wickets
    points +=  player_data["bowling"]["wickets"]*10

    #caught
    points +=  player_data["fielding"]["catches"]*4

    #runout and stumping
    points +=  player_data["fielding"]["runout_throw"]*4 + player_data["fielding"]["runout_catch"]*2 + player_data["fielding"]["runout_direct"]*6 + player_data["fielding"]["stumping"]*6

    #TODO
    #Starting XI
    #Duck Rule
    #Maiden Over

    #Century and half century
    if player_data["batting"]["runs"]>=100:
        points += 8
    elif player_data["batting"]["runs"]>=50:
        points += 4

    #4/5 wickets
    if player_data["bowling"]["wickets"]>=5:
        points += 8
    elif player_data["bowling"]["wickets"] >= 4:
        points += 4

    #Economy Rate
    if player_data["bowling"]["balls"] >= 12:
        econ = player_data["bowling"]["runs"]/player_data["bowling"]["balls"]
        if econ>=5 and econ<=6:
            points += 1
        elif econ>=4 and econ<5:
            points += 2
        elif econ<4:
            points += 3
        elif econ>=9 and econ<=10:
            points += -1
        elif econ>10 and econ<=11:
            points += -2
        elif econ>11:
            points += -3

    #Strike Rate
    if player_data["batting"]["balls"]>=10:
        str_rate = 100 * player_data["batting"]["runs"]/player_data["batting"]["balls"]
        if str_rate>=60 and str_rate<=70:
            points += -1
        elif str_rate>=50 and str_rate<60:
            points += -2
        elif str_rate<50:
            points += -3

    return points
