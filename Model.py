import pygame
import os
import sys
from enum import Enum
from ObserverModel import Subject

# Enum for character positions
class Position(Enum):
    LEFT = 1
    RIGHT = 2

# Character class: Represents each character in the game
class Character():
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.position = Position.LEFT  # Default position

    def toggle_position(self):
        """Move the character to the opposite side."""
        if self.position == Position.LEFT:
            self.position = Position.RIGHT
        else:
            self.position = Position.LEFT


class Model(Subject):
    def __init__(self):
        super().__init__()
        self.characters = self._create_characters()
        self.reset()

    def _create_characters(self):
        return [
            Character("farmer"),
            Character("wolf"),
            Character("goat"),
            Character("cabbage"),
        ]

    def get_positions(self):
        """Return the current positions of all characters."""
        return {character.name: character.position for character in self.characters}

    def reset(self):
        """Reset the game to the initial state."""
        for character in self.characters:
            character.position = Position.LEFT
        self.state = (False, "")
        self.notify()

    def get_state(self):
        return self.state

    def check_game_state(self):
        """
        Check if the current game state is valid according to the river crossing rules.
        Returns:
            tuple: (is_valid, message) where is_valid is a boolean and message explains any violation
        """
        # Get current positions
        positions = self.get_positions()

        # Check win condition
        if all(pos == Position.RIGHT for pos in positions.values()):
            return (True, "Puzzle solved! All characters are safely across.")

        # Get lists of characters on each bank
        left_bank = [name for name, pos in positions.items() if pos == Position.LEFT]
        right_bank = [name for name, pos in positions.items() if pos == Position.RIGHT]

        # Check dangerous combinations on left bank
        if "farmer" not in left_bank:
            if "wolf" in left_bank and "goat" in left_bank:
                return (False, "Game Over: Wolf ate the goat on the left bank!")
            if "goat" in left_bank and "cabbage" in left_bank:
                return (False, "Game Over: Goat ate the cabbage on the left bank!")

        # Check dangerous combinations on right bank
        if "farmer" not in right_bank:
            if "wolf" in right_bank and "goat" in right_bank:
                return (False, "Game Over: Wolf ate the goat on the right bank!")
            if "goat" in right_bank and "cabbage" in right_bank:
                return (False, "Game Over: Goat ate the cabbage on the right bank!")

        return (True, "")

    def is_valid_move(self, character_name):
        """
        Check if moving a character is valid according to the game rules.
        Args:
            character_name: Name of the character to move
        Returns:
            tuple: (is_valid, message) where is_valid is a boolean and message explains why if invalid
        """
        # Can't move if it's not the farmer and the farmer is on the opposite bank
        farmer_pos = next(char.position for char in self.characters if char.name == "farmer")
        char_pos = next(char.position for char in self.characters if char.name == character_name)

        if character_name != "farmer" and farmer_pos != char_pos:
            return (False, "The farmer must be on the same bank to move this character!")

        # Simulate the move
        positions = self.get_positions()
        new_positions = positions.copy()

        # Toggle positions for the move
        new_positions[character_name] = (Position.RIGHT if positions[character_name] == Position.LEFT
                                         else Position.LEFT)
        if character_name != "farmer":
            new_positions["farmer"] = (Position.RIGHT if positions["farmer"] == Position.LEFT
                                       else Position.LEFT)

        # Check if this would create a dangerous situation
        left_bank = [name for name, pos in new_positions.items() if pos == Position.LEFT]
        right_bank = [name for name, pos in new_positions.items() if pos == Position.RIGHT]

        if "farmer" not in left_bank:
            if "wolf" in left_bank and "goat" in left_bank:
                return (False, "This move would leave the wolf to eat the goat on the left bank!")
            if "goat" in left_bank and "cabbage" in left_bank:
                return (False, "This move would leave the goat to eat the cabbage on the left bank!")

        if "farmer" not in right_bank:
            if "wolf" in right_bank and "goat" in right_bank:
                return (False, "This move would leave the wolf to eat the goat on the right bank!")
            if "goat" in right_bank and "cabbage" in right_bank:
                return (False, "This move would leave the goat to eat the cabbage on the right bank!")

        return (True, "")


    def toggle_character_position(self, name):
        """Toggle the position of a given character."""
        character = next(character for character in self.characters if character.name == name)
        character.toggle_position()
        if character.name != "farmer":
            # toggle farmer
            self.characters[0].toggle_position()
        # check board for a valid state
        self.state = self.check_game_state()
        self.notify()