import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- Functions ----------
@st.cache_data
def load_csv(file):
    df = pd.read_csv(file)
    return df['multiplier'].tolist()

def compute_advanced_confidence(data, threshold=2.0, trend_window=5):
    if not data:
        return 0.5, 0.5, "Neutral"

    data = np.array(data)
    # Base frequency
    above = np.sum(data > threshold)
    under = np.sum(data <= threshold)
    total = above + under
    base_above = above / total
    base_under = under / total

    # Recent trend
    recent = data[-trend_window:] if len(data) >= trend_window else data
    recent_above = np.sum(recent > threshold)
    recent_under = np.sum(recent <= threshold)

    trend_bias = 0
    if recent_under > recent_above:
        trend_bias = 0.05  # slight push toward Above
    elif recent_above > recent_under:
        trend_bias = -0.05  # slight push toward Under

    # Streak adjustment
    streak_bias = 0
    streak = 1
    for i in range(len(data)-2, -1, -1):
        if (data[i] > threshold and data[i+1] > threshold) or (data[i] <= threshold and data[i+1] <= threshold):
            streak += 1
        else:
            break
    if streak >= 3:
        if data[-1] <= threshold:
            streak_bias = 0.08  # bias toward Above after Under streak
        else:
            streak_bias = -0.08  # bias toward Under after Above streak

    # Final confidence
    above_conf = min(max(base_above + trend_bias + streak_bias, 0), 1)
    under_conf = 1 - above_conf

    # Risk level
    if above_conf > 0.65:
        risk = "Low risk for Above 2"
    elif above_conf < 0.35:
        risk = "Low risk for Under 2"
    else:
        risk = "High risk / uncertain"

    return above_conf, under_conf, risk

def risk_bar(above_conf):
    fig, ax = plt.subplots(figsize=(6, 0.4))
    color = "green" if above_conf > 0.5 else "red"
    ax.barh(["Confidence"], [above_conf*100], color=color)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Above 2 Confidence (%)")
    st.pyplot(fig)

def main():
    st.title("Crash Game Advanced Predictor")

    st.write("Upload a CSV or enter values manually. Advanced model uses frequency, trends, and streaks.")

    # Upload CSV
    uploaded_file = st.file_uploader("Upload multipliers CSV", type=["csv"])
    data = []
    if uploaded_file:
        data = load_csv(uploaded_file)
        st.success(f"Loaded {len(data)} multipliers from file.")

    # Manual input
    st.subheader("Manual Input")
    new_val = st.text_input("Enter a new multiplier (e.g., 1.87)")
    if st.button("Add to history"):
        try:
            val = float(new_val)
            data.append(val)
            st.success(f"Added {val} to history")
        except:
            st.error("Invalid number.")

    # Display history
    st.subheader("Recent History (last 10)")
    if data:
        st.write(data[-10:])
    else:
        st.write("No data yet.")

    # Compute advanced confidence
    above_conf, under_conf, risk = compute_advanced_confidence(data)
    st.subheader("Prediction Confidence")
    st.write(f"Above 200%: {above_conf:.1%}")
    st.write(f"Under 200%: {under_conf:.1%}")
    st.write(f"Risk Level: {risk}")

    # Visualization
    st.subheader("Risk Visualization")
    if data:
        risk_bar(above_conf)

    # Prediction buttons
    st.subheader("Make a Prediction")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Predict Above 2"):
            st.write(f"Prediction: Above 200% ({above_conf:.1%} confidence)")
    with col2:
        if st.button("Predict Under 2"):
            st.write(f"Prediction: Under 200% ({under_conf:.1%} confidence)")

if __name__ == "__main__":
    main()
