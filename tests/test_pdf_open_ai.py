from unittest.mock import patch, MagicMock
from src.pdf_open_ai import flatten_data, extract_and_save_metrics, query_llm_for_metrics

def test_flatten_data():
    success_metrics_data = [{'Company1': {'Metric1': 'Value1', 'Metric2': 'Value2'}}]
    df = flatten_data(success_metrics_data)
    assert df.shape == (1, 3)
    assert df['Company'].values[0] == 'Company1'
    assert df['Metric1'].values[0] == 'Value1'
    assert df['Metric2'].values[0] == 'Value2'

def test_extract_and_save_metrics():
    companies_text = {'Company1': 'Text1', 'Company2': 'Text2'}
    with patch('pdf_open_ai.query_llm_for_metrics', return_value='{"Metric1": "Value1"}'):
        success_metrics_data, failed_metrics_data = extract_and_save_metrics(companies_text)
    assert len(success_metrics_data) == 0
    assert len(failed_metrics_data) == 2

def test_extract_and_save_metrics_malformed():
    companies_text = {'Company1': 'Text1', 'Company2': 'Text2'}
    with patch('pdf_open_ai.query_llm_for_metrics', return_value='Not a JSON string'):
        success_metrics_data, failed_metrics_data = extract_and_save_metrics(companies_text)
    assert len(success_metrics_data) == 0
    assert len(failed_metrics_data) == 2