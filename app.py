import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader

#Load variables from .env file
load_dotenv()

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

DATA_PATH = 'data/Profile.pdf'
loader = PyPDFLoader(file_path=DATA_PATH)
pages = loader.load_and_split()
pdf_content=''
for page in pages:
  pdf_content += page.page_content
    
model = genai.GenerativeModel('gemini-1.5-flash-latest')
prompt="You are a Career Mentor. Provide your guidance based on this profile."
response = model.generate_content(contents=[prompt,pdf_content])

print(response.text)