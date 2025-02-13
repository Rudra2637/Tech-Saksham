import streamlit as st
import requests

def get_weather(location):
   
    api_key = "Api key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = f"{base_url}q={location}&appid={api_key}&units=metric"  
    
  
    response = requests.get(complete_url)
   
    if response.status_code == 200:
        data = response.json() 
        main = data['main']
        weather = data['weather'][0]
        
    
        temp = main['temp']
        humidity = main['humidity']
        description = weather['description']
        icon = weather['icon']  
        
        return temp, humidity, description, icon
    else:
     
        return None

def main():
   
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
    

    location = st.text_input("Enter a location:", placeholder="e.g., New York")
    
    if st.button("Get Weather"):
        if location:
            
            weather_data = get_weather(location)
            
            if weather_data:
                temp, humidity, description, icon = weather_data
                
                
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