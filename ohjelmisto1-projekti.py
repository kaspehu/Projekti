import random
import tarinaesim
from geopy import distance
import mysql.connector
import pyfiglet

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='root',
    password='',
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
        input("\033[32mPress enter to continue...\033[0m")
        print("You fight the guardian")
        while game == True: #while loop to play until hp reaches 0

            input("\033[32mPress enter to initiate the next round!\033[0m")

            print("------------------------------")
            guardian_attack = random.randint(1, 2)
            print(f"\033[91mThe guardian attacks you dealing {guardian_attack} damage\033[0m")
            player_hp = player_hp - guardian_attack
            while player_hp <= 0:  # when lost
                try_again = input("Do you want to try again? Y/N:").upper().strip()
                if try_again == "Y" and snail < 10:
                    golden_ball = 0
                    snail = snail + 1
                    print(f"The snail is {10 - snail} turns away from you")
                    print("\033[32mYou prepare to fight again.\033[0m")
                    player_hp = 8
                    boss_hp = 8
                elif try_again == "N":
                    golden_ball = 0
                    snail = snail + 1
                    print("You flee from the guardian abandoning the golden ball.")
                    game == False
                    return golden_ball, snail
                elif snail > 9:
                    golden_ball = 0
                    snail = snail + 1
                    return golden_ball, snail
                else:
                    print("\033[31mInvalid input\033[0m")
            if game == True:
                print(f"You have {player_hp} health left")
                attack = (input("\033[32mWould you like to smash(1), "
                        "stab(2) or shoot(3) the guardian? 1/2/3 :\033[0m"))

                if attack == "2":
                    if stab > 0:  # stab outcomes
                        boss_hp = boss_hp - stab
                        print(f"\033[36mYou stab the guardian with your sword dealing {stab} amount of damage\033[0m")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif stab == 0:
                        print("\033[35mYour stab is ineffective.\033[0m")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif stab < 0:
                        print(f"\033[31mYou try to stab the guardian, but you slip dealing {stab} damage to "
                              f"yourself instead\033[0m")
                        player_hp = player_hp + stab #player taking negative damage
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                elif attack == "3":  # shoot outcomes
                    if shoot > 0:
                        boss_hp = boss_hp - shoot
                        print(f"\033[36mYou shoot the guardian and deal {shoot} amount of damage\033[0m")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif shoot == 0:
                        print("\033[35mYour weapon seems to be ineffective.\033[0m")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif shoot < 0:
                        print(f"\033[31mYou try to shoot the guardian, but your gun explodes dealing {shoot} damage to "
                              f"yourself instead\033[36m")
                        player_hp = player_hp + shoot #player taking negative damage
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                elif attack == "1":  # smash outcomes
                    if stab < 2 and shoot < 2: # to prevent a situation where no possible weapon can win
                        smash = 2
                        boss_hp = boss_hp - smash
                        print(f"\033[36mYou smash with your hammer the boss and deal {smash} amount of damage\033[0m")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                    elif smash > 0:
                        boss_hp = boss_hp - smash
                        print(f"\033[36mYou smash with your hammer the boss and deal {smash} amount of damage\033[0m")
                        print(f"The guardian has {boss_hp} health left")
                        print(f"You have {player_hp} health left")
                elif attack != "1" or "2" or "3":
                    print("\033[44mYou fumble your attack missing your turn!\033[0m")

                if boss_hp <= 0: #when victorious
                    golden_ball =+ 1
                    snail = snail - 1
                    print(f"\033[32m---You have defeated the guardian!!!---\033[0m")
                    print(f"You feel the snail slowing down")
                    print("You grab the golden ball!")
                    game == False
                    return golden_ball, snail
                while player_hp <= 0:  # when lost
                    try_again = input("Do you want to try again? Y/N:").upper().strip()
                    if try_again == "Y" and snail < 10:
                        golden_ball = 0
                        snail = snail + 1
                        print(f"The snail is {10 - snail} turns away from you")
                        print("\033[32mYou prepare to fight again.\033[0m")
                        player_hp = 8
                        boss_hp = 8
                    elif try_again == "N":
                        golden_ball = 0
                        snail = snail + 1
                        print("You flee from the guardian abandoning the golden ball.")
                        game == False
                        return golden_ball, snail
                    elif snail > 9:
                        golden_ball = 0
                        snail = snail + 1
                        return golden_ball, snail
                    else:
                        print("\033[31mInvalid input\033[0m")
                        
    elif boss_chance == 2:  # return ball if no fight
        print("The ball is guarded by a golden guardian. The only way forward is to fight the guardian!")
        input("\033[32mPress enter to continue...\033[0m")
        print("\033[32mYou manage to sneak past the guardian!\033[0m")
        golden_ball = + 1
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

def print_intro():
    intro = pyfiglet.figlet_format("Curse Of The Mad Snail", font="Slant")
    print("\033[92m" + intro + "\033[0m")

def print_outro():
    outro = pyfiglet.figlet_format(f"Thank you for playing {player}!", font="Slant")
    print("\033[92m" + outro + "\033[0m")


# game starts
print_intro()
# ask to show the story
storyDialog = input('Do you want to read the background story? (Y/N): ').upper()
if storyDialog == 'Y':
    print(tarinaesim.tarina)



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

# snail that chases you, beginning value 0
snail = 0

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
    if snail > 9: # snail "catches" you after reaching value "5"
        print('Snail Got you, Game over!')
        game_over = True
        break

    if goal:
        if goal['money'] == 1:
            money += goal['money']
            snail -= 2
            shield = [("You have acquired the snail shield! The thought of golden balls fills you "
                       "with determination. The snail is 2 turns further."),
                      ("You have acquired the snail shield! It's dangerous to go alone,"
                       " take this. The snail is 2 turns further."),
                      ("You have acquired the snail shield! Congratulations,"
                       " the power of snail shield compels you to be safer. The snail is 2 turns further.")]
            vaikutus = random.choice(shield)
            print(f"{vaikutus}")
            input("\033[32mPress Enter to continue...\033[0m")
        elif goal['money'] == 2:
            money += goal['money']
            snail -= 1
            adhesive = [("You have acquired the snail adhesive! The snail is stuck in traffic! It's so slow.. The snail is a turn further."),
                        ("You have acquired the snail adhesive! You found some go-away-snail-dust. You sprinkled it around,"
                            " the snail felt that somewhere and somehow and slowed down. The snail is a turn further."),
                        ("You have acquired the snail adhesive! Someone stepped on the snail, it spent the rest of the day recovering. The snail is a turn further.")]
            vaikutus3 = random.choice(adhesive)
            print(f"{vaikutus3}")
            input("\033[32mPress Enter to continue...\033[0m")
        elif goal['money'] == 3:
            new_golden_ball, snail = boss()
            golden_ball = new_golden_ball + golden_ball  # to get new value for golden ball
            # snail = snail + new_snail #to get new value for snail
            print(f"\033[93mYou have {golden_ball} golden balls\033[0m")
            print(f"Snail is {10 - snail} turns away from you")  # updated information from after the boss"""
            input("\033[32mPress Enter to continue...\033[0m")
        elif goal['money'] == 4:
            snail += 1
            headache = [("You have acquired a headache! Your vision blurs for a moment and the world around you feels hazy, you should rest. The snail is a turn closer."),
                        ("You have acquired a headache! Did you remember to drink enough water? The snail is a turn closer."),
                        ("You have acquired a headache! Your head beats like a drum with every heartbeat. The snail is a turn closer.")]
            vaikutus2 = random.choice(headache)
            print(f"{vaikutus2}")
            input("\033[32mPress Enter to continue...\033[0m")
        else:
            snail += 2
            raging = [("You have acquired a raging diarrhea! Drinking that strange tasting water wasn’t a"
                       " great idea… The snail is 2 turns closer."),
                      ("You have acquired a raging diarrhea! Moving around is too risky. "
                       "You spent the rest of the day near the toilet. The snail is 2 turns closer."),
                      ("You have acquired a raging diarrhea! "
                       "Cold sweat rises on your forehead, your stomach is rumbling. RUN! The snail is 2 turns closer.")]
            vaikutus1 = random.choice(raging)
            print(f"{vaikutus1}")
            input("\033[32mPress Enter to continue...\033[0m")


    # show airports in range. if none, game over
    airports = all_airports

    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
    else:

        r = random.randint(1, 6)
        if r == 1:
            print(f"\033[32mThe golden dice gave you {r} new airport.\033[0m")
        else:
            print(f"\033[32mThe golden dice gave you {r} new airports.\033[0m")
        random_list = random.sample(airports, r)
        for n, item in enumerate(random_list):
            ap_distance = calculate_distance(current_airport, item['ident'])
            print(f"{n + 1}. {item['name']}")



        while True:
            try:
                if r > 1:
                    ask = int(input(f"\033[32mSelect one of the above airports (1 to {len(random_list)}): \033[0m"))
                else:
                    print("\033[32mYou only rolled one airport so that's where you're headed!\033[0m")
                    ask = 1
                if 1 <= ask <= len(random_list):
                    dest = random_list[ask - 1]
                    icao = dest['ident']
                    selected_distance = calculate_distance(current_airport, icao)
                    
                    #Delete current airport
                    for i, item in enumerate(airports):
                        if item.get('ident') == icao:
                            del airports[i]
                            break
                    update_location(icao, player_range, money, game_id)
                    current_airport = icao
                    break
                else:
                    print("\033[31mInvalid choice! Please select a number from the list.\033[0m")

            except ValueError:
                print("\033[31mInvalid input! Please enter a number.\033[0m")



    # if 5 Golden balls, game is won
    if golden_ball == 5:
        game_over = True


if golden_ball == 5:
    print("You've gathered enough balls and can banish the curse!")
    decision = input("Will you give up your balls Y/N?: ").upper()
    if decision == 'Y':
        epilogue_input = input("Do you want to read the epilogue Y/N?: ").upper()
        if epilogue_input == "Y":
            print(f"\n{tarinaesim.epilogi}")
        else:
            print("Thanks for playing!")
    else:
        print("Looks like your greed still lingers about you...the snail curses you for all eternity.")
else:
    print("Game over! You couldn't overcome the curse.")

input("\033[32mPress Enter to exit...\033[0m")

print_outro()
