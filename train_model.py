import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Features
X = df[[
    "CGPA",
    "Programming",
    "Communication",
    "Aptitude",
    "Projects",
    "Internships"
]]

# Target
y = df["Placed"]

# Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved successfully!")