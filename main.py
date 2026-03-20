import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import time
import requests
from google import genai
import os
from datetime import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "news_api_key"

def speak(text):
     engine = pyttsx3.init('sapi5')  # re-init every time
     engine.setProperty('rate', 170)
     engine.setProperty('volume', 1.0)
     voices = engine.getProperty('voices')
     engine.setProperty('voice', voices[1].id)

     engine.say(text)
     engine.runAndWait()
     engine.stop()
     
def aiPowered(command):
    YOUR_API_KEY = "Your API Key"
    client = genai.Client(api_key= YOUR_API_KEY)

    chat = client.chats.create(
    model="gemini-2.5-flash"
    )

# 2. Send user input to the chat
    response = chat.send_message(command)

# Return the AI’s answer
    return response.text     

def processCommand(c):
   if "open google" in c.lower():
       webbrowser.open("https://www.google.com")
       
   elif "open figma" in c.lower():
       webbrowser.open("https://www.figma.com/")
       
   elif "open youtube" in c.lower():
       webbrowser.open("https://www.youtube.com/")
       
   elif "open netflix" in c.lower():
       webbrowser.open("https://www.netflix.com/in/")
                
   elif c.lower().startswith("play"):
       song = c.lower().split(" ")[1]
       link = musiclibrary.music[song]
       speak(f"playing {song}")
       webbrowser.open(link)
       
   elif "news" in c.lower():
       r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
       speak("Here's the latest news")
       if r.status_code == 200:
           data = r.json()
    
           articles = data.get('articles', [])
           print("Number of articles:", len(articles))

           for article in articles:
                speak(article['title'])      
                
   elif "date" in c.lower():
       today = datetime.now().strftime("%A, %d %B %Y")
       speak(f"Today's date is {today}") 
       
   elif "time" in c.lower():
      current_time = datetime.now().strftime("%I:%M %p")
      speak(f"The time is {current_time}")    
        
   else:
       #Let Ai handle the rest 
       output = aiPowered(c)
       speak(output)
       
if __name__ == "__main__":
    speak("Initialising Jarvis")
    while True:
    # Listen for the wake word "Jarvis"
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
               print("Listening...")
               audio = r.listen(source, timeout = 2, phrase_time_limit=2) 
            word = r.recognize_google(audio)
            
            if "jarvis" in word.lower():
                time.sleep(0.5)
                speak("yes sir")
                # Listen for command
                with sr.Microphone() as source:
                  
                  print("Jarvis Active...")
                  audio = r.listen(source) 
                  command = r.recognize_google(audio)
                  
                  processCommand(command)
                  
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
                      
        except sr.WaitTimeoutError:
            print("Sorry, I could not understand.")  
              
        except sr.RequestError as e:
            print(" Speech service is unavailable.", format(e))
