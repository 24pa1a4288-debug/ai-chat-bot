"""
Conversational AI Module
Provides psychological support and adaptive conversations
"""

import random
from typing import Dict, List, Tuple, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConversationAI:
    """Provides adaptive conversations for psychological support"""
    
    def __init__(self):
        """Initialize the conversational AI"""
        self.conversation_history = []
        self.emotion_context = {}
        self.intervention_level = 'normal'  # normal, supportive, critical
        
        # Response templates based on emotions
        self.response_templates = {
            'sad': [
                "I notice you might be feeling down. Would you like to talk about what's on your mind?",
                "It's okay to feel this way. Remember, you're doing important work. Would you like to share what's bothering you?",
                "I'm here to listen. Sometimes talking about our feelings can help. What would you like to discuss?",
                "You've been working hard. It's normal to feel overwhelmed. Let's take a moment to breathe together."
            ],
            'angry': [
                "I sense some frustration. Let's take a deep breath together. What's causing this feeling?",
                "It sounds like something is bothering you. Would you like to discuss it?",
                "I understand this might be challenging. Let's work through this together, step by step."
            ],
            'fearful': [
                "I notice some anxiety. Remember, you're safe and well-trained for this mission. What's making you feel this way?",
                "It's natural to feel concerned. Let's talk through what's worrying you.",
                "You're in a controlled environment with excellent support. What specific concern would you like to address?"
            ],
            'happy': [
                "Great to see you're in good spirits! How has your day been?",
                "I'm glad you're feeling positive! Is there anything specific that's going well?",
                "Wonderful! It's good to see you're doing well. Keep up the great work!"
            ],
            'neutral': [
                "How are you feeling today?",
                "How can I assist you today?",
                "Is there anything you'd like to talk about or any support you need?"
            ],
            'surprised': [
                "Something unexpected happened? Would you like to discuss it?",
                "I notice a reaction. What's going on?",
                "Is everything okay? I'm here to help if you need anything."
            ],
            'disgust': [
                "I sense some discomfort. What's causing this feeling?",
                "Would you like to talk about what's bothering you?",
                "I'm here to help. What can we address together?"
            ]
        }
        
        # Supportive interventions
        self.interventions = {
            'breathing_exercise': [
                "Let's do a breathing exercise together. Inhale slowly for 4 counts... hold for 4... exhale for 4...",
                "Take a moment to breathe deeply. This can help calm your nervous system.",
                "Let's practice some deep breathing. Focus on your breath."
            ],
            'positive_reminder': [
                "Remember, you're part of an incredible mission. Your work is making a difference.",
                "You've trained extensively for this. You have the skills and knowledge to succeed.",
                "You're not alone. Your team and ground control are here to support you."
            ],
            'activity_suggestion': [
                "Would you like to try a brief exercise routine? Physical activity can help improve mood.",
                "How about listening to some calming music?",
                "Would you like to review your mission objectives? Sometimes focusing on goals can help."
            ]
        }
        
        logger.info("Conversation AI initialized")
    
    def generate_response(self, emotion: str, confidence: float, 
                         audio_emotion: Optional[str] = None,
                         user_input: Optional[str] = None) -> str:
        """
        Generate an adaptive response based on detected emotions
        
        Args:
            emotion: Detected facial emotion
            confidence: Confidence level of detection
            audio_emotion: Detected audio emotion (optional)
            user_input: User's text input (optional)
            
        Returns:
            Generated response string
        """
        # Determine primary emotion
        primary_emotion = emotion.lower()
        
        # If audio emotion differs significantly, consider both
        if audio_emotion and audio_emotion != primary_emotion:
            # Combine insights
            if primary_emotion in ['sad', 'angry', 'fearful']:
                primary_emotion = primary_emotion  # Prioritize negative emotions
            elif audio_emotion in ['sad', 'angry', 'fearful']:
                primary_emotion = audio_emotion
        
        # Check if intervention is needed
        if confidence > 0.7 and primary_emotion in ['sad', 'angry', 'fearful']:
            self.intervention_level = 'supportive'
        elif confidence > 0.8 and primary_emotion in ['sad', 'angry']:
            self.intervention_level = 'critical'
        else:
            self.intervention_level = 'normal'
        
        # Generate response
        if user_input:
            # Respond to user input
            response = self._respond_to_input(user_input, primary_emotion)
        else:
            # Proactive response based on emotion
            if primary_emotion in self.response_templates:
                response = random.choice(self.response_templates[primary_emotion])
            else:
                response = random.choice(self.response_templates['neutral'])
        
        # Add intervention if needed
        if self.intervention_level == 'supportive':
            intervention = random.choice(self.interventions['breathing_exercise'])
            response += f"\n\n{intervention}"
        elif self.intervention_level == 'critical':
            intervention = random.choice(self.interventions['positive_reminder'])
            response += f"\n\n{intervention}"
            # Suggest activity
            activity = random.choice(self.interventions['activity_suggestion'])
            response += f"\n\n{activity}"
        
        # Log conversation
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'emotion': primary_emotion,
            'confidence': confidence,
            'user_input': user_input,
            'response': response,
            'intervention_level': self.intervention_level
        })
        
        return response
    
    def _respond_to_input(self, user_input: str, emotion: str) -> str:
        """
        Respond to user's text input
        
        Args:
            user_input: User's message
            emotion: Current detected emotion
            
        Returns:
            Response string
        """
        user_lower = user_input.lower()
        
        # Keyword-based responses (in production, use NLP/LLM)
        if any(word in user_lower for word in ['help', 'support', 'need']):
            return "I'm here to help. What specific support do you need right now?"
        
        elif any(word in user_lower for word in ['tired', 'exhausted', 'sleep']):
            return "I understand you're feeling tired. Rest is important. Have you been able to get adequate sleep? Remember, your health is a priority."
        
        elif any(word in user_lower for word in ['stress', 'stressed', 'pressure']):
            return "Stress is a natural response. Let's work through this together. What's causing you the most stress right now?"
        
        elif any(word in user_lower for word in ['lonely', 'alone', 'isolated']):
            return "I understand that isolation can be challenging. Remember, you're part of a team, and we're all connected. Would you like to talk about what you're missing?"
        
        elif any(word in user_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome! I'm here whenever you need support. How are you feeling now?"
        
        elif any(word in user_lower for word in ['fine', 'okay', 'good', 'well']):
            return "That's good to hear! I'm glad you're doing well. Is there anything else you'd like to discuss?"
        
        else:
            # Generic empathetic response
            if emotion in ['sad', 'angry', 'fearful']:
                return "I hear you. It sounds like you're going through something challenging. Would you like to talk more about it?"
            else:
                return "Thank you for sharing. How can I best support you right now?"
    
    def get_conversation_summary(self) -> Dict:
        """
        Get summary of conversation history
        
        Returns:
            Dictionary with conversation summary
        """
        if not self.conversation_history:
            return {'total_interactions': 0}
        
        emotions = [entry['emotion'] for entry in self.conversation_history]
        intervention_levels = [entry['intervention_level'] for entry in self.conversation_history]
        
        return {
            'total_interactions': len(self.conversation_history),
            'most_common_emotion': max(set(emotions), key=emotions.count) if emotions else 'neutral',
            'critical_interventions': intervention_levels.count('critical'),
            'supportive_interventions': intervention_levels.count('supportive'),
            'recent_emotions': emotions[-10:] if len(emotions) > 10 else emotions
        }
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        self.intervention_level = 'normal'
        logger.info("Conversation history reset")

