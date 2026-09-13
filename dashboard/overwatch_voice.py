# dashboard/overwatch_voice.py - Human Conversational Cadence Engine
import os
import base64

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import VoiceSettings
    ELEVEN_AVAILABLE = True
except ImportError:
    ELEVEN_AVAILABLE = False

# Set to "YOUR_ELEVENLABS_API_KEY_HERE" to rely on env variable ELEVENLABS_API_KEY
HARDCODED_KEY = "YOUR_ELEVENLABS_API_KEY_HERE"

class OverwatchVoiceEngine:
    def __init__(self, api_key: str = None, voice_id: str = "Q9Vh1SycNbxygVIup9vI"): 
        resolved_key = HARDCODED_KEY if HARDCODED_KEY != "YOUR_ELEVENLABS_API_KEY_HERE" else (api_key or os.getenv("ELEVENLABS_API_KEY"))
        self.api_key = resolved_key
        self.voice_id = voice_id
        
        if self.api_key and ELEVEN_AVAILABLE:
            self.client = ElevenLabs(api_key=self.api_key)
        else:
            self.client = None

    def synthesize_speech(self, text_prompt: str) -> str:
        """Synthesizes text into natural human speech using dynamic VoiceSettings."""
        if not self.client or not self.api_key:
            print("[!] ElevenLabs API Key missing in overwatch_voice.py")
            return None

        try:
            # Human speech inflection and cadence tuning
            voice_config = VoiceSettings(
                stability=0.35,          # Lower stability = dynamic human expression/inflection
                similarity_boost=0.85,   # High clarity for custom cloned/accented voices
                style=0.55,              # Stylistic warmth and natural pacing
                use_speaker_boost=True
            )

            audio_generator = self.client.text_to_speech.convert(
                text=text_prompt,
                voice_id=self.voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings=voice_config
            )
            
            # Consume stream generator into raw bytes
            audio_bytes = b"".join(audio_generator)
            base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
            
            # Return raw Base64 Data URI
            return f"data:audio/mp3;base64,{base64_audio}"
        except Exception as e:
            print(f"[!] ElevenLabs Synthesis Error: {str(e)}")
            return None

voice_engine = OverwatchVoiceEngine()
