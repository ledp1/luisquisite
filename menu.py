"""
Menu configuration for Luisquisite restaurant.
"""

MENU = {
    "salmon bowl": {
        "name": "Salmon Bowl",
        "description": "Raw salmon, sushi rice, asparagus, avocado, broccoli",
        "price": 0,  # Price can be added later
        "ingredients": ["raw salmon", "sushi rice", "asparagus", "avocado", "broccoli"]
    },
    "kiwi brunch": {
        "name": "Kiwi Brunch",
        "description": "3 kiwis, 3 raw oatmeal spoons, 2 fried eggs, 2 brazil nuts",
        "price": 0,
        "ingredients": ["3 kiwis", "3 raw oatmeal spoons", "2 fried eggs", "2 brazil nuts"]
    },
    "tuna bowl": {
        "name": "Tuna Bowl",
        "description": "Raw tuna, sushi rice, beet, spinach, kale",
        "price": 0,
        "ingredients": ["raw tuna", "sushi rice", "beet", "spinach", "kale"]
    }
}

def get_menu_items():
    """Return list of menu item names."""
    return list(MENU.keys())

def get_menu_item(item_name):
    """Get menu item by name (case-insensitive)."""
    item_name_lower = item_name.lower().strip()
    return MENU.get(item_name_lower)

def format_menu_for_display():
    """Format menu for voice announcement."""
    items = []
    for key, item in MENU.items():
        items.append(f"{item['name']}: {item['description']}")
    return "Here is our menu today: " + ". ".join(items) + "."


