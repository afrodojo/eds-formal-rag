# dashboard/overwatch_voice.py - ElevenLabs SDK v1.0+ Compatible Engine
import os
import base64
from elevenlabs import ElevenLabs

class OverwatchVoiceEngine:
    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Default Voice ID (Rachel)
        
        if self.api_key:
            self.client = ElevenLabs(api_key=self.api_key)
        else:
            self.client = None

    def synthesize_speech(self, text: str) -> str:
        if not self.client or not text:
            return None

        try:
            # SDK v1.0+ uses client.text_to_speech.convert()
            audio_generator = self.client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_monolingual_v1"
            )
            
            # Consume stream generator into bytes
            audio_bytes = b"".join(list(audio_generator))
            
            # Encode to Base64 URI for HTML5 audio element
            base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            return f"data:audio/mp3;base64,{base64_audio}"

        except Exception as e:
            print(f"[!] ElevenLabs Synthesis Error: {str(e)}")
            return None
