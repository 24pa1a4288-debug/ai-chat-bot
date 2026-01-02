# Models Directory

This directory is for storing trained model files.

## Expected Model Files

- Facial expression recognition models (if using custom models)
- Audio emotion classification models (if using custom models)
- Pre-trained weights and checkpoints

## Current Implementation

The current implementation uses:
- **FER library** for facial expression detection (models downloaded automatically)
- **Rule-based approach** for audio emotion detection (can be replaced with trained models)

## Future Enhancements

To improve accuracy, you can:
1. Train custom models on astronaut-specific data
2. Fine-tune pre-trained models for space mission contexts
3. Add ensemble models for better reliability
4. Implement transfer learning from general emotion datasets

## Model Training

If you want to train custom models:

1. Collect training data (video/audio with emotion labels)
2. Preprocess and augment the data
3. Train models using TensorFlow/Keras
4. Save models in this directory
5. Update the detection modules to use custom models

