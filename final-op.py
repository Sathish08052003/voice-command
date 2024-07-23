
#This code is designed to create a simple voice assistant using Python
#the pyttsx3 library for text-to-speech,
#the speech_recognition library to capture and process speech
# fetching information from Wikipedia and opening web pages.


import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser

#pyttsx3: To convert text to speech.
#speech_recognition: To recognize and process spoken commands.
#datetime: To handle date and time operations.
#wikipedia: To fetch summaries from Wikipedia.
#webbrowser: To open web pages in a browser.
 
# Initialize the pyttsx3 engine

#This block initializes the pyttsx3 engine and sets the voice to the first available voice.
#  Any initialization errors are caught and printed./

try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
except Exception as e:
    print("Error initializing pyttsx3 engine:", e)
 
 #Speak Function
 #The speak function takes a string (audio) and uses the pyttsx3 engine to convert it to speech. 
 # Errors during speech synthesis are caught and printed.
def speak(audio):
    try:
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print("Error in speak function:", e)

 #WishMe Function
 #The wishMe function greets the user based on the current time. 
 # It gets the current hour and determines the appropriate greeting to speak.
def wishMe():
    """Function to greet the user based on the time of the day."""
    try:
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour < 12:
            speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
    except Exception as e:
        print("Error in wishMe function:", e)
 
 #TakeCommand Function
 #The takeCommand function listens for a spoken command using the microphone.
 #  It adjusts for ambient noise, captures the audio, and tries to recognize it using Google's speech recognition service.
 #  Any errors during recognition are handled, and the recognized text (query) is returned.
def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise, please wait...")
            r.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = r.listen(source)
            print("Recording complete. Processing...")
       
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print("Error in takeCommand function:", e)
            return None
        return query
    except Exception as e:
        print("Microphone not working:", e)
        return None
    
 #Main Logic

 #1)Greeting and Initial Prompt:

#The program starts by calling wishMe() to greet the user.
#It then speaks an initial prompt to the user: "I am Optimus Prime, Please tell me how may I help you".

#2)Listening for Commands:

#The program enters an infinite loop to continuously listen for commands.
#It calls takeCommand() to capture and recognize the user's spoken command.

#3)Processing Commands:

#If the command includes "wikipedia", it searches Wikipedia for a summary of the query.
#It handles disambiguation errors, page errors, and other exceptions gracefully.
#If the command includes "open youtube", "open google", or "open stackoverflow", it opens the respective website in the default web browser.
#If the command includes "the time", it speaks the current time.

if __name__ == "__main__":
    wishMe()
    speak("I am Optimus Prime, Please tell me how may I help you")
   
    while True:
        query = takeCommand()
        if query:
            query = query.lower()
 
            if 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    print("Disambiguation error:", e.options)
                    speak("There were multiple results for this query. Please be more specific.")
                except wikipedia.exceptions.PageError as e:
                    print("Page error:", e)
                    speak("Sorry, I could not find any results for that query.")
                except Exception as e:
                    print("Error fetching Wikipedia summary:", e)
                    speak("Sorry, I couldn't fetch the Wikipedia summary.")
           
            elif 'open youtube' in query:
                webbrowser.open("youtube.com")
           
            elif 'open google' in query:
                webbrowser.open("google.com")
           
            elif 'open stackoverflow' in query:
                webbrowser.open("stackoverflow.com")
           
            elif 'the time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strTime}")


                