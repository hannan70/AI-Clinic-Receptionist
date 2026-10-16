
import os

import speech_recognition as sr
from dotenv import load_dotenv
import io
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()



# 1. Check environment variables
required_keys = [
    "OPENAI_API_KEY",
    "ELEVENLABS_API_KEY",
    "ELEVENLABS_VOICE_ID",
]
 
for key in required_keys:
    if not os.getenv(key):
        raise ValueError(f"Missing {key} in .env file")

# 2. Configure LangChain + OpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a friendly and professional AI receptionist
        for HealthCare Physiotherapy.

        Clinic information:
        - Monday-Friday: 9 AM to 7 PM
        - Saturday: 10 AM to 3 PM
        - Sunday: Closed
        - Initial consultation: $50
        - Follow-up consultation: $35
        - Location: 123 Main Street, London

        Rules:
        - Keep spoken answers short and natural.
        - Answer using the clinic information above.
        - Never invent clinic information.
        - Do not diagnose conditions or provide medical advice.
        - For appointments, ask for the patient's name,
          preferred date, and preferred time.
        - Do not claim an appointment is booked.
          Explain that staff must confirm it.
        - For urgent medical concerns, recommend contacting
          an appropriate healthcare professional or emergency
          services when needed.
        """
    ),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

# 3. Configure ElevenLabs text-to-speech
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

voice_id = os.getenv("ELEVENLABS_VOICE_ID")

# 4. Configure microphone speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def listen():
    """Capture speech and convert it to text."""
    with microphone as source:
        print("\nListening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return None


def speak(text):
    """Generate and play speech using ElevenLabs."""

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Collect streamed audio chunks
    audio_bytes = b"".join(audio)

    # Decode MP3 using FFmpeg
    sound = AudioSegment.from_file(
        io.BytesIO(audio_bytes),
        format="mp3",
    )

    # Convert audio to a NumPy array
    samples = np.array(sound.get_array_of_samples())

    if sound.channels == 2:
        samples = samples.reshape(-1, 2)

    samples = samples.astype(np.float32)
    samples /= float(1 << (8 * sound.sample_width - 1))

    # Play through your speakers
    sd.play(samples, samplerate=sound.frame_rate)
    sd.wait()


def main():
    print("AI Clinic Receptionist is starting...")
    print("Say 'exit' or 'quit' to stop.")

    speak(
        "Hello! Welcome to HealthCare Physiotherapy. "
        "How may I help you today?"
    )

    while True:
        try:
            user_text = listen()

            if not user_text:
                continue

            if user_text.lower().strip() in {
                "exit", "quit", "stop", "goodbye"
            }:
                speak("Thank you for calling. Goodbye!")
                break

            # LangChain sends the question to OpenAI
            response = chain.invoke({"question": user_text})
            print(f"Receptionist: {response}")

            # ElevenLabs speaks the response
            speak(response)

        except KeyboardInterrupt:
            print("\nStopping the receptionist...")
            break
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
