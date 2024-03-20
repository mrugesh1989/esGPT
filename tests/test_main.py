# test_main.py
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from src.main import app, upload, find_indicators, ping, is_literal
from io import BytesIO

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload(client):
    with patch('src.main.upload_file_to_gcs') as mock_upload, \
         patch('src.main.read_pdfs_in_bucket') as mock_read, \
         patch('src.main.store_entity_text_in_bucket') as mock_store_text, \
         patch('src.main.extract_and_save_metrics') as mock_extract, \
         patch('src.main.store_data_in_bigtable') as mock_store_data:
        mock_upload.return_value = 'file_url'
        mock_read.return_value = 'entity_text'
        mock_store_text.return_value = 'entity_text_file_url'
        mock_extract.return_value = ('success_metrics_data', None)
        mock_store_data.return_value = (True, None)
        response = client.post('/esg/benchmark/upload/testEntity', data={'documentUpload': (BytesIO(b'my file contents'), 'test.pdf')})
        assert response.status_code == 200

def test_find_indicators(client):
    with patch('google.cloud.bigtable.Client') as mock_client:
        mock_instance = MagicMock()
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_client.return_value.instance.return_value = mock_instance
        mock_instance.table.return_value = mock_table
        mock_table.read_row.return_value = mock_row
        mock_row.cells = {'cf1': {b'esgType': [MagicMock(value=b'{"esgIndicator": "value"}')]}}
        response = client.get('/esg/benchmark/find_indicators/testEntity')
        assert response.status_code == 200
        
def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.get_json() == {"status": "alive"}

def test_is_literal():
    assert is_literal('{"key": "value"}') == True
    assert is_literal('not a literal') == False