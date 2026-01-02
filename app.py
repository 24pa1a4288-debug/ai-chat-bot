"""
MAITRI - Streamlit Web Interface
AI Assistant for Psychological & Physical Well-Being of Astronauts
"""

import streamlit as st
import cv2
import numpy as np
from datetime import datetime
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from facial_expression import FacialExpressionDetector
from audio_emotion import AudioEmotionDetector
from conversation_ai import ConversationAI
from critical_detector import CriticalIssueDetector

# Page configuration with custom CSS
st.set_page_config(
    page_title="MAITRI - AI Assistant for Astronauts",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1e3c72;
    }
    .chat-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        max-height: 500px;
        overflow-y: auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .status-active {
        color: #28a745;
        font-weight: bold;
    }
    .status-inactive {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'maitri' not in st.session_state:
    st.session_state.maitri = None
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'last_message_time' not in st.session_state:
    st.session_state.last_message_time = None


def initialize_maitri():
    """Initialize MAITRI components"""
    if st.session_state.maitri is None:
        with st.spinner("🔄 Initializing MAITRI components..."):
            try:
                st.session_state.maitri = {
                    'facial_detector': FacialExpressionDetector(),
                    'audio_detector': AudioEmotionDetector(),
                    'conversation_ai': ConversationAI(),
                    'critical_detector': CriticalIssueDetector()
                }
                st.success("✅ MAITRI initialized successfully!")
            except Exception as e:
                st.error(f"❌ Error initializing: {e}")


def main():
    """Main Streamlit application"""
    
    # Header with better styling
    st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; padding:0;">🚀 MAITRI</h1>
        <p style="margin:0.5rem 0 0 0; font-size:1.1rem;">AI Assistant for Psychological & Physical Well-Being of Astronauts</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize MAITRI
    initialize_maitri()
    
    # Sidebar with improved design
    with st.sidebar:
        st.markdown("### ⚙️ System Controls")
        
        if st.button("🔄 Initialize/Reset System", use_container_width=True, type="primary"):
            st.session_state.maitri = None
            st.session_state.emotion_history = []
            st.session_state.conversation_history = []
            st.session_state.is_running = False
            initialize_maitri()
            st.rerun()
        
        st.markdown("---")
        
        # Status section
        st.markdown("### 📊 System Status")
        if st.session_state.maitri:
            st.markdown('<p class="status-active">✅ System Active</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-inactive">❌ System Inactive</p>', unsafe_allow_html=True)
        
        # Quick stats
        if st.session_state.emotion_history:
            st.metric("Emotions Detected", len(st.session_state.emotion_history))
        if st.session_state.conversation_history:
            st.metric("Conversations", len([m for m in st.session_state.conversation_history if m['role'] == 'user']))
        
        st.markdown("---")
        st.markdown("### ℹ️ Quick Guide")
        st.markdown("""
        **Getting Started:**
        1. Click **Start Monitoring** to begin
        2. Allow camera access when prompted
        3. Type or speak to interact with MAITRI
        4. View real-time emotion detection
        5. Check reports for insights
        
        **Tips:**
        - Ensure good lighting for better detection
        - Speak clearly for audio analysis
        - Regular interactions improve accuracy
        """)
    
    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["📹 Live Monitoring", "💬 Conversation", "📊 Reports & Analytics"])
    
    # Tab 1: Live Monitoring
    with tab1:
        st.markdown("### Real-Time Emotion Detection")
        
        col_monitor1, col_monitor2 = st.columns([3, 1])
        
        with col_monitor1:
            # Start/Stop button
            monitor_button_text = "⏸️ Stop Monitoring" if st.session_state.is_running else "▶️ Start Monitoring"
            monitor_button_type = "secondary" if st.session_state.is_running else "primary"
            
            if st.button(monitor_button_text, use_container_width=True, type=monitor_button_type):
                st.session_state.is_running = not st.session_state.is_running
                st.rerun()
            
            if st.session_state.is_running and st.session_state.maitri:
                # Use Streamlit's camera input
                camera_img = st.camera_input("Camera Feed", label_visibility="collapsed")
                
                if camera_img is not None:
                    # Convert to numpy array
                    img_array = np.array(bytearray(camera_img.read()), dtype=np.uint8)
                    frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    
                    if frame is not None:
                        detector = st.session_state.maitri['facial_detector']
                        emotions = detector.detect_emotion(frame)
                        dominant, confidence = detector.get_dominant_emotion(frame)
                        
                        # Store emotion
                        emotion_data = {
                            'timestamp': datetime.now(),
                            'emotion': dominant,
                            'confidence': confidence,
                            'emotions': emotions
                        }
                        st.session_state.emotion_history.append(emotion_data)
                        
                        # Keep last 100
                        if len(st.session_state.emotion_history) > 100:
                            st.session_state.emotion_history = st.session_state.emotion_history[-100:]
            else:
                st.info("👆 Click 'Start Monitoring' to begin real-time emotion detection")
        
        with col_monitor2:
            if st.session_state.emotion_history:
                latest = st.session_state.emotion_history[-1]
                st.markdown("### Current Status")
                st.metric("Emotion", latest['emotion'].title(), delta=None)
                st.metric("Confidence", f"{latest['confidence']:.1%}")
                
                # Emotion breakdown
                emotions = latest['emotions']
                emotion_df = pd.DataFrame(list(emotions.items()), columns=['Emotion', 'Probability'])
                st.bar_chart(emotion_df.set_index('Emotion'), height=200)
                
                # Check for critical issues
                if len(st.session_state.emotion_history) >= 5 and st.session_state.maitri:
                    critical_detector = st.session_state.maitri['critical_detector']
                    issues = critical_detector.check_critical_issues(
                        [{
                            'timestamp': e['timestamp'].isoformat(),
                            'dominant_emotion': e['emotion'],
                            'confidence': e['confidence']
                        } for e in st.session_state.emotion_history[-20:]]
                    )
                    
                    if issues:
                        st.warning("⚠️ Critical Issue Detected!")
                        for issue in issues:
                            with st.expander(f"🔴 {issue['type'].replace('_', ' ').title()}"):
                                st.write(f"**Severity:** {issue['severity']}")
                                st.write(f"**Recommendation:** {issue['recommendation']}")
    
    # Tab 2: Conversation
    with tab2:
        st.markdown("### Chat with MAITRI")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display conversation history
            if st.session_state.conversation_history:
                for msg in st.session_state.conversation_history[-20:]:  # Show last 20 messages
                    with st.chat_message(msg['role']):
                        st.write(msg['content'])
                        if 'timestamp' in msg:
                            st.caption(msg['timestamp'].strftime("%H:%M:%S"))
            else:
                st.info("👋 Start a conversation with MAITRI. I'm here to support you!")
        
        # Input form for better UX
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Type your message:",
                key="chat_input",
                placeholder="How are you feeling today?",
                label_visibility="visible"
            )
            
            col_send, col_audio = st.columns([2, 1])
            
            with col_send:
                send_button = st.form_submit_button("💬 Send Message", use_container_width=True, type="primary")
            
            with col_audio:
                audio_button = st.form_submit_button("🎤 Audio", use_container_width=True)
        
        # Handle message sending
        if send_button and user_input and st.session_state.maitri:
            with st.spinner("🤔 MAITRI is thinking..."):
                # Get latest emotion
                if st.session_state.emotion_history:
                    latest = st.session_state.emotion_history[-1]
                    emotion = latest['emotion']
                    confidence = latest['confidence']
                else:
                    emotion = 'neutral'
                    confidence = 0.5
                
                # Generate response
                conversation_ai = st.session_state.maitri['conversation_ai']
                response = conversation_ai.generate_response(emotion, confidence, user_input=user_input)
                
                # Store conversation
                st.session_state.conversation_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now()
                })
                st.session_state.conversation_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now()
                })
                
                st.session_state.last_message_time = datetime.now()
                st.rerun()
        
        # Handle audio input
        if audio_button and st.session_state.maitri:
            with st.spinner("🎤 Recording audio (3 seconds)..."):
                audio_detector = st.session_state.maitri['audio_detector']
                try:
                    audio_path = audio_detector.record_audio(duration=3.0)
                    if audio_path:
                        audio_emotion, conf = audio_detector.get_dominant_emotion(audio_path)
                        st.success(f"🎵 Detected emotion: **{audio_emotion}** ({conf:.1%})")
                        
                        # Generate response
                        if st.session_state.emotion_history:
                            latest = st.session_state.emotion_history[-1]
                            emotion = latest['emotion']
                            confidence = latest['confidence']
                        else:
                            emotion = 'neutral'
                            confidence = 0.5
                        
                        conversation_ai = st.session_state.maitri['conversation_ai']
                        response = conversation_ai.generate_response(
                            emotion, confidence, audio_emotion=audio_emotion
                        )
                        
                        st.session_state.conversation_history.append({
                            'role': 'assistant',
                            'content': response,
                            'timestamp': datetime.now()
                        })
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error processing audio: {e}")
    
    # Tab 3: Reports & Analytics
    with tab3:
        st.markdown("### Well-Being Analytics & Reports")
        
        col_report1, col_report2 = st.columns(2)
        
        with col_report1:
            st.markdown("#### 📈 Emotion Trends")
            if st.session_state.emotion_history:
                df = pd.DataFrame([
                    {
                        'timestamp': e['timestamp'],
                        'emotion': e['emotion'],
                        'confidence': e['confidence']
                    }
                    for e in st.session_state.emotion_history[-50:]
                ])
                
                if not df.empty:
                    # Emotion distribution pie chart
                    emotion_counts = df['emotion'].value_counts()
                    fig = px.pie(
                        values=emotion_counts.values, 
                        names=emotion_counts.index, 
                        title="Emotion Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Timeline
                    df['timestamp'] = pd.to_datetime(df['timestamp'])
                    fig2 = px.line(
                        df, 
                        x='timestamp', 
                        y='confidence', 
                        color='emotion',
                        title="Emotion Confidence Over Time",
                        labels={'confidence': 'Confidence Level', 'timestamp': 'Time'}
                    )
                    fig2.update_layout(showlegend=True, height=300)
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("📊 No emotion data yet. Start monitoring to collect data.")
        
        with col_report2:
            st.markdown("#### ⚠️ Critical Issues")
            if st.session_state.maitri:
                critical_detector = st.session_state.maitri['critical_detector']
                issues = critical_detector.get_issue_history(hours=24)
                
                if issues:
                    for issue in issues[-5:]:
                        severity_emoji = {
                            'high': '🔴',
                            'medium': '🟡',
                            'low': '🟢'
                        }
                        with st.expander(f"{severity_emoji.get(issue['severity'], '⚪')} {issue['issue_type'].replace('_', ' ').title()}"):
                            st.write(f"**Severity:** {issue['severity'].upper()}")
                            st.write(f"**Time:** {issue['timestamp']}")
                            if 'details' in issue:
                                st.json(issue['details'])
                else:
                    st.success("✅ No critical issues detected in the last 24 hours")
            else:
                st.info("Initialize system to view critical issues")
            
            st.markdown("---")
            
            # Conversation summary with safe key access
            st.markdown("#### 💬 Conversation Summary")
            if st.session_state.maitri:
                conversation_ai = st.session_state.maitri['conversation_ai']
                summary = conversation_ai.get_conversation_summary()
                
                # Safe key access with defaults
                total = summary.get('total_interactions', 0)
                critical = summary.get('critical_interventions', 0)
                supportive = summary.get('supportive_interventions', 0)
                most_common = summary.get('most_common_emotion', 'neutral')
                
                col_metric1, col_metric2 = st.columns(2)
                with col_metric1:
                    st.metric("Total Interactions", total)
                    st.metric("Critical Interventions", critical)
                with col_metric2:
                    st.metric("Supportive Interventions", supportive)
                    st.metric("Most Common Emotion", most_common.title())
            else:
                st.info("Initialize system to view conversation summary")


if __name__ == "__main__":
    main()
