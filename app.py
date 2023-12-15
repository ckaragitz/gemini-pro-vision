from flask import Flask, render_template, jsonify, Response
import cv2
import threading
import time
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

# Initialize Vertex AI
PROJECT_ID = "ck-vertex"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)

app = Flask(__name__)

# Global variables
camera_thread = None
analyze_thread = None
camera_running = False
analyze_running = False
latest_image_path = None
latest_ai_response = "No response yet."

def analyze_image():
    global latest_image_path, latest_ai_response, analyze_running

    analyze_running = True
    while analyze_running:
        if latest_image_path:
            image_path = latest_image_path
            latest_image_path = None

            image = Image.load_from_file(image_path)
            generative_multimodal_model = GenerativeModel("gemini-pro-vision")
            response = generative_multimodal_model.generate_content(["What is shown in this image? Describe it in a few words but be detailed. Only point out new observations.", image])
            print(str(response))

            if response and response.candidates:
                ai_response_text = response.candidates[0].content.parts[0].text.strip()
                latest_ai_response = ai_response_text
        time.sleep(1)

def capture_frames():
    global latest_image_path, camera_running
    camera_running = True
    first_frame_captured = False
    cap = cv2.VideoCapture(0)

    while camera_running and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if not first_frame_captured:
            time.sleep(1)  # Wait for 1 second before capturing the first frame
            first_frame_captured = True
        else:
            time.sleep(9)  # Wait for 9 seconds before capturing subsequent frames

        timestamp = int(time.time())
        filename = f'images/image_{timestamp}.png'
        cv2.imwrite(filename, frame)
        latest_image_path = filename

    cap.release()

def start_threads():
    global camera_thread, analyze_thread, camera_running, analyze_running
    camera_running = True
    analyze_running = True

    if not camera_thread or not camera_thread.is_alive():
        camera_thread = threading.Thread(target=capture_frames, daemon=True)
        camera_thread.start()

    if not analyze_thread or not analyze_thread.is_alive():
        analyze_thread = threading.Thread(target=analyze_image, daemon=True)
        analyze_thread.start()

def stop_threads():
    global camera_thread, analyze_thread, camera_running, analyze_running
    camera_running = False
    analyze_running = False

    # If the threads are not daemonic, you would join them here
    # However, if they are daemonic, they will be stopped when the main thread stops

@app.route('/start_camera', methods=['POST'])
def start_camera():
    start_threads()
    return jsonify({"status": "Camera started"})

@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    stop_threads()
    return jsonify({"status": "Camera stopped"})

@app.route('/response_stream')
def response_stream():
    def generate_latest_response():
        global latest_ai_response
        previous_response = None
        while True:
            if latest_ai_response != previous_response:
                yield f"data: {latest_ai_response}\n\n"
                previous_response = latest_ai_response
            time.sleep(1)
    return Response(generate_latest_response(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, threaded=True)


