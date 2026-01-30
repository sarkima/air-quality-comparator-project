import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def run():
    st.title("Pollutants Level Analysis")

    df = pd.read_csv("data/nox_predictions.csv")

        # --- Pollutant selection ---
    pollutant_cols = ["no2", "o3"]
    selected_pollutant = st.selectbox("Select Pollutant", pollutant_cols)


    # --- Smoothing slider ---
    smoothing = st.slider(
        "Smoothing window (moving average)",
        min_value=1,
        max_value=20,
        value=1,
        step=1
    )

    df["smooth"] = (
        df[selected_pollutant].rolling(window=smoothing, min_periods=1).mean()
    )

        # --- Plotly sensor chart ---
    st.markdown(f"### {selected_pollutant} Over Time (Interactive)")
    fig_sensor = px.line(
        df,
        x="date",
        y="smooth",
        title=f"{selected_pollutant} (Smoothed)",
        markers=True
    )
    st.plotly_chart(fig_sensor, use_container_width=True)

    # --- Summary statistics ---
    st.markdown("### Summary Statistics")
    st.write(df[selected_pollutant].describe())

    # --- Correlation heatmap ---
    st.markdown("### Pollutant Correlation Heatmap")

    corr = df.drop(columns=["date", "true_nox", "pred_nox"]).corr()

    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Sensor Pollutant Correlation Matrix"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)