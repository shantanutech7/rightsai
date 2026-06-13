import re

# Red flag clauses - dangerous
RED_FLAGS = {
    "Non-Compete Clause": [
        "non-compete", "non compete", "not compete", "shall not work",
        "cannot join", "competitor", "competing business", "restraint of trade"
    ],
    "IP Ownership of Side Projects": [
        "all inventions", "all work product", "side project", "personal project",
        "any work created", "intellectual property shall vest", "assigns all rights"
    ],
    "Forced Arbitration": [
        "binding arbitration", "waive right to court", "arbitration only",
        "shall be resolved by arbitration", "no right to jury", "class action waiver"
    ],
    "Immediate Termination Without Notice": [
        "terminate immediately", "termination without notice", "at will termination",
        "terminate at any time without", "no notice required"
    ],
    "Unlimited Liability": [
        "unlimited liability", "personally liable", "indemnify fully",
        "bear all costs", "sole responsibility for all damages"
    ],
    "Auto-Renewal Trap": [
        "auto-renew", "automatically renew", "automatic renewal",
        "unless cancelled", "unless terminated 30 days prior"
    ],
}

# Yellow flag clauses - needs review
YELLOW_FLAGS = {
    "Notice Period Imbalance": [
        "notice period", "30 days notice", "60 days notice", "90 days notice",
        "serving notice", "notice of resignation"
    ],
    "Confidentiality Clause": [
        "confidential", "non-disclosure", "nda", "trade secret",
        "proprietary information", "shall not disclose"
    ],
    "Unilateral Changes": [
        "may amend", "may change", "reserves the right to modify",
        "at our discretion", "without prior notice may update"
    ],
    "Data Sharing": [
        "share your data", "third party", "data may be shared",
        "partners may access", "transferred to affiliates"
    ],
    "Variable Compensation": [
        "at the discretion of", "may be revised", "subject to change",
        "performance-based", "bonus not guaranteed"
    ],
}

# Green / safe clauses
GREEN_FLAGS = {
    "Clear Salary Mentioned": [
        "gross salary", "ctc", "cost to company", "per annum", "monthly salary",
        "fixed compensation", "base salary"
    ],
    "Leave Policy Mentioned": [
        "annual leave", "sick leave", "casual leave", "earned leave",
        "paid leave", "leaves per year"
    ],
    "Probation Period Defined": [
        "probation period", "probationary period", "confirmation after"
    ],
    "Grievance Mechanism": [
        "grievance", "escalation", "dispute resolution", "hr can be contacted"
    ],
}


def analyze_document(text):
    """
    Analyze document text and return categorized risk flags.
    Returns dict with red, yellow, green findings.
    """
    text_lower = text.lower()
    results = {
        "red": [],
        "yellow": [],
        "green": [],
        "summary": {}
    }

    # Check red flags
    for clause_name, keywords in RED_FLAGS.items():
        matched_keywords = [kw for kw in keywords if kw in text_lower]
        if matched_keywords:
            snippet = _extract_snippet(text_lower, matched_keywords[0], text)
            results["red"].append({
                "clause": clause_name,
                "keywords_found": matched_keywords[:3],
                "snippet": snippet,
                "risk_level": "High Risk"
            })

    # Check yellow flags
    for clause_name, keywords in YELLOW_FLAGS.items():
        matched_keywords = [kw for kw in keywords if kw in text_lower]
        if matched_keywords:
            snippet = _extract_snippet(text_lower, matched_keywords[0], text)
            results["yellow"].append({
                "clause": clause_name,
                "keywords_found": matched_keywords[:3],
                "snippet": snippet,
                "risk_level": "Review Needed"
            })

    # Check green flags
    for clause_name, keywords in GREEN_FLAGS.items():
        matched_keywords = [kw for kw in keywords if kw in text_lower]
        if matched_keywords:
            snippet = _extract_snippet(text_lower, matched_keywords[0], text)
            results["green"].append({
                "clause": clause_name,
                "keywords_found": matched_keywords[:3],
                "snippet": snippet,
                "risk_level": "Safe"
            })

    # Summary
    results["summary"] = {
        "total_red": len(results["red"]),
        "total_yellow": len(results["yellow"]),
        "total_green": len(results["green"]),
        "overall_risk": _overall_risk(len(results["red"]), len(results["yellow"]))
    }

    return results


def _extract_snippet(text_lower, keyword, original_text):
    """Extract a small surrounding context snippet for a keyword."""
    try:
        idx = text_lower.find(keyword)
        if idx == -1:
            return ""
        start = max(0, idx - 80)
        end = min(len(original_text), idx + 150)
        snippet = original_text[start:end].strip()
        snippet = re.sub(r'\s+', ' ', snippet)
        return f"...{snippet}..."
    except:
        return ""


def _overall_risk(red_count, yellow_count):
    """Determine overall document risk level."""
    if red_count >= 3:
        return "🔴 High Risk — Do not sign without legal advice"
    elif red_count >= 1:
        return "🟠 Moderate Risk — Review flagged clauses carefully"
    elif yellow_count >= 3:
        return "🟡 Low-Moderate Risk — Some clauses need attention"
    else:
        return "🟢 Low Risk — Document looks generally safe"
