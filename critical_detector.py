"""
Critical Issue Detection Module
Detects critical psychological or physical well-being issues
"""

from typing import Dict, List, Tuple
import logging
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CriticalIssueDetector:
    """Detects critical issues requiring ground control notification"""
    
    def __init__(self):
        """Initialize the critical issue detector"""
        self.issue_history = []
        self.critical_thresholds = {
            'sustained_negative_emotion': {
                'emotion': ['sad', 'angry', 'fearful'],
                'duration_minutes': 15,
                'confidence_threshold': 0.7
            },
            'rapid_emotion_swings': {
                'swings_per_minute': 3,
                'time_window_minutes': 5
            },
            'extreme_emotion': {
                'emotion': ['angry', 'fearful'],
                'confidence_threshold': 0.9,
                'duration_minutes': 5
            },
            'communication_breakdown': {
                'no_response_minutes': 30
            }
        }
        
        logger.info("Critical Issue Detector initialized")
    
    def check_critical_issues(self, emotion_data: List[Dict], 
                            audio_data: List[Dict] = None,
                            last_interaction: datetime = None) -> List[Dict]:
        """
        Check for critical issues based on emotion patterns
        
        Args:
            emotion_data: List of emotion dictionaries with timestamps
            audio_data: List of audio emotion dictionaries (optional)
            last_interaction: Last time user interacted (optional)
            
        Returns:
            List of detected critical issues
        """
        issues = []
        
        # Check sustained negative emotion
        sustained = self._check_sustained_negative_emotion(emotion_data)
        if sustained:
            issues.append(sustained)
        
        # Check rapid emotion swings
        swings = self._check_rapid_emotion_swings(emotion_data)
        if swings:
            issues.append(swings)
        
        # Check extreme emotions
        extreme = self._check_extreme_emotion(emotion_data)
        if extreme:
            issues.append(extreme)
        
        # Check communication breakdown
        if last_interaction:
            breakdown = self._check_communication_breakdown(last_interaction)
            if breakdown:
                issues.append(breakdown)
        
        # Log issues
        for issue in issues:
            self.issue_history.append({
                'timestamp': datetime.now().isoformat(),
                'issue_type': issue['type'],
                'severity': issue['severity'],
                'details': issue['details']
            })
        
        return issues
    
    def _check_sustained_negative_emotion(self, emotion_data: List[Dict]) -> Dict:
        """Check for sustained negative emotions"""
        if len(emotion_data) < 5:
            return None
        
        threshold = self.critical_thresholds['sustained_negative_emotion']
        negative_emotions = threshold['emotion']
        duration = threshold['duration_minutes']
        confidence_threshold = threshold['confidence_threshold']
        
        # Get recent emotions within duration window
        now = datetime.now()
        recent_emotions = [
            e for e in emotion_data 
            if (now - datetime.fromisoformat(e.get('timestamp', now.isoformat()))).total_seconds() / 60 <= duration
        ]
        
        if len(recent_emotions) < 3:
            return None
        
        # Count negative emotions
        negative_count = sum(
            1 for e in recent_emotions 
            if e.get('dominant_emotion') in negative_emotions 
            and e.get('confidence', 0) >= confidence_threshold
        )
        
        if negative_count >= len(recent_emotions) * 0.7:  # 70% of recent emotions are negative
            return {
                'type': 'sustained_negative_emotion',
                'severity': 'high',
                'details': {
                    'emotion': recent_emotions[-1].get('dominant_emotion'),
                    'duration_minutes': duration,
                    'negative_percentage': (negative_count / len(recent_emotions)) * 100
                },
                'recommendation': 'Immediate psychological support recommended. Consider ground control notification.'
            }
        
        return None
    
    def _check_rapid_emotion_swings(self, emotion_data: List[Dict]) -> Dict:
        """Check for rapid emotion swings"""
        if len(emotion_data) < 5:
            return None
        
        threshold = self.critical_thresholds['rapid_emotion_swings']
        swings_per_minute = threshold['swings_per_minute']
        time_window = threshold['time_window_minutes']
        
        # Get recent emotions
        now = datetime.now()
        recent_emotions = [
            e for e in emotion_data 
            if (now - datetime.fromisoformat(e.get('timestamp', now.isoformat()))).total_seconds() / 60 <= time_window
        ]
        
        if len(recent_emotions) < 3:
            return None
        
        # Count emotion changes
        emotion_changes = 0
        prev_emotion = None
        for e in recent_emotions:
            current = e.get('dominant_emotion')
            if prev_emotion and current != prev_emotion:
                emotion_changes += 1
            prev_emotion = current
        
        if emotion_changes >= swings_per_minute * time_window:
            return {
                'type': 'rapid_emotion_swings',
                'severity': 'medium',
                'details': {
                    'swings_detected': emotion_changes,
                    'time_window_minutes': time_window
                },
                'recommendation': 'Monitor closely. May indicate stress or instability.'
            }
        
        return None
    
    def _check_extreme_emotion(self, emotion_data: List[Dict]) -> Dict:
        """Check for extreme emotions"""
        if not emotion_data:
            return None
        
        threshold = self.critical_thresholds['extreme_emotion']
        extreme_emotions = threshold['emotion']
        confidence_threshold = threshold['confidence_threshold']
        duration = threshold['duration_minutes']
        
        # Get recent emotions
        now = datetime.now()
        recent_emotions = [
            e for e in emotion_data 
            if (now - datetime.fromisoformat(e.get('timestamp', now.isoformat()))).total_seconds() / 60 <= duration
        ]
        
        if not recent_emotions:
            return None
        
        # Check for extreme emotions
        extreme_count = sum(
            1 for e in recent_emotions 
            if e.get('dominant_emotion') in extreme_emotions 
            and e.get('confidence', 0) >= confidence_threshold
        )
        
        if extreme_count >= 2:  # At least 2 extreme emotion detections
            return {
                'type': 'extreme_emotion',
                'severity': 'high',
                'details': {
                    'emotion': recent_emotions[-1].get('dominant_emotion'),
                    'confidence': recent_emotions[-1].get('confidence', 0),
                    'occurrences': extreme_count
                },
                'recommendation': 'Immediate attention required. Consider ground control notification.'
            }
        
        return None
    
    def _check_communication_breakdown(self, last_interaction: datetime) -> Dict:
        """Check for communication breakdown"""
        threshold = self.critical_thresholds['communication_breakdown']
        no_response_minutes = threshold['no_response_minutes']
        
        if not last_interaction:
            return None
        
        minutes_since = (datetime.now() - last_interaction).total_seconds() / 60
        
        if minutes_since >= no_response_minutes:
            return {
                'type': 'communication_breakdown',
                'severity': 'high',
                'details': {
                    'minutes_since_last_interaction': minutes_since
                },
                'recommendation': 'Attempt to re-establish communication. If unsuccessful, notify ground control.'
            }
        
        return None
    
    def generate_report(self, issues: List[Dict]) -> str:
        """
        Generate a formatted report for ground control
        
        Args:
            issues: List of critical issues
            
        Returns:
            Formatted report string
        """
        if not issues:
            return "No critical issues detected. All systems normal."
        
        report = f"CRITICAL ISSUE REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "=" * 50 + "\n\n"
        
        for i, issue in enumerate(issues, 1):
            report += f"Issue #{i}: {issue['type'].replace('_', ' ').title()}\n"
            report += f"Severity: {issue['severity'].upper()}\n"
            report += f"Details: {json.dumps(issue['details'], indent=2)}\n"
            report += f"Recommendation: {issue['recommendation']}\n\n"
        
        return report
    
    def get_issue_history(self, hours: int = 24) -> List[Dict]:
        """
        Get issue history for specified time period
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of issues
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        return [
            issue for issue in self.issue_history
            if datetime.fromisoformat(issue['timestamp']) >= cutoff
        ]

