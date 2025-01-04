# Screen-N-Cam-Plus

A Python-based camera application that provides real-time face detection, FPS monitoring, and video processing capabilities.

## Features

- Real-time face detection with circular highlighting
- FPS (Frames Per Second) monitoring
- Contour detection
- Modular design with separate components for:
  - Camera feed handling
  - AI-powered camera operations
  - Post-processing effects
  - Face detection and highlighting
  - Text overlay

## Requirements

- Python 3.x
- OpenCV (cv2)
- Additional dependencies (list them in requirements.txt)

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd Screen-N-Cam-Plus
```

2. Install required packages
```bash
pip install -r requirements.txt
```

Test
Test the main application:
```bash
python app/Modules/test.py
```
- Press 'q' to quit the application

- The application will display the camera feed with:

    + Face detection (circular highlight)

    + Real-time FPS counter

    + Contour detection (if enabled)

## Project Structure
<pre>
app/
├── Modules/
│   ├── test.py
│   ├── post_process.py
│   ├── camera_feed.py
│   ├── ai_camera.py
│   └── post_process
</pre>
## Components
- CameraFeed: Handles video capture and frame retrieval

- AICamera: Manages AI-powered camera operations

- FaceCircle: Implements face detection and circular highlighting

- TextOverlay: Handles text overlay on frames

- Contour: Manages contour detection and processing

## Contributing
1. Fork the repository

2. Create your feature branch

3. Commit your changes

4. Push to the branch

5. Create a new Pull Request

## License
see LICENSE file.

## Acknowledgments
OpenCV for computer vision capabilities
