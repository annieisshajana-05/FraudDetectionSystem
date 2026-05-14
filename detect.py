import joblib
import os
from user_data import user_history
from risk_score import calculate_risk
from behavior import behavior_check
from location_check import check_location

# Load model
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "model.pkl")
# Load optional second model for ensemble (if available)
model2_path = os.path.join(os.path.dirname(__file__), "..", "models", "model2.pkl")
try:
    model2 = joblib.load(model2_path)
except Exception:
    model2 = None
model = joblib.load(model_path)

def detect_fraud(user, features, amount, location):

    user_info = user_history[user]

    # ML probability from primary model
    prob1 = model.predict_proba([features])[0][1]
    # ML probability from secondary model (if available)
    if model2 is not None:
        prob2 = model2.predict_proba([features])[0][1]
        avg_prob = (prob1 + prob2) / 2
    else:
        avg_prob = prob1
    prob = avg_prob  # unified probability used downstream

    # Checks
    behavior_flag = behavior_check(amount, user_info["avg_amount"])
    location_flag = check_location(user_info["last_location"], location)

    # Risk score
    risk_score = calculate_risk(prob, amount, user_info["avg_amount"])

    # 🔥 Reasons
    reasons = []

    if behavior_flag:
        reasons.append("Unusual spending behavior")

    if location_flag:
        reasons.append("Location mismatch")

    if risk_score > 70:
        reasons.append("High ML risk score")

    # Decision
    if risk_score > 70:
        result = "Fraud ❌"
    elif behavior_flag or location_flag:
        result = "Suspicious ⚠️"
    else:
        result = "Safe ✅"

    return result, risk_score, reasons, prob