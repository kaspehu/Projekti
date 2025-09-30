import random
import tarinaesim
from geopy import distance
import mysql.connector


conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='root',
    password='1q2w3e',
    autocommit=True
)



# FUNCTIONS

# removed continent and used brazil as game base, with medium airports
# select 31 airports for the game
def get_airports():
    sql = """SELECT ident, name, type, latitude_deg, longitude_deg
FROM airport
WHERE iso_country = 'BR' 
AND type='medium_airport'
ORDER by RAND()
LIMIT 31;""" # muutettu limit 31, koska probabilitys yhteensä 30kpl
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

def boss():
    global snail
    boss_chance = random.randint(1, 2)
    smash = random.randint(1, 2)
    stab = random.randint(-1, 3)  # weapon stats per airport boss
    shoot = random.randint(-2, 4) #real value
    #shoot = 7 #for fast testing
    boss_hp = 8
    player_hp = 8  # defining hp values
    game = True
    if boss_chance == 1: #if fight
        print("The ball is guarded by a golden guardian. The only way forward is to fight the guardian!")
        print("You fight the guardian")
        while game == True: #while loop to play until hp reaches 0

            input("Press enter to initiate the next round!")
            print("------------------------------")
            guardian_attack = random.randint(1, 2)
            print(f"The guardian attacks you dealing {guardian_attack} damage")
            player_hp = player_hp - guardian_attack
            if player_hp <= 0:  # when lost
                golden_ball = 0
                snail = snail + 1
                print("You have lost the battle")
                print("The Snail gains some speed")
                print(snail)
                try_again = input("Do you want to try again? Y/N:").capitalize().strip()
                if try_again == "Y" and snail < 5:
                    print(f"The snail is {5 - snail} turns away from you")
                    print("You prepare to fight again.")
                    player_hp = 8
                    boss_hp = 8
                elif try_again == "N":
                    print("You flee from the guardian abandoning the golden ball.")
                    game == False
                    return golden_ball, snail
                if snail == 5:
                    return golden_ball, snail
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
                    if stab < 2 and shoot < 2: # to prevent a situation where no possilble weapon can win
                        smash = 2
                        boss_hp = boss_hp - smash
                        print(smash)
                        print(f"You smash with your hammer the boss and deal {smash} amount of damage")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif smash > 0:
                        boss_hp = boss_hp - smash
                        print(f"You smash with your hammer the boss and deal {smash} amount of damage")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")

                if boss_hp <= 0: #when victorious
                    golden_ball =+ 1
                    snail = snail - 1
                    print(f"---You have defeated the guardian!!!---")
                    print(f"You feel the snail slowing down")
                    print("You grab the golden ball!")
                    game == False
                    return golden_ball, snail
                elif player_hp <= 0: #when lost
                    golden_ball = 0
                    snail = snail + 1
                    print("You have lost the battle")
                    print("The Snail gains some speed")
                    try_again = input("Do you want to try again? Y/N:").upper().strip()
                    if try_again == "Y" and snail < 5:
                            print(f"The snail is {5- snail} turns away from you")
                            print("You prepare to fight again.")
                            player_hp = 8
                            boss_hp = 8
                    elif try_again == "N":
                            print("You flee from the guardian abandoning the golden ball.")
                            game == False
                            return golden_ball, snail
                    if snail == 5:
                        return golden_ball, snail

    elif boss_chance == 2:# return ball if no fight
        golden_ball =+ 1
        snail = snail - 1
        print("You grab the golden ball!")
        print("You feel the snail slowing down")
        return golden_ball, snail

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

golden_ball = 0

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
    print(f"\033[93mYou have {golden_ball} golden balls\033[0m")
    # pause
    input('\033[32mPress Enter to continue...\033[0m')
    # check goal type
    goal = check_goal(game_id, current_airport)
    snail += 1 # add + 1 on each loop
    print(snail)
    if snail > 9: # snail "catches" you after reaching value "5"
        print('Snail Got you, Game over!')
        game_over = True
        break

    if goal:
        print(f"There's something in the airport...")
        if goal['money'] == 1:
            money += goal['money']
            snail -= 2
            print(f"Congratulations! You've found a snail shield")
            print(f"The snail won't be able to touch you for a while")
            input("\033[32mPress Enter to continue...\033[0m")
        elif goal['money'] == 2:
            money += goal['money']
            snail -= 1
            print(f"Congratulations! You've found snail adhesive")
            print(f"The Snail slows down...")
            input("\033[32mPress Enter to continue...\033[0m")
        elif goal['money'] == 3:
            new_golden_ball, snail = boss()
            golden_ball = new_golden_ball + golden_ball  # to get new value for golden ball
            # snail = snail + new_snail #to get new value for snail
            print(f"You have a total of {golden_ball} golden balls")
            print(f"Snail is {5 - snail} turns away from you")  # updated information from after the boss"""
            input("\033[32mPress Enter to continue...\033[0m")
        elif goal['money'] == 4:
            snail += 1
            print(f'''You get a horrible headache.''')
            print("The snail catches up...")
            input("\033[32mPress Enter to continue...\033[0m")
        else:
            snail += 2
            print(f'''Your stomach aches like crazy...''')
            print("The snail lurks in closer...")
            input("\033[32mPress Enter to continue...\033[0m")


    # ask to buy fuel/range

    # show airports in range. if none, game over
    airports = all_airports

    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
    else:

        r = random.randint(1, 6)
        print(f"\033[32mThe golden dice gave you {r} new airports.\033[0m")
        random_list = random.sample(airports, r)
        for n, item in enumerate(random_list):
            ap_distance = calculate_distance(current_airport, item['ident'])
            print(f"{n + 1}. {item['name']}, {item['ident']}")

        # ask for destination
        ask = int(input("\033[32mSelect one of the following airports:\033[0m"))
        dest = random_list[ask - 1]  # no nested indexing
        icao=dest['ident']
        selected_distance = calculate_distance(current_airport, icao)

        # Delete current airport
        for i, item in enumerate(airports):
            if item.get('ident') == icao:
                del airports[i]

        update_location(icao, player_range, money, game_id)
        current_airport = icao
        if player_range < 0:
            game_over = True


    # if 5 Golden balls, game is won
    if golden_ball == 100:
        game_over = True


# if game is over loop stops
# show game result
print(f'''{'You won!' if golden_ball == 1 else 'You lost!'}''')
print(f"You Found {golden_ball} Golden Balls")
