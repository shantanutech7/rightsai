def calculate_risk_score(analysis_results):
    """
    Calculate a 0-100 risk score based on detected clauses.
    Lower score = more dangerous document.
    Higher score = safer document.
    """

    # Each red flag deducts points — weighted by severity
    RED_FLAG_WEIGHTS = {
        "Non-Compete Clause": 20,
        "IP Ownership of Side Projects": 18,
        "Forced Arbitration": 15,
        "Immediate Termination Without Notice": 17,
        "Unlimited Liability": 20,
        "Auto-Renewal Trap": 10,
    }

    # Each yellow flag deducts fewer points
    YELLOW_FLAG_WEIGHTS = {
        "Notice Period Imbalance": 5,
        "Confidentiality Clause": 4,
        "Unilateral Changes": 7,
        "Data Sharing": 5,
        "Variable Compensation": 4,
    }

    # Each green flag adds points
    GREEN_FLAG_WEIGHTS = {
        "Clear Salary Mentioned": 8,
        "Leave Policy Mentioned": 6,
        "Probation Period Defined": 5,
        "Grievance Mechanism": 7,
    }

    score = 60  # Base score

    # Deduct for red flags
    for item in analysis_results["red"]:
        deduction = RED_FLAG_WEIGHTS.get(item["clause"], 10)
        score -= deduction

    # Deduct for yellow flags
    for item in analysis_results["yellow"]:
        deduction = YELLOW_FLAG_WEIGHTS.get(item["clause"], 3)
        score -= deduction

    # Add for green flags
    for item in analysis_results["green"]:
        addition = GREEN_FLAG_WEIGHTS.get(item["clause"], 4)
        score += addition

    # Clamp between 0 and 100
    score = max(0, min(100, score))

    # Risk label based on score
    if score >= 75:
        label = "Safe to Sign"
        color = "#06D6A0"
        emoji = "🟢"
    elif score >= 50:
        label = "Review Carefully"
        color = "#FFD166"
        emoji = "🟡"
    elif score >= 25:
        label = "Risky — Get Advice"
        color = "#FF9F43"
        emoji = "🟠"
    else:
        label = "Dangerous — Do Not Sign"
        color = "#FF6B6B"
        emoji = "🔴"

    return {
        "score": score,
        "label": label,
        "color": color,
        "emoji": emoji
    }
