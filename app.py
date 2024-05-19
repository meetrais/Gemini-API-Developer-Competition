import os
from dotenv import load_dotenv
import google.generativeai as genai

#Load variables from .env file
load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
    
model = genai.GenerativeModel('gemini-1.5-flash-latest')
#response = model.generate_content("What is the meaning of life?")

#print(response.candidates[0].content.parts[0].text)

response = model.generate_content("What is the meaning of life?", stream=True)
for chunk in response:
  print(chunk.text)
  print("_"*80)