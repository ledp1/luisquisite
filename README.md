# 🤖 Luisquisite Robot Waitress Voice Agent

A voice-powered AI waitress for Luisquisite restaurant in Cartagena, Colombia. This agent can take orders via voice commands in both Spanish and English.

## 🍽️ Menu

1. **Salmon Bowl**: Raw salmon, sushi rice, asparagus, avocado, broccoli
2. **Kiwi Brunch**: 3 kiwis, 3 raw oatmeal spoons, 2 fried eggs, 2 brazil nuts
3. **Tuna Bowl**: Raw tuna, sushi rice, beet, spinach, kale

## 🚀 Setup

### Prerequisites

- Python 3.7 or higher
- Microphone connected to your computer
- Internet connection (for speech recognition)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

**Note for macOS users**: If you encounter issues with PyAudio, you may need to install PortAudio first:
```bash
brew install portaudio
pip install pyaudio
```

**Note for Linux users**: You may need to install:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**Note for Windows users**: PyAudio should install directly, but if you have issues, download the appropriate wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio).

2. Run the voice agent:
```bash
python main.py
```

## 🎤 Usage

1. Start the program - the waitress will greet you
2. Speak your order naturally (e.g., "I'd like a salmon bowl")
3. Ask for the menu by saying "menu" or "menú"
4. Confirm your order by saying "that's all" or "eso es todo"
5. The waitress will confirm your order and you can place another or exit

### Example Interactions

- **Customer**: "Hola, can I see the menu?"
- **Waitress**: *Reads the menu*

- **Customer**: "I want a salmon bowl and a kiwi brunch"
- **Waitress**: "Great! I've added Salmon Bowl, Kiwi Brunch to your order. Anything else?"

- **Customer**: "That's all"
- **Waitress**: "Perfect! Your order is confirmed..."

## 🌍 Language Support

The agent supports both Spanish and English, perfect for Cartagena's international visitors!

## 🛠️ Technical Details

- **Speech Recognition**: Google Speech Recognition API (works offline with fallback)
- **Text-to-Speech**: pyttsx3 (offline TTS engine)
- **Language**: Configured for Colombian Spanish (es-CO) with English support

## 📝 Project Structure

```
luisquisite/
├── main.py              # Main entry point
├── voice_agent.py       # Speech recognition and TTS
├── order_handler.py     # Order processing logic
├── menu.py              # Menu configuration
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Customization

You can customize the menu in `menu.py` and adjust TTS settings (voice speed, volume) in `voice_agent.py`.

## ⚠️ Troubleshooting

- **Microphone not working**: Check your system's microphone permissions
- **Speech not recognized**: Speak clearly and ensure there's not too much background noise
- **PyAudio installation issues**: See installation notes above for platform-specific solutions

## 📄 License

This project is created for Luisquisite restaurant.


