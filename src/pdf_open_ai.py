from openai import OpenAI
import json
import pandas as pd
from parse_pdf import read_pdfs_in_directory

#client = OpenAI(api_key='') #Commented out for security reasons. Enable this line and replace the empty string with your OpenAI API key.

def flatten_data(success_metrics_data):
    flattened_data = []
    for entry in success_metrics_data:
        for company, metrics in entry.items():
            flat_entry = {'Company': company}
            # Check if metrics is a dictionary before attempting to iterate over it
            if isinstance(metrics, dict):
                for key, value in metrics.items():
                    # Handle nested dictionaries
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            flat_entry[f"{key} - {subkey}"] = subvalue
                    else:
                        flat_entry[key] = value
            else:
                # If metrics is not a dictionary, handle accordingly (e.g., log a warning or skip)
                print(f"Expected a dictionary for metrics, but got a different type for company: {company}")
            flattened_data.append(flat_entry)

    df = pd.DataFrame(flattened_data)
    return df

def extract_and_save_metrics(companies_text):
    extracted_company_metrics = []
    extracted_company_metrics_malformed = []
    for company in companies_text.keys():
        extracted_metrics = query_llm_for_metrics(companies_text[company])

        try:
            extracted_metrics = extracted_metrics.replace("```", "")
            extracted_metrics = extracted_metrics.replace("json", "")
            extracted_metrics = json.loads(extracted_metrics)
            extracted_company_metrics.append(extracted_metrics)
        except:
            extracted_company_metrics_malformed.append(extracted_metrics)

    # Convert the lists to JSON strings
    success_metrics_json = json.dumps(extracted_company_metrics, indent=4)
    failed_metrics_json = json.dumps(extracted_company_metrics_malformed, indent=4)

    # Convert the JSON strings back to Python data structures
    success_metrics_data = json.loads(success_metrics_json)
    failed_metrics_data = json.loads(failed_metrics_json)

    return success_metrics_data, failed_metrics_data

def query_llm_for_metrics(text_chunk):
    query=f"Extract primary entity and include key ESG MSCI Sustain analytics, Net zero target, Renewable electricity target, Interim emission reduction target, Circularity strategy and target , Social - Diversity, equity and inclusion target, employee health and safety, supply chain audit metrics from this text. Use the following output format in json, Include primary entity as root key, metric:value. Do not use markdown: {text_chunk}"
    response = client.chat.completions.create(
    messages=[
        {'role': 'system', 'content': 'Can you extract key ESG metrics from the content provided'},
        {'role': 'user', 'content': query},
    ],
    model="gpt-4-1106-preview",
    temperature=0,
)
    my_openai_obj = list(response.choices)[0]
    
    return my_openai_obj.message.content
