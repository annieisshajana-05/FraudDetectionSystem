import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Load dataset (FULL PATH)
data = pd.read_csv(r"C:\Users\moksh\OneDrive\Desktop\FraudDetectionSystem\data\creditcard.csv")
print("✅ Dataset loaded")

# Preprocessing
data['Amount'] = StandardScaler().fit_transform(data[['Amount']])
data = data.drop(['Time'], axis=1)
print("✅ Preprocessing done")

# Reduce dataset size (important for speed)
data = data.sample(10000)
print("✅ Data reduced")

# Split data
X = data.drop("Class", axis=1)
y = data["Class"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print("✅ Data split")

# Train model
model = RandomForestClassifier(n_estimators=50)
model.fit(X_train, y_train)
print("✅ Model trained")

# Create models folder if not exists
model_dir = r"C:\Users\moksh\OneDrive\Desktop\FraudDetectionSystem\models"
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# Save model
model_path = os.path.join(model_dir, "model.pkl")
joblib.dump(model, model_path)

print("✅ Model saved at:", model_path)