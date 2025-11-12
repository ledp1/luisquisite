"""
Order handling logic for Luisquisite restaurant.
"""

from menu import MENU, get_menu_item, format_menu_for_display


class OrderHandler:
    def __init__(self):
        """Initialize order handler."""
        self.current_order = []
        self.greeting_said = False
    
    def process_input(self, text):
        """
        Process customer input and return appropriate response.
        
        Args:
            text: Customer's spoken input
            
        Returns:
            tuple: (response_text, should_continue)
        """
        if not text:
            return "I'm sorry, I didn't catch that. Could you repeat?", True
        
        text_lower = text.lower().strip()
        
        # Greeting
        if not self.greeting_said or any(word in text_lower for word in ["hola", "hello", "hi", "buenos"]):
            self.greeting_said = True
            greeting = (
                "¡Bienvenido a Luisquisite! Welcome to Luisquisite! "
                "I'm your robot waitress. How can I help you today? "
                "Would you like to see our menu?"
            )
            return greeting, True
        
        # Menu request
        if any(word in text_lower for word in ["menu", "menú", "dishes", "platos", "what do you have", "qué tienen"]):
            menu_text = format_menu_for_display()
            return menu_text, True
        
        # Ordering items
        order_keywords = ["quiero", "i want", "i'd like", "order", "pedir", "me gustaría", "dame", "give me"]
        if any(keyword in text_lower for keyword in order_keywords):
            return self._handle_order(text_lower), True
        
        # Confirming order
        if any(word in text_lower for word in ["yes", "sí", "confirm", "confirmar", "that's all", "eso es todo", "listo"]):
            if not self.current_order:
                return "You haven't ordered anything yet. What would you like?", True
            return self._confirm_order(), False
        
        # Canceling or starting over
        if any(word in text_lower for word in ["cancel", "cancelar", "start over", "empezar de nuevo", "no", "nada"]):
            self.current_order = []
            return "Order canceled. How can I help you?", True
        
        # Check current order
        if any(word in text_lower for word in ["what did i order", "qué pedí", "my order", "mi pedido"]):
            return self._get_current_order_summary(), True
        
        # Default response
        return (
            "I'm here to take your order. You can ask for the menu, "
            "order a dish, or say 'that's all' when you're done. What would you like?",
            True
        )
    
    def _handle_order(self, text):
        """Extract order items from text and add to current order."""
        found_items = []
        
        # Check for each menu item
        for item_key, item_data in MENU.items():
            item_name = item_data["name"].lower()
            # Check if item name or key is mentioned
            if item_key in text or item_name in text:
                found_items.append(item_data)
                self.current_order.append(item_data)
        
        if found_items:
            items_list = ", ".join([item["name"] for item in found_items])
            response = f"Great! I've added {items_list} to your order."
            if len(self.current_order) > len(found_items):
                response += f" Your order now has {len(self.current_order)} item(s)."
            response += " Anything else?"
            return response
        else:
            return (
                "I'm sorry, I didn't recognize that dish. "
                "Please ask for the menu if you'd like to see our options, "
                "or try ordering one of our dishes: salmon bowl, kiwi brunch, or tuna bowl."
            )
    
    def _get_current_order_summary(self):
        """Get summary of current order."""
        if not self.current_order:
            return "You haven't ordered anything yet."
        
        items = [item["name"] for item in self.current_order]
        if len(items) == 1:
            return f"Your order: {items[0]}."
        else:
            items_text = ", ".join(items[:-1]) + f", and {items[-1]}"
            return f"Your order: {items_text}."
    
    def _confirm_order(self):
        """Confirm the final order."""
        if not self.current_order:
            return "You haven't ordered anything yet."
        
        items = [item["name"] for item in self.current_order]
        items_text = ", ".join(items[:-1]) + f", and {items[-1]}" if len(items) > 1 else items[0]
        
        confirmation = (
            f"Perfect! Your order is confirmed: {items_text}. "
            f"Your order will be ready shortly. ¡Gracias por visitar Luisquisite! "
            f"Thank you for visiting Luisquisite!"
        )
        
        # Reset order for next customer
        self.current_order = []
        self.greeting_said = False
        
        return confirmation
    
    def reset(self):
        """Reset the order handler for a new customer."""
        self.current_order = []
        self.greeting_said = False


