###########################################################################
##  This is the room class for my text adventure prototype.              ##
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


class Room():

    def __init__(self, room_name, description):
        """ Input: room_name (string), description (string)
            Return: none
            Initializes instance of Room class w/ 5 attributes.  
            room_name and description must be set at time of creation.
            Place an item or character in the room (optional) via their 
            setter methods.  In order to access room in game, link it 
            to at least one other room via the link_room method.
        """
        self._name = room_name
        self._description = description
        self._characters = []
        self._item = None 
        self._search_gen = None       
        self.linked_rooms = {}
        
    @property
    def name(self):
        """ Input: nothing
            Return: room's name (string)
        """
        return self._name 

    @name.setter
    def name(self, new_name):
        """ Input: new_name (string)
            Return: none
        """
        self._name = new_name

    @property
    def description(self):
        """ Input: nothing
            Return: room's description (string)
        """
        return self._description
    
    @description.setter
    def description(self, room_description):
        """ Input: room_description (string)
            Return: none
        """
        self._description = room_description

    @property
    def characters(self):
        """ Input: nothing
            Return: character in the room (Character object) or
                    None if no character in room
        """
        return self._characters
    
    @characters.setter
    def characters(self, characters):
        """ Input: list of characters objects
            Return: none
            Places a character in the room

            NOTE: The add_characters and remove_characters methods were removed.
            To add (a) character(s): room.characters += [character(s)]
            To remove one character: room.characters.remove(character)
            To remove multiple characters: room.characters = [character for 
            character in room.characters if not in [charactersToRemove]]
        """
        self._characters = characters

    @property
    def item(self):
        """ Input: nothing
            Return: item name and its description (string)
        """
        return self._item

    @item.setter
    def item(self, item):
        """ Input: item (Item object)
            Return: none
            Places an item in the room
        """
        self._item = item

    @property
    def search_gen(self):
        """ Input: none
            Return: generator or None
        """
        return self._search_gen

    @search_gen.setter
    def search_gen(self, search_responses):
        """ Input: A tuple of tuples containing (1) search response 
            (string) (2) whether item found/event triggered (boolean)
            Return: none
            Assigns self._search_gen to the search method (generator)
        """
        self._search_gen = self.search(search_responses)

    def link_room(self, room_to_link, direction):
        """ Input: room_to_link (Room object), direction (string)
            Return: none  
            
            NOTE: The default paradigm is to only link rooms that are
            directly adjacent, but could implement fast travel/secret
            passages by linking rooms not directly adjacent.
        """
        self.linked_rooms[direction] = room_to_link

    def move(self, direction, party):
        """ Input: direction (string), party (list of Friend objects)
            Return: room object
            If possible, moves player in direction input, otherwise  
            returns self to keep player in current room, informs player.
        """
        if direction in self.linked_rooms:
            # Move party to next room and remove from this room
            self.linked_rooms[direction].characters += party
            self.characters = [character for character in self.characters if character 
                               not in party]
            # Move player to new room
            return self.linked_rooms[direction]
        else:
            print("\nYou can't go that way.")
            return self

    def search(self, search_responses):
        """ Input: information gained by searching (list of strings)
            Yield: Tuple containing (1) search response (string), 
            (2) whether to find item/trigger event (boolean)
        """
        for response in search_responses:
            yield response

        while True:
            yield ("You find nothing new.", False)

    def __str__(self):
        """ Input: nothing
            Return: roomStr (string)
            String representation includes room name, description, and 
            the names and relative directions of all rooms linked to it.
        """
    
        roomStr = "The {0}\n".format(self.name)         
        roomStr += "-------------------------\n"
        roomStr += "{0}\n\n".format(self.description)
        for direction in self.linked_rooms:
            room = self.linked_rooms[direction]            
            roomStr += "The {0} is {1}.\n".format(room.name, direction)

        return roomStr    
