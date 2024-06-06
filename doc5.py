import requests
from docx import Document

# Function to convert Word document to text
def convert_docx_to_text(docx_path):
    doc = Document(docx_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to send POST request to API and get answer
def get_answer(question, text):
    url = "http://localhost:11434/api/generate"
    prompt = {
        "model": "llama3",
        "prompt": text,
        "stream": False
    }
    response = requests.post(url, json=prompt)  # Send a POST request to the API
    if response.status_code == 200:  # Check if the request was successful
        response_json = response.json()
        if "response" in response_json:  # Check if the response contains the summary
            return response_json["response"].strip()  # Return the summary
        else:
            raise Exception("No summary found in the API response.")
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# Main function
def main():
    # Path to Word document
    docx_path = "/home/mdelgert/DocAI/docs/test.docx"

    # Convert Word document to text
    document_text = convert_docx_to_text(docx_path)
    
    while True:
        # Prompt user for a question
        user_question = input("Please ask a question (or enter 'q' to quit): ")
        if user_question.lower() == 'q':
            print("Exiting the program...")
            break

        # Get answer from LLM
        try:
            answer = get_answer(user_question, document_text)
            print("Answer:", answer)
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    main()
