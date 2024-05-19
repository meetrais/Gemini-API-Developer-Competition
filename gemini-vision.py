import PIL.Image
import os
import io
import cv2
from dotenv import load_dotenv
import google.generativeai as genai
from vertexai.generative_models import Part


#Load variables from .env file
load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
img = PIL.Image.open('images/image.jpg')
model = genai.GenerativeModel('gemini-1.5-flash-latest')

prompt="You are a Story Writter. Write a story based on provided video."
response = model.generate_content(contents=[prompt,img])

print(response.text)
"""print("===========================================================================================")
response = model.generate_content(["Write a short, engaging blog post based on this picture. It should include a description of the meal in the photo and talk about my journey meal prepping.", img], stream=True)
response.resolve()"""

print(response.text)

