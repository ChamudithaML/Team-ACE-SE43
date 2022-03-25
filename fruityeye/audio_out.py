# Import the required module for text to speech conversion
import pyttsx3

def voice_out(audio_text):
    # init function to get an engine instance for the speech synthesis
    engine = pyttsx3.init()
    # methos to decrease the speed of voice
    engine. setProperty("rate",120)
    voices = engine.getProperty('voices')
    #method to change the voice
    engine.setProperty('voice', voices[1].id) 
    # say method on the engine that passing input text to be spoken
    engine.say(audio_text)
    # run and wait method, it processes the voice commands
    engine.runAndWait()

    


   




