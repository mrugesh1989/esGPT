# AI Companion for Creating ESG Indexes and Predictions

This project is a web application that allows users to upload PDF files, extract ESG (Environmental, Social, and Governance) metrics from the content, store the extracted data in a Bigtable database, and provide a user interface for searching and displaying the stored ESG metrics.

# Demo videoes are uploaded in 3 parts due to size limitations in github
-videodemo_concept_design_part1.mp4: Explains the conceptual design and motviation for the ESGGpt app
-videodemo_application_demo_part2.mp4: Actual UI application demo showing GPT chat, Compare indicators, Find indicators etc,
-videodemo_api_demo_part3.mp4: Show API powering the app built on API first design implemented in flask using Postman


## Features

- Upload PDF files containing ESG-related information
- Extract key ESG metrics from the PDF content using OpenAI's GPT-4 language model
- Store the extracted ESG metrics in a Google Cloud Bigtable database
- Search for entities and display their associated ESG metrics
- Interactive chat with the PDF content using OpenAI's GPT-4 language model

## Technologies Used

- Python
- Flask
- Streamlit
- OpenAI API
- Google Cloud Bigtable
- Google Cloud Storage
- PyPDF2

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Hackathon2024-March/aimlexplorers.git

2.Install the required dependencies:
pip install -r requirements.txt



3.Set up the required environment variables:
export OPENAI_API_KEY="your-openai-api-key"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/gcp/credentials.json"

4.Run the Flask application:
python main.py


5.Run the Streamlit application:
Copy code
streamlit run webpage.py

Usage
Open the web application in your browser (e.g., http://localhost:8501 for Streamlit).
Choose the desired option from the sidebar (Upload File, Search Entity Indicators, or Chat with PDF).
Follow the on-screen instructions to upload a PDF file, search for entities and their ESG metrics, or chat with the PDF content.
Contributing
Contributions are welcome! Please follow the standard GitHub workflow:
Fork the repository
Create a new branch (git checkout -b feature/your-feature)
Commit your changes (git commit -am 'Add some feature')
Push to the branch (git push origin feature/your-feature)
Create a new Pull Request

License
TBD


Acknowledgments
OpenAI for their powerful language models
Google Cloud Bigtable for the NoSQL database
Google Cloud Storage for file storage
PyPDF2 for PDF parsing
