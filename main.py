#!/usr/bin/env python3
"""
Main entry point for Luisquisite Robot Waitress Voice Agent.
"""

import sys
from voice_agent import VoiceAgent
from order_handler import OrderHandler


def main():
    """Main function to run the voice agent."""
    print("=" * 60)
    print("🤖 Luisquisite Robot Waitress - Voice Agent")
    print("📍 Cartagena, Colombia")
    print("=" * 60)
    print()
    
    try:
        # Initialize components
        voice_agent = VoiceAgent()
        order_handler = OrderHandler()
        
        # Welcome message
        welcome_msg = (
            "¡Bienvenido a Luisquisite! Welcome to Luisquisite! "
            "I'm your robot waitress. How can I help you today?"
        )
        voice_agent.speak(welcome_msg)
        
        # Main conversation loop
        continue_conversation = True
        while continue_conversation:
            # Listen for customer input
            customer_input = voice_agent.listen(timeout=10, phrase_time_limit=15)
            
            # Process input and get response
            response, continue_conversation = order_handler.process_input(customer_input)
            
            # Speak the response
            voice_agent.speak(response)
            
            # If order is confirmed, ask if they want to place another order
            if not continue_conversation:
                voice_agent.speak("Would you like to place another order? Say 'yes' to continue or 'no' to exit.")
                another_order = voice_agent.listen(timeout=10, phrase_time_limit=10)
                
                if another_order and any(word in another_order.lower() for word in ["yes", "sí", "si"]):
                    order_handler.reset()
                    continue_conversation = True
                    voice_agent.speak("Great! How can I help you?")
                else:
                    voice_agent.speak("Thank you! Have a wonderful day! ¡Hasta luego!")
                    break
        
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")
        voice_agent.speak("Goodbye! Have a wonderful day!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


