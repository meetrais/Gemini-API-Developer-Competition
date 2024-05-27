import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
import gradio as gr

#Load variables from .env file
load_dotenv()

def run_generation(user_text, top_p, temperature, top_k, max_new_tokens):
  GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
  genai.configure(api_key=GOOGLE_API_KEY)
  DATA_PATH = 'data/Profile.pdf'
  loader = PyPDFLoader(file_path=DATA_PATH)
  pages = loader.load_and_split()
  pdf_content=''
  for page in pages:
    pdf_content += page.page_content
    
  model = genai.GenerativeModel('gemini-1.5-flash-latest')
  
  prompt = "You are a helpful digital assistant and exper Career Coach. Please provide safe, ethical and accurate career guidance to user based on profile."
  prompt+= "Usre Question: "
  prompt+= user_text
  
  response = model.generate_content(contents=[prompt,pdf_content])

  return response.text

# Gradio UI setup
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=4):
            user_text = gr.Textbox(placeholder="Write your question here", label="User input")
            model_output = gr.Textbox(label="Model output", lines=10, interactive=False)
            button_submit = gr.Button(value="Submit")

        with gr.Column(scale=1):
            max_new_tokens = gr.Slider(minimum=1, maximum=1000, value=250, step=1, label="Max New Tokens")
            top_p = gr.Slider(minimum=0.05, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)")
            top_k = gr.Slider(minimum=1, maximum=50, value=50, step=1, label="Top-k")
            temperature = gr.Slider(minimum=0.1, maximum=1.0, value=0.5, step=0.1, label="Temperature")

    user_text.submit(run_generation, [user_text, top_p, temperature, top_k, max_new_tokens], model_output)
    button_submit.click(run_generation, [user_text, top_p, temperature, top_k, max_new_tokens], model_output)

    demo.queue(max_size=32).launch(server_port=8082)