import os
import requests
from docx import Document

# Configuration variables
GENERATE_URL = "http://localhost:11434/api/generate"  # URL for the Ollama API
MODEL_NAME = "llama3"  # Model name to be used for generating summaries
RESUME_FOLDER = "/home/mdelgert/DocReader/docs"  # Path to the folder containing the resumes

def read_docx(file_path):
    """
    Reads the content of a Word document (.docx) and returns it as a string.
    
    Args:
        file_path (str): Path to the .docx file.

    Returns:
        str: Text content of the document.
    """
    doc = Document(file_path)  # Load the document
    full_text = []
    for para in doc.paragraphs:  # Loop through each paragraph in the document
        full_text.append(para.text)  # Append the text of the paragraph to the list
    return '\n'.join(full_text)  # Join all paragraphs with newline characters

def summarize_text_ollama(text):
    """
    Sends the text to the Ollama API to generate a summary.

    Args:
        text (str): Text to be summarized.

    Returns:
        str: Summary of the text.
    """
    data = {
        "model": MODEL_NAME,  # Model name
        "prompt": f"Please summarize this doc:\n\n{text}",  # Prompt for the API
        "stream": False
    }
    response = requests.post(GENERATE_URL, json=data)  # Send a POST request to the API
    if response.status_code == 200:  # Check if the request was successful
        response_json = response.json()
        if "response" in response_json:  # Check if the response contains the summary
            return response_json["response"].strip()  # Return the summary
        else:
            raise Exception("No summary found in the API response.")
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

def evaluate_summaries(summaries):
    """
    Sends a list of summaries to the Ollama API to evaluate and determine the best one.

    Args:
        summaries (list of str): List of summaries to be evaluated.

    Returns:
        str: The best summary according to the API.
    """
    data = {
        "model": MODEL_NAME,  # Model name
        "prompt": "please summarize in one paragraph the best document:\n\n" + "\n\n".join(summaries),  # Prompt for evaluation
        "stream": False
    }
    response = requests.post(GENERATE_URL, json=data)  # Send a POST request to the API
    if response.status_code == 200:  # Check if the request was successful
        response_json = response.json()
        if "response" in response_json:  # Check if the response contains the evaluation result
            return response_json["response"].strip()  # Return the best summary
        else:
            raise Exception("No evaluation result found in the API response.")
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# Collect summaries
summaries = []

# Loop through each file in the folder
for filename in os.listdir(RESUME_FOLDER):
    if filename.endswith(".docx"):  # Process only .docx files
        # Read the content of the Word document
        file_path = os.path.join(RESUME_FOLDER, filename)  # Get the full path to the file
        document_text = read_docx(file_path)  # Read the document content
        
        # Summarize the content using Ollama's API
        try:
            summary = summarize_text_ollama(document_text)  # Generate the summary
            #summaries.append(summary)  # Add the summary to the list
            # Print the filename and summary
            print(f"Summary of {filename}:")
            print(summary)
            print("-" * 50)  # Separator for better readability
        except Exception as e:
            print(f"Failed to summarize {filename}: {e}")  # Print an error message if summarization fails

# After collecting all summaries, send them for evaluation
# try:
#     best_summary = evaluate_summaries(summaries)  # Evaluate the summaries and get the best one
#     print("Best Summary:")
#     print(best_summary)
# except Exception as e:
#     print(f"Failed to evaluate summaries: {e}")  # Print an error message if evaluation fails
