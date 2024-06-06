import requests
from docx import Document
from docx.shared import Inches

# Function to convert Word document to text
def convert_docx_to_text(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to prompt user for a question
def ask_question():
    question = input("Please ask a question: ")
    return question

# Function to send POST request to API and get answer
def get_answer(question, text):
    url = "http://localhost:11434/api/generate"
    prompt = {
        "model": "llama3",
        "prompt": text,
        "stream": False
    }
    response = requests.post(url, json=prompt)
    answer = response.json()
    return answer

# Main function
def main():
    # Prompt user for a question
    user_question = ask_question()

    # Path to Word document
    docx_path = "/home/mdelgert/DocAI/docs/test.docx"

    # Convert Word document to text
    document_text = convert_docx_to_text(docx_path)

    # Get answer from LLM
    answer = get_answer(user_question, document_text)

    print("Answer:", answer)

if __name__ == "__main__":
    main()
