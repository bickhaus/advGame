###########################################################################
##  This is the main file for my text adventure prototype.               ##
##  Copyright (C) 2018  Chris Bickhaus                                   ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.                                              ##
## If not, see https://www.gnu.org/licenses/gpl-3.0.html.                ##
###########################################################################


from rpgclasses import Room, Item, Character, Enemy, Friend, Player
from random import choice
from time import sleep
from sys import exit


###########################################################################
####                    Helper Functions                               ####
###########################################################################


def choose(prompt, min_length = 0, max_length = 0, choices = []):
    """ Input: prompt (string) re: user input, min_length (int), 
        max_length (int), choices (list)
        Return: player input (string) or player's choice (type varies)
        NOTE: should either use (min_length and max_length) or choices
    """
    # Player enters input with given length constraints
    if min_length > 0 and max_length >= min_length:        
        player_input = ""
        while len(player_input) < min_length or len(player_input) > max_length:
            player_input = input("{0} ({1} < length <= {2}): ".format(prompt, min_length,
                                 max_length))
        return player_input
    
    # Player chooses from a predetermined list 
    #(e.g., conversation replies, character creation)
    if choices != []:
        print("{0}\n".format(prompt))
        print("".join([choice + "\n" for choice in choices]))

        player_choice = ""
        # Can input either the number of choice or choice itself
        while (player_choice not in [choice[0] for choice in choices] and player_choice not in
               [choice[3:] for choice in choices]):
            player_choice = input("Make a selection from the list: ")
        return player_choice


def fight(party, enemies, player, can_flee=True):
    """ Input: player's party (list), enemies (list), player, 
               whether player can flee (boolean)
        Return: tuple: (1) list of party members killed (2) list of
                enemies killed (3) boolean re: whether player fled
        Provides a flow for the fight, keeps track of whose turn it
        is to attack and calls characters' attack and defend methods.
    """    
    # Create new copies of lists and add player to party
    party = list(party)
    party.append(player)
    enemies = list(enemies)
    combatants = party + enemies

    # Keep track of character deaths.  Will be returned after fight.
    party_killed = []
    enemies_killed = []

    # Track where we are at in turn order (combatants list)
    index = 0 

    # Keep track of whether player fled (this is returned)
    fled = False  
  
    # Roll initiative and order combatants from highest to lowest roll
    # NOTE: could add code to give party priority in case of tie
    combatants = sorted([[combatant.roll_dice(), combatant] for combatant in combatants],  
                        key=lambda x: x[0], reverse=True) 
    combatants = [combatant[1] for combatant in combatants]

    # Provides the structure for a single turn in combat.  
    # Loop exits if enemies defeated, player dies or flees
    while True:
        attacker = combatants[index]    

        # If player's turn to attack, allow chance to flee.
        if can_flee and attacker == player and player.constitution < 5:

            # If fleeing, random enemy gets free hit.
            if player.flee_check():
                fled = True
                last_attacker = choice(enemies_team)
                flee_penalty = last_attacker.roll_dice(1,3)
                player.constitution -= flee_penalty

                # Message re: outcome of flight, exit loop, end fight.
                if player.constitution < 1:
                    print("You were killed by {0} while trying to escape.".format(
                          last_attacker.name))
                    gameOver(False)
                else:
                    print("{0} attacked you for {1} damage whilst fleeing.".format(
                          last_attacker.name, flee_penalty))
                break

        # Figure out who attacker's opponents are and call attack method
        if attacker in enemies:
            attack = attacker.attack(party)                        
        else:
            attack = attacker.attack(enemies)

        # Defender is determined by attack() method.
        defender = attack[0]    
        outcome = defender.defend(attack[1], attack[2], attack[3])
    
        # Display's outcome of attack
        print(attacker.name + outcome[1])

        # Handle death of a character
        if not outcome[0]:
            
            # Compensate for shifting indexes when mutating list 
            if combatants.index(defender) < combatants.index(attacker):
                index -= 1

            combatants.remove(defender)
            
            if defender == player:
                gameOver(False)
            elif defender in party:
                party_killed.append(defender)
                party.remove(defender)                
            else:
                enemies_killed.append(defender)
                enemies.remove(defender)

        # All enemies have been killed, fight is over.
        if len(enemies) == 0:
            break     

        # Update index so next character can attack.
        if index >= (len(combatants) - 1):
            index = 0
            print()
        else:
            index += 1

        # Pause so player has time to read.
        sleep(1)

    return (party_killed, enemies_killed, fled)


def newScreen():
    """ Clears screen by moving cursor to top left 
        and clearing everything after cursor
    """
    #NOTE: This only works on ANSI compatible terminals. YMMV.  
    print("\033[H\033[J")
    return


def pressToContinue(message="Press Enter to continue."):
    """ Input: optional prompt to the user (string)
        Return: None
        Effectively pauses game until player presses a key
    """    
    print("\n")
    input(message)
    return

def gameOver(player_initiated):
    """ Input: indication of whether player initiated exit (boolean)
        Return: None
        Prints game over message, clears screen, exits to terminal
    """
    if player_initiated:
        print("\nThanks for playing!")
    else:
        print("You lost")    
        sleep(1)
        print("\t.")
        sleep(1)
        print("\t .")
        sleep(1)
        print("\t  .")
        sleep(1)
        print("\t   your life.")
        sleep(1)
        print("Game Over.")

    sleep(2)
    newScreen()
    exit()


###########################################################################
####              Scripted Story Events (SPOILER ALERT!)               ####
###########################################################################

# NOTE: both scripted events below are trigged by searches, so events 
# is only called after searches However, events could be triggered by 
# entering a room for the first time, conversation, etc.
# Add calls to the relevant commands, or call at the end of every turn.

def events(command, room, result, party, neutral, enemies, player):
    """ Input: most recent command (string), name of current room 
        (string), last output (string), party (list), neutral (list),
        enemies (list), and player (Player object)
        Return: None
        This is a repository for scripted events.  Events are grouped by
        room and triggered by matching both a command and result.
    """
    if room == "Ballroom":

        # You find the old library and Jill joins your party
        if command == "search" and "You check out the crack" in result:

            # In case you didn't previously talk w/ Jill, prevent her
            # from asking you to search for the library
            jill.conversation = ["..."]
        
            # Jill joins players party
            print("\n[Jill]: You found it!  I'll be joining you, if you don't mind.  Let's go!")
            jill.in_party = True

            # Link ballrom and library, inform player
            ballroom.link_room(old_library, "west")
            old_library.link_room(ballroom, "east")
            print("\nNew room found: Old Library")

    elif room == "Old Library":

        # This is the end game scene.
        if command == "search" and "On a table in the center" in result:

            # A bit of story to read.            
            print("\n[{0}]: This was easy enough.  I'm pretty good at this adventuring thing."
                  .format(player.name))
            sleep(2)
            print("\nFrom behind a stack of books across the room, you hear an old man humming to",
                  "himself.  He stands and looks you in the eye.  He appears to be a spirit.")
            sleep(5)

            # The choice made here determines which ending you get
            choice = choose("\n[Old Man]: Why do you seek that book?", 
                            choices=["1. knowledge", "2. create new order", "3. world domination"])
            newScreen()

            # This is the non-combat ending.
            if choice in "1. personal knowledge":
                print("\n[Old Man]: Fine, just be quiet, and close the door on your way out.")
                sleep(4)
                newScreen()
                print("In the book, you find the answers to your questions.",
                      " Your quest is complete, and it's time to return home.")
                sleep(5)
                gameOver(True)

            # The other two choices lead to combat.            
            else:
                # Create old_man as enemy w/ henchman and add them to room
                print("The Old Man now appears to be corporeal.  From the brick walls,",
                      "he summons a golem.")
                sleep(3)                
                old_man = Enemy("Protector", "cleric of the old religion", 25, None,
                          1.0, 6, None, "none")
                golem = Enemy("Golem", "golem", 5, fists, .75, 3, [], "any")

                old_library.characters += [old_man, golem]
                enemies += [old_man, golem]


                # Battle ensues and Jill fights for your cause 
                if choice in ["2", "heal the world"]:
                    
                    print("\n[Old Man]: I cannot allow you to share this knowledge.  Only someone",
                         "who has made their way to this library is worthy of its knowledge.",
                         "Now young adventurer...you will die.")
                    sleep(5)
                    print("\n[Jill]: I've got your back.  I believe in you.")
                    pressToContinue("Press ENTER to begin the battle.")
                    newScreen()
                    outcome = fight(party, enemies, player, False) 
                    
                    newScreen()

                    if outcome[0] == []:                    
                        # Ending based on Jill surviving the battle.
                        print("You have won the day.  As you pick up the tome you came for,",
                              "Jill speaks.")
                        sleep(2)
                        print("\n[Jill]: Let me come with you.  We will start the new order,",
                              "together.")
                        sleep(2)
                        print("\nYou silently nod your head, and you head off into the sunset.")
                        
                        pressToContinue()
                        gameOver(True)

                    else:           
                        # Ending if Jill dies during the battle.
                        print("You have won the day, but this victory came with a price.")
                        sleep(2)
                        print("\nJill did not survive the battle.  You resolve to yourself that",
                              "her sacrifice will not have been in vain.")
                        sleep(2)
                        print("\nAfter you lay Jill to rest, you go back out into the world,", 
                              "with new knowledge.  With it, you will start a new order of",
                              "clerics who will bring balance to the world.")
                        
                        pressToContinue()
                        gameOver(True)
                    
                # You chose evil: fight everyone, including Jill to win
                else:
                    
                    print("\n[Old Man]: You chose poorly.  Time to die.")
                    sleep(2)
                    print("\n[Jill]: I didn't sign up for this.  I'm inclined to agree with",
                          "Old Man River.  I can't allow you to do this.")
                    pressToContinue("Press ENTER to begin the battle.")
                    
                    # Jill is now an enemy
                    jill.in_party = False
                    enemies += [jill]
                    party.remove(jill)         

                    newScreen()
                    outcome = fight(party, enemies, player, False) 
                    newScreen()
                    
                    # The evil ending.
                    print("[{0}]: How pathetic.".format(player.name))
                    sleep(2)
                    print("\nArmed with new knowledge to twist for your own evil ends,",
                         "you set off to do the same thing you do everyday...")

                    pressToContinue()
                    gameOver(True)
            



###########################################################################
####           Create Gameworld, Characters, Items                     ####
###########################################################################


# Create rooms
kitchen = Room("Kitchen", "A dank and dirty room buzzing with flies.")
ballroom = Room("Ballroom", "A vast, opulent room with a golden shimmer and a shiny wood floor." 
                + "  A harpsicord sits in the corner.")
dining_hall = Room("Dining Hall", "An ornately decorated room, with large game adorning the"
                   + " walls and a larger table at which to dine.")
old_library = Room("Old Library", "A musty room, filled with tomes old and new.  The pungent"
                   + " aroma of book mold fills the air.")


# Add information that can be found by searching
kitchen.search_gen = (("You see a pile of dishes that has been sitting for days.", False),
                      ("Next to the dishes you find a letter.", True))

ballroom.search_gen = (("Along the northwest side of the room, you see just a few specks of"
                        + " light shimmering through the mortar.", False), ("You check out the"
                        + " crack, brush away some mortar, remove a brick, and find a door that"
                        + " has long been covered over.", True))

old_library.search_gen = (("After gagging on the stale air, you take a moment to soak in the"
                           + " fact that you are standing in the presence of thousands of years"
                           + " of knowledge.", False), ("On a table in the center of the room,"
                           + " the book you seek lies open.", True))

# Link rooms
kitchen.link_room(dining_hall, "south")
dining_hall.link_room(kitchen, "north")
dining_hall.link_room(ballroom, "west")
ballroom.link_room(dining_hall, "east")

# Create default weapon (fists)
fists = Item("fists", "weapon", "bare knuckles")

# Player starting inventory items
mace_of_base = Item("Mace of Base", "weapon", "At first it appears to be a standard mace."
                    + "  Then you see the sign.") 
hunters_bow = Item("hunter's bow", "weapon", "a standard hunting bow")
wine_flask = Item("wine flask", "food", "It smells a bit soured, but it will get the job done.")

# Jack (enemy) inventory items
gold_sack = Item("sack of gold", "currency", "It's money.")
simple_club = Item("simple club", "weapon", "It's not much more than a broken tree branch.")


# Jill (friend) inventory items
dagger_backstab = Item("Dagger of Backstabbing", "weapon", "not a frontstabber")

# Room items
cooks_letter = Item("Cook's letter", "story", "Dear brother,\n\nI found it.  The map to the lost"
                    + " treasure of our family.  Meet at the Red Dragon Inn at King's landing in a"
                    + " fortnight.  Together we will restore our family's riches and regain title" 
                    + " to our family's land.\n\nSincerely,\n\nAl")
kitchen.item = cooks_letter

# Create enemies and place them in dining hall
jack = Enemy("Jack", "smelly zombie", 8, fists, .75, 3, [gold_sack, simple_club], "Mace of Base")
jack.conversation = ["Aargh!",]
jack2 = Enemy("Jack2", "smelly zombie", 8, fists, .75, 3, [], "any")
jack2.conversation = ["Uuugghhh!",]
dining_hall.characters += [jack, jack2]

# Create a friend and place her in ballroom
jill = Friend("Jill", "A lovely rogue", 15, dagger_backstab, 1.0, 5, [dagger_backstab, ], False)
jill.conversation = ["Nice to meet you.", "I have been looking for the lost library.  Is that what"
                     + " you are searching for?", "My research has led me to believe that it is"
                     + " adjacent to this room, but I haven't been able to find it yet.  Perhaps"
                     + " if you searched the room, you could find something I missed."]
ballroom.characters += [jill]

# Set location at which player will begin game
current_room = kitchen


###########################################################################
####                Player Creation/Game Introduction                  ####
###########################################################################


# Create player character w/ input from player
player_name = choose("Enter a name for your character", 1, 24)
player_description = choose("Enter a description for your character", 1, 48)
player = Player(player_name, player_description, 50, mace_of_base, 1.25, 6, [mace_of_base, hunters_bow, wine_flask])
player.conversation = "Can I help you?"

newScreen()
print("Character created successfully.")
print(player)
pressToContinue()
newScreen()

# Print all valid commands
command_list = ("north", "south", "east", "west", "gift", "fight", "help", "inspect", "quit", "search", "steal", "talk")  
print("\nThe following is a complete list of valid commands in this game: {0}".format(
      ", ".join(command_list)))
print("\nTo see these commands later, type \"help\" at the prompt.")

pressToContinue()
newScreen()

# Introduction begins
print("<insert something inspiring>...You are {0}, a {1}.".format(player.name, player.description)
      + "Your hero's quest has brought you to Smith Manor.  A polite knock at the front door went"
      + " unanswered. The manor seems to be deserted. You walk around to the back, peering into"
      + " the windows along the way.  The back door is unlocked.")

pressToContinue("Press Enter to...enter.")
newScreen()


###########################################################################
####                        Core Game Logic                            ####
###########################################################################

# NOTE: See under Player Creation/Introduction under the comment 
# "Print all valid commands" for tuple containing all valid commands

# Store previous command, which will allow for easier repitiion below
previous_command = ""

while True:

    # Tell player current location, describe it and denote exits
    print(current_room)
    print()    
    
    # Check for characters in the room, print name(s)/description(s)
    party = [character for character in current_room.characters if (isinstance(character,
             Friend) and character.in_party)]
    if party != []:
        print("Party: {0}".format(", ".join(str(character) for character in party)))
        print()

    neutral = [character for character in current_room.characters if (isinstance(character, 
               Friend) and not character.in_party)]
    if neutral != []:
        print("Neutral: {0}".format(", ".join(str(character) for character in neutral)))
        print()

    enemies = [character for character in current_room.characters if isinstance(character, Enemy)]
    if enemies != []:
        print("Enemies: {0}".format(", ".join(str(character) for character in enemies)))

        print("\n" * 2)

    # Print previous command, get new command, update previous_command
    print("Previous command: {0}".format(previous_command))
    command = input("> ").lower()
    if command in command_list:
        previous_command = command

    # If player types nothing repeat previous command
    if command == "":
        command = previous_command

    if command in ("north", "south", "east", "west"):        
        # Attempt to move in given direction, see room.move() for more
        current_room = current_room.move(command, party)

 
    elif command == "fight":
        # Check to see if enemy in room; if so, fight
        if enemies != []:

            # Player chooses weapon for this fight
            player_weapon = player.pick_item("Choose your weapon for this encounter: ", "weapon")

            # Cancel fight if player typed, "cancel", else set weapon
            if player_weapon == "cancel":
                print("Perhaps some other time.")
                pressToContinue()
                newScreen()
                continue
            else:
                print()
                player.weapon = player_weapon
    
            # Fight and remove characters who were killed from room
            outcome = fight(party, enemies, player)
            current_room.characters = [character for character in current_room.characters if character not in outcome[0] + outcome[1]]

            # Print message re: fight outcome
            print("\n" * 2)                        
            if outcome[2]:
                print("You live to fight another day, but you're still a quitter.")
            else:                
                print("You have vanquished your enemies!")
            
            if outcome[0] != []:
                
                # Print message regarding party members deaths
                print("Unfortunately, some of your party did not survive. {0} died during the \
                       battle.".format(", ".join(str(character) for character in outcome[0])))
        else:
            print("There is no one to fight.")


    elif command == "search":        
        # If there is something to find, make call to generator
        if current_room.search_gen is not None:
            search_result = next(current_room.search_gen)
            print(search_result[0])

            # Add item to inventory, inform player when conditions met
            if current_room.item is not None and search_result[1] == True:
                print("\n" + current_room.item.description)
                player.items += [current_room.item]
                print("\n[Item added to your inventory]: {0}".format(current_room.item.name))
                current_room.item = None
            elif search_result[1] == True:
                events(command, current_room.name, search_result[0], party, neutral, enemies, 
                       player)
        else:
            print("You find nothing of note.")


    elif command == "talk":
        # If someone else in room, player chooses with whom to talk
        if party != [] or neutral != [] or enemies != []:
            talk_to = player.pick_char(party + neutral + enemies)            
            if talk_to is not None:
                print(next(talk_to.conversation))
        else:
            print("There's no one here to talk to but yourself.")


    elif command == "steal":
        # If enemy in room, choose who to steal from
        if enemies != []:
        
            target = player.pick_char(enemies)
            if target is not None:
                result = target.steal(player.roll_dice())
            
            # Add stolen item to inventory, if player successful
            if result[0] is not None:
                player.items += [result[0],]

            # Print message regarding attempt to steal
            print(result[1])  
        else: 
            print("There is no one to steal from in this room.")


    elif command == "inspect":
        # Player chooses item, info prints, unless cancelled
        inspection = player.inspect_item()
        if inspection is not None:
            print("\n" + str(inspection))


    elif command == "gift":
        # Make sure inhabitant is a friend, then give gift
        if party != [] or neutral != []:
            recipient = player.pick_char(party + neutral)
            recipient.receive_gift(player.give_item())
        else:
            print("There is no one for you to give an item to at this time.")


    elif command == "quit":
        gameOver(True)


    elif command == "help":
        # Print list of valid commands
        print("\nThe following is a complete list of valid commands in this game: {0}".format(
              ", ".join(command_list)))
        print("\nYou can repeat your previous command, just press Enter at the prompt.")


    else:
        print("Invalid Command.  Type \"help\" for a list of commands.")
  

    # Wait for player input to move on and clear screen
    pressToContinue()
    newScreen()
