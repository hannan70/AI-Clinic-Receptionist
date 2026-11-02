
import os
import signal
import sys

from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs

from elevenlabs.conversational_ai.conversation import (
    Conversation,
)

from elevenlabs.conversational_ai.default_audio_interface import (
    DefaultAudioInterface,
)


# ==========================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
AGENT_ID = os.getenv("AGENT_ID")

if not AGENT_ID:
    raise ValueError("AGENT_ID is missing from .env")

# API key is required for private agents.
# Public agents can work without an API key.


# ==========================================
# 2. INITIALIZE ELEVENLABS CLIENT
# ==========================================

elevenlabs = ElevenLabs(
    api_key=API_KEY
)


# ==========================================
# 3. CALLBACK FUNCTIONS
# ==========================================

def on_agent_response(response):
    print(f"\nReceptionist: {response}")


def on_agent_correction(original, corrected):
    print("\nResponse correction:")
    print(f"Original: {original}")
    print(f"Corrected: {corrected}")


def on_user_transcript(transcript):
    print(f"\nYou: {transcript}")


def on_disconnect(details):
    print("\nConversation disconnected.")
    print(f"Reason: {details.reason}")

    if details.message:
        print(f"Message: {details.message}")


# ==========================================
# 4. CREATE CONVERSATION
# ==========================================

conversation = Conversation(
    client=elevenlabs,

    agent_id=AGENT_ID,

    requires_auth=bool(API_KEY),

    audio_interface=DefaultAudioInterface(),

    callback_agent_response=on_agent_response,

    callback_agent_response_correction=on_agent_correction,

    callback_user_transcript=on_user_transcript,

    callback_disconnect=on_disconnect,
)


# ==========================================
# 5. MAIN APPLICATION
# ==========================================

def main():

    print("=" * 50)
    print("AI CLINIC RECEPTIONIST")
    print("=" * 50)

    print("Initializing ElevenLabs Agent...")

    try:

        print("\nConnecting to your AI Agent...")

        conversation.start_session()

        print("\nConnected successfully!")

        print("Your AI receptionist is ready.")
        print("Start speaking into your microphone.")
        print("Press CTRL+C to stop.")

        # Wait until conversation ends
        conversation_id = conversation.wait_for_session_end()

        print("\nConversation ended.")

        print(f"Conversation ID: {conversation_id}")

    except KeyboardInterrupt:

        print("\nStopping AI Receptionist...")

        conversation.end_session()

    except Exception as error:

        print(f"\nApplication Error: {error}")

        try:
            conversation.end_session()
        except Exception:
            pass

    finally:

        print("\nAI Clinic Receptionist stopped.")


# ==========================================
# 6. RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    main()
