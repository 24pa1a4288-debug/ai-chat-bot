"""
Facial Expression Detection Module
Detects emotions from facial expressions using computer vision and deep learning
"""

import cv2
import numpy as np
from typing import Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import FER with multiple fallback options
FER = None
try:
    # Try the newer package structure first
    from fer.fer import FER
except (ImportError, AttributeError) as e:
    try:
        # Try the older package structure
        from fer import FER
    except (ImportError, AttributeError):
        try:
            # Try importing the module and accessing FER class
            import fer.fer as fer_module
            FER = getattr(fer_module, 'FER', None)
        except (ImportError, AttributeError):
            logger.warning("FER library not available. Using fallback emotion detection.")
            FER = None

# TensorFlow import is optional - FER will handle it
try:
    import tensorflow as tf
except ImportError:
    tf = None


class FacialExpressionDetector:
    """Detects facial expressions and emotions from video frames"""
    
    def __init__(self):
        """Initialize the facial expression detector"""
        self.detector = None
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        
        if FER is None:
            logger.warning("FER library not available. Using fallback emotion detection.")
            return
            
        try:
            # Initialize FER (Facial Expression Recognition) detector
            self.detector = FER(mtcnn=True)
            logger.info("Facial Expression Detector initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing detector: {e}")
            logger.warning("Falling back to basic emotion detection")
            self.detector = None
    
    def detect_emotion(self, frame: np.ndarray) -> Dict[str, float]:
        """
        Detect emotion from a single frame
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            Dictionary with emotion probabilities
        """
        if self.detector is None:
            # Fallback: Use basic face detection
            return self._fallback_emotion_detection(frame)
        
        try:
            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect emotions
            result = self.detector.detect_emotions(rgb_frame)
            
            if result and len(result) > 0:
                # Get the first face detected
                emotions = result[0]['emotions']
                return emotions
            else:
                return {'neutral': 1.0}
                
        except Exception as e:
            logger.error(f"Error detecting emotion: {e}")
            return self._fallback_emotion_detection(frame)
    
    def _fallback_emotion_detection(self, frame: np.ndarray) -> Dict[str, float]:
        """
        Fallback emotion detection using basic face detection
        Returns neutral emotion when FER is not available
        """
        try:
            # Use OpenCV's face detector as fallback
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # Face detected but can't determine emotion - return neutral
                return {'neutral': 0.8, 'happy': 0.1, 'sad': 0.1}
            else:
                return {'neutral': 1.0}
        except Exception as e:
            logger.error(f"Error in fallback detection: {e}")
            return {'neutral': 1.0}
    
    def get_dominant_emotion(self, frame: np.ndarray) -> Tuple[str, float]:
        """
        Get the dominant emotion from a frame
        
        Args:
            frame: Input image frame
            
        Returns:
            Tuple of (emotion_name, confidence)
        """
        emotions = self.detect_emotion(frame)
        if emotions:
            dominant = max(emotions.items(), key=lambda x: x[1])
            return dominant
        return ('neutral', 1.0)
    
    def process_video_stream(self, video_source: int = 0):
        """
        Process video stream in real-time
        
        Args:
            video_source: Video source (0 for webcam)
            
        Yields:
            Tuple of (frame, emotion_dict, dominant_emotion)
        """
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            logger.error("Error opening video source")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect emotion
            emotions = self.detect_emotion(frame)
            dominant_emotion, confidence = self.get_dominant_emotion(frame)
            
            # Draw bounding box and emotion on frame
            if self.detector is not None:
                try:
                    result = self.detector.detect_emotions(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    if result:
                        box = result[0]['box']
                        x, y, w, h = box
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{dominant_emotion}: {confidence:.2f}", 
                                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                except Exception:
                    # Fallback: use OpenCV face detection
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{dominant_emotion}: {confidence:.2f}", 
                                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        break
            
            yield frame, emotions, (dominant_emotion, confidence)
        
        cap.release()
    
    def analyze_emotion_trend(self, emotion_history: list) -> Dict[str, any]:
        """
        Analyze emotion trends over time
        
        Args:
            emotion_history: List of emotion dictionaries over time
            
        Returns:
            Analysis dictionary with trends and patterns
        """
        if not emotion_history:
            return {'trend': 'stable', 'dominant': 'neutral'}
        
        # Calculate average emotions
        avg_emotions = {}
        for emotion in self.emotions:
            avg_emotions[emotion] = np.mean([e.get(emotion, 0) for e in emotion_history])
        
        dominant = max(avg_emotions.items(), key=lambda x: x[1])
        
        # Detect trends
        recent = emotion_history[-10:] if len(emotion_history) >= 10 else emotion_history
        recent_avg = {}
        for emotion in self.emotions:
            recent_avg[emotion] = np.mean([e.get(emotion, 0) for e in recent])
        
        # Compare with overall average
        trend = 'stable'
        if recent_avg.get('sad', 0) > avg_emotions.get('sad', 0) + 0.2:
            trend = 'declining'
        elif recent_avg.get('happy', 0) > avg_emotions.get('happy', 0) + 0.2:
            trend = 'improving'
        
        return {
            'trend': trend,
            'dominant': dominant[0],
            'confidence': dominant[1],
            'averages': avg_emotions
        }

