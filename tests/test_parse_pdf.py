import pytest
import io, os
from unittest.mock import patch, MagicMock
from src.parse_pdf import read_bytes_pdf, read_pdf, read_pdfs_in_bucket, read_pdfs_in_directory

    
def test_read_pdf():
    # Mock a PDF file with one page containing the text "Hello, world!"
    mock_pdf_file = MagicMock()
    mock_pdf_file.pages = [MagicMock(extract_text=MagicMock(return_value="Hello, world!"))]

    # Mock the PdfReader to return the mock PDF file
    with patch('PyPDF2.PdfReader', return_value=mock_pdf_file) as mock_PdfReader:
        text = read_pdf('fake file path')

    # Check that the PdfReader was called with the correct file path
    assert mock_PdfReader.call_args[0][0] == 'fake file path'

    # Check that the text was extracted correctly
    assert text == "Hello, world!"

def test_read_pdfs_in_bucket():
    # Mock a blob with a name ending in ".pdf"
    mock_blob = MagicMock()
    mock_blob.name = 'fake_blob.pdf'
    mock_blob.download_as_bytes.return_value = b'fake file bytes'

    # Mock a bucket to return the mock blob
    mock_bucket = MagicMock()
    mock_bucket.list_blobs.return_value = [mock_blob]

    # Mock the storage.Client to return the mock bucket
    with patch('google.cloud.storage.Client', return_value=MagicMock(get_bucket=MagicMock(return_value=mock_bucket))) as mock_client:
        # Mock the read_pdf function to return "Hello, world!"
        with patch('src.parse_pdf.read_pdf', return_value="Hello, world!") as mock_read_pdf:
            texts = read_pdfs_in_bucket('fake bucket name', 'fake entity name')

    # Check that get_bucket was called with the correct bucket name
    assert mock_client.return_value.get_bucket.call_args[0][0] == 'fake bucket name'

    # Check that the read_pdf function was called with a BytesIO object
    assert isinstance(mock_read_pdf.call_args[0][0], io.BytesIO)

    # Check that the texts were extracted correctly
    assert texts == {'fake_blob.pdf': "Hello, world!"}

def test_read_pdfs_in_bucket_no_pdf():
    # Mock a bucket to return no blobs
    mock_bucket = MagicMock()
    mock_bucket.list_blobs.return_value = []

    # Mock the storage.Client to return the mock bucket
    with patch('google.cloud.storage.Client', return_value=MagicMock(get_bucket=MagicMock(return_value=mock_bucket))) as mock_client:
        with pytest.raises(ValueError):
            read_pdfs_in_bucket('fake bucket name', 'fake entity name')

def test_read_pdfs_in_directory():
    # Mock os.listdir to return a list containing one filename ending in ".pdf"
    with patch('os.listdir', return_value=['fake_file.pdf']) as mock_listdir:
        # Mock read_pdf to return the text "Hello, world!"
        with patch('src.parse_pdf.read_pdf', return_value="Hello, world!") as mock_read_pdf:
            texts = read_pdfs_in_directory('fake directory path')

    # Check that os.listdir was called with the correct directory path
    assert mock_listdir.call_args[0][0] == 'fake directory path'

    # Check that read_pdf was called with the correct file path
    expected_file_path = os.path.join('fake directory path', 'fake_file.pdf')
    assert mock_read_pdf.call_args[0][0] == expected_file_path

    # Check that the texts were extracted correctly
    assert texts == {'fake_file.pdf': "Hello, world!"}