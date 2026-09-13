# dashboard/overwatch_voice.py - ElevenLabs Voice Engine (Sanitized for Remote Push)
import os
import tempfile
import uuid

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import save
    ELEVEN_AVAILABLE = True
except ImportError:
    ELEVEN_AVAILABLE = False

# Set to "YOUR_ELEVENLABS_API_KEY_HERE" to rely strictly on env variable ELEVENLABS_API_KEY
HARDCODED_KEY = "YOUR_ELEVENLABS_API_KEY_HERE"

class OverwatchVoiceEngine:
    def __init__(self, api_key: str = None, voice_id: str = "21m00Tcm4TlvDq8ikWAM"): 
        resolved_key = HARDCODED_KEY if HARDCODED_KEY != "YOUR_ELEVENLABS_API_KEY_HERE" else (api_key or os.getenv("ELEVENLABS_API_KEY"))
        self.api_key = resolved_key
        self.voice_id = voice_id
        
        if self.api_key and ELEVEN_AVAILABLE:
            self.client = ElevenLabs(api_key=self.api_key)
        else:
            self.client = None

    def synthesize_speech(self, text_prompt: str) -> str:
        """Synthesizes text into audio and saves to an accessible local MP3 file."""
        if not self.client or not self.api_key:
            print("[!] ElevenLabs API Key missing in overwatch_voice.py")
            return None

        try:
            audio = self.client.generate(
                text=text_prompt,
                voice=self.voice_id,
                model="eleven_turbo_v2_5"
            )
            
            # Save audio to a unique file in the working folder
            filename = f"overwatch_speech_{uuid.uuid4().hex[:8]}.mp3"
            save(audio, filename)
            return os.path.abspath(filename)
        except Exception as e:
            print(f"[!] ElevenLabs Synthesis Error: {str(e)}")
            return None

voice_engine = OverwatchVoiceEngine()
