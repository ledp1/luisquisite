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
            for entry in st.session_state.conversation_history:
                if entry['type'] == 'waitress':
                    st.markdown(f"""
                        <div class="waitress-message">
                            <strong>🤖 Waitress:</strong> {entry['text']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="customer-message">
                            <strong>👤 Customer:</strong> {entry['text']}
                        </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input section
    st.subheader("💬 Chat with the Waitress")
    st.write("Type your message below (e.g., 'Show me the menu', 'I'd like a salmon bowl', 'That's all')")
    
    # Text input
    user_input = st.text_input(
        "Your message:",
        placeholder="e.g., 'I'd like a salmon bowl' or 'Show me the menu'",
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
