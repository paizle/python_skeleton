# app/main.py
import copy # For deep copying rooms for test resets

artifact_name = "Lost Artifact of Zyx"

initial_rooms_state = {
    'entrance': {
        'name': "Ancient Entrance",
        'description': "You are at the stone entrance of an ancient ruin. A passage leads east.",
        'exits': {"east": "hallway"},
        'items': ['torch']
    },
    'hallway': {
        'name': "Dusty Hallway",
        'description': "You are in a dusty hallway. Passages lead west, east, and north.",
        'exits': {"west": "entrance", "east": "treasure_chamber", "north": "hidden_alcove"},
        'items': []
    },
    'treasure_chamber': {
        'name': "Treasure Chamber",
        'description': "The treasure chamber is quite dark. It's hard to make out any details. A passage leads west.",
        'exits': {"west": "hallway"},
        'items': [],
        'is_lit': False
    },
    'hidden_alcove': {
        'name': "Hidden Alcove",
        'description': "A small, dark alcove. A passage leads south.",
        'exits': {"south": "hallway"},
        'items': ['key']
    }
}
rooms = copy.deepcopy(initial_rooms_state) # Use a deep copy to allow resetting for tests

current_room = 'entrance'
inventory = []

def main():
    global current_room, inventory, rooms # Ensure we can modify global variables

    print(rooms[current_room]['description'])

    while True:
        user_input = input("What do you do? ").strip().lower()
        parts = user_input.split()
        action = parts[0] if parts else ""
        # Handle multi-word item names by joining parts after the action
        item_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        if user_input == "quit":
            print("Exiting game.")
            break
        elif user_input == "look" or user_input == "look around":
            print(rooms[current_room]['description'])
            if rooms[current_room]['items']:
                print("You see:")
                for item in rooms[current_room]['items']:
                    print(f" - a {item}") # Standardized "a" prefix
            else:
                print("You see no items of interest here.")
        elif action == "go":
            if item_name: # Here item_name is actually the direction
                direction = item_name
                if direction in rooms[current_room]['exits']:
                    current_room = rooms[current_room]['exits'][direction]
                    print(rooms[current_room]['description'])
                else:
                    print("You can't go that way.")
            else:
                print("Go where?")
        elif action == "take":
            if item_name:
                found_item = None
                for room_item in rooms[current_room]['items']:
                    if room_item.lower() == item_name:
                        found_item = room_item
                        break
                if found_item:
                    rooms[current_room]['items'].remove(found_item)
                    inventory.append(found_item) # Add original cased item to inventory
                    print(f"You took the {found_item}.")
                    if found_item == artifact_name:
                        print("Congratulations! You have found the Lost Artifact of Zyx! You are a true adventurer!")
                        return # End the game
                else:
                    print(f"You don't see a {item_name} here.")
            else:
                print("Take what?")
        elif user_input == "inventory" or user_input == "i":
            if not inventory:
                print("You are not carrying anything.")
            else:
                print("You are carrying:")
                for item in inventory:
                    print(f" - a {item}") # Standardized "a" prefix
        elif action == "use":
            if not item_name:
                print("Use what?")
            else:
                item_in_inventory = None
                for inv_item in inventory:
                    if inv_item.lower() == item_name:
                        item_in_inventory = inv_item
                        break
                if not item_in_inventory:
                    print(f"You don't have a {item_name}.")
                else:
                    # Puzzle specific logic - use item_in_inventory for checks (original case)
                    if current_room == 'treasure_chamber' and item_in_inventory == 'torch' and not rooms[current_room]['is_lit']:
                        rooms[current_room]['is_lit'] = True
                        rooms[current_room]['items'].append(artifact_name)
                        new_description = "The torchlight illuminates the chamber, revealing intricate carvings on the walls. You see the Lost Artifact of Zyx gleaming in a niche! A passage leads west."
                        rooms[current_room]['description'] = new_description
                        print("You light the torch. The chamber brightens, revealing the Lost Artifact of Zyx!")
                        # Optional: remove torch if consumed: inventory.remove(item_in_inventory)
                    else: # This else is for the puzzle condition
                        print("Nothing interesting happens.")
        else: # This else is for unknown commands
            print("Unknown command.")

if __name__ == '__main__':
    main()
