###########################################################################
##  This is item class for my text adventure prototype.                  ##
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


class Item():
    
    def __init__(self, item_name, item_type, item_description = None):
        """ Input: item_name (string), item_type (string), 
            item_description (string)
            Return: none
            Initializes an instance of the Item class w/ 3 attributes.
            item_description is the only optional attribute.  All 
            attributes can also be changed via setter methods.
        """
        self._name = item_name
        self._description = item_description
        self._item_type = item_type                
    
    @property
    def name(self):
        """ Input: nothing
            Return: item's name (string)
        """
        return self._name  

    @name.setter
    def name(self, item_name):  
        """ Input: item_name (string)
            Return: none
        """
        self._name = item_name  

    @property
    def description(self):
        """ Input: nothing
            Return: item's description (string)
        """
        return self._description    

    @description.setter
    def description(self, item_description):
        """ Input: item_description (string)
            Return: none
        """
        self._description = item_description

    @property
    def type(self):
        """ Input: nothing
            Return: item's type (string)
        """
        return self._item_type

    @type.setter
    def type(self, item_type):
        """ Input: item_type (string)
            Return: none
        """
        self._item_type = item_type


    def __str__(self):
        """ Input: none
            Return: item name (type of item) and description (string)
        """        
        if self.type == "story":   
            return "{0} ({1})\n\n{2}".format(self.name, self.type, self.description)

        return "{0} ({1}): {2}".format(self.name, self.type, self.description)
