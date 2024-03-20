import spacy
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler
from collections import defaultdict
import PyPDF2

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Read PDF file
def read_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Process text with spaCy
def process_text(text):
    doc = nlp(text)
    return doc

# Extract entities using spaCy's named entity recognition (NER)
def extract_entities(doc):
    entities = defaultdict(list)
    for ent in doc.ents:
        entities[ent.label_].append(ent.text)
        print(ent.text, " | ", ent.label_, " | ", spacy.explain(ent.label_))
    return entities

# Extract relationships between entities using spaCy's dependency parsing
def extract_relationships(doc):
    relationships = defaultdict(list)
    for token in doc:
        if token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            relationships[token.head.lemma_].append(token.text)
    return relationships

# Extract insights based on extracted entities and relationships
def extract_insights(entities, relationships):
    insights = []
    for entity_type, entity_list in entities.items():
        for relationship, related_entities in relationships.items():
            insight = f"{entity_type.capitalize()}s involved in {relationship}: {', '.join(entity_list)} - {', '.join(related_entities)}"
            insights.append(insight)
    return insights

# Main function to process PDF and extract insights
def process_pdf(pdf_path):
    text = read_pdf(pdf_path)
    doc = process_text(text)
    entities = extract_entities(doc)
    relationships = extract_relationships(doc)
    insights = extract_insights(entities, relationships)
    return insights

# Example usage
pdf_path = "./data/esap-br032_-en-p.pdf"
insights = process_pdf(pdf_path)
# for insight in insights:
#     print(insight)
