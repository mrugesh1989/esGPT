from unittest.mock import patch, MagicMock
from src.gcp_services import upload_file_to_gcs, store_entity_text_in_bucket, store_data_in_bigtable

def test_upload_file_to_gcs():
    with patch('google.cloud.storage.Client') as mock_client:
        mock_file = MagicMock()
        mock_file.filename = 'test_file.pdf'
        mock_file.stream = 'fake_stream'
        mock_blob = MagicMock()
        mock_client.return_value.get_bucket.return_value.blob.return_value = mock_blob
        upload_file_to_gcs(mock_file, 'entity_name', 'bucket_name')
        assert mock_blob.upload_from_file.called

def test_store_entity_text_in_bucket():
    with patch('google.cloud.storage.Client') as mock_client:
        mock_blob = MagicMock()
        mock_client.return_value.get_bucket.return_value.blob.return_value = mock_blob
        store_entity_text_in_bucket('entity_text', 'entityName', 'bucket_name', 'filename')
        assert mock_blob.upload_from_string.called

def test_store_data_in_bigtable():
    with patch('google.cloud.bigtable.Client') as mock_client:
        data = [{'entity': {'metric': 'value'}}]
        mock_table = MagicMock()
        mock_client.return_value.instance.return_value.table.return_value = mock_table
        result, message = store_data_in_bigtable('instance_id', 'table_id', data, 'entityName')
        assert mock_table.direct_row.called
        assert result

def test_store_data_in_bigtable_table_does_not_exist():
    with patch('google.cloud.bigtable.Client') as mock_client:
        data = [{'entity': {'metric': 'value'}}]
        mock_instance = MagicMock()
        mock_instance.list_tables.return_value = []
        mock_client.return_value.instance.return_value = mock_instance
        result, message = store_data_in_bigtable('instance_id', 'table_id', data, 'entityName')
        assert mock_instance.table.called
        assert result