import speech_recognition as sr
from datetime import datetime
import subprocess
import pywhatkit
import pyttsx3
import webbrowser

recognizer = sr.Recognizer()

def speak(text):
    """Speak text with pyttsx3 and print it (re-inits each time to avoid voice bug)"""
    print("Assistant:", text)
    engine = pyttsx3.init()  # re-init each time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # use voices[1] if you prefer female
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def cmd():
    """Listen for a voice command and process it"""
    with sr.Microphone() as source:
        print('Clearing background noises..Please Wait!!')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Ask anything...")
        try:
            recordedaudio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected (timeout). Try again.")
            return

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(recordedaudio)
        print('Your message:', command)
    except sr.UnknownValueError:
        print("Could not understand your speech. Please try again.")
        return
    except sr.RequestError as e:
        print("Could not request results; check your internet connection.", e)
        return
    except Exception as ex:
        print("Error:", ex)
        return

    command = command.lower()

    if 'chrome' in command:
        speak("Opening Chrome")
        program = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  
        try:
            subprocess.Popen([program])
        except FileNotFoundError:
            speak("Chrome path is incorrect. Please check the program path.")

    elif 'time' in command:
        time = datetime.now().strftime('%I:%M %p')
        speak("The current time is " + time)

    elif 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            speak("Playing " + song + " on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Please say the song name after play")

    elif 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'exit' in command or 'quit' in command:
        speak("Goodbye Harshini")
        return "exit"

    else:
        speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    while True:
        result = cmd()
        if result == "exit":
            break
