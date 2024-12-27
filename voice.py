import speech_recognition as sr
import pyttsx3
import requests
import time
import datetime
from pydub import AudioSegment
from pydub.playback import play

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user's voice command and save it to a file
def listen_and_save_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Please speak into the microphone.")
        audio = recognizer.listen(source)
        # Save audio to a file
        with open("audio_input.wav", "wb") as f:
            f.write(audio.get_wav_data())
    print("Audio saved as 'audio_input.wav'.")

# Function to process saved audio file and convert it to text
def recognize_audio_from_file():
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile("audio_input.wav") as source:
            audio = recognizer.record(source)  # Record the audio file content
        command = recognizer.recognize_google(audio)  # Use Google Web Speech API
        print("You said:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None

# Function to get weather information
def get_weather():
    api_key = "1d36e6f6631d5d7e983dc87bdfaf8a02"
    city = "kolkata"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        speak(f"The current weather is {weather} with a temperature of {temp}°C.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

# Function to get the latest news
def get_news():
    api_key = "e4e882df33664d2e853bdafc58aba203"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == 'ok':
        articles = data['articles']
        speak("Here are the top news headlines:")
        for article in articles[:5]:
            speak(f"{article['title']}")
    else:
        speak("Sorry, I couldn't fetch the news.")

# Function to set a reminder
def set_reminder():
    speak("What is the reminder?")
    reminder = listen_and_save_audio()
    if reminder:
        speak("When do you want to be reminded?")
        time_input = listen_and_save_audio()
        if time_input:
            try:
                reminder_time = datetime.datetime.strptime(time_input, "%I:%M %p")
                now = datetime.datetime.now()
                time_to_wait = (reminder_time - now).total_seconds()
                if time_to_wait > 0:
                    speak(f"Reminder set for {reminder_time.strftime('%I:%M %p')}")
                    time.sleep(time_to_wait)
                    speak(f"Reminder: {reminder}")
                else:
                    speak("The time you entered is in the past. Please enter a future time.")
            except ValueError:
                speak("Sorry, I couldn't understand the time format. Please try again.")
        else:
            speak("I couldn't catch the time. Please try again.")
    else:
        speak("I couldn't catch the reminder. Please try again.")

# Main function to control the assistant
def run_assistant():
    speak("Hello, I'm your personal assistant. How can I help you today?")
    while True:
        listen_and_save_audio()
        command = recognize_audio_from_file()
        
        if command:
            if "weather" in command:
                get_weather()
            elif "news" in command:
                get_news()
            elif "reminder" in command:
                set_reminder()
            elif "exit" in command or "bye" in command:
                speak("Goodbye!")
                break
            else:
                speak("I didn't catch that. Please say something else.")

# Start the assistant
if __name__ == "__main__":
    run_assistant()
