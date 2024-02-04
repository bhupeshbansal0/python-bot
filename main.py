import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import wikipedia
import random
import psutil
import sys
import shutil

import warnings

warnings.catch_warnings()
warnings.simplefilter("ignore")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.energy_threshold = 200
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising...")
        string = r.recognize_google(audio, language="en-IN")
        print(f"User said: {string}")
    except Exception as e:
        print(e)
        speak("Sorry couldn't recognise. Say it again...")
        return "None"
    return string


def wish_me(name):
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak(f"Good Morning {name}!")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon {name}!")
    else:
        speak(f"Good Evening {name}!")
    return "How may I help You?"


def open_related(given_query):
    modified_str = given_query.replace("open", "").strip()
    if "from my computer" in modified_str:
        query_list = given_query.split(" ")
        speak(f"Opening {query_list[1]}")
        if 'spotify' in query_list:
            file_path = "C:\\Program Files\\WindowsApps\\SpotifyAB.SpotifyMusic_1.174.631.0_x86__zpdnekdrzrea0" \
                        "\\Spotify.exe "
        elif 'telegram' in query_list:
            file_path = "C:\\Program Files\\WindowsApps\\TelegramMessengerLLP.TelegramDesktop_3.3.0" \
                        ".0_x64__t4vj0pshhgkwm\\Telegram.exe "
        elif "browser" or "google" or "chrome" in query_list:
            file_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\sedge.exe"
        else:
            file_path = "This PC:\\"
        return os.startfile(file_path)
    else:
        try:
            return webbrowser.open(f"{modified_str}.com")
        except Exception as e:
            print(e)
            return f"Can't open {modified_str} right now."


def search_wikipedia(article):
    if "according to" not in article:
        article = " ".join([article, "according to"])
    speak(f"Searching on Wikipedia, Please wait a few seconds...")
    try:
        result = wikipedia.summary(article, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Match not found. Searching relevant...")
        result = wikipedia.summary(e.options, sentences=2)
    except wikipedia.exceptions.PageError:
        result = "Nothing found"
    finally:
        speak("According to Wikipedia: ")
    print(result)
    return result


def play_music(user_name):
    speak(f"Here are some songs {user_name} might like")
    url = "https://www.youtube.com/watch?v=KRA26LhuTP4"
    webbrowser.open_new_tab(url)


def current_time():
    return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"


def how_am_i(battery_percentage):
    if battery_percentage >= 80:
        message = "I am feeling great... full of energy. Ready to perform any kind of work at your command."
    elif 80 > battery_percentage >= 50:
        message = "I am good... Can perform any task."
    elif 50 > battery_percentage >= 25:
        message = "I am fine but might go on power saving mode soon."
    else:
        message = "Not so good. Could really use some charge."

    return message


def create_txt_file(name_of_the_file):
    speak('Creating new file....')

    with open(f"{name_of_the_file}.txt", "a") as file:
        speak('Please tell me what to write')
        content = take_command().lower()
        file.write(str(content))

    os.mkdir("Docs")
    shutil.move(f"{name_of_the_file}.txt", "Docs")

    return "File created and saved successfully in Docs folder."


def tell_joke(list_of_jokes):
    return random.choice(list_of_jokes)


def who_am_i(name):
    return f"Hello, I am {name}. I am a bot."


def bot_name(list_of_names, file):
    if list_of_names[1] == "":
        speak("You can only decide this once. So what would you like to call me?")
        name = take_command().capitalize()
        while name == "None":
            name = take_command().capitalize()
        with open(file, "w") as f:
            f.truncate()
            f.write(f"{USER_NAME}\n{name}")
    else:
        name = NAMES[1]
    return name


def define_username(list_of_names, file):
    if list_of_names[0] == "":
        speak("Hello... long time no see. What was ur name again?")
        user_name = take_command().capitalize()
        while user_name == "None":
            user_name = take_command().capitalize()
        with open(file, "w") as f:
            f.truncate()
            f.write(f"{user_name}\n{NAMES[1]}")
    else:
        user_name = NAMES[0]
    return user_name


def initialize_name_list(file_name):
    # noinspection PyBroadException
    try:
        with open(file_name, "r") as file:
            list_of_names = file.read().split("\n")
            if len(list_of_names) < 2:
                list_of_names.append("")
    except:
        with open(file_name, "w") as file:
            file.write("\n")
            list_of_names = ["", ""]
    return list_of_names


if __name__ == '__main__':

    NAME_FILE = "bot.txt"
    NAMES = initialize_name_list(NAME_FILE)
    JOKES = [
        "What do you call a boomerang that won’t come back?.....................A stick.",
        "What did one toilet say to the other?....................You look a bit flushed.",
        "Why did the kid bring a ladder to school?....................Because she wanted to go to high school.",
        "How do you get a squirrel to like you?....................Act like a nut.",
        "How do we know that the ocean is friendly?.....................It waves.",
        "How do you talk to a giant?....................Use big words.",
        "What did the Dalmatian say after lunch?....................That hit the spot......That's what she said.",
        "What did the little corn say to the mama corn?....................Where is pop corn?",
        "Your Mom is so small... her best-friend is an ant.",
        "Why is six afraid of seven?....................Because seven eight nine.",
    ]
    USER_NAME = define_username(NAMES, NAME_FILE)
    BOT_NAME = bot_name(NAMES, NAME_FILE)

    wish_me(USER_NAME)
    while True:
        os.system(f"attrib +h {NAME_FILE}")
        speak("How may I help you?")
        query = take_command().lower()

        if "who are you" in query:
            speak(who_am_i(BOT_NAME))

        elif "how are you" in query:
            battery = psutil.sensors_battery()
            speak(how_am_i(battery.percent))

        elif "open" in query:
            speak(open_related(query))

        elif "wikipedia" in query:
            modified_query = query.replace("wikipedia", "").strip()
            speak(search_wikipedia(modified_query))

        elif "time" in query:
            speak(current_time())

        elif "repeat after me" in query:
            query = query.replace("repeat after me ", " ")
            speak(f"You siad: {query}")

        elif "create" in query:
            speak("What name would you like to give to your text file?")
            filename = take_command().lower()
            speak(create_txt_file(filename))

        elif "music" in query:
            play_music(USER_NAME)

        elif "joke" in query:
            speak(tell_joke(JOKES))

        elif "quit" in query:
            speak("It was nice spending time with you. Hope to see you soon.")
            sys.exit()
