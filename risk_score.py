def calculate_risk(probability, amount, avg_amount):
    score = 0

    # 🔹 1. ML Model Contribution (0–50)
    score += probability * 50

    # 🔹 2. Amount-Based Risk (0–30)
    if amount > avg_amount * 5:
        score += 30
    elif amount > avg_amount * 3:
        score += 20
    elif amount > avg_amount * 2:
        score += 10

    # 🔹 3. Low Probability Adjustment
    if probability < 0.2:
        score -= 10

    # 🔹 Final score limit (0–100)
    score = max(0, min(score, 100))

    return score