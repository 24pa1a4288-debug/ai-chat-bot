# MAITRI: An AI Assistant for Psychological & Physical Well-Being of Astronauts

## Description

MAITRI is a multimodal AI assistant designed to detect emotional and physical well-being of crew members using audio-video inputs. It provides psychological companionship, adaptive conversations, and reports critical issues to ground control.

## Features

- **Facial Expression Detection**: Real-time emotion recognition from video input
- **Audio Emotion Analysis**: Voice tone and emotion detection from audio
- **Psychological Support**: Adaptive conversations to maintain balanced emotional state
- **Critical Issue Reporting**: Automatic detection and reporting of concerning patterns
- **Offline Operation**: Standalone system that works without internet connection

## Installation

### Prerequisites
- Python 3.8 or higher
- Webcam (for video input)
- Microphone (for audio input, optional)

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or use the setup script:
```bash
python setup.py
```

**Note for Windows users:** PyAudio installation may require additional steps:
- Download the appropriate wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Install using: `pip install <downloaded_wheel_file>`

## Usage

### Option 1: Command-Line Interface
Run the main application:
```bash
python main.py
```

**Controls:**
- `q` - Quit application
- `s` - Record and analyze audio (3 seconds)
- `r` - Generate well-being report
- `c` - Show conversation summary

### Option 2: Web Interface (Recommended)
Run the Streamlit web interface:
```bash
streamlit run app.py
```

The web interface provides:
- Real-time video feed with emotion detection
- Interactive chat interface
- Audio recording and analysis
- Visual emotion trends and charts
- Critical issue alerts
- Comprehensive well-being reports

## Features

### 1. Facial Expression Detection
- Real-time emotion recognition from video
- Supports 7 emotions: angry, disgust, fear, happy, sad, surprise, neutral
- Confidence scoring for each detection

### 2. Audio Emotion Analysis
- Voice tone analysis from audio recordings
- Feature extraction using MFCC, chroma, spectral features
- Emotion classification from audio characteristics

### 3. Multimodal Integration
- Combines facial and audio emotion data
- Provides comprehensive emotional state assessment
- Adaptive responses based on detected emotions

### 4. Psychological Support
- Adaptive conversational AI
- Evidence-based interventions
- Breathing exercises and positive reminders
- Activity suggestions

### 5. Critical Issue Detection
- Sustained negative emotion detection
- Rapid emotion swing identification
- Extreme emotion alerts
- Communication breakdown monitoring
- Automatic ground control reporting

## Architecture

The system consists of four main modules:

1. **Facial Expression Detector** (`facial_expression.py`)
   - Uses FER (Facial Expression Recognition) library
   - Real-time video processing
   - Emotion trend analysis

2. **Audio Emotion Detector** (`audio_emotion.py`)
   - Feature extraction from audio
   - Emotion classification
   - Voice tone analysis

3. **Conversation AI** (`conversation_ai.py`)
   - Adaptive response generation
   - Psychological support interventions
   - Conversation history management

4. **Critical Issue Detector** (`critical_detector.py`)
   - Pattern recognition for critical states
   - Automated reporting
   - Issue history tracking

## Performance Notes

- The system is designed to run offline
- For production use, consider training custom models on astronaut-specific data
- Current implementation uses pre-trained models and rule-based approaches
- Can be extended with custom ML models for improved accuracy

## Future Enhancements

- Integration with physical health monitoring sensors
- Custom model training on astronaut-specific data
- Multi-language support
- Enhanced NLP for more natural conversations
- Integration with mission control systems

## Project Structure

```
.
├── main.py                 # Main application entry point
├── app.py                  # Streamlit web interface
├── facial_expression.py    # Facial expression detection module
├── audio_emotion.py       # Audio emotion detection module
├── conversation_ai.py     # Conversational AI component
├── critical_detector.py   # Critical issue detection
├── models/                # Trained model files
├── utils/                 # Utility functions
└── requirements.txt       # Python dependencies
```

## Challenges Addressed

- Correct interpretation of human emotions from audio-visual input
- Situation-based short relevant interactions
- Evidence-based interventions for psychological support

## Usage Context

Designed for use in Bhartiya Antariksh Station (BAS) as a useful assistant to crew members.

