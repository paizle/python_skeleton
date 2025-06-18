# app/main.py
from app.game_objects import Item, Room, Player
# sys, io might be needed if we add more complex output/input handling later,
# but for now, basic input() and print() are handled within Game.

class Game:
    def __init__(self):
        self.rooms: dict[str, Room] = {}
        self.player: Player | None = None # Will be initialized
        self.is_running: bool = False
        self.artifact_name: str = "Lost Artifact of Zyx"
        self.torch_name: str = "torch"
        self.key_name: str = "key"

        # This specific Item instance will be the one placed and won.
        self.the_true_artifact: Item | None = None

        self._setup_game()

    def _setup_game(self):
        # Create Items
        torch = Item(self.torch_name, "A sturdy wooden torch, unlit.")
        key = Item(self.key_name, "A small, ornate key.")
        # Define and store the one true artifact
        self.the_true_artifact = Item(self.artifact_name, "The legendary Lost Artifact of Zyx! It glows faintly.")

        # Create Rooms
        entrance = Room(
            name="Entrance",
            description="You are at the stone entrance of an ancient ruin. A passage leads east.",
            exits={"east": "Hallway"}
        )
        hallway = Room(
            name="Hallway",
            description="You are in a dusty hallway. Passages lead west, east, and north.",
            exits={"west": "Entrance", "east": "Treasure Chamber", "north": "Hidden Alcove"}
        )
        treasure_chamber = Room(
            name="Treasure Chamber",
            description="The treasure chamber is quite dark. It's hard to make out any details. A passage leads west.",
            exits={"west": "Hallway"},
            is_lit=False
        )
        hidden_alcove = Room(
            name="Hidden Alcove",
            description="A small, dark alcove. A passage leads south.",
            exits={"south": "Hallway"}
        )

        # Add items to rooms
        entrance.add_item(torch)
        hidden_alcove.add_item(key)
        # The true artifact is added to Treasure Chamber when lit, via process_command

        self.rooms = {
            entrance.name: entrance,
            hallway.name: hallway,
            treasure_chamber.name: treasure_chamber,
            hidden_alcove.name: hidden_alcove,
        }

        # Create Player
        self.player = Player(starting_room=entrance)

    def start(self):
        self.is_running = True
        if self.player: # Ensure player is initialized
            print(self.player.current_room.describe()) # Initial room description
        else:
            print("Error: Player not initialized.") # Should not happen if _setup_game works
            return

        while self.is_running:
            try:
                command_full = input("What do you do? ").strip()
                if command_full: # Process only if command is not empty
                    self.process_command(command_full)
                # If command is empty, loop continues, effectively re-prompting
            except EOFError:
                print("\nExiting game.") # Add newline for cleaner exit with EOF
                self.is_running = False
                break # Exit loop immediately

    def process_command(self, command_full: str):
        if not self.player: # Should not happen if game started correctly
            return

        parts = command_full.lower().split()
        action = parts[0] if parts else "" # Ensure action is not empty
        argument = " ".join(parts[1:]) if len(parts) > 1 else "" # argument can be empty string if no arg

        if action == "quit":
            print("Exiting game.")
            self.is_running = False
        elif action == "look":
            print(self.player.current_room.describe())
        elif action == "inventory" or action == "i":
            print(self.player.get_inventory_string())
        elif action == "go":
            if argument:
                if self.player.move(argument, self.rooms):
                    print(self.player.current_room.describe())
                else:
                    print("You can't go that way.")
            else:
                print("Go where?")
        elif action == "take":
            if argument:
                success, message, item_taken = self.player.take_item(argument)
                print(message)
                if success and item_taken and item_taken.name == self.artifact_name:
                    print("Congratulations! You have found the Lost Artifact of Zyx! You are a true adventurer!")
                    self.is_running = False # End game
            else:
                print("Take what?")
        elif action == "use":
            if argument:
                if not self.player.has_item(argument):
                    print(f"You don't have a {argument}.") # Use argument as it was typed for item name
                    return

                # Specific Torch logic in Treasure Chamber
                # argument is already lowercased from user input
                if argument == self.torch_name and self.player.current_room.name == "Treasure Chamber":
                    if not self.player.current_room.is_lit:
                        self.player.current_room.is_lit = True
                        if self.the_true_artifact: # Check if it was initialized
                             self.player.current_room.add_item(self.the_true_artifact)
                        self.player.current_room.description = "The torchlight illuminates the chamber, revealing intricate carvings on the walls. You see the Lost Artifact of Zyx gleaming in a niche! A passage leads west."
                        print("You light the torch. The chamber brightens, revealing the Lost Artifact of Zyx!")
                    else:
                        print("The Treasure Chamber is already lit.")
                # Example of how Player.use_item could be integrated if it had more complex return values or effects
                # else:
                #    message_from_player_use = self.player.use_item(argument, self) # Pass the game instance
                #    print(message_from_player_use)
                # For now, if not torch in treasure chamber:
                else:
                     print("Nothing interesting happens.")
            else:
                print("Use what?")
        else:
            print("Unknown command.")

def main():
    game = Game()
    game.start()

if __name__ == "__main__":
    main()
