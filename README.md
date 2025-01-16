# Real-Time Vision Analysis with Gemini Pro Vision

## Historical Context

This project was developed during the initial release of Google's Gemini Pro Vision model. While the implementation uses the original Gemini Pro Vision API, it's worth noting that Google has since released several significant updates:

- Gemini Multimodal Live API
- Gemini 1.5 Flash
- Gemini 2.0 Flash
- Gemini 1.5 Pro

These newer versions offer enhanced capabilities for handling multi-modal inputs (audio, image, text) and real-time processing of audio/video feeds (Multimodal Live API). Consider updating to one of these APIs / models with the latest Google SDKs.

## Project Overview

This application creates a real-time video analysis system using Flask and Google's Vertex AI platform. It captures frames from a webcam and processes them through the Gemini Pro Vision model to generate descriptions of what it sees.

### Features

- Real-time webcam capture
- Automated image analysis using Gemini Pro Vision
- Server-sent events for live updates
- Clean, minimalist web interface
- Threaded processing for smooth performance

## Prerequisites

- Python 3.7+
- Flask
- OpenCV (cv2)
- Google Cloud Vertex AI access
- Webcam

## Setup

1. Set up Google Cloud Project:
   ```bash
   export PROJECT_ID="your-project-id"
   export REGION="your-region"
   ```

2. Install dependencies:
   ```bash
   pip install flask opencv-python google-cloud-aiplatform
   ```

3. Create an images directory:
   ```bash
   mkdir images
   ```

4. Configure Google Cloud credentials:
   - Set up application credentials for Google Cloud
   - Enable Vertex AI API in your project

## Project Structure

```
├── app.py              # Main Flask application
├── templates/
│   └── index.html     # Web interface
├── test.py            # Test script for Gemini Vision API
└── images/            # Directory for captured frames
```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Use the interface buttons to:
   - Start camera capture and analysis
   - Stop camera capture and analysis
   - View real-time Gemini Vision descriptions

## How It Works

1. The application runs two main threads:
   - Camera thread: Captures frames every 10 seconds
   - Analysis thread: Processes the latest captured frame through Gemini Pro Vision

2. The web interface:
   - Displays the live camera feed
   - Shows real-time AI analysis results
   - Provides control buttons for starting/stopping the system

3. Server-sent events (SSE) are used to push updates to the browser without requiring page refreshes.

## Technical Details

- Frame capture rate: 1 frame every 10 seconds
- Image format: PNG
- API: Gemini Pro Vision (Vertex AI)
- Web server: Flask with threading enabled
- Frontend: HTML5 with vanilla JavaScript

## Limitations

- Currently uses the legacy Gemini Pro Vision API
- Only processes one frame every 10 seconds to manage API usage
- Requires constant internet connection for API calls


