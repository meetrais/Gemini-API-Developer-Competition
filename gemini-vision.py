import os
import PIL
from dotenv import load_dotenv
import google.generativeai as genai
import cv2
import time

#Load variables from .env file
load_dotenv()

def identify_animal_in_image(imagename):
    GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    # Initialize Gemini model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    imagepath = 'videos/frames/' + imagename
    img = PIL.Image.open(imagepath)
    prompt="Identify animal in the image and output only animal type not breed without . or EOF."
    response = model.generate_content(contents=[prompt,img])

    return response.text

def find_animal(videoname):
    videopath = "videos/" + videoname
    vidcap = cv2.VideoCapture(videopath)
    success,image = vidcap.read()
    count = 0
    while success:
        imagename = "frame%d.jpg" % count
        imagepath = 'videos/frames/'+imagename  
        cv2.imwrite(imagepath, image)     # save frame as JPEG file    
        time.sleep(2)
        animal = identify_animal_in_image(imagename)
        print(animal)
        time.sleep(2)
        success,image = vidcap.read()
        count += 1
        if(count>9):
            success=False

if __name__ == "__main__":
    find_animal('video4.mp4')