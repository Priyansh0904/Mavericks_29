from neuralintents import BasicAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Home Work','Assignment']

def create_note():
    global recognizer
    speaker.say("What do you want to write in your note?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                mess = recognizer.listen(mic)
                note = recognizer.recognize_google(mess).lower()

                speaker.say("Give a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                mess = recognizer.listen(mic)
                filename = recognizer.recognize_google(mess).lower()

            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say(f" successfully created the note {filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()


def add_todo():
    global recognizer

    speaker.say('What is the task')
    speaker.runAndWait()

    done = False
    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio).lower()
                todo_list.append(item)
                done = True
                speaker.say(f"Addition complete")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()


def show_todos():
    speaker.say("Tasks pending are ")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello Master! How may I help you?")
    speaker.runAndWait()


def quit():
    speaker.say('Power core shutting down')
    speaker.runAndWait()
    sys.exit(0)

mappings = {
    'greeting': hello,
    'create_note': create_note,
    'add_todo': add_todo,
    'show_todos': show_todos,
    'exit': quit
}

assistant = BasicAssistant('intents.json', mappings)
assistant.fit_model()
assistant.save_model()
while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            print('mic is on')

            message = recognizer.recognize_google(audio)
            message = message.lower()
            print('message received')
        assistant.process_input(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
        speaker.say("I did not understand! Please try again!")
        speaker.runAndWait()