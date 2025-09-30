import random

#bossi program

snail = 0
golden_ball = 0
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
                try_again = input("Do you want to try again? Y/N:").upper().strip()
                if try_again == "Y" and snail < 10:
                    print(f"The snail is {10 - snail} turns away from you")
                    print("You prepare to fight again.")
                    player_hp = 8
                    boss_hp = 8
                elif try_again == "N":
                    print("You flee from the guardian abandoning the golden ball.")
                    game == False
                    return golden_ball, snail
                if snail > 9:
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
                    try_again = input("Do you want to try again? Y/N:").capitalize().strip()
                    if try_again == "Y" and snail < 10:
                            print(f"The snail is {10 - snail} turns away from you")
                            print("You prepare to fight again.")
                            player_hp = 8
                            boss_hp = 8
                    elif try_again == "N":
                            print("You flee from the guardian abandoning the golden ball.")
                            game == False
                            return golden_ball, snail
                    if snail > 9:
                        return golden_ball, snail

    elif boss_chance == 2:# return ball if no fight
        golden_ball =+ 1
        snail = snail - 1
        print("You grab the golden ball!")
        print("You feel the snail slowing down")
        return golden_ball, snail

new_golden_ball, snail = boss()
golden_ball = new_golden_ball + golden_ball #to get new value for golden ball
#snail = snail + new_snail #to get new value for snail
print(f"You have a total of {golden_ball} golden balls")
print(f"Snail is {10 - snail} turns away from you") #updated information from after the boss"""


