import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from google.cloud import storage
from werkzeug.utils import secure_filename
from google.cloud import bigtable
from google.cloud.bigtable import column_family, row_filters


def upload_file_to_gcs(file, entity_name, bucket_name):
    storage_client = storage.Client(project='wellsfargo-genai24-8021')
    bucket = storage_client.get_bucket(bucket_name)
    filename = secure_filename(file.filename)
    # Include the entity name as a prefix in the blob name
    blob = bucket.blob(f'{entity_name}/{filename}')
    file.seek(0)  # Ensure you're at the start of the file
    blob.upload_from_file(file.stream)
    logger.info(f'File {filename} uploaded to {blob.public_url}')
    return blob.public_url

def store_entity_text_in_bucket(entity_text, entityName, bucket_name, filename):
    storage_client = storage.Client(project='wellsfargo-genai24-8021')
    bucket = storage_client.get_bucket(bucket_name)
    
    # Include the entity name as a prefix in the blob name
    blob = bucket.blob(f'{entityName}/{filename}')
    
    # Convert entity_text to a string if it's not already a string
    if not isinstance(entity_text, str):
        entity_text = str(entity_text)
        
    blob.upload_from_string(entity_text)
    logger.info(f'Entity text for {entityName} uploaded to {blob.public_url}')
    return blob.public_url
    
def store_data_in_bigtable(instance_id, table_id, data, entityName):
    try:
        # Create a Bigtable client
        client = bigtable.Client(project='wellsfargo-genai24-8021', admin=True)

        # Get a reference to a Bigtable instance
        instance = client.instance(instance_id)

        # Check if the table exists
        tables = [table.table_id for table in instance.list_tables()]
        if table_id not in tables:
            # If the table does not exist, create it
            print(f'Table {table_id} does not exist. Creating...')
            table = instance.table(table_id)
            cf1 = table.column_family('cf1')
            cf1.create()
            print(f'Table {table_id} created successfully.')
        else:
            # If the table exists, get a reference to it
            print(f'Table {table_id} exists.')
            table = instance.table(table_id)

        # Iterate over the data
        for entity, metrics in data[0].items():
            # Create a row key
            row_key = entityName

            # Create a new row in the table
            row = table.direct_row(row_key)

            # Iterate over the metrics
            for metric, value in metrics.items():
                 # Convert the value to a string and encode it as UTF-8
                value_str = str(value).encode('utf-8')

                # Set the cell in the row
                row.set_cell('cf1', metric, value_str)

            # Insert the row into the table
            row.commit()

        return True, 'Successfully inserted data into Bigtable.'
    except Exception as e:
        print(f'An error occurred: {e}')
        return False, str(e)