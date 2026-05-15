"""
Voice Service module.
Handles:
- Speech-to-text
- Text-to-speech
"""

from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
from typing import Optional


class VoiceService:

    def __init__(self):

        self.recognizer = sr.Recognizer()

    def speech_to_text_from_audio(
        self,
        input_audio_path: str
    ) -> Optional[str]:
        """
        Convert browser recorded audio into text.
        """

        try:

            # Convert audio to proper WAV PCM
            sound = AudioSegment.from_file(input_audio_path)

            converted_path = "converted_audio.wav"

            sound.export(
                converted_path,
                format="wav"
            )

            # Read converted audio
            with sr.AudioFile(converted_path) as source:

                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio)

            return text

        except sr.UnknownValueError:

            print("Could not understand audio")

            return None

        except sr.RequestError as e:

            print(f"Speech recognition service error: {e}")

            return None

        except Exception as e:

            print(f"Speech recognition error: {e}")

            return None

    def text_to_speech(
        self,
        text: str
    ) -> Optional[str]:
        """
        Convert text to speech.
        """

        try:

            tts = gTTS(
                text=text,
                lang="en"
            )

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            tts.save(temp_file.name)

            return temp_file.name

        except Exception as e:

            print(f"TTS error: {e}")

            return None