import flask
from flask import app, Flask
import streamlit as st
import ast
from openai import OpenAI
from parse_pdf import read_bytes_pdf
from main import upload
from google.cloud import bigtable
import io
from werkzeug.datastructures import FileStorage, FileMultiDict
from werkzeug.datastructures import CombinedMultiDict
from pprint import pformat

app = Flask(__name__)

# Set the OpenAI API key
client = OpenAI(api_key='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')

# Add a header
st.markdown("""
    <style>
    .header {
        font-size:20px !important;
        color: #FFA500;  # Light orange
    }
    .team {
        font-size:20px !important;
        color: #FFA500;  # Light orange
    }
    .title {
        font-size: 40px !important;
        color: #0099ff;  # Light orange
    }
    </style>
    """, unsafe_allow_html=True)

# Add the title
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <p class="title" style="margin-left: 175px;">Hackathon - 2024</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add project name
st.markdown(
    """
    <div style="display: flex; align-items: left; justify-content: left;">
        <p class="header" style="margin-left: 10px;">AI companion for creating ESG indexes and predictions with an eco friendly touch</p>
    </div>
    """,
    unsafe_allow_html=True,
)
class PDFFile:
    def __init__(self, file_bytes):
        self.file = io.BytesIO(file_bytes)
        self.content_type = 'application/pdf'

    def read(self):
        return self.file.read()
    
# Options
options = ["", "Upload File", "Search Entity Indicators", "Indicator Comparison Report", "Chat with PDF"]

#Save the resized image if needed
st.sidebar.image('esg.jpg')
option = st.sidebar.selectbox("Choose an option", options)

# Add team name and members
st.sidebar.markdown(
    """
    <div style="text-align: left;">
        <p class="team">Team: AIML-Explorers</p>
        <ul class="team" style="list-style-type: none; padding: 0;">
            <li>* Rohit Chandramohan</li>
            <li>* Brahmananda Bandela</li>
            <li>* Mrugesh Patel</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

if option == "Upload File":
    # Create text input field for the entity name
    entity_name = st.text_input('Entity Name')

    if entity_name:
        # Create a file uploader
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

        if uploaded_file is not None:
                 
            # Convert the uploaded file to a file-like object
            file_bytes = uploaded_file.read()
            file_object = io.BytesIO(file_bytes)

            # Create a PDFFile object from the bytes
            # file_object = PDFFile(file_bytes)

            # Get the filename of the uploaded file
            filename = uploaded_file.name
            
            # Create a FileStorage object
            file_storage = FileStorage(stream=file_object, filename=filename, content_type='application/pdf')

            # Create a new FileMultiDict object with the file
            file_dict = FileMultiDict([('documentUpload', file_storage)])

            # Mimic an HTTP request
            with app.test_request_context():
                app.preprocess_request()

                # Combine the original request.files with the new file_dict
                flask.request.files = CombinedMultiDict([flask.request.files, file_dict])

                # Call the upload function directly
                response, status_code = upload(entity_name)

            pretty_data = pformat(response, indent=4)
            st.text_area("Response :", pretty_data, height=600)   

elif option == "Search Entity Indicators":
    # Create a Bigtable client
    client = bigtable.Client(project='wellsfargo-genai24-8021', admin=True)

    # Get a reference to a Bigtable instance and table
    instance = client.instance('hackathon2024')
    table = instance.table('entity_metrics')

    # Read all rows from the table
    rows = table.read_rows()

    # Get the row keys (entity names)
    entity_names = [row.row_key.decode('utf-8') for row in rows]
    
    # Create a placeholder for the entity name dropdown menu
    entity_name_placeholder = st.empty()

    # Create a placeholder for the ESG type dropdown menu
    esg_type_placeholder = st.empty()

    # Create a dropdown menu for the entity names
    entity_name = entity_name_placeholder.selectbox('Entity Name', [''] + entity_names)

    if entity_name:
        # Read the row from the table
        row = table.read_row(entity_name)
        if row is not None:
            # Get the column names (ESG types)
            esg_types = [esgType.decode('utf-8') for esgType in row.cells['cf1'].keys()]
                
            # Create a dropdown menu for the ESG types
            esg_type = esg_type_placeholder.selectbox('ESG Type', [''] + esg_types)


            if esg_type:
                # Get the esgIndicator for the selected esgType
                cell = row.cells['cf1'].get(esg_type.encode('utf-8'), [None])[0]
                if cell is not None:
                    esg_type_value = cell.value.decode('utf-8')
                    if esg_type_value.startswith('{') and esg_type_value.endswith('}'):
                        esg_indicator = ast.literal_eval(esg_type_value)
                        # Create a dropdown menu for the ESG indicators
                        esg_indicator_key = st.selectbox('ESG Indicator', list(esg_indicator.keys()))
                        # Display the value of the selected ESG indicator
                        st.write(esg_indicator[esg_indicator_key])
                    else:
                        esg_indicator = str(esg_type_value)
                        # Display the value of the ESG type
                        ignored_values = ['Not Provided', 'Not provided', 'Not specified', 'Not Specified', 'null', 'None']
                        if esg_indicator in ignored_values:
                            st.write("ESG Type value is not Provided")
                        else:
                            st.write(esg_indicator)
                    
        else:
            st.error(f'Entity {entity_name} not found')
            
elif option == "Indicator Comparison Report":
    # Create a Bigtable client
    client = bigtable.Client(project='wellsfargo-genai24-8021', admin=True)

    # Get a reference to a Bigtable instance and table
    instance = client.instance('hackathon2024')
    table = instance.table('entity_metrics')

    # Read all rows from the table
    rows = table.read_rows()

    # Get the row keys (entity names)
    entity_names = [row.row_key.decode('utf-8') for row in rows]

    # Create a multiselect menu for the entity names
    selected_entities = st.multiselect('Select at least two entities for the report', entity_names)

    if len(selected_entities) < 2:
        st.error('Please select at least two entities.')
    else:
        # Create a placeholder for the report
        report_placeholder = st.empty()

        # Create a button for generating the report
        if st.button('Generate Report'):
            # Create a dictionary to store the report data
            report_data = {}

            # For each selected entity, read the row from the table and add it to the report data
            for entity_name in selected_entities:
                row = table.read_row(entity_name)
                if row is not None:
                    # Get the column names (ESG types) and values
                    esg_types = {esgType.decode('utf-8'): cell[0].value.decode('utf-8') for esgType, cell in row.cells['cf1'].items()}
                    report_data[entity_name] = esg_types

            # Display the report data
            report_placeholder.table(report_data)
    
elif option == "Chat with PDF":
    # Create a file uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Convert the uploaded file to bytes
        file_bytes = uploaded_file.read()

        # TODO: Extract text from the PDF file
        file_text = read_bytes_pdf(file_bytes)

        # Create a text input field for the user's question
        question = st.text_input('Ask a question about the PDF file')

        if st.button('Ask'):
            # Call the OpenAI API to chat with the PDF
            response = client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': f"This is a helpful assistant. The content of the PDF is: {file_text}"},
                {'role': 'user', 'content': question},
            ],
            model="gpt-4-1106-preview",
            temperature=0,
            )
            # Get the first choice from the response
            choice = response.choices[0]

            # Get the message from the choice
            message = choice.message
            
             # Get the content of the message
            content = message.content

            # Display the message
            st.markdown(f'**Response:**\n{content}')