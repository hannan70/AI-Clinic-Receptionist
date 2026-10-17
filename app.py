import os
import signal
from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import (
    DefaultAudioInterface,
)

load_dotenv()

# 1. Load configuration
api_key = os.getenv("ELEVENLABS_API_KEY")
agent_id = os.getenv("AGENT_ID")

if not agent_id:
    raise ValueError("Missing AGENT_ID in .env file")

# 2. Create ElevenLabs client
client = ElevenLabs(api_key=api_key) if api_key else ElevenLabs()

# 3. Create the conversation with your existing Agent
conversation = Conversation(
    client,
    agent_id,
    requires_auth=bool(api_key),
    audio_interface=DefaultAudioInterface(),

    callback_agent_response=lambda response:
        print(f"Receptionist: {response}"),

    callback_user_transcript=lambda transcript:
        print(f"You: {transcript}"),

    callback_agent_response_correction=lambda original, corrected:
        print(f"Corrected response: {corrected}"),
)


def main():
    print("AI Clinic Receptionist is starting...")
    print("Speak into your microphone.")
    print("Press Ctrl+C to stop.")

    session_started = False

    try:
        conversation.start_session()
        session_started = True

        conversation.wait_for_session_end()

    except KeyboardInterrupt:
        print("\nStopping the receptionist...")

    except Exception as e:
        print(f"\nError starting or running the conversation: {e}")

    finally:
        if session_started:
            conversation.end_session()

        print("Conversation ended.")


if __name__ == "__main__":
    main()

