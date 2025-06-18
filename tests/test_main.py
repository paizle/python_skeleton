# tests/test_main.py
import unittest
from unittest.mock import patch
from app.main import main, initial_rooms_state, artifact_name # Import initial_rooms_state and artifact_name
from app import main as app_main # Import module to allow attribute patching/resetting
import io
import sys
import copy

class TestMain(unittest.TestCase):

    def setUp(self):
        # Reset game state before each test
        app_main.current_room = 'entrance'
        app_main.inventory = []
        app_main.rooms = copy.deepcopy(initial_rooms_state)

    @patch('builtins.input', side_effect=['quit'])
    def test_initial_room_description_and_quit(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output.splitlines()[0])
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['go east', 'quit'])
    def test_basic_movement(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output)
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['go north', 'quit'])
    def test_invalid_movement(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output)
        self.assertIn("You can't go that way.", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['look', 'quit'])
    def test_look_command_with_item(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output)
        self.assertIn("You see:", output)
        self.assertIn("- a torch", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['go east', 'look', 'quit'])
    def test_look_command_no_item(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn("You see no items of interest here.", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['take torch', 'inventory', 'quit'])
    def test_take_item_success_and_inventory(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("You took the torch.", output)
        self.assertNotIn('torch', app_main.rooms['entrance']['items'])
        self.assertIn('torch', app_main.inventory)
        self.assertIn("You are carrying:", output)
        self.assertIn("- a torch", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['take key', 'quit'])
    def test_take_item_not_present(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("You don't see a key here.", output)
        self.assertNotIn('key', app_main.inventory)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['take', 'quit'])
    def test_take_item_no_argument(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Take what?", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['inventory', 'quit'])
    def test_inventory_command_empty(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("You are not carrying anything.", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['take torch', 'go east', 'go north', 'take key', 'inventory', 'quit'])
    def test_inventory_multiple_items(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("You took the torch.", output)
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn(app_main.initial_rooms_state['hidden_alcove']['description'], output)
        self.assertIn("You took the key.", output)
        self.assertIn("You are carrying:", output)
        self.assertIn("- a torch", output)
        self.assertIn("- a key", output)
        self.assertIn("Exiting game.", output)
        self.assertCountEqual(['torch', 'key'], app_main.inventory)
        self.assertNotIn('torch', app_main.rooms['entrance']['items'])
        self.assertNotIn('key', app_main.rooms['hidden_alcove']['items'])

    # --- New tests for "use" command and puzzle ---
    @patch('builtins.input', side_effect=['use', 'quit'])
    def test_use_item_no_argument(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("Use what?", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['use sword', 'quit'])
    def test_use_item_not_in_inventory(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("You don't have a sword.", output)
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['take torch', 'go east', 'use torch', 'quit'])
    def test_use_torch_in_wrong_room(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn("You took the torch.", output)
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn("Nothing interesting happens.", output)
        self.assertFalse(app_main.rooms['treasure_chamber']['is_lit'])
        self.assertIn("Exiting game.", output)

    @patch('builtins.input', side_effect=['take torch', 'inventory', 'go east', 'go north', 'take key', 'inventory', 'go south', 'go east', 'use key', 'quit'])
    def test_use_wrong_item_in_treasure_chamber(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("You took the torch.", output)
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn(app_main.initial_rooms_state['hidden_alcove']['description'], output)
        self.assertIn("You took the key.", output)
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn(app_main.initial_rooms_state['treasure_chamber']['description'], output)

        self.assertIn("You are carrying:", output)
        self.assertIn("- a torch", output)
        self.assertIn("- a key", output)

        self.assertIn("Nothing interesting happens.", output) # Result of "use key"
        self.assertFalse(app_main.rooms['treasure_chamber']['is_lit'])
        self.assertNotIn(artifact_name, app_main.rooms['treasure_chamber']['items'])
        self.assertIn("Exiting game.", output)

    # Updated test for win condition
    @patch('builtins.input', side_effect=['take torch', 'go east', 'go east', 'use torch', 'look', 'take ' + artifact_name]) # Removed 'inventory', 'quit'
    def test_win_condition_when_artifact_taken(self, mock_input): # Renamed for clarity
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main() # Should return after artifact is taken
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # 1. Initial messages and taking torch
        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output)
        self.assertIn("You took the torch.", output)

        # 2. Moving to treasure chamber
        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output)
        self.assertIn(app_main.initial_rooms_state['treasure_chamber']['description'], output) # Dark description

        # 3. Using the torch
        self.assertIn("You light the torch. The chamber brightens, revealing the Lost Artifact of Zyx!", output)
        self.assertTrue(app_main.rooms['treasure_chamber']['is_lit'])

        # 4. 'look' command output after lighting
        expected_look_output = (
            f"{app_main.rooms['treasure_chamber']['description']}\n" # This is the new, lit description
            "You see:\n"
            f" - a {artifact_name}"
        )
        self.assertIn(expected_look_output, output)

        # 5. 'take Lost Artifact of Zyx' and win condition
        self.assertIn(f"You took the {artifact_name}.", output)
        self.assertIn("Congratulations! You have found the Lost Artifact of Zyx! You are a true adventurer!", output)

        # 6. State checks after taking artifact
        self.assertIn(artifact_name, app_main.inventory)
        self.assertNotIn(artifact_name, app_main.rooms['treasure_chamber']['items'])

        # 7. Game should end; "inventory" command (which was removed from side_effect) should not be processed.
        #    Also, the "Exiting game." message (from "quit") should not be present.
        self.assertNotIn("You are carrying:", output.split("Congratulations!")[-1]) # Check output *after* win
        self.assertNotIn("Exiting game.", output)


    @patch('builtins.input', side_effect=['take torch', 'go east', 'go east', 'use torch', 'use torch', 'quit'])
    def test_use_torch_in_treasure_chamber_already_lit(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn("You took the torch.", output)
        self.assertIn("You light the torch. The chamber brightens, revealing the Lost Artifact of Zyx!", output) # First use
        self.assertTrue(app_main.rooms['treasure_chamber']['is_lit'])
        self.assertIn(artifact_name, app_main.rooms['treasure_chamber']['items']) # Artifact is still there

        self.assertIn("Nothing interesting happens.", output) # Second use
        self.assertIn("Exiting game.", output) # Game ends via 'quit'

    # --- New tests for case insensitivity and incomplete commands ---
    @patch('builtins.input', side_effect=['tAkE tOrCh', 'InvEnToRy', 'gO eAsT', 'lOoK', 'qUiT'])
    def test_case_insensitive_commands_and_items(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output) # Initial room
        self.assertIn("You took the torch.", output)
        self.assertIn('torch', app_main.inventory)
        self.assertNotIn('torch', app_main.rooms['entrance']['items'])

        self.assertIn("You are carrying:", output)
        self.assertIn("- a torch", output)

        self.assertIn(app_main.initial_rooms_state['hallway']['description'], output) # After 'gO eAsT'
        self.assertIn("You see no items of interest here.", output) # 'lOoK' in hallway

        self.assertIn("Exiting game.", output) # 'qUiT'

    @patch('builtins.input', side_effect=['go', 'quit'])
    def test_go_command_no_direction(self, mock_input):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        initial_description_first_line = app_main.initial_rooms_state['entrance']['description'].splitlines()[0]

        main()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Check initial room description is printed
        self.assertIn(app_main.initial_rooms_state['entrance']['description'], output)
        self.assertIn("Go where?", output)

        # Check that player is still in the entrance.
        # The "Go where?" is printed, then the loop continues and prints the prompt.
        # The next output from the game, after "Go where?" and before "Exiting game.",
        # should be the prompt from the *same room* if the room hasn't changed.
        # If main were to reprint the room description on a bad command, this would be easier.
        # For now, we check that the "Go where?" message is followed by "Exiting game."
        # without an intervening different room description.
        # A more robust check would be to see if current_room is still 'entrance'.
        self.assertEqual(app_main.current_room, 'entrance', "Player should remain in the entrance room.")

        # Check that the game eventually quits
        self.assertIn("Exiting game.", output)

        # Verify that "Go where?" appears before "Exiting game."
        self.assertTrue(output.find("Go where?") < output.find("Exiting game."))

        # Verify that no other room description appears after "Go where?" and before "Exiting game."
        # This is a bit tricky as main() prints current room desc at start of loop *after* input is processed (except for first print)
        # The input 'go' is processed, 'Go where?' is printed.
        # Then 'quit' is processed, 'Exiting game.' is printed, loop breaks.
        # So, no other room description should be printed.
        # The output structure is: InitialDesc, Prompt, "Go where?", Prompt, "Exiting game."
        # We can check that the description of another room (e.g. hallway) is not present after "Go where?"

        # Find the output after "Go where?"
        output_after_go_where = output.split("Go where?", 1)[1] if "Go where?" in output else ""
        self.assertNotIn(app_main.initial_rooms_state['hallway']['description'], output_after_go_where.split("Exiting game.")[0])


if __name__ == '__main__':
    unittest.main()
