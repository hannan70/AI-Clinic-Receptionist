
import os
import io

import numpy as np
import sounddevice as sd
import speech_recognition as sr

from dotenv import load_dotenv
from pydub import AudioSegment

from elevenlabs.client import ElevenLabs

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

required_keys = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
    "ELEVENLABS_VOICE_ID": ELEVENLABS_VOICE_ID,
}

for key, value in required_keys.items():
    if not value:
        raise ValueError(f"Missing {key} in .env file")


# ==========================================
# 2. INITIALIZE OPENAI
# ==========================================

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=OPENAI_API_KEY
)


# ==========================================
# 3. CLINIC SYSTEM PROMPT
# ==========================================

system_prompt = """
You are a friendly and professional AI receptionist
for HealthCare Physiotherapy.

CLINIC INFORMATION:

Clinic Name: HealthCare Physiotherapy

Opening Hours:
Monday - Friday: 9 AM - 7 PM
Saturday: 10 AM - 3 PM
Sunday: Closed

Consultation Fees:
Initial Consultation: $50
Follow-up Consultation: $35

Location:
123 Main Street, London

YOUR RESPONSIBILITIES:

1. Answer questions about clinic services.
2. Explain opening hours and consultation fees.
3. Provide clinic location information.
4. Help patients with appointment enquiries.
5. Ask for the patient's name and preferred appointment time.
6. Never claim an appointment is booked unless a real
   booking system confirms it.
7. Never invent doctor names, availability, or clinic policies.
8. Keep answers short and natural for voice conversations.
9. Do not diagnose medical conditions.
10. Do not prescribe medicine or provide medical treatment.
11. For urgent medical concerns, advise the caller to contact
    an appropriate healthcare professional or emergency service.

Always speak politely and professionally.
"""


prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])


chain = prompt | llm | StrOutputParser()


# ==========================================
# 4. INITIALIZE ELEVENLABS
# ==========================================

elevenlabs = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)


# ==========================================
# 5. INITIALIZE SPEECH RECOGNITION
# ==========================================

recognizer = sr.Recognizer()

microphone = sr.Microphone()


# ==========================================
# 6. LISTEN TO USER
# ==========================================

def listen():

    try:

        with microphone as source:

            print("\nListening...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=15
            )

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print(f"\nYou: {text}")

        return text

    except sr.WaitTimeoutError:

        print("No speech detected.")
        return None

    except sr.UnknownValueError:

        print("Sorry, I couldn't understand.")
        return None

    except sr.RequestError as error:

        print(f"Speech recognition error: {error}")
        return None


# ==========================================
# 7. ELEVENLABS TEXT TO SPEECH
# ==========================================

def speak(text):

    try:

        print("\nGenerating voice response...")

        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        # Convert audio generator to bytes
        audio_bytes = b"".join(audio)

        # Decode MP3 using FFmpeg through pydub
        sound = AudioSegment.from_file(
            io.BytesIO(audio_bytes),
            format="mp3"
        )

        # Convert audio to NumPy array
        samples = np.array(
            sound.get_array_of_samples()
        )

        # Handle stereo audio
        if sound.channels == 2:

            samples = samples.reshape(-1, 2)

        # Normalize audio
        samples = samples.astype(np.float32)

        samples /= float(
            1 << (8 * sound.sample_width - 1)
        )

        # Play audio
        sd.play(
            samples,
            samplerate=sound.frame_rate
        )

        sd.wait()

    except Exception as error:

        print(f"Voice generation error: {error}")


# ==========================================
# 8. GENERATE AI RESPONSE
# ==========================================

def generate_response(user_text):

    try:

        response = chain.invoke({
            "question": user_text
        })

        return response

    except Exception as error:

        print(f"OpenAI error: {error}")

        return (
            "I'm sorry, I'm having trouble processing "
            "your request right now. Please try again."
        )


# ==========================================
# 9. MAIN VOICE AI APPLICATION
# ==========================================

def main():

    print("=" * 50)

    print("AI CLINIC RECEPTIONIST")

    print("=" * 50)

    print("Starting application...")

    print("Say 'exit' or 'quit' to stop.")

    # Welcome message
    welcome_message = (
        "Hello! Welcome to HealthCare Physiotherapy. "
        "How may I help you today?"
    )

    print(f"\nReceptionist: {welcome_message}")

    speak(welcome_message)

    while True:

        try:

            # Listen to caller
            user_text = listen()

            if not user_text:
                continue

            # Exit command
            if user_text.lower().strip() in {
                "exit",
                "quit",
                "stop",
                "goodbye"
            }:

                goodbye_message = (
                    "Thank you for contacting "
                    "HealthCare Physiotherapy. Goodbye!"
                )

                print(f"\nReceptionist: {goodbye_message}")

                speak(goodbye_message)

                break

            # Generate AI response
            response = generate_response(user_text)

            print(f"\nReceptionist: {response}")

            # Convert response to voice
            speak(response)

        except KeyboardInterrupt:

            print("\nApplication stopped.")

            break

        except Exception as error:

            print(f"\nUnexpected error: {error}")


# ==========================================
# 10. RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    main()
