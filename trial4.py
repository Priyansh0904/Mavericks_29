from flask import Flask, request, jsonify
from flask_cors import CORS
import pyttsx3 as tts
import speech_recognition as sr
import io
import sys
from pydub import AudioSegment

app = Flask(__name__)
CORS(app)  

speaker = tts.init()
speaker.setProperty('rate', 150)


recognizer = sr.Recognizer()


todo_list = ['Home Work']
timetable = {}
attendance = {}


def hello():
    speaker.say("Hello Master! How may I help you?")
    speaker.runAndWait()

def create_note():
    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                note = recognizer.recognize_google(audio).lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                filename = recognizer.recognize_google(audio).lower()

            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()

def add_todo():
    speaker.say('Name the task')
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                item = recognizer.recognize_google(audio).lower()
                todo_list.append(item)
                done = True
                speaker.say(f"Addition complete")
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()

def show_todos():
    speaker.say("Tasks pending are ")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()

def add_timetable():
    speaker.say("Which subject or task do you want to add?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                subject = recognizer.recognize_google(audio).lower()

                speaker.say("Which day and time?")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                day_time = recognizer.recognize_google(audio).lower()

                timetable[day_time] = subject
                done = True
                speaker.say(f"Timetable entry for {subject} on {day_time} has been added")
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()

def show_timetable():
    if timetable:
        speaker.say("Your timetable is as follows:")
        for day_time, subject in timetable.items():
            speaker.say(f"{day_time}: {subject}")
    else:
        speaker.say("Your timetable is empty.")
    speaker.runAndWait()

def delete_timetable():
    speaker.say("Which day and time's entry do you want to delete?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                day_time = recognizer.recognize_google(audio).lower()

                if day_time in timetable:
                    del timetable[day_time]
                    speaker.say(f"Deleted timetable entry for {day_time}")
                else:
                    speaker.say(f"No entry found for {day_time}")
                done = True
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()

def add_attendance():
    speaker.say("Which subject's attendance do you want to update?")
    speaker.runAndWait()
    done = False
    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                subject = recognizer.recognize_google(audio).lower()

                speaker.say("How many total classes were there?")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                total_classes = int(recognizer.recognize_google(audio))

                speaker.say("How many classes did you attend?")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                attended_classes = int(recognizer.recognize_google(audio))

                attendance[subject] = {'total': total_classes, 'attended': attended_classes}
                done = True
                speaker.say(f"Attendance for {subject} has been updated")
                speaker.runAndWait()
        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand! Please try again!")
            speaker.runAndWait()

def check_attendance():
    speaker.say("Checking attendance records")
    speaker.runAndWait()
    if attendance:
        for subject, data in attendance.items():
            total = data['total']
            attended = data['attended']
            attendance_percentage = (attended / total) * 100 if total > 0 else 0

            if attendance_percentage >= 75:
                speaker.say(f"For {subject}, your attendance is {attendance_percentage:.2f}%. You are meeting the requirement.")
            else:
                required_classes = (0.75 * total) - attended + 1
                speaker.say(f"For {subject}, your attendance is {attendance_percentage:.2f}%. You need to attend {required_classes:.0f} more classes to meet the 75% requirement.")
        speaker.runAndWait()
    else:
        speaker.say("No data related to attendance found")
        speaker.runAndWait()

def quit():
    speaker.say('Power core shutting down')
    speaker.runAndWait()
    sys.exit(0)

def process_command(command):
    mappings = {
        'greeting': hello,
        'create_note': create_note,
        'add_todo': add_todo,
        'show_todos': show_todos,
        'add_timetable': add_timetable,
        'show_timetable': show_timetable,
        'delete_timetable': delete_timetable,
        'add_attendance': add_attendance,
        'check_attendance': check_attendance,
        'exit': quit
    }

    for key in mappings:
        if key in command:
            mappings[key]()
            return f"Executed: {key}"

    return "Command not recognized"

@app.route('/process/', methods=['POST'])
def process():
    audio_file = request.files.get('audio')
    if not audio_file:
        return jsonify({'response': 'No audio file provided'}), 400

    audio_data = io.BytesIO(audio_file.read())

    try:
        audio_segment = AudioSegment.from_file(audio_data, format="wav")
        audio_segment.export("temp.wav", format="wav")
        with sr.AudioFile("temp.wav") as source:
            audio = recognizer.record(source)
            command = recognizer.recognize_google(audio).lower()
            response = process_command(command)
            return jsonify({'response': response})
    except sr.UnknownValueError:
        return jsonify({'response': 'Sorry, I could not understand the audio.'}), 400
    except Exception as e:
        return jsonify({'response': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5500)
