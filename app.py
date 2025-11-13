"""
Streamlit web app for Luisquisite Robot Waitress Voice Agent.
This provides a browser-based interface for testing the voice agent.
"""

import streamlit as st
from order_handler import OrderHandler
from menu import MENU, format_menu_for_display

# Page configuration
st.set_page_config(
    page_title="Luisquisite Robot Waitress",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'order_handler' not in st.session_state:
    st.session_state.order_handler = OrderHandler()
    st.session_state.conversation_history = []
    st.session_state.order_handler.greeting_said = True  # Skip greeting in web version

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .waitress-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    .customer-message {
        background-color: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #9c27b0;
        margin: 1rem 0;
    }
    .order-summary {
        background-color: #fff3e0;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #ff9800;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="main-header">
        <h1>🤖 Luisquisite Robot Waitress</h1>
        <p>📍 Cartagena, Colombia | Voice-Powered Ordering System</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar with menu
with st.sidebar:
    st.header("🍽️ Menu")
    for key, item in MENU.items():
        with st.expander(f"**{item['name']}**"):
            st.write(item['description'])
    
    st.markdown("---")
    st.header("📋 Current Order")
    current_order = st.session_state.order_handler.current_order
    if current_order:
        for idx, item in enumerate(current_order, 1):
            st.write(f"{idx}. {item['name']}")
    else:
        st.write("No items yet")
    
    if st.button("🔄 Start New Order", use_container_width=True):
        st.session_state.order_handler.reset()
        st.session_state.conversation_history = []
        st.rerun()

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Conversation")
    
    # Display conversation history
    conversation_container = st.container()
    with conversation_container:
        if not st.session_state.conversation_history:
            welcome_msg = "¡Bienvenido a Luisquisite! Welcome to Luisquisite! I'm your robot waitress. How can I help you today? Would you like to see our menu?"
            st.markdown(f"""
                <div class="waitress-message">
                    <strong>🤖 Waitress:</strong> {welcome_msg}
                </div>
            """, unsafe_allow_html=True)
        else:
            for idx, entry in enumerate(st.session_state.conversation_history):
                if entry['type'] == 'waitress':
                    # Add TTS button for waitress messages
                    message_id = f"waitress_msg_{idx}"
                    st.markdown(f"""
                        <div class="waitress-message" id="{message_id}">
                            <strong>🤖 Waitress:</strong> {entry['text']}
                            <button onclick="speakText('{entry['text'].replace("'", "\\'")}', '{message_id}')" 
                                    style="float: right; background: #2196f3; color: white; border: none; 
                                           border-radius: 4px; padding: 0.25rem 0.5rem; cursor: pointer; 
                                           font-size: 0.8rem; margin-left: 0.5rem;">
                                🔊 Speak
                            </button>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="customer-message">
                            <strong>👤 Customer:</strong> {entry['text']}
                        </div>
                    """, unsafe_allow_html=True)
    
    # Add TTS JavaScript
    st.components.v1.html("""
    <script>
        function speakText(text, elementId) {
            if ('speechSynthesis' in window) {
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'es-CO'; // Spanish (Colombia) with English fallback
                utterance.rate = 0.9;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                // Try to find a Spanish voice
                const voices = window.speechSynthesis.getVoices();
                const spanishVoice = voices.find(voice => 
                    voice.lang.startsWith('es') || voice.lang.includes('Spanish')
                );
                if (spanishVoice) {
                    utterance.voice = spanishVoice;
                }
                
                utterance.onstart = function() {
                    const btn = document.querySelector(`#${elementId} button`);
                    if (btn) {
                        btn.textContent = '⏸️ Speaking...';
                        btn.style.background = '#4caf50';
                    }
                };
                
                utterance.onend = function() {
                    const btn = document.querySelector(`#${elementId} button`);
                    if (btn) {
                        btn.textContent = '🔊 Speak';
                        btn.style.background = '#2196f3';
                    }
                };
                
                utterance.onerror = function(event) {
                    const btn = document.querySelector(`#${elementId} button`);
                    if (btn) {
                        btn.textContent = '🔊 Speak';
                        btn.style.background = '#2196f3';
                    }
                    console.error('Speech synthesis error:', event);
                };
                
                window.speechSynthesis.speak(utterance);
            } else {
                alert('Text-to-speech is not supported in this browser.');
            }
        }
        
        // Load voices when available
        if ('speechSynthesis' in window) {
            window.speechSynthesis.onvoiceschanged = function() {
                // Voices loaded
            };
        }
    </script>
    """, height=0)
    
    st.markdown("---")
    
    # Input section
    st.subheader("💬 Chat with the Waitress")
    st.write("🎤 **Speak your order** or type your message below")
    
    # Voice input JavaScript component - injects into text input
    st.components.v1.html("""
    <div style="margin-bottom: 1rem;">
        <button id="voiceBtn" style="
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            margin-bottom: 0.5rem;
            font-weight: bold;
        ">🎤 Click to Speak</button>
        <div id="status" style="text-align: center; color: #666; font-size: 0.9rem; min-height: 1.5rem;"></div>
    </div>
    <script>
        (function() {
            const voiceBtn = document.getElementById('voiceBtn');
            const status = document.getElementById('status');
            let recognition = null;
            let isListening = false;
            
            // Find the Streamlit text input
            function findTextInput() {
                const inputs = document.querySelectorAll('input[type="text"]');
                for (let input of inputs) {
                    if (input.placeholder && input.placeholder.includes('salmon bowl')) {
                        return input;
                    }
                }
                // Fallback: find last text input
                return inputs[inputs.length - 1];
            }
            
            // Check if browser supports speech recognition
            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                recognition = new SpeechRecognition();
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.lang = 'es-CO,en-US'; // Spanish (Colombia) and English
                
                recognition.onstart = function() {
                    isListening = true;
                    voiceBtn.textContent = '🛑 Listening... Click to Stop';
                    voiceBtn.style.background = 'linear-gradient(90deg, #f44336 0%, #e91e63 100%)';
                    status.textContent = '🎤 Listening... Speak now!';
                    status.style.color = '#f44336';
                };
                
                recognition.onresult = function(event) {
                    const transcript = event.results[0][0].transcript;
                    const textInput = findTextInput();
                    if (textInput) {
                        textInput.value = transcript;
                        // Trigger input event to update Streamlit
                        textInput.dispatchEvent(new Event('input', { bubbles: true }));
                        textInput.dispatchEvent(new Event('change', { bubbles: true }));
                    }
                    status.textContent = '✅ Heard: "' + transcript + '" - Click Send to submit';
                    status.style.color = '#4caf50';
                };
                
                recognition.onerror = function(event) {
                    status.textContent = '❌ Error: ' + event.error + ' (Make sure to allow microphone access)';
                    status.style.color = '#f44336';
                    isListening = false;
                    voiceBtn.textContent = '🎤 Click to Speak';
                    voiceBtn.style.background = 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)';
                };
                
                recognition.onend = function() {
                    isListening = false;
                    voiceBtn.textContent = '🎤 Click to Speak';
                    voiceBtn.style.background = 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)';
                    if (status.textContent.indexOf('Heard:') === -1 && status.textContent.indexOf('Error') === -1) {
                        status.textContent = '⏹️ Stopped listening';
                        status.style.color = '#666';
                    }
                };
                
                voiceBtn.addEventListener('click', function() {
                    if (isListening) {
                        recognition.stop();
                    } else {
                        status.textContent = '🎤 Starting...';
                        status.style.color = '#667eea';
                        try {
                            recognition.start();
                        } catch(e) {
                            status.textContent = '❌ Error: ' + e.message;
                            status.style.color = '#f44336';
                        }
                    }
                });
            } else {
                voiceBtn.textContent = '❌ Voice not supported in this browser';
                voiceBtn.disabled = true;
                voiceBtn.style.background = '#ccc';
                status.textContent = 'Please use Chrome, Edge, or Safari for voice input';
                status.style.color = '#f44336';
            }
        })();
    </script>
    """, height=100)
    
    # Text input (populated by voice or manual entry)
    user_input = st.text_input(
        "Your message:",
        placeholder="e.g., 'I'd like a salmon bowl' or 'Show me the menu' (or use voice input above)",
        key="text_input",
        label_visibility="collapsed"
    )
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("📤 Send", use_container_width=True, type="primary"):
            if user_input:
                # Process the input
                response, should_continue = st.session_state.order_handler.process_input(user_input)
                
                # Update conversation history
                st.session_state.conversation_history.append({
                    'type': 'customer',
                    'text': user_input
                })
                st.session_state.conversation_history.append({
                    'type': 'waitress',
                    'text': response
                })
                
                # Clear input
                st.session_state.text_input = ""
                
                # If order confirmed, reset for next order
                if not should_continue:
                    st.session_state.order_handler.reset()
                
                st.rerun()
    
    with col_btn2:
        if st.button("📋 Show Menu", use_container_width=True):
            menu_text = format_menu_for_display()
            st.session_state.conversation_history.append({
                'type': 'customer',
                'text': 'Show me the menu'
            })
            st.session_state.conversation_history.append({
                'type': 'waitress',
                'text': menu_text
            })
            st.rerun()

with col2:
    st.header("📊 Order Status")
    
    current_order = st.session_state.order_handler.current_order
    if current_order:
        st.markdown("""
            <div class="order-summary">
        """, unsafe_allow_html=True)
        
        total_items = len(current_order)
        st.metric("Items in Order", total_items)
        
        st.write("**Order Details:**")
        for idx, item in enumerate(current_order, 1):
            st.write(f"{idx}. **{item['name']}**")
            st.caption(item['description'])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("✅ Confirm Order", use_container_width=True, type="primary"):
            confirmation = st.session_state.order_handler._confirm_order()
            st.session_state.conversation_history.append({
                'type': 'customer',
                'text': 'That\'s all'
            })
            st.session_state.conversation_history.append({
                'type': 'waitress',
                'text': confirmation
            })
            st.session_state.order_handler.reset()
            st.rerun()
    else:
        st.info("No items in your order yet. Start ordering to see them here!")
    
    st.markdown("---")
    st.subheader("💡 Quick Actions")
    if st.button("❓ What did I order?", use_container_width=True):
        summary = st.session_state.order_handler._get_current_order_summary()
        st.session_state.conversation_history.append({
            'type': 'customer',
            'text': 'What did I order?'
        })
        st.session_state.conversation_history.append({
            'type': 'waitress',
            'text': summary
        })
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 Luisquisite Robot Waitress | Built with Streamlit</p>
        <p>Supports English and Spanish (Español) | <a href="https://github.com/ledp1/luisquisite" target="_blank">View on GitHub</a></p>
    </div>
""", unsafe_allow_html=True)
