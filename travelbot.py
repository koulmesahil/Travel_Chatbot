import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import time






def travelbot_ui():
    # Custom CSS Styling for an Elegant UI
    st.markdown(
        """
        <style>
            .main {
                background: linear-gradient(to bottom, #1e3c72, #2a5298); 
                background-size: cover;
                background-attachment: fixed;
                color: white;
                padding: 20px;
            }
            .chat-message {
                background-color: #a0d1e7;
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            }
            .invisible-button {
                background-color: transparent;
                border: none;
                cursor: pointer;
                display: block;
                width: 100%;
                height: auto;
            }
            .invisible-button img {
                width: 100%;
                border-radius: 10px;
            }
            .caption {
                text-align: center;
                font-size: 18px;
                margin-top: 10px;
                font-weight: bold;
            }


        </style>
        """,
        unsafe_allow_html=True
    )

    # Travel Header with a Hero Image
    #st.image("images/travel_beach_mountains.jpg", use_container_width =True)
    st.markdown("<h1 style='text-align: center;'>🌍 Welcome to Travelbot! 🛫</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Ask me anything about travel destinations, tips, and bookings.</p>", unsafe_allow_html=True)

    # Popular Destinations with Card Layout
    st.subheader("Explore Popular Destinations")
    # List of images and captions
    images = [
        "images/paris.jpg", "images/bali.jpg", "images/tokyo.jpg", "images/nyc.jpg",
        "images/rome.jpg", "images/sydney.jpg", "images/kyoto.jpg", "images/london.jpg",
        "images/cape_town.jpg", "images/istanbul.jpg", "images/barcelona.jpg", "images/amsterdam.jpg"
    ]

    captions = [
        "Paris, France\nA city of love, lights, and stunning architecture.",
        "Bali, Indonesia\nA paradise of beaches, temples, and lush landscapes.",
        "Tokyo, Japan\nA futuristic blend of culture, technology, and food.",
        "New York, USA\nThe city that never sleeps, full of energy and attractions.",
        "Rome, Italy\nThe Eternal City, rich in history and ancient ruins.",
        "Sydney, Australia\nFamous for its Opera House, beaches, and vibrant culture.",
        "Kyoto, Japan\nA city steeped in tradition with beautiful temples and gardens.",
        "London, UK\nA dynamic city known for its history, culture, and landmarks.",
        "Cape Town, South Africa\nA coastal city with stunning landscapes and diverse culture.",
        "Istanbul, Turkey\nA city where East meets West, rich in history and culture.",
        "Barcelona, Spain\nA city known for its art, architecture, and Mediterranean vibes.",
        "Amsterdam, Netherlands\nA picturesque city filled with canals, museums, and cycling culture."
    ]

    # Initialize session state for image index
    if 'image_index' not in st.session_state:
        st.session_state.image_index = 0

    # Current image index
    image_index = st.session_state.image_index

    # Create two columns for displaying images side by side
    col1, col2 = st.columns(2)

    with col1:
        st.image(images[image_index], caption=captions[image_index], use_container_width=True)

    with col2:
        next_index = (image_index + 1) % len(images)  # Next image in the list (looping back)
        st.image(images[next_index], caption=captions[next_index], use_container_width=True)

    # Add navigation arrows using columns for positioning
    col3, col4, col5 = st.columns([1, 5, 1])

    with col3:
        if st.button("←"):
            st.session_state.image_index = (image_index - 1) % len(images)  # Previous image

    with col5:
        if st.button("→"):
            st.session_state.image_index = (image_index + 1) % len(images)  # Next image


# No need for rerun; Stre
    def calculate_weighted_score(answers):
        # Initialize category scores
        category_scores = {
            "Beaches & Relaxation": 0,
            "History & Culture": 0,
            "Adventure & Nature": 0,
            "City Life & Shopping": 0
        }

        # Weighted scoring system
        weighted_map = {
            "Lazing on the beach with a good book": {"Beaches & Relaxation": 1.0},
            "Visiting historic landmarks and museums": {"History & Culture": 0.8, "City Life & Shopping": 0.2},
            "Hiking or exploring nature": {"Adventure & Nature": 0.9, "History & Culture": 0.1},
            "Shopping and exploring city life": {"City Life & Shopping": 1.0},

            "Tropical and warm": {"Beaches & Relaxation": 0.9, "Adventure & Nature": 0.1},
            "Mediterranean or temperate": {"History & Culture": 0.7, "City Life & Shopping": 0.3},
            "Cold or mountain climates": {"Adventure & Nature": 0.9, "History & Culture": 0.1},
            "Mild and urban climates": {"City Life & Shopping": 0.8, "History & Culture": 0.2},

            "Seafood and tropical fruits": {"Beaches & Relaxation": 1.0},
            "Italian, Greek, and Mediterranean cuisines": {"History & Culture": 0.9, "City Life & Shopping": 0.1},
            "Barbecue, fresh produce, and local delicacies": {"Adventure & Nature": 0.8, "History & Culture": 0.2},
            "Street food, sushi, and trendy cafés": {"City Life & Shopping": 0.9, "History & Culture": 0.1},

            "Relaxing by the beach or a spa": {"Beaches & Relaxation": 1.0},
            "Visiting ancient ruins and landmarks": {"History & Culture": 0.9, "Adventure & Nature": 0.1},
            "Outdoor adventure activities": {"Adventure & Nature": 1.0},
            "Exploring a vibrant city with lots of shopping": {"City Life & Shopping": 1.0},

            "By beach resort with luxury amenities": {"Beaches & Relaxation": 1.0},
            "With a cultural guide for historical tours": {"History & Culture": 1.0},
            "Through remote, off-the-beaten-path destinations": {"Adventure & Nature": 1.0},
            "By city tour and shopping spree": {"City Life & Shopping": 1.0}
        }

        # Iterate through answers and apply weighted scoring
        for answer in answers:
            if answer in weighted_map:
                for category, weight in weighted_map[answer].items():
                    category_scores[category] += weight  # Add weighted value

        return category_scores

    map_center = [30.0, 40.0]  # Center of the map
    m = folium.Map(location=map_center, zoom_start=1.5, tiles='CartoDB dark_matter')

    # Add marker cluster for performance
    marker_cluster = MarkerCluster().add_to(m)
    destinations = [
        {"name": "Rome", "lat": 41.9028, "lon": 12.4964, "info": "Capital of Italy, famous for its ancient history."},
        {"name": "Santorini", "lat": 36.3932, "lon": 25.4615, "info": "A beautiful island in Greece known for its whitewashed buildings."},
        {"name": "Kyoto", "lat": 35.0116, "lon": 135.7681, "info": "Historical city in Japan, full of temples and gardens."},
        {"name": "Cape Town", "lat": -33.9249, "lon": 18.4241, "info": "A stunning coastal city in South Africa."},
        {"name": "New York", "lat": 40.7128, "lon": -74.0060, "info": "The bustling metropolis known for its iconic skyline."},
        {"name": "Paris", "lat": 48.8566, "lon": 2.3522, "info": "The City of Light, famous for the Eiffel Tower and art."},
        {"name": "Sydney", "lat": -33.8688, "lon": 151.2093, "info": "Australia's largest city known for the Opera House."},
        {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729, "info": "A vibrant city in Brazil, home to the Christ the Redeemer statue."},
        {"name": "Istanbul", "lat": 41.0082, "lon": 28.9784, "info": "A city that straddles two continents, rich in history and culture."},
        {"name": "Dubai", "lat": 25.276987, "lon": 55.296249, "info": "A modern city known for its towering skyscrapers and luxury shopping."},
        {"name": "Barcelona", "lat": 41.3784, "lon": 2.1915, "info": "A cultural hub in Spain, famous for architecture by Gaudi."},
        {"name": "Bangkok", "lat": 13.7563, "lon": 100.5018, "info": "The capital city of Thailand, known for vibrant street life."},
        {"name": "London", "lat": 51.5074, "lon": -0.1278, "info": "The capital of the UK, famous for its landmarks and history."},
        {"name": "Moscow", "lat": 55.7558, "lon": 37.6173, "info": "Capital city of Russia, rich in history and culture."},
        {"name": "Cairo", "lat": 30.0444, "lon": 31.2357, "info": "The capital of Egypt, home to the Pyramids of Giza."},
        {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437, "info": "The entertainment capital of the world, home to Hollywood."},
        {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694, "info": "A bustling metropolis known for its skyline and shopping."},
        {"name": "Singapore", "lat": 1.3521, "lon": 103.8198, "info": "A global financial hub known for its cleanliness and greenery."},
        {"name": "Amsterdam", "lat": 52.3676, "lon": 4.9041, "info": "Known for its canals, art museums, and vibrant culture."},
        {"name": "Madrid", "lat": 40.4168, "lon": -3.7038, "info": "The capital of Spain, famous for its royal palace and museums."},
        {"name": "Seoul", "lat": 37.5665, "lon": 126.9780, "info": "The capital of South Korea, a blend of modern and traditional culture."},

        # North Africa Destinations
        {"name": "Algiers", "lat": 36.737232, "lon": 3.086472, "info": "Capital of Algeria, known for its beautiful Mediterranean coastline."},
        {"name": "Tunis", "lat": 36.8065, "lon": 10.1815, "info": "The capital of Tunisia, rich in history and ancient ruins."},
        {"name": "Casablanca", "lat": 33.5731, "lon": -7.5898, "info": "The largest city in Morocco, known for its modern art deco architecture."},
        {"name": "Marrakesh", "lat": 31.6295, "lon": -7.9811, "info": "Famous for its palaces, gardens, and vibrant souks."},
        {"name": "Cairo", "lat": 30.0444, "lon": 31.2357, "info": "Capital of Egypt, home to the ancient Pyramids of Giza."},

        # Additional Asia Destinations
        {"name": "Bangladesh", "lat": 23.685,"lon": 90.3563,"info": "Known for its lush green landscapes and cultural heritage."},
        {"name": "Kathmandu", "lat": 27.7172, "lon": 85.324,"info": "Capital city of Nepal, rich in history and surrounded by mountains."},
        {"name": "Manila", "lat": 14.5995, "lon": 120.9842, "info": "The capital of the Philippines, known for its history and vibrant culture."},
        {"name": "Hanoi", "lat": 21.0285, "lon": 105.8542, "info": "Capital city of Vietnam, known for its centuries-old architecture."},
        {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456, "info": "Capital of Indonesia, a bustling city with a blend of modern and traditional."},
        {"name": "Bali", "lat": -8.4095, "lon": 115.1889, "info": "Known for its beautiful beaches, temples, and vibrant culture."},
        {"name": "Lahore", "lat": 31.5497, "lon": 74.3436, "info": "A historic city in Pakistan known for its Mughal architecture."},
        {"name": "Kuala Lumpur", "lat": 3.139,"lon": 101.6869,"info": "The capital of Malaysia, known for its modern skyscrapers and culture."},
        {"name": "Colombo", "lat": 6.9271, "lon": 79.8612, "info": "Capital of Sri Lanka, famous for its coastal beauty and colonial buildings."}
    ]

    # Add markers with popups
    for destination in destinations:
        folium.Marker(
            location=[destination["lat"], destination["lon"]],
            popup=f'<b>{destination["name"]}</b><br>{destination["info"]}',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(marker_cluster)

    st.subheader("📍 Destination Map")
    st.components.v1.html(m._repr_html_(),height=600)









    
    
    col1, col2 = st.columns([1, 1])  # Adjust the ratio to control width distribution

    with col1:
        # Travel Quiz Section with Expander
        st.header("🏝️ Where Should You Travel Next? Take the Quiz!")
        with st.expander("🧳 Click here to find your dream destination in just a few questions!"):

            # Questions using dropdowns instead of radio buttons
            question_1 = st.selectbox("What is your ideal vacation activity?", 
                                    ["Select an option", "Lazing on the beach with a good book", 
                                        "Visiting historic landmarks and museums", 
                                        "Hiking or exploring nature", 
                                        "Shopping and exploring city life"])

            question_2 = st.selectbox("What type of climate do you prefer?", 
                                    ["Select an option", "Tropical and warm", 
                                        "Mediterranean or temperate", 
                                        "Cold or mountain climates", 
                                        "Mild and urban climates"])

            question_3 = st.selectbox("Which kind of food do you enjoy the most?", 
                                    ["Select an option", "Seafood and tropical fruits", 
                                        "Italian, Greek, and Mediterranean cuisines", 
                                        "Barbecue, fresh produce, and local delicacies", 
                                        "Street food, sushi, and trendy cafés"])

            question_4 = st.selectbox("Which of these is a must on your itinerary?", 
                                    ["Select an option", "Relaxing by the beach or a spa", 
                                        "Visiting ancient ruins and landmarks", 
                                        "Outdoor adventure activities", 
                                        "Exploring a vibrant city with lots of shopping"])

            question_5 = st.selectbox("How do you prefer to travel?", 
                                    ["Select an option", "By beach resort with luxury amenities", 
                                        "With a cultural guide for historical tours", 
                                        "Through remote, off-the-beaten-path destinations", 
                                        "By city tour and shopping spree"])

            # Ensure that the user selects a valid option before proceeding
            if "Select an option" in (question_1, question_2, question_3, question_4, question_5):
                st.warning("Please select an option for all questions.")
            else:
                answers = [question_1, question_2, question_3, question_4, question_5]
                scores = calculate_weighted_score(answers)

                # Sort scores from highest to lowest
                sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

                # Get the top category
                top_destination, _ = sorted_scores[0]

                # Display the top destination
                st.subheader("Results")

                if top_destination == "Beaches & Relaxation":
                    st.success("🌴 **You should visit the Maldives, the Bahamas, or Bali!**")
                    st.image("images/tropical.jpg", caption="Tropical Beach Destination")
                    st.write("These stunning destinations are perfect for unwinding. Expect crystal-clear waters, white sandy beaches, and world-class resorts. Whether you love lounging under palm trees, indulging in fresh seafood, or experiencing luxury spas, this is your ideal getaway.")

                elif top_destination == "History & Culture":
                    st.success("🏛️ **You should visit Rome, Athens, or Cairo!**")
                    st.image("images/historic.jpg", caption="Historic Destination")
                    st.write("For the history enthusiast, these cities offer an immersive experience into ancient civilizations. Walk through historic ruins, marvel at architectural wonders, and savor the rich traditions passed down through generations.")

                elif top_destination == "Adventure & Nature":
                    st.success("⛰️ **You should visit Patagonia, New Zealand, or Iceland!**")
                    st.image("images/adventure.jpg", caption="Adventure Destination")
                    st.write("If you're an explorer at heart, these destinations will take you on breathtaking journeys through rugged landscapes. Expect thrilling hikes, stunning wildlife encounters, and endless outdoor activities.")

                else:  # City Life & Shopping
                    st.success("🌆 **You should visit New York, Tokyo, or London!**")
                    st.image("images/city.jpg", caption="City Destination")
                    st.write("These global metropolises are the heart of culture, fashion, and entertainment. From high-end shopping streets to vibrant nightlife, there's always something exciting to discover.")

        
        
        
        
        # Real-Time Weather Feature
        st.subheader("☀️ Check Weather for Your Destination")
        city = st.text_input("Enter a city name:")
        if city:
            st.write(f"🔍 Searching weather for {city}... (Integration Pending)")  # Placeholder for AP


    
       
        
    
    
    
    
    st.markdown("🌐 _Plan your next trip with Travelbot!_")
