import unittest
from unittest.mock import patch # May still be needed for input if we test game.start() directly
from app.main import Game # Import the Game class
from app.game_objects import Item, Room # May be useful for assertions
import io
import sys

class TestMain(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        # Redirect stdout for capturing print statements from game methods
        self.captured_output = io.StringIO()
        sys.stdout = self.captured_output
        # For tests calling process_command directly, assume game is in a "running" state.
        # Game.start() normally sets this, but Game.__init__ sets it to False.
        self.game.is_running = True
        # The initial room description is printed by game.start(), not by __init__ or setup.
        # If tests need that initial description, they should call a method that prints it,
        # or we can print it here in setUp if all tests expect it.
        # For now, let's have tests that need it, trigger it (e.g. via "look" or first "go").
        # Or, more simply, print it after setup if game.start() is not called.
        # print(self.game.player.current_room.describe()) # This would be like start() printing it

    def tearDown(self):
        # Reset stdout
        sys.stdout = sys.__stdout__
        # Optional: print captured output for debugging failed tests
        # if hasattr(self, '_outcome') and hasattr(self._outcome, 'success') and not self._outcome.success:
        #     print("\nCaptured output for failed test:\n", self.captured_output.getvalue())

    # Helper to get clean output
    def get_output(self):
        return self.captured_output.getvalue()

    # Helper to reset output buffer if needed between commands in a single test
    def reset_output(self):
        self.captured_output.truncate(0)
        self.captured_output.seek(0)

    # --- New Test Methods ---

    def test_initial_player_room_and_look(self):
        # Player should be in Entrance by default after Game init
        self.assertEqual(self.game.player.current_room.name, "Entrance")

        # Test 'look' command
        self.game.process_command("look")
        output = self.get_output()
        self.assertIn("You are at the stone entrance of an ancient ruin.", output)
        self.assertIn("You see:", output)
        self.assertIn(f"- a {self.game.torch_name}", output) # Using defined torch_name

    def test_quit_game(self):
        self.assertTrue(self.game.is_running)
        self.game.process_command("quit")
        self.assertFalse(self.game.is_running)
        self.assertIn("Exiting game.", self.get_output())

    def test_movement_go_east_then_west(self):
        # Initial room description is not printed by process_command itself.
        # 'go' command prints the description of the new room.
        self.game.process_command("go east")
        output_east = self.get_output()
        self.assertEqual(self.game.player.current_room.name, "Hallway")
        self.assertIn("You are in a dusty hallway.", output_east)

        self.reset_output()
        self.game.process_command("go west")
        output_west = self.get_output()
        self.assertEqual(self.game.player.current_room.name, "Entrance")
        self.assertIn("You are at the stone entrance of an ancient ruin.", output_west)

    def test_invalid_movement(self):
        initial_room_name = self.game.player.current_room.name
        self.game.process_command("go north") # From Entrance
        output = self.get_output()
        self.assertEqual(self.game.player.current_room.name, initial_room_name)
        self.assertIn("You can't go that way.", output)

    def test_take_item_success_and_inventory(self):
        # Player starts in Entrance, torch is there.
        self.game.process_command(f"take {self.game.torch_name}")
        output_take = self.get_output()
        self.assertIn(f"You took the {self.game.torch_name}.", output_take)
        self.assertTrue(self.game.player.has_item(self.game.torch_name))
        self.assertFalse(any(item.name == self.game.torch_name for item in self.game.rooms["Entrance"].items))

        self.reset_output()
        self.game.process_command("inventory")
        output_inv = self.get_output()
        self.assertIn("You are carrying:", output_inv)
        self.assertIn(f"- a {self.game.torch_name}", output_inv)

    def test_take_item_not_present(self):
        self.game.process_command("take non_existent_item")
        output = self.get_output()
        self.assertIn("You don't see that item here.", output)
        self.assertFalse(self.game.player.has_item("non_existent_item"))

    def test_inventory_empty(self):
        self.game.process_command("inventory")
        output = self.get_output()
        self.assertIn("You are not carrying anything.", output)

    def test_use_torch_in_treasure_chamber_success(self):
        # Setup: Player needs torch, go to treasure chamber
        self.game.player.inventory.append(Item(self.game.torch_name, "A torch")) # Give player torch directly
        self.game.player.current_room = self.game.rooms["Treasure Chamber"]
        self.assertFalse(self.game.player.current_room.is_lit) # Confirm it's dark

        self.reset_output()
        self.game.process_command(f"use {self.game.torch_name}")
        output = self.get_output()

        self.assertIn("You light the torch. The chamber brightens, revealing the Lost Artifact of Zyx!", output)
        self.assertTrue(self.game.player.current_room.is_lit)
        self.assertTrue(any(item.name == self.game.artifact_name for item in self.game.player.current_room.items))
        self.assertIn("The torchlight illuminates the chamber", self.game.player.current_room.description)

    def test_win_condition_when_artifact_taken(self):
        # Setup: Light treasure chamber, artifact appears, player takes it.
        torch = Item(self.game.torch_name, "A torch")
        self.game.player.inventory.append(torch)
        self.game.player.current_room = self.game.rooms["Treasure Chamber"]

        # Use torch to make artifact appear
        self.game.process_command(f"use {self.game.torch_name}")
        self.assertTrue(self.game.player.current_room.is_lit)
        self.assertTrue(any(item.name == self.game.artifact_name for item in self.game.player.current_room.items))

        self.reset_output()
        self.game.process_command(f"take {self.game.artifact_name}")
        output = self.get_output()

        self.assertIn(f"You took the {self.game.artifact_name}.", output)
        self.assertIn("Congratulations! You have found the Lost Artifact of Zyx! You are a true adventurer!", output)
        self.assertTrue(self.game.player.has_item(self.game.artifact_name))
        self.assertFalse(self.game.is_running) # Game should stop

    def test_case_insensitive_commands_and_items(self):
        # Take torch (case insensitive)
        self.game.process_command(f"tAkE {self.game.torch_name.upper()}")
        self.assertIn(f"You took the {self.game.torch_name}.", self.get_output())
        self.assertTrue(self.game.player.has_item(self.game.torch_name))

        self.reset_output()
        self.game.process_command("iNvEnToRy")
        self.assertIn(f"- a {self.game.torch_name}", self.get_output())

        self.reset_output()
        self.game.process_command("gO eAsT")
        self.assertEqual(self.game.player.current_room.name, "Hallway")
        self.assertIn("You are in a dusty hallway.", self.get_output())

        self.reset_output()
        self.game.process_command("lOoK")
        self.assertIn("You see no items of interest here.", self.get_output()) # Hallway is empty

        self.reset_output()
        self.game.process_command("qUiT")
        self.assertFalse(self.game.is_running)
        self.assertIn("Exiting game.", self.get_output())

    def test_go_no_direction(self):
        initial_room_name = self.game.player.current_room.name
        self.game.process_command("go")
        self.assertEqual(self.game.player.current_room.name, initial_room_name)
        self.assertIn("Go where?", self.get_output())

    def test_take_no_argument(self):
        self.game.process_command("take")
        self.assertIn("Take what?", self.get_output())

    def test_use_no_argument(self):
        self.game.process_command("use")
        self.assertIn("Use what?", self.get_output())

    def test_use_item_not_in_inventory(self):
        self.game.process_command("use non_existent_item")
        self.assertIn("You don't have a non_existent_item.", self.get_output())

    def test_use_torch_in_wrong_room(self):
        self.game.player.inventory.append(Item(self.game.torch_name, "A torch"))
        # Player is in Entrance, not Treasure Chamber
        self.game.process_command(f"use {self.game.torch_name}")
        self.assertIn("Nothing interesting happens.", self.get_output()) # Or more specific message if desired
        self.assertFalse(self.game.rooms["Treasure Chamber"].is_lit)

    def test_use_torch_in_treasure_chamber_already_lit(self):
        # Setup: Player has torch, in Treasure Chamber, which is already lit
        self.game.player.inventory.append(Item(self.game.torch_name, "A torch"))
        self.game.player.current_room = self.game.rooms["Treasure Chamber"]
        self.game.player.current_room.is_lit = True
        # Add the artifact to simulate it being there from previous lighting
        if self.game.the_true_artifact:
             self.game.player.current_room.add_item(self.game.the_true_artifact)

        self.reset_output()
        self.game.process_command(f"use {self.game.torch_name}")
        output = self.get_output()
        self.assertIn("The Treasure Chamber is already lit.", output)
        # Ensure artifact is still there, not re-added or anything
        self.assertEqual(sum(1 for item in self.game.player.current_room.items if item.name == self.game.artifact_name), 1)

    # Test that EOFError in start() is handled (relevant if testing start() directly)
    @patch('builtins.input', side_effect=EOFError)
    def test_start_game_with_eof_error(self, mock_input):
        self.game.is_running = False # start() will set it to True
        self.game.start() # game.start() calls input()
        output = self.get_output()
        self.assertIn("\nExiting game.", output) # Check for the EOF handling message
        self.assertFalse(self.game.is_running)


if __name__ == '__main__':
    unittest.main()
