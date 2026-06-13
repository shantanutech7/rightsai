import spacy
import re

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    """
    Extract key entities from legal document using SpaCy NLP.
    Returns salary, notice period, company name, dates, locations.
    """
    doc = nlp(text[:5000])  # Process first 5000 chars

    entities = {
        "company_name": None,
        "salary": None,
        "notice_period": None,
        "joining_date": None,
        "probation_period": None,
        "locations": [],
        "dates": [],
    }

    # Extract ORG and GPE entities from SpaCy
    orgs = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    locations = list(set([ent.text for ent in doc.ents if ent.label_ == "GPE"]))
    dates = list(set([ent.text for ent in doc.ents if ent.label_ == "DATE"]))

    if orgs:
        entities["company_name"] = orgs[0]
    if locations:
        entities["locations"] = locations[:3]
    if dates:
        entities["dates"] = dates[:3]

    # Extract salary using regex
    salary_patterns = [
        r'(?:INR|Rs\.?|₹)\s*[\d,]+(?:\s*(?:per annum|p\.a\.|per year|monthly|lakh|lakhs))?',
        r'[\d,]+\s*(?:per annum|p\.a\.|CTC|LPA|lakh)',
        r'salary.*?(?:INR|Rs\.?|₹)\s*[\d,]+',
    ]
    for pattern in salary_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entities["salary"] = match.group(0).strip()
            break

    # Extract notice period using regex
    notice_patterns = [
        r'notice period.*?(\d+)\s*(days?|months?|weeks?)',
        r'(\d+)\s*(days?|months?|weeks?)\s*notice',
        r'serve.*?(\d+)\s*(days?|months?)',
    ]
    for pattern in notice_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entities["notice_period"] = match.group(0).strip()
            break

    # Extract probation period
    probation_patterns = [
        r'probation.*?(\d+)\s*(months?|days?|weeks?)',
        r'(\d+)\s*(months?|days?)\s*probation',
    ]
    for pattern in probation_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entities["probation_period"] = match.group(0).strip()
            break

    return entities
