# MAITRI Quick Start Guide

## Quick Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or use setup script
python setup.py
```

## Running the Application

### Web Interface (Easiest)

```bash
streamlit run app.py
```

Then open your browser to the URL shown (usually http://localhost:8501)

### Command Line Interface

```bash
python main.py
```

## First Steps

1. **Start the application** using one of the methods above
2. **Allow camera access** when prompted
3. **Click "Start Monitoring"** (web interface) or the app will start automatically (CLI)
4. **Interact with MAITRI**:
   - The system will automatically detect your facial expressions
   - Press 's' (CLI) or click "Record Audio" (web) to analyze your voice
   - Type messages to have a conversation
   - View reports to see your emotional trends

## Understanding the Output

### Emotions Detected
- **Happy**: Positive emotional state
- **Sad**: Low mood, may need support
- **Angry**: Frustration or irritation
- **Fearful**: Anxiety or concern
- **Surprised**: Unexpected reaction
- **Disgust**: Discomfort or aversion
- **Neutral**: Balanced emotional state

### Confidence Scores
- Higher confidence (>0.7) = More reliable detection
- Lower confidence (<0.5) = May need better lighting/positioning

### Critical Issues
The system will alert you if it detects:
- Sustained negative emotions (15+ minutes)
- Rapid emotion swings
- Extreme emotional states
- Communication breakdowns

## Tips for Best Results

1. **Lighting**: Ensure good lighting on your face
2. **Position**: Face the camera directly
3. **Audio**: Speak clearly when recording audio
4. **Privacy**: All processing is done locally - no data is sent to external servers

## Troubleshooting

### Camera not working?
- Check camera permissions
- Try a different camera (change video_source in code)
- Restart the application

### Audio not working?
- Check microphone permissions
- Install PyAudio properly (see README for Windows instructions)
- Audio is optional - facial detection works without it

### Model loading errors?
- Ensure all dependencies are installed
- Check internet connection for first-time model downloads
- Models are cached after first download

## Next Steps

- Review the full README.md for detailed documentation
- Customize responses in `conversation_ai.py`
- Adjust detection thresholds in `critical_detector.py`
- Train custom models for improved accuracy

## Support

For issues or questions, check the code comments or refer to the main README.md file.

