from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import uvicorn
import requests
from io import BytesIO

app = FastAPI()

# CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/sketch-to-image")
async def sketch_to_image(prompt: str = Form(...)):
    # Open the local sketch file
    sketch_file_object = open("sketch.jpg", "rb")

    # API endpoint for the sketch-to-image service
    api_endpoint = "https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image"

    # Prepare data for API call
    data = {'prompt': prompt + ", pixel art"}
    headers = {'x-api-key': '4084125c2e3a566a90feb8a713c8444135a8d8704fa96abf5f80f5920c71b02c0bf337ee5d454d6618116eafe33d75be'}

    # Send POST request to the sketch-to-image API
    response = requests.post(api_endpoint, files={
        "sketch_file": ('sketch.jpg', sketch_file_object, 'image/jpeg'),
    }, data=data, headers=headers)

    # Save response image locally
    with open("result.jpg", "wb") as result_file:
        result_file.write(response.content)

    # Get the content of the response
    result_content = BytesIO(response.content)

    # Return the result as a StreamingResponse
    return StreamingResponse(result_content, media_type="image/jpeg")

if __name__ == "__main__":

    # Run the FastAPI app using UVicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
