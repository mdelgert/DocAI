from docx import Document
import requests
import os

def read_docx(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def summarize_text_ollama(text):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": f"please summarize this in one paragraph:\n\n{text}",
        "stream": False
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response_json = response.json()
        if "response" in response_json:
            return response_json["response"].strip()
        else:
            raise Exception("No summary found in the API response.")
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# Directory containing docs
resume_folder = "/home/mdelgert/DocAI/docs"

# Loop through each file in the folder
for filename in os.listdir(resume_folder):
    if filename.endswith(".docx"):
        # Read the content of the Word document
        file_path = os.path.join(resume_folder, filename)
        document_text = read_docx(file_path)
        
        # Summarize the content using Ollama's API
        try:
            summary = summarize_text_ollama(document_text)
            # Print the filename and summary
            print(f"Summary of {filename}:")
            print(summary)
            print("-" * 50)  # Separator for better readability
        except Exception as e:
            print(f"Failed to summarize {filename}: {e}")

