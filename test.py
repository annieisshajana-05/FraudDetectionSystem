import pandas as pd
import os

# Get correct file path
file_path = os.path.join(os.path.dirname(__file__), "../data/creditcard.csv")

print("📂 File path:", file_path)

try:
    data = pd.read_csv(file_path)
    
    print("\n✅ Dataset loaded successfully!\n")
    
    print("🔹 First 5 rows:")
    print(data.head())
    
    print("\n🔹 Dataset Info:")
    data.info()
    
    print("\n🔹 Fraud vs Normal count:")p
    print(data['Class'].value_counts())

except Exception as e:
    print("❌ Error:", e)