import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image
import time  # Import the time module

PROJECT_ID = "ck-vertex"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)

IMAGE_FILE = "Gemini.png"
image = Image.load_from_file(IMAGE_FILE)

generative_multimodal_model = GenerativeModel("gemini-pro-vision")

# Start the timer
start_time = time.time()

# Execute the code block
response = generative_multimodal_model.generate_content(["What is shown in this image?", image])

# End the timer
end_time = time.time()

# Calculate the duration
duration = end_time - start_time

print(response)
print(f"Time taken: {duration} seconds")
