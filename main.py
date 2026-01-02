"""
MAITRI - Main Application
AI Assistant for Psychological & Physical Well-Being of Astronauts
"""

import cv2
import time
from datetime import datetime
from typing import Optional
import logging

from facial_expression import FacialExpressionDetector
from audio_emotion import AudioEmotionDetector
from conversation_ai import ConversationAI
from critical_detector import CriticalIssueDetector

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MAITRI:
    """Main MAITRI application class"""
    
    def __init__(self):
        """Initialize MAITRI components"""
        logger.info("Initializing MAITRI...")
        
        self.facial_detector = FacialExpressionDetector()
        self.audio_detector = AudioEmotionDetector()
        self.conversation_ai = ConversationAI()
        self.critical_detector = CriticalIssueDetector()
        
        # Data storage
        self.emotion_history = []
        self.audio_history = []
        self.last_interaction = datetime.now()
        
        logger.info("MAITRI initialized successfully")
    
    def run(self, video_source: int = 0, enable_audio: bool = True):
        """
        Run the main application loop
        
        Args:
            video_source: Video source (0 for webcam)
            enable_audio: Whether to enable audio analysis
        """
        logger.info("Starting MAITRI...")
        print("\n" + "="*60)
        print("MAITRI - AI Assistant for Astronaut Well-Being")
        print("="*60)
        print("\nPress 'q' to quit, 's' to speak, 'r' for report\n")
        
        cap = cv2.VideoCapture(video_source)
        
        if not cap.isOpened():
            logger.error("Error opening video source")
            return
        
        frame_count = 0
        last_emotion_check = time.time()
        emotion_check_interval = 2.0  # Check emotion every 2 seconds
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                current_time = time.time()
                
                # Process frame every few frames for performance
                if frame_count % 5 == 0:
                    # Detect facial expression
                    emotions = self.facial_detector.detect_emotion(frame)
                    dominant_emotion, confidence = self.facial_detector.get_dominant_emotion(frame)
                    
                    # Store emotion data
                    emotion_data = {
                        'timestamp': datetime.now().isoformat(),
                        'emotions': emotions,
                        'dominant_emotion': dominant_emotion,
                        'confidence': confidence
                    }
                    self.emotion_history.append(emotion_data)
                    
                    # Keep only last 100 entries
                    if len(self.emotion_history) > 100:
                        self.emotion_history = self.emotion_history[-100:]
                    
                    # Draw on frame
                    result = self.facial_detector.detector.detect_emotions(
                        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    ) if self.facial_detector.detector else None
                    
                    if result:
                        box = result[0]['box']
                        x, y, w, h = box
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.putText(frame, f"{dominant_emotion}: {confidence:.2f}", 
                                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    # Check for critical issues periodically
                    if current_time - last_emotion_check >= emotion_check_interval:
                        issues = self.critical_detector.check_critical_issues(
                            self.emotion_history,
                            self.audio_history,
                            self.last_interaction
                        )
                        
                        if issues:
                            print("\n⚠️  CRITICAL ISSUE DETECTED ⚠️")
                            report = self.critical_detector.generate_report(issues)
                            print(report)
                            logger.warning(f"Critical issues detected: {len(issues)}")
                        
                        # Generate proactive response if needed
                        if confidence > 0.6 and dominant_emotion in ['sad', 'angry', 'fearful']:
                            response = self.conversation_ai.generate_response(
                                dominant_emotion, confidence
                            )
                            print(f"\nMAITRI: {response}\n")
                            self.last_interaction = datetime.now()
                        
                        last_emotion_check = current_time
                
                # Display frame
                cv2.imshow('MAITRI - Emotion Detection', frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    # Audio interaction
                    self._handle_audio_interaction()
                elif key == ord('r'):
                    # Generate report
                    self._generate_report()
                elif key == ord('c'):
                    # Show conversation summary
                    summary = self.conversation_ai.get_conversation_summary()
                    print("\nConversation Summary:")
                    print(f"Total interactions: {summary['total_interactions']}")
                    print(f"Most common emotion: {summary['most_common_emotion']}")
                    print(f"Critical interventions: {summary['critical_interventions']}")
        
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            logger.info("MAITRI session ended")
    
    def _handle_audio_interaction(self):
        """Handle audio-based interaction"""
        print("\n🎤 Recording audio (3 seconds)...")
        try:
            audio_path = self.audio_detector.record_audio(duration=3.0)
            if audio_path:
                audio_emotion, confidence = self.audio_detector.get_dominant_emotion(audio_path)
                print(f"Detected audio emotion: {audio_emotion} (confidence: {confidence:.2f})")
                
                # Store audio data
                audio_data = {
                    'timestamp': datetime.now().isoformat(),
                    'emotion': audio_emotion,
                    'confidence': confidence
                }
                self.audio_history.append(audio_data)
                
                # Get latest facial emotion
                if self.emotion_history:
                    latest = self.emotion_history[-1]
                    facial_emotion = latest['dominant_emotion']
                    facial_conf = latest['confidence']
                else:
                    facial_emotion = 'neutral'
                    facial_conf = 0.5
                
                # Generate response
                response = self.conversation_ai.generate_response(
                    facial_emotion, facial_conf, audio_emotion
                )
                print(f"\nMAITRI: {response}\n")
                self.last_interaction = datetime.now()
        except Exception as e:
            logger.error(f"Error in audio interaction: {e}")
            print("Error processing audio. Please try again.")
    
    def _generate_report(self):
        """Generate and display a well-being report"""
        print("\n" + "="*60)
        print("WELL-BEING REPORT")
        print("="*60)
        
        # Emotion trends
        if self.emotion_history:
            trend_analysis = self.facial_detector.analyze_emotion_trend(
                [e['emotions'] for e in self.emotion_history[-20:]]
            )
            print(f"\nEmotion Trend: {trend_analysis['trend']}")
            print(f"Dominant Emotion: {trend_analysis['dominant']}")
            print(f"Confidence: {trend_analysis['confidence']:.2f}")
        
        # Conversation summary
        summary = self.conversation_ai.get_conversation_summary()
        print(f"\nConversation Summary:")
        print(f"  Total interactions: {summary['total_interactions']}")
        print(f"  Critical interventions: {summary['critical_interventions']}")
        print(f"  Supportive interventions: {summary['supportive_interventions']}")
        
        # Critical issues
        issues = self.critical_detector.get_issue_history(hours=24)
        if issues:
            print(f"\n⚠️  Critical Issues (last 24h): {len(issues)}")
            for issue in issues[-5:]:  # Show last 5
                print(f"  - {issue['issue_type']} ({issue['severity']})")
        else:
            print("\n✅ No critical issues detected")
        
        print("="*60 + "\n")


def main():
    """Main entry point"""
    maitri = MAITRI()
    
    # Run with webcam (change video_source if using different camera)
    maitri.run(video_source=0, enable_audio=True)


if __name__ == "__main__":
    main()

