# Description: This is a virtual assistant program that gets the date, current time, responds back with a
#               random greeting, and returns information on a person.

# import the libraries
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

# Ignore any warning messages
warnings.filterwarnings('ignore')

# Record audio and return the audio as a stream

def recordAudio():
    #Record the audio
    r = sr.Recognizer() # creating a recognizer object

    #Open the microphone and start recording
    with sr.Microphone() as source:
        print('Say something')
        audio = r.listen(source)

    # Use Google speech recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
    except sr.UnknownValueError: #Check for unknown error
        print('Google speech recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request results from Google Speech Recognition service error' + e)

    return data

# A function to get the virtual assistant response
def assistantResponse(text):
    print(text)

    #Convert text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    #Save the converted autio to a file
    myobj.save('assistant_response.mp3')

    # Play the converted file
    os.system('start assistant_response.mp3')

# a function for wake word or phrase
def wakeWord(text):
    WAKE_WORDS = ['hey girl', 'okay girl'] # A list of wake words

    text = text.lower() # converting text to lowercase

    # Check to see if users command/text contains a wake word or phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    # If the wake word is not found in the text
    return False

# A function to give the current date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]
    monthNum = now.month
    dayNum = now.day

    # List of months
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                   'September', 'October', 'November', "December"]
    # A list of ordinal numbers
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                      '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th',
                      '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    #A list of ordinal numbers
    return 'Today is ' + weekday + ', ' + month_names[monthNum - 1] + ' ' + ordinalNumbers[dayNum - 1] + '.'

# A function to return a random greeting response
def greeting(text):
    # Greeting inputs
    GREETING_INPUTS = ['hi', 'hey', 'hello', 'greetings', 'wassup']

    # Greeting responses
    GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there', 'hey girl']

    #If the users input is a greeting, then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + '.'
    # if no greeting was detected then return empty string
    return ''

# A function to get a persons first and last name from the text
def getPerson(text):
    wordList = text.split() # Splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]

while True:
    #Record the audio
    text = recordAudio()
    response = ''

    # Check for the wake word/phrase
    if(wakeWord(text) == True):
        # Check for greetings by the user
        response = response + greeting(text)
        # Check if the user said anything having to do with date
        if ('date' in text):
            get_date = getDate()
            response = response + ' ' + get_date
        # Check if user said "who is"
        if ('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + ' ' + wiki
        #Check to see if user said anything having to do with the time
        if ('time' in text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >= 12:
                meridiem = 'p.m'
                hour = now.hour - 12
            else:
                meridiem = 'a.m'
                hour = now.hour
            if now.minute < 10:
                minute = '0' + str(now.minute)
            else:
                minute = str(now.minute)
            response = response + ' ' + 'it is ' + str(hour) + ':' + minute + ' ' + meridiem + '.'
        #Have assistant respond back using audio and text from response
        assistantResponse(response)