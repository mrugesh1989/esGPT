
# AI Companion for ESG Indexes and Predictions

Welcome to our innovative web application designed to empower users with the ability to upload PDF files, extract critical ESG (Environmental, Social, and Governance) metrics, and interact with this data in meaningful ways. Our platform is built for those who are committed to sustainable and ethical investing, providing tools to analyze and engage with ESG data efficiently.

# Streamlit URL
  - https://streamlit-hzjjublqba-ue.a.run.app/

# Flask URL(REST Endpoints)
  - https://esgbenchmark-hzjjublqba-ue.a.run.app/esg/benchmark/keepalive/ping
  - https://esgbenchmark-hzjjublqba-ue.a.run.app/esg/benchmark/upload/{entityName}
  - https://esgbenchmark-hzjjublqba-ue.a.run.app/esg/benchmark/upload/{entityName}/{entityType}/{entityIndicator}

# Demo videos are uploaded in 3 parts due to size limitations in github
- videodemo_concept_design_part1.mp4: Explains the conceptual design and motviation for the ESGGpt app 
- videodemo_application_demo_part2.mp4: Actual UI application demo showing GPT chat, Compare indicators, Find indicators etc, 
- videodemo_api_demo_part3.mp4: Show API powering the app built on API first design implemented in flask using Postman
- https://github.com/Hackathon2024-March/aimlexplorers/tree/main/artifacts/demo_presentation

  
# Design

The following diagram illustrates the conceptual overview of the ESG Survey Automation workflow:

<img width="764" alt="image" src="https://github.com/Hackathon2024-March/aimlexplorers/assets/43395721/5f10f0b5-b986-4fe9-8b0d-92df05c45b8d">


Key components of the system:

- **User Interaction**: Initiates the process by uploading PDFs and asking questions.
- **PDF Upload**: Users can upload ESG-related PDF documents.
- **ESG Survey Find Indicators**: Identifies and extracts ESG metrics from uploaded documents.
- **PDF Ask a Question**: Allows users to interact with the uploaded PDF content.
- **Indicator Comparison Report**: Allows users to compare ESG metrics with other entities.
- **Flask**: Serves as the backend framework, managing requests and interactions.
- **Streamlit**: Provides an interactive web interface for user interactions.
- **Google Cloud Platform**: Includes services like Cloud Storage for file management and Bigtable for database solutions.
- **OpenAI**: Powers the system with AI models, prompts, embeddings, and Q&A retrieval capabilities.

This design ensures a seamless, scalable, and interactive user experience, utilizing state-of-the-art technologies to provide quick and accurate ESG data analysis.

## Features

- **PDF Upload**: Securely upload PDF files containing ESG-related information.
- **ESG Metrics Extraction**: Utilize the power of OpenAI's GPT-4 to intelligently extract key ESG metrics from your documents.
- **Data Storage**: Safely store your extracted ESG metrics in Google Cloud Bigtable, ensuring scalability and reliability.
- **Interactive Search**: Easily search for entities and view their associated ESG metrics in a user-friendly interface.
- **Indicator Comparison Report**: Allows users to compare ESG metrics with other entities.
- **PDF Content Chat**: Engage in interactive chat sessions with your PDF content, powered by GPT-4, to explore your data further.

## Technologies Used

- Python
- Flask
- Streamlit
- OpenAI API (GPT-4)
- Google Cloud Bigtable
- Google Cloud Storage
- Google Cloud Run
- PyPDF2

## Getting Started

Follow these simple steps to get your AI Companion up and running:

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Hackathon2024-March/aimlexplorers.git
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### Configuration

Set up the required environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/gcp/credentials.json"
```

### Running the Application

1. **Start the Flask application:**

```bash
python main.py
```

2. **Launch the Streamlit UI:**

```bash
streamlit run webpage.py
```

## How to Use

Visit the web application in your browser (typically `http://localhost:8501` for Streamlit). Choose an option from the sidebar: Upload File, Search Entity Indicators, or Chat with PDF, and follow the prompts to interact with your ESG data.

## Contributing

We welcome contributions from the community! Please follow our contribution guidelines:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Submit a Pull Request.

## Acknowledgments

- OpenAI, for their groundbreaking language models.
- Google Cloud Services, for providing robust cloud storage and database solutions.
- The Python community, for the versatile PyPDF2 library.

## License

TBD - Your project's license will be determined and added here.
