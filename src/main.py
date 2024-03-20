from flask import Flask, request, jsonify
import os
import ast
import logging
import json
from pdf_open_ai import extract_and_save_metrics
from parse_pdf import read_pdfs_in_bucket
from google.cloud import bigtable
from gcp_services import upload_file_to_gcs, store_entity_text_in_bucket, store_data_in_bigtable
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/esg/benchmark/upload/<entityName>', methods=['POST'])
def upload(entityName):
    
    # Check if the request contains a entityName
    if entityName is None:
        return jsonify({"error": "entityName not found"}), 400
    
    # Check if the request contains a file
    if 'documentUpload' not in request.files:
        return jsonify({"error": "documentUpload file not found"}), 400
    
    file = request.files['documentUpload']
    
     # Check if the file is a PDF
    if file.content_type != 'application/pdf':
        return jsonify({"error": "Only PDF files are allowed"}), 400
    
    # Get the filename without the extension
    name, _ = os.path.splitext(file.filename)
    # Append .txt to the name
    txt_filename = f'{name}.txt'
    
    file_url = upload_file_to_gcs(file, entityName, 'ingest-pdf-files')
    
    if file_url:
        logger.info(f'File {file.filename} uploaded to {file_url}')
        #Look for the file with the Entity Name in the GCS bucket & parse it
        entity_text = read_pdfs_in_bucket('ingest-pdf-files', entityName)
        entity_text_file_url = store_entity_text_in_bucket(entity_text, entityName, 'raw-llm-response', txt_filename)
        #Create the Json outut with ESG Type & Indicator
        success_metrics_data, _ = extract_and_save_metrics(entity_text)
        success, message = store_data_in_bigtable('hackathon2024', 'entity_metrics', success_metrics_data, entityName)
        if not success:
            return jsonify({"error": message}), 500
    else:
        return jsonify({"error": "Failed to upload file"}), 500
    


    # Replace the following line with your actual processing code
    esgResponse = {
    'Uploaded File URL' : f'{file_url}',
    'Uploaded Raw Text File URL' : f'{entity_text_file_url}',
    'ESG metrics': f'{success_metrics_data}'
    }

    logger.info(f'Response generated for /esg/benchmark/upload/{entityName}')
    return esgResponse, 200

@app.route('/esg/benchmark/upload/<entityName>/<esgType>/<esgIndicator>', methods=['GET'])
def find_indicators(entityName, esgType, esgIndicator):
    
    #  Check if the request contains valid parameters
    if not entityName:
        return jsonify({"error": "entityName not found"}), 400
    if not esgType:
        return jsonify({"error": "esgType not found"}), 400
    if not esgIndicator:
        return jsonify({"error": "esgIndicator not found"}), 400
    
    # Create a Bigtable client
    client = bigtable.Client(project='wellsfargo-genai24-8021', admin=True)

    # Get a reference to a Bigtable instance and table
    instance = client.instance('hackathon2024')
    table = instance.table('entity_metrics')

    # Read the row from the table
    row = table.read_row(entityName)
    if row is None:
        return {'error': f'Entity {entityName} not found'}, 404
    
    logger.info({column: cell[0].value for column, cell in row.cells['cf1'].items()})
    # Initialize an empty dictionary to store the esgTypes and their indicators
    esg_data = {}


    # Iterate over the cells in the 'cf1' column family
    for esgType, cell in row.cells['cf1'].items():
            # Decode the esgType from bytes to a string
            esgType = esgType.decode('utf-8').lower()

            # Parse the esgIndicators string into a Python dictionary
            value = cell[0].value.decode('utf-8').lower()
            if is_literal(value):
                esgIndicator = ast.literal_eval(value)
            else:
                esgIndicator = value
            esg_data[esgType] = esgIndicator

    esg_data = json.dumps(esg_data)
    output_response = esg_data
    return output_response, 200

def is_literal(s):
    try:
        ast.literal_eval(s)
        return True
    except (ValueError, SyntaxError):
        return False

@app.route('/esg/benchmark/keepalive/ping', methods=['GET'])
def ping():
    # Respond with a simple message indicating the service is alive
    return jsonify({"status": "alive"}), 200

if __name__ == '__main__':
    logger.info('Starting Flask server')
    app.run(debug=True, port=8080)
