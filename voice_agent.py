"""
Voice Agent for Luisquisite Robot Waitress.
Handles speech recognition and text-to-speech.
"""

import speech_recognition as sr
import pyttsx3
import threading
import queue


class VoiceAgent:
    def __init__(self):
        """Initialize the voice agent with speech recognition and TTS."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # Configure TTS
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready to listen!")
    
    def speak(self, text):
        """Convert text to speech and speak it."""
        print(f"🤖 Waitress: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen for voice input and return transcribed text.
        
        Args:
            timeout: Maximum seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for a phrase
            
        Returns:
            str: Transcribed text or None if no speech detected
        """
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing speech...")
            try:
                # Use Google's speech recognition (works offline with fallback)
                text = self.recognizer.recognize_google(audio, language='es-CO')
                print(f"👤 Customer: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"❌ Error with speech recognition service: {e}")
                return None
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected within timeout")
            return None
        except Exception as e:
            print(f"❌ Error listening: {e}")
            return None


