import speech_recognition as sr
import pyttsx3
from pytube import Search
import webbrowser

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_command():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 400  # tweak this if it's too sensitive
    recognizer.pause_threshold = 0.8

    with sr.Microphone() as source:
        print("Listening...")
        speak("Say the song name or any line from the song.")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return ""


def search_and_play_on_youtube(query):
    speak(f"Searching YouTube for {query}")
    print(f"Searching for: {query}")
    search = Search(query)
    if search.results:
        top_video = search.results[0]
        webbrowser.open(top_video.watch_url)
        speak(f"Playing {top_video.title}")
    else:
        speak("Sorry, I couldn't find anything.")

# Main loop
def main():
    while True:
        command = listen_command()
        if command:
            if "stop" in command or "exit" in command:
                speak("Exiting. Stay safe!")
                break
            else:
                search_and_play_on_youtube(command)

if __name__ == "__main__":
    main()
