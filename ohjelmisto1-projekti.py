import random
import tarinaesim
from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='',
    user='',
    password='',
    autocommit=True
)



# FUNCTIONS

# removed continent and used brazil as game base, with medium airports
# select 30 airports for the game
def get_airports():
    sql = """SELECT ident, name, type, latitude_deg, longitude_deg
FROM airport
WHERE iso_country = 'BR' 
AND type='medium_airport'
ORDER by RAND()
LIMIT 30;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# get all goals
def get_goals():
    sql = "SELECT * FROM goal;"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# create new game
def create_game(start_money, p_range, cur_airport, p_name, a_ports):
    sql = "INSERT INTO game (money, player_range, location, screen_name) VALUES (%s, %s, %s, %s);"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (start_money, p_range, cur_airport, p_name))
    g_id = cursor.lastrowid

    # add goals / loot boxes
    goals = get_goals()
    goal_list = []
    for goal in goals:
        for i in range(0, goal['probability'], 1):
            goal_list.append(goal['id'])

    # exclude starting airport
    g_ports = a_ports[1:].copy()
    random.shuffle(g_ports)

    for i, goal_id in enumerate(goal_list):
        sql = "INSERT INTO ports (game, airport, goal) VALUES (%s, %s, %s);"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (g_id, g_ports[i]['ident'], goal_id))

    return g_id


# get airport info
def get_airport_info(icao):
    sql = f'''SELECT ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result


# check if airport has a goal
def check_goal(g_id, cur_airport):
    sql = f'''SELECT ports.id, goal, goal.id as goal_id, name, money 
    FROM ports 
    JOIN goal ON goal.id = ports.goal 
    WHERE game = %s 
    AND airport = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (g_id, cur_airport))
    result = cursor.fetchone()
    if result is None:
        return False
    return result


# calculate distance between two airports
def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


# get airports in range
def airports_in_range(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = calculate_distance(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range


# set loot box opened

# update location
def update_location(icao, p_range, u_money, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s, money = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, u_money, g_id))

#bossi ohjelma
import random
#snail = 5 en saanu toimii 0 arvolla jostai syystä
golden_egg = 0
def boss():
    boss_chance = random.randint(1, 2)
    smash = random.randint(1, 2)
    stab = random.randint(-1, 3)  # weapon stats per bossfight
    #shoot = random.randint(-2, 4) #real value
    shoot = 7 #for fast testing
    boss_hp = 8
    player_hp = 8  # defining hp values
    game = True
    snail = 0
    if boss_chance == 1: #if fight
        print("The egg is guarded by a golden guardian. The only way forward is to fight the guardian!")
        print("You fight the guardian")
        while game == True: #while loop to play until hp reaches 0

            input("Press enter to initiate the next round!")
            print("------------------------------")
            guardian_attack = random.randint(1, 2)
            print(f"The guardian attacks you dealing {guardian_attack} damage")
            player_hp = player_hp - guardian_attack
            if player_hp <= 0: #checking inbetween guardian attacks and player attacks
                game == False
                print("You have lost the battle")
                print("The snail gains some speed")
                golden_egg = + 1 - 1
                snail = + 1
                return golden_egg, snail
            elif game == True:
                print(f"You have {player_hp} health left")
                attack = input("Would you like to smash, stab or shoot the guardian?").lower()
                if attack == "stab":
                    if stab > 0:  # stab outcomes
                        boss_hp = boss_hp - stab
                        print(f"You stab the guardian with your sword dealing {stab} amount of damage")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif stab == 0:
                        print("Your stab is ineffective.")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif stab < 0:
                        print(f"You try to stab the guardian, but you slip dealing {stab} damage to "
                              f"yourself instead")
                        player_hp = player_hp + stab #player taking negative damage
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                if attack == "shoot":  # shoot outcomes
                    if shoot > 0:
                        boss_hp = boss_hp - shoot
                        print(f"You shoot the guardian and deal {shoot} amount of damage")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif shoot == 0:
                        print("Your weapon seems to be ineffective.")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif shoot < 0:
                        print(f"You try to shoot the guardian, but your gun explodes dealing {shoot} damage to "
                              f"yourself instead")
                        player_hp = player_hp + shoot #player taking negative damage
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                if attack == "smash":  # smash outcomes
                    if smash > 0:
                        boss_hp = boss_hp - smash
                        print(f"You smash with your hammer the boss and deal {smash} amount of damage")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")

                if boss_hp <= 0: #when victorious
                    golden_egg =+ 1
                    snail =- 1
                    print(f"---You have defeated the boss!!!---")
                    print(f"You feel the snail slowing down")
                    print("You Grab the golden egg!")
                    game == False
                    return golden_egg, snail
                elif player_hp <= 0: #when lost
                    golden_egg =+ 1 - 1
                    snail =+ 1
                    print("You have lost the battle")
                    print("The Snail gains some speed")

                    game == False
                    return golden_egg, snail


    elif boss_chance == 2:# return egg if no fight
        golden_egg =+ 1
        snail =- 1
        print("You Grab the golden egg!")
        return golden_egg, snail

"""new_golden_egg, new_snail = boss()
golden_egg = new_golden_egg + golden_egg #to get new value for golden egg
snail = snail + new_snail #to get new value for snail
print(f"You have a total of {golden_egg} golden eggs")
print(f"Snail is {10 - snail} turns away from you") updated information from after the boss"""


# game starts
# ask to show the story
storyDialog = input('Do you want to read the background story? (Y/N): ').upper()
if storyDialog == 'Y':
    # print wrapped string line by line
    for line in tarinaesim.haetarina():
        print(line)



# GAME SETTINGS
print('When you are ready to start, ')
player = input('type player name: ')
# boolean for game over and win
game_over = False
win = False

# start money = 1000
money = 1000
# start range in km = 2000
player_range = 2000

# score = 0
score = 0

# snail that chases you, beginning value 0
snail = 0

# boolean for diamond found
diamond_found = False

# all airports
all_airports = get_airports()
# start_airport ident
start_airport = all_airports[0]['ident']

# current airport
current_airport = start_airport

# game id
game_id = create_game(money, player_range, start_airport, player, all_airports)

# GAME LOOP
while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)
    # show game status
    print(f'''You are at {airport['name']}.''')
    print(f'''You have {money:.0f}$ and {player_range:.0f}km of range.''')
    # pause
    input('\033[32mPress Enter to continue...\033[0m')
    # if airport has goal ask if player wants to open it
    # check goal type and add/subtract money accordingly
    goal = check_goal(game_id, current_airport)
    snail += 1 # add + 1 on each loop
    if snail == 5: # snail "catches" you after reaching value "5"
        print('Game over!')
        game_over = True


    if goal:
        snail -= 1 # subtract 1 when finding treasure, snail "slows down" for one turn
        question = input(
            f'''Do you want to open lootbox for {"100$ or " if money > 100 else ""}{"50km range" if player_range > 50 else ""}? M = money, R = range, enter to skip: ''')
        if not question == '':
            if question == 'M':
                money -= 100
            elif question == 'R':
                player_range -= 50
            if goal['money'] > 0:
                money += goal['money']
                print(f'''Congratulations! You found {goal['name']}. That is worth {goal['money']}$.''')
                print(f'''You have now {money:.0f}$''')
            elif goal['money'] == 0:
                win = True
                print(f'''Congratulations! You found the diamond. Now go to start.''')
                input("\033[32mPress Enter to continue...\033[0m")
            else:
                money = 0
                print(f'''Oh no! You have been robbed. You lost all your money''')
                input("\033[32mPress Enter to continue...\033[0m")

    # ask to buy fuel/range
    if money > 0:
        question2 = input('Do you want to by fuel? 1$ = 2km of range. Enter amount or press enter. ')
        if not question2 == '':
            question2 = float(question2)
            if question2 > money:
                print(f'''You don't have enough money.''')
            else:
                player_range += question2 * 2
                money -= question2
                print(f'''You have now {money:.0f}$ and {player_range:.0f}km of range''')
        # pause
        input("\033[32mPress Enter to continue...\033[0m")

    # if no range, game over
    # show airports in range. if none, game over
    airports = airports_in_range(current_airport, all_airports, player_range)
    print(f'''\033[34mThere are {len(airports)} airports in range: \033[0m''')
    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
    else:
        print(f'''Airports: ''')
        for airport in airports:
            ap_distance = calculate_distance(current_airport, airport['ident'])
            print(f'''{airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km''')
        # ask for destination
        dest = input('Enter destination icao: ')
        selected_distance = calculate_distance(current_airport, dest)
        player_range -= selected_distance
        update_location(dest, player_range, money, game_id)
        current_airport = dest
        if player_range < 0:
            game_over = True
    # if diamond is found and player is at start, game is won
    if win and current_airport == start_airport:
        print(f'''You won! You have {money}$ and {player_range}km of range left.''')
        game_over = True


# if game is over loop stops
# show game result
print(f'''{'You won!' if win else 'You lost!'}''')
print(f'''You have {money:.0f}$''')
print(f'''Your range is {player_range:.0f}km''')