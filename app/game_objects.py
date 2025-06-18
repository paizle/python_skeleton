from typing import TYPE_CHECKING, Optional, List # Added List for type hint

if TYPE_CHECKING:
    from app.main import Game # Forward reference for Game class

class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __repr__(self): # For easier debugging
        return f"Item({self.name!r})"

class Room:
    def __init__(self, name: str, description: str, exits: dict[str, str], is_lit: bool = True):
        self.name = name
        self.description = description
        self.exits = exits  # e.g., {"north": "another_room_name"}
        self.items: List[Item] = []  # Will be populated with Item objects - Changed to List[Item]
        self.is_lit = is_lit # True by default, False for special rooms like Treasure Chamber initially

    def add_item(self, item: Item):
        self.items.append(item)

    def remove_item(self, item_name: str) -> Optional[Item]: # Changed return type hint
        for i, item_in_room in enumerate(self.items):
            if item_in_room.name.lower() == item_name.lower():
                return self.items.pop(i)
        return None

    def describe(self) -> str:
        description_parts = [self.description]
        if not self.is_lit:
            pass
        elif self.items:
            description_parts.append("You see:")
            for item in self.items:
                description_parts.append(f" - a {item.name}")
        else:
            description_parts.append("You see no items of interest here.")
        return "\n".join(description_parts)

    def __repr__(self): # For easier debugging
        return f"Room({self.name!r})"

class Player:
    def __init__(self, starting_room: Room):
        self.current_room: Room = starting_room
        self.inventory: List[Item] = [] # Changed to List[Item]

    def move(self, direction: str, all_rooms: dict[str, Room]) -> bool:
        room_name_or_id = self.current_room.exits.get(direction.lower())
        if room_name_or_id:
            next_room = all_rooms.get(room_name_or_id)
            if next_room:
                self.current_room = next_room
                return True
        return False

    def take_item(self, item_name: str) -> tuple[bool, str, Optional[Item]]:
        item_to_take = self.current_room.remove_item(item_name)
        if item_to_take:
            self.inventory.append(item_to_take)
            return True, f"You took the {item_to_take.name}.", item_to_take
        return False, f"You don't see that item here.", None

    def get_inventory_string(self) -> str:
        if not self.inventory:
            return "You are not carrying anything."
        inventory_list_str = "\n".join([f" - a {item.name}" for item in self.inventory])
        return f"You are carrying:\n{inventory_list_str}"

    def has_item(self, item_name: str) -> bool:
        return any(item.name.lower() == item_name.lower() for item in self.inventory)

    def use_item(self, item_name: str, game: 'Game') -> str:
        if not self.has_item(item_name):
            return f"You don't have a {item_name}."

        # Using item_name.lower() for consistent checks
        normalized_item_name = item_name.lower()

        if normalized_item_name == 'torch':
            # Using current_room.name for room identification as per Room class
            if self.current_room.name == 'Treasure Chamber': # Assuming 'Treasure Chamber' is the exact name string
                if not self.current_room.is_lit:
                    # The Game class will handle changing room state and adding artifact via game.light_treasure_chamber() or similar
                    return "You are about to use the torch in the Treasure Chamber."
                else:
                    return "The Treasure Chamber is already lit."
            else:
                return "This isn't the best place to use the torch."
        return "Nothing interesting happens."

    def __repr__(self): # For easier debugging
        return f"Player(current_room={self.current_room.name!r})"
