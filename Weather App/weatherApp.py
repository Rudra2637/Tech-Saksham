import streamlit as st
import requests

def get_weather(location):
    # Replace with your OpenWeatherMap API key
    api_key = "87b8502249e686620b7affc0f5e214bd"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Construct the full URL
    complete_url = f"{base_url}q={location}&appid={api_key}&units=metric"  # You can use 'metric' for Celsius
    
    # Make the request to the OpenWeatherMap API
    response = requests.get(complete_url)
    
    # If the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()  # Convert response to JSON
        main = data['main']
        weather = data['weather'][0]
        
        # Extracting temperature, humidity, and description
        temp = main['temp']
        humidity = main['humidity']
        description = weather['description']
        icon = weather['icon']  # Get the weather icon code
        
        return temp, humidity, description, icon
    else:
        # If the location is not found
        return None

def main():
    # Setting a custom background image with CSS
    st.markdown("""
        <style>
            .stApp {
                background-image: url('https://example.com/your-image.jpg');
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                height: 100vh;
            }
            .css-1aumxhk {
                background-color: rgba(255, 255, 255, 0.7);  # Optional: light background for text to be more visible
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🌤️ Weather App 🌤️")
    
    st.markdown(
        """
        Welcome to the Weather App! 🌍
        Enter the name of any city to get the current weather details.
        """
    )
    
    # User input for location
    location = st.text_input("Enter a location:", placeholder="e.g., New York")
    
    if st.button("Get Weather"):
        if location:
            # Fetch weather data
            weather_data = get_weather(location)
            
            if weather_data:
                temp, humidity, description, icon = weather_data
                
                # Display weather details with icon
                st.image(f"http://openweathermap.org/img/wn/{icon}.png", width=100)  # Display weather icon
                st.write(f"### Weather in {location.capitalize()}:")
                st.write(f"**Temperature:** {temp}°C")
                st.write(f"**Humidity:** {humidity}%")
                st.write(f"**Description:** {description.capitalize()}")
                st.success("Data fetched successfully!")
            else:
                st.error("Location not found. Please check the spelling or try a different location.")
        else:
            st.warning("Please enter a location.")

    st.markdown("""
    <style>
        .stApp {
            background-image: url('background.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()