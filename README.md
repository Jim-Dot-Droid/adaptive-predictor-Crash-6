# Crash Game Advanced Predictor

Streamlit app that predicts if the next multiplier in a crash game will be above or under 2.0 (200%) using advanced logic.

## Features
- Upload a CSV with a column named `multiplier`
- Manual input for new values
- Confidence calculation based on:
  - Frequency (historical data)
  - Recent trend bias
  - Streak detection
- Risk visualization bar
- Prediction buttons

## Setup
```
pip install -r requirements.txt
streamlit run app.py
```
