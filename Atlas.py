import speech_recognition as sr
import pyttsx3
import pycountry
import time

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 135)

# Initialize recognizer
recognizer = sr.Recognizer()

# Get list of countries
countries = [country.name.lower() for country in pycountry.countries]
used = []

# Scores
user_score = 0
bot_score = 0
max_score = 3

def speak(text):
    print("Bot:", text)
    engine.say(text)
    engine.runAndWait()

def get_last_char(name):
    for char in reversed(name.lower()):
        if char.isalpha():
            return char
    return ''

def is_valid_country(name):
    return name.lower() in countries and name.lower() not in used

def get_next_country(last_letter):
    for country in countries:
        if country.startswith(last_letter) and country not in used:
            used.append(country)
            return country.title()
    return None

def listen_with_timer(timeout=30, phrase_limit=3):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print(f"(Listening for {timeout} seconds...)")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)
            text = recognizer.recognize_google(audio)
            return text
    except:
        return None

def listen_during_countdown(prompt_letter=None):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        for i in range(1, 11):
            speak(f"Take {i}")
            print(f"(Take {i}) Listening...")
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                user_input = recognizer.recognize_google(audio)
                print(f"You said: {user_input}")
                if is_valid_country(user_input):
                    if prompt_letter is None or user_input.lower().startswith(prompt_letter):
                        used.append(user_input.lower())
                        return user_input
            except:
                continue
    return None

def show_score():
    print("\n=============================")
    print(f"SCORE: You - {user_score} | Bot - {bot_score}")
    print("=============================\n")
    speak(f"The score is: You {user_score}, Bot {bot_score}")

def play_game():
    global user_score, bot_score
    speak("Welcome to the Atlas Voice Game! First to score 3 points wins.")
    user_turn = True
    last_letter = ''

    while user_score < max_score and bot_score < max_score:
        show_score()

        if user_turn:
            if last_letter:
                speak(f"Your turn. Say a country starting with {last_letter.upper()}.")
            else:
                speak("Your turn. Say any country.")

            user_country = listen_with_timer(timeout=30)

            if user_country:
                user_country = user_country.strip().lower()
                print(f"You said: {user_country}")
                if is_valid_country(user_country) and (last_letter == '' or user_country.startswith(last_letter)):
                    used.append(user_country)
                    last_letter = get_last_char(user_country)
                    user_turn = False
                else:
                    speak("Invalid country or wrong letter. Countdown starting now.")
                    user_country = listen_during_countdown(prompt_letter=last_letter)
                    if user_country:
                        speak(f"You said {user_country}. Saved!")
                        last_letter = get_last_char(user_country)
                        user_turn = False
                    else:
                        speak("Time's up! Bot gets a point.")
                        bot_score += 1
                        user_turn = False
            else:
                speak("No input detected. Countdown starting.")
                user_country = listen_during_countdown(prompt_letter=last_letter)
                if user_country:
                    speak(f"You said {user_country}. Saved!")
                    last_letter = get_last_char(user_country)
                    user_turn = False
                else:
                    speak("Still nothing. Bot gets a point.")
                    bot_score += 1
                    user_turn = False

        else:
            bot_country = get_next_country(last_letter)
            if bot_country:
                last_letter = get_last_char(bot_country)
                speak(f"My turn. I say {bot_country}. Your turn with {last_letter.upper()}.")
                user_turn = True
            else:
                speak("I can't think of a country. You win this round!")
                user_score += 1
                user_turn = True

