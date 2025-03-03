import streamlit as st

def customersupportbot_ui():
    # Modern gradient background with professional color scheme
    st.markdown(
        """
        <style>
            .main {
                background: linear-gradient(to right, #2c3e50, #3498db);
                color: white;
                padding: 20px;
            }
            .user-message {
                background: #2980b9;
                border-radius: 15px;
                padding: 12px;
                margin: 5px 0;
                max-width: 80%;
                float: right;
                clear: both;
            }
            .bot-message {
                background: #34495e;
                border-radius: 15px;
                padding: 12px;
                margin: 5px 0;
                max-width: 80%;
                float: left;
                clear: both;
            }
            .stButton>button {
                background: #27ae60;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            .stTextInput>div>div>input {
                background: #ecf0f1;
                border-radius: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Main header with service-oriented messaging
    st.markdown("<h1 style='text-align: center;'>🛎️ Customer Support Hub 🧑💻</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>24/7 assistance for all your needs. Ask me anything!</p>", unsafe_allow_html=True)

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Split layout into 3 columns for different functionalities
    col1, col2 = st.columns(2)

    with col1:
        # Travel Assistance Ticket System
        st.subheader("🎫 Request Travel Assistance")
        ticket_type = st.radio("Issue Type:", ["Flight Booking", "Hotel Reservation", "Baggage Issues", "Visa Assistance", "Travel Insurance", "Other"])
        ticket_desc = st.text_area("Describe your issue:")
        if st.button("Submit Request"):
            if ticket_desc:
                st.success(f"Request submitted for {ticket_type} issue!")
                st.session_state.chat_history.append({
                    'type': 'bot',
                    'content': f"Request submitted: {ticket_type} - Reference #:{hash(ticket_desc) % 100000}"
                })

    with col2:
        # Main chat interface
        st.subheader("💬 Live Chat")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['type'] == 'user':
                st.markdown(f"<div class='user-message'>👤 You: {message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='bot-message'>🤖 Bot: {message['content']}</div>", unsafe_allow_html=True)
        
        # Chat input with send button
        user_input = st.text_input("Type your message here...", key="chat_input")
        if st.button("Send"):
            if user_input:
                st.session_state.chat_history.append({'type': 'user', 'content': user_input})
                # Simulate bot response (replace with actual API call)
                bot_response = "Thank you for your question. Our team will get back to you shortly."
                st.session_state.chat_history.append({'type': 'bot', 'content': bot_response})



    # FAQ Section
    st.subheader("📖 Frequently Asked Questions")

    faq_data = {
        "How do I reset my password?": "To reset your password, go to the login page and click on 'Forgot Password'. Enter your registered email address, and we will send you a password reset link. Follow the instructions in the email to create a new password.",
        "How can I update my payment method?": "To update your payment method, navigate to 'Account Settings' > 'Payment Methods'. Here, you can add a new card, remove an old one, or update your existing payment details. Make sure your payment method is valid and up to date to avoid transaction issues.",
        "How do I track my order?": "You can track your order by going to the 'Order History' section in your account. Click on the specific order to view tracking details, including estimated delivery time and courier service information.",
        "What is the refund policy?": "Our refund policy allows you to request a refund within 30 days of purchase. To initiate a refund, go to 'Order History', select the order, and click 'Request Refund'. Refunds are processed within 5-7 business days back to your original payment method.",
        "How can I contact customer support?": "You can reach our support team through multiple channels: Live chat (available 24/7), email (support@example.com), or phone (123-456-7890). Our customer service representatives are happy to assist you with any issues.",
        "Why was my payment declined?": "There could be several reasons why your payment was declined: incorrect card details, insufficient funds, expired card, or restrictions from your bank. Try using a different payment method or contact your bank for further assistance.",
        "How do I change my account email?": "To change your email address, go to 'Account Settings' > 'Email'. You will need to verify your new email address before the change is applied to your account.",
        "How do I book a flight?": "To book a flight, go to our 'Flights' section and enter your departure and destination cities, travel dates, and number of passengers. Browse the available flights and select the one that suits you best. Complete the payment, and you will receive your e-ticket via email.",
        "What should I do if my flight is delayed or canceled?": "If your flight is delayed or canceled, check your email and phone for updates from the airline. You may be eligible for a refund or rebooking. Contact the airline directly or visit our 'Manage Booking' section for assistance.",
        "How can I modify or cancel my hotel reservation?": "To modify or cancel your hotel reservation, go to the 'My Bookings' section in your account. Select the hotel reservation and choose the modify/cancel option. Cancellation policies vary, so check the terms before proceeding.",
        "What documents do I need for international travel?": "For international travel, you generally need a valid passport, visa (if required), travel insurance, and any necessary health documents like vaccination certificates. Check the embassy website of your destination country for specific requirements.",
        "How do I claim lost baggage?": "If your baggage is lost, immediately report it to the airline’s baggage claim desk at the airport. Provide your flight details and baggage tag number. Most airlines provide compensation for lost luggage and assist in tracking it down.",
        "What travel insurance options do you offer?": "We offer a range of travel insurance options, including trip cancellation coverage, medical emergency coverage, and lost baggage protection. You can purchase travel insurance during the booking process or from the 'Travel Insurance' section on our website."
    }

    question = st.selectbox("Select a question", ["Select a question"] + list(faq_data.keys()))

    if question != "Select a question":
        st.markdown(f"**Answer:** {faq_data[question]}")











    # Footer with additional resources
    st.markdown("---")
    st.markdown("📞 Contact us: 24/7 Support Hotline | 📧 Email: support@company.com")

