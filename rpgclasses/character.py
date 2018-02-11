from random import choice, randrange


###########################################################################
####                Basic Character Class                              ####
####         (every other character class inherits from this)          ####
###########################################################################


class Character():

    def __init__(self, char_name, char_description, constitution, weapon=None, attack_mod=1.0,
                 max_damage=5, items=None):
        """ Input: char_name (string), char_description (string), 
            constitution (hit points) (int), items (list of item 
            objects), default weapon (item), attack_mod (float), 
            max_damage (int)
            Return: nothing returned
            Initializes instance of Character class w/ 8 attributes.  
            NOTE: self.conversation is set via set_conversation().
        """        
        self._name = char_name
        self._description = char_description
        self._constitution = constitution
        self._conversation = None
        self._weapon = weapon
        self._attack_mod = attack_mod
        self._max_damage = max_damage

        if items is None:
            self._items = []
        else:
            self._items = items

    @property
    def name(self):
        """ Input: none
            Return: character name (string)
        """
        return self._name

    @name.setter
    def name(self, new_name):
        """ Input: new name for character (string)
            Return: none
        """
        self._name = new_name

    @property
    def description(self):
        """ Input: none
            Return: character description (string)
        """
        return self._description

    @description.setter
    def description(self, new_description):
        """ Input: new_description (string)
            Return: none
        """ 
        self._description = new_description

    @property
    def constitution(self):
        """ Input: none
            Return: character's constitution (hit points) (int)
        """
        return self._constitution

    @constitution.setter
    def constitution(self, constitution):
        """ Input: consitution (int)
            Return: none
        """
        self._constitution = constitution

    @property
    def conversation(self):
        """ Input: none
            Return: character response to player salutation (string)
        """
        return self._conversation
    
    @conversation.setter  
    def conversation(self, conversation):
        """ Input: list of strings
            Return: none
            Set what this character will say when talking to player
        """
        self._conversation = self.talk(conversation)

    @property
    def items(self):        
        """ Input: none
            Return: character inventory (list of item objects)
        """
        return self._items

    @items.setter
    def items(self, items):
        """ Input: item object(s) (list)
            Return: None
            NOTE: The add_item and remove_item methods were removed.
            To add items: character.items += [item(s)]
            To remove one item: character.items.remove(item) 
            To remove multiple items: character.items = [item for 
            item in self.items if not in [itemsToRemove]]
        """
        self._items = items

    @property
    def item_names(self):
        """ Input: none
            Return: item names in character inventory (list of strings)
        """
        return [item.name for item in self.items]

    @property
    def weapon(self):
        """ Input: none
            Return: default weapon (item object)
        """
        return self._weapon

    @weapon.setter
    def weapon(self, weapon):
        """ Input: weapon (item object)
            Return: none
        """
        self._weapon = weapon

    @property
    def attack_mod(self):
        """ Input: none
            Return: name of default weapon (string)
        """
        return self._attack_mod

    @attack_mod.setter
    def attack_mod(self, attack_mod):
        """ Input: modifies attack roll affecting chance to hit (float)
            (e.g., weaker enemies may have a .75 modifier, while bosses
            may have 1.25 to increase roll)
            Return: none
        """
        self._attack_mod = attack_mod

    @property
    def max_damage(self):
        """ Returns max damage character can inflict (int) """
        return self._max_damage

    @max_damage.setter
    def max_damage(self, max_damage):
        """ Input: max damage character can inflict (int)
            Return: None
        """
        self._max_damage = max_damage

    def talk(self, conversation=None):
        """ Return/Yield: response to player's salutation (string) """

        if conversation is not None:
            for statement in conversation:
                yield "[{0}]: {1}".format(self.name, statement)
            while True:
                yield "[{0}]: ...".format(self.name)
        else:
            return "{0} doesn't want to talk to you.".format(self.name)

    def attack(self, opponents):
        """ Input: list of opponents (character objects)
            Return: tuple containing (1) who is being attacked 
            (character object), (2) the attack roll (int), (3) damage
            roll (int), (4) weapon used (item)
        """
        defender = opponents[0]

        # Choose to attack opponent with highest constitution
        if len(opponents) > 1:
            for opponent in opponents:
                if opponent.constitution > defender.constitution:
                    defender = opponent
    
        # Roll attack and damage dice
        attack_roll = self.roll_dice() * self.attack_mod
        damage_roll = self.roll_dice(1, self.max_damage)    

        return (defender, attack_roll, damage_roll, self.weapon)

    def defend(self, attack, damage, weapon):
        """ Input: attack roll (int), damage roll (int), weapon (item)
            Return: tuple containing (1) boolean (True if still alive,
            false otherwise) and (2) info re: outcome of attack (string)
        """
        defense_roll = self.roll_dice()
    
        # Attacker hits, reduce constitution accordingly        
        if attack > defense_roll:

            # If attack is 20, Critical Hit, different rules for damage
            if attack == 20:
                print("Critical Hit! ", end=" ")
                if self.constitution > 6:
                    self.constitution //= 2
                else:
                    self.constitution = 0
            else:
                # Add extra damage if weapon is enemie's weakness
                if isinstance(self, Enemy) and (self.weakness == weapon.name or 
                                                self.weakness == "any"):
                    damage += 1
                
                self.constitution -= damage

            # Return message relevant to attack/damage done
            if self.constitution > 0 and attack == 20:
                return (True, " reduces {0}'s hitpoints by half. {1} has {2} hit points left."
                        .format(self.name, self.name, self.constitution))
            elif self.constitution > 0:
                return (True, " hits {0} for {1} damage.  {2} has {3} hit points left.".format(
                        self.name, damage, self.name, self.constitution))
            else:            
                return (False, " kills {0}.".format(self.name))
        
        # If attack roll much lower than defense roll, attacker whiffs
        elif defense_roll - attack > 2:
            return (True, " misses {0}.".format(self.name))
       
        # Defender successfully blocks attack 
        else:    
            return (True, " is blocked by {0}.".format(self.name))

    def roll_dice(self, num_dice = 1, num_sides = 20):
        """ Input: number of dice (int), number of sides to dice (int)
            Returns: number equal to total of rolled dice
        """
        total = 0
        for die in range(num_dice):
            total += randrange(1,(num_sides + 1))

        return total

    def __str__(self):
        """ Input: none
            Return: character name and description (string)
        """            
        return "{0} ({1})".format(self.name, self.description)        


###########################################################################
####                Enemy Character Class                              ####
###########################################################################
        

class Enemy(Character):
    
    def __init__(self, char_name, char_description, constitution, weapon=None, attack_mod=1.0,
                 max_damage=5, items=None, weakness="any"):
        """ Input: char_name (string), char_description (string),
            constitution (int), items (list of item objects), 
            default weapon (item), attack_mod (float), max_damage (int),
            weakness (string)
            Return: none
            Initializes isntance of Enemy class w/ 10 attributes.  
            NOTE: self.conversation is set via set_conversation() and
            theft_victim will be updated automatically.
        """         
        super().__init__(char_name, char_description, constitution, weapon, attack_mod, max_damage,
                         items)
        self._weakness = weakness        
        self._theft_victim = False

    @property
    def weakness(self):
        """ Input: none
            Return: character's weakness (string)
        """
        return self._weakness

    @weakness.setter
    def weakness(self, weakness):
        """ Input: weakness (string)
            Return: None
            NOTE: weakness can be specific weapon, "any", "none"
        """
        self._weakness = weakness

    def steal(self, dice_roll):
        """ Input: dice_roll (int)
            Return: tuple containing (1) an item object (if successful) 
            or None (if unsuccessful), (2) is a related message (string) 
            If enemy has items and you haven't previously tried to steal, 
            allow player to attempt to steal and, if successful return 
            randomly chosen item
        """
        # Check to see if there is an item to steal
        if self.items == []:
            return (None, "{0} has nothing to steal.".format(self.name))
        
        # If you have already attempted to steal, prevent attempt
        if self._theft_victim:
            return (None, "{0} has been alerted to your prior theft attempt.  Do not try again."
                    .format(self.name))
        
        # If you haven't attempted to steal, attempt to steal
        if dice_roll > 8:
            item_stolen = choice(self.items)
            self.remove_item([item_stolen,])
            self._theft_victim = True
            return (item_stolen, "Item stolen: {0}".format(item_stolen))

        # Roll to see if enemy noticed your attempt to steal
        # if so prevent further attempts
        if self.roll_dice(1,8) > 5:
            self._theft_victim = True 
            return (None, "You were unsuccessful, and {0} took notice.  Don't try it again."
                    .format(self.name))
        
        return (None, "You were unsuccesful, but {0} didn't notice your attempt."
                .format(self.name))


###########################################################################
####                Friend Character Class                             ####
###########################################################################


class Friend(Character):

    def __init__(self, char_name, char_description, constitution, weapon=None, attack_mod=1.0,
                 max_damage=5, items=None, in_party=False):
        """ Input: char_name (string), char_description (string), 
            constitution (hit points) (int), items (list of item 
            objects), default weapon (item), attack_mod (float), and
            max_damage (int)
            Return: none
            Initializes isntance of Enemy class w/ 8 attributes.  
            NOTE: self.conversation is set via set_conversation().
        """ 
        super().__init__(char_name, char_description, constitution, weapon, attack_mod, max_damage,
                         items)

        self._in_party = in_party

    @property
    def in_party(self):
        """ Return True if in player's party, else False (boolean) """
        return self._in_party

    @in_party.setter
    def in_party(self, true_or_false):
        """ Input: True if character in party, False otherwise (boolean)
            Return: None        
        """
        self._in_party = true_or_false

    def receive_gift(self, gift):
        """ Input: gift (item object or None)
            Return: none
            Append gift to inventory, thank player, unless gift is None
        """        
        if gift is not None:        
            self.items += [gift,]
            print("\n{0}'s inventory: {1}".format(self.name, ", ".join(self.item_names)))
            print("[{0}]: Thank you.  Your kindness will not be soon forgotten.".format(self.name))
        return


###########################################################################
####                Player Character Class                             ####
###########################################################################


class Player(Character):

    def __init__(self, char_name, char_description, constitution, weapon=None, attack_mod=1.0,
                 max_damage=5, items=None):
        """ Input: char_name (string), char_description (string), 
            constitution (hit points) (int), items (list of item 
            objects), default weapon (item), attack_mod (float), and
            max_damage (int)
            Return: none
            Initializes isntance of Enemy class w/ 8 attributes.  
            NOTE: self.conversation is set via set_conversation()
        """
        super().__init__(char_name, char_description, constitution, weapon, attack_mod, max_damage,
                         items)

    def pick_char(self, characters, can_cancel=True):
        """ Input: characters (list), whether can cancel (boolean)
            Return: character object or "cancel" (string) 
            Gets user to pick character and returns character or
            "cancel" (if allowed)
        """
        # Print a list of characters from which to choose
        print("Characters: {0}".format(", ".join([character.name for character in characters])))

        # Link name to item so user input can be used to return item        
        character_dict = {character.name: character for character in characters}

        if can_cancel:
            # Get input from player
            chosen_character = ""        
            while chosen_character != "cancel" and chosen_character not in character_dict.keys(): 
                chosen_character = input("Choose a character, or type cancel: ")
    
            if chosen_character == "cancel":
                return None

        else:
            # Require player to pick a character (e.g., during battle)
            chosen_character = ""
            while chosen_character not in character_dict.keys():
                chosen_character = input("Choose a character: ")
                
        return character_dict[chosen_character]

    def pick_item(self, header, item_type=None):
        """ Input: header (string) is message that precedes items list,
            item_type (string) denoting item type to filter
            Return: item object or "cancel" (string)
            Gets user to pick item and returns item picked or "cancel"
        """
        # Print list of character's items and filter if applicable
        if item_type is None:
            items_list = [item.name for item in self.items]
        else:
            items_list = [item.name for item in self.items if item.type == item_type]

        print("\n{0} {1}\n".format(header, ", ".join(items_list)))

        # Link name to item so user input can be used to return item
        items_dict = {item.name: item for item in self.items}

        # Get input from player
        item = ""        
        while item != "cancel" and item not in items_dict.keys(): 
            item = input("Enter the item you choose, or type cancel: ")
    
        if item == "cancel":
            return "cancel"
                
        return items_dict[item]

    def attack(self, opponents):
        """ Input: list of opponents (character objects)
            Return: tuple containing (1) defender (character object),
            (2) attack roll (int), (3) damage roll (int), 
            (4) weapon (item)
        """
        # Pick character to attack, when more than one enemy present.
        if len(opponents) == 1:
            defender = opponents[0]
        else:
            defender = self.pick_char(opponents, False)

        # Roll attack and damage dice
        attack_roll = self.roll_dice() * self.attack_mod
        damage_roll = self.roll_dice(1, self.max_damage)

        return (defender, attack_roll, damage_roll, self.weapon)

    def flee_check(self):
        """ Input: none
            Return: True if wants to flee, false otherwise (boolean)
        """
        valid_responses = ["yes", "y", "no", "n"]
        response = ""

        while response not in valid_responses:
            response = input("You have {0} hit points left.  Attempt to flee? ".format(
                             self.constitution)).lower()

        if response == "yes" or response == "y":
            return True
        else:
            return False 

    def give_item(self):
        """ Input: none
            Return: item object or None if player cancels gift
            Uses the pick_item method to give gift to friend.
        """
        item = self.pick_item("Here are the items in your inventory:")
        
        if item == "cancel":
            return None
                            
        self.items.remove(item)
        return item
     
    def inspect_item(self):
        """ Input: none
            Return: item name (string) or None if player cancels
            Uses the pick_item method to choose item and get info.
        """
        item = self.pick_item("Here are the items that you may inspect:")
        
        if item == "cancel":
            return None
                            
        return item
