"""
Audio Emotion Detection Module
Detects emotions from voice tone and audio characteristics
"""

import librosa
import numpy as np
import soundfile as sf
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple, Optional
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioEmotionDetector:
    """Detects emotions from audio/voice input"""
    
    def __init__(self):
        """Initialize the audio emotion detector"""
        self.emotions = ['neutral', 'calm', 'happy', 'sad', 'angry', 'fearful', 'disgust', 'surprised']
        self.scaler = StandardScaler()
        logger.info("Audio Emotion Detector initialized")
    
    def extract_features(self, audio_path: str, duration: float = 3.0) -> np.ndarray:
        """
        Extract audio features for emotion detection
        
        Args:
            audio_path: Path to audio file
            duration: Duration of audio to analyze (seconds)
            
        Returns:
            Feature vector
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, duration=duration, sr=22050)
            
            # Extract features
            features = []
            
            # MFCC (Mel-frequency cepstral coefficients)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            features.extend(np.mean(mfccs, axis=1))
            features.extend(np.std(mfccs, axis=1))
            
            # Chroma features
            chroma = librosa.feature.chroma(y=y, sr=sr)
            features.extend(np.mean(chroma, axis=1))
            features.extend(np.std(chroma, axis=1))
            
            # Mel spectrogram
            mel = librosa.feature.melspectrogram(y=y, sr=sr)
            features.append(np.mean(mel))
            features.append(np.std(mel))
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)
            features.append(np.mean(zcr))
            features.append(np.std(zcr))
            
            # Spectral centroid
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
            features.append(np.mean(spectral_centroids))
            features.append(np.std(spectral_centroids))
            
            # Spectral rolloff
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            features.append(np.mean(spectral_rolloff))
            features.append(np.std(spectral_rolloff))
            
            # Tempo
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features.append(tempo)
            
            return np.array(features)
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return np.zeros(50)  # Return zero vector if error
    
    def detect_emotion_from_features(self, features: np.ndarray) -> Dict[str, float]:
        """
        Detect emotion from extracted features using rule-based approach
        (In production, this would use a trained ML model)
        
        Args:
            features: Feature vector
            
        Returns:
            Dictionary with emotion probabilities
        """
        # This is a simplified rule-based approach
        # In production, use a trained classifier (SVM, Random Forest, or Neural Network)
        
        # Normalize features
        if len(features) > 0:
            features = features / (np.abs(features).max() + 1e-8)
        
        # Simple heuristic-based emotion detection
        # (This would be replaced with a trained model)
        emotions = {}
        
        # Extract key features (simplified indices)
        mfcc_mean = np.mean(features[:13]) if len(features) > 13 else 0
        tempo = features[-1] if len(features) > 0 else 100
        zcr = features[-3] if len(features) > 3 else 0
        
        # Rule-based emotion mapping
        if tempo > 120 and mfcc_mean > 0.1:
            emotions['happy'] = 0.6
            emotions['neutral'] = 0.2
            emotions['calm'] = 0.2
        elif tempo < 80 and mfcc_mean < -0.1:
            emotions['sad'] = 0.6
            emotions['neutral'] = 0.3
            emotions['calm'] = 0.1
        elif zcr > 0.1:
            emotions['angry'] = 0.5
            emotions['fearful'] = 0.3
            emotions['neutral'] = 0.2
        else:
            emotions['neutral'] = 0.7
            emotions['calm'] = 0.3
        
        # Normalize probabilities
        total = sum(emotions.values())
        if total > 0:
            emotions = {k: v/total for k, v in emotions.items()}
        else:
            emotions = {'neutral': 1.0}
        
        return emotions
    
    def detect_emotion(self, audio_path: str) -> Dict[str, float]:
        """
        Detect emotion from audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with emotion probabilities
        """
        features = self.extract_features(audio_path)
        return self.detect_emotion_from_features(features)
    
    def get_dominant_emotion(self, audio_path: str) -> Tuple[str, float]:
        """
        Get the dominant emotion from audio
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Tuple of (emotion_name, confidence)
        """
        emotions = self.detect_emotion(audio_path)
        if emotions:
            dominant = max(emotions.items(), key=lambda x: x[1])
            return dominant
        return ('neutral', 1.0)
    
    def record_audio(self, duration: float = 3.0, sample_rate: int = 22050) -> str:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            sample_rate: Sample rate for recording
            
        Returns:
            Path to saved audio file
        """
        try:
            import pyaudio
            import wave
            
            chunk = 1024
            format = pyaudio.paInt16
            channels = 1
            
            p = pyaudio.PyAudio()
            
            stream = p.open(format=format,
                          channels=channels,
                          rate=sample_rate,
                          input=True,
                          frames_per_buffer=chunk)
            
            logger.info("Recording...")
            frames = []
            
            for _ in range(0, int(sample_rate / chunk * duration)):
                data = stream.read(chunk)
                frames.append(data)
            
            logger.info("Finished recording")
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Save to file
            output_path = "temp_audio.wav"
            wf = wave.open(output_path, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None

