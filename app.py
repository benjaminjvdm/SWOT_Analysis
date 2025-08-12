import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

def initialize_session_state():
    """Initializes session state variables if they don't exist."""
    if "factors" not in st.session_state:
        st.session_state.factors = {
            "Strengths": [],
            "Weaknesses": [],
            "Opportunities": [],
            "Threats": [],
        }

def factor_input_ui(category):
    """Renders the UI for adding and managing factors for a category."""
    st.subheader(category)

    # Input for new factor
    new_factor = st.text_input(f"Add a new factor for {category}", key=f"new_{category}")
    if st.button(f"Add Factor", key=f"add_{category}"):
        if new_factor:
            st.session_state.factors[category].append({"name": new_factor, "importance": 1})
            # Clear the input box after adding
            st.rerun()

    # Display existing factors
    for i, factor in enumerate(st.session_state.factors[category]):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.text(factor["name"])
        with col2:
            st.session_state.factors[category][i]["importance"] = st.slider(
                f"Importance", 1, 3, factor["importance"], key=f"{category}_{i}_slider"
            )
        with col3:
            if st.button("Remove", key=f"remove_{category}_{i}"):
                st.session_state.factors[category].pop(i)
                st.rerun()

def calculate_average_importance(factors):
    """Calculates the average importance for each SWOT category."""
    avg_values = {}
    for category, items in factors.items():
        if items:
            avg_values[category] = np.mean([item["importance"] for item in items])
        else:
            avg_values[category] = 0
    return avg_values

def create_radar_chart(avg_values):
    """Creates and returns a Plotly radar chart."""
    categories = list(avg_values.keys())
    values = list(avg_values.values())

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values + values[:1],
        theta=categories + categories[:1],
        fill='toself',
        name='SWOT Analysis'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3]
            )),
        showlegend=False,
        title="SWOT Analysis Radar Chart"
    )
    return fig

def main():
    """The main function that runs the Streamlit application."""
    st.set_page_config(page_title="SWOT Analysis Radar Chart", page_icon="💪", layout="wide")

    initialize_session_state()

    # --- Sidebar ---
    st.sidebar.subheader("About the Author")
    st.sidebar.image("assets/author_image.png", caption="Moon Benjee (문벤지)")
    st.sidebar.markdown(
        """
        This app was Built with ❤️ by **Benjee(문벤지)**.
        You can connect with me on: [LinkedIn](https://www.linkedin.com/in/benjaminjvdm/)
        """
    )

    # --- Main Content ---
    st.title("SWOT Analysis Radar Chart")
    st.write("Add factors for each category and set their importance from 1 (Normal) to 3 (Highest).")

    # --- Factor Input ---
    cols = st.columns(4)
    categories = ["Strengths", "Weaknesses", "Opportunities", "Threats"]
    for i, category in enumerate(categories):
        with cols[i]:
            factor_input_ui(category)

    # --- Chart and Export ---
    st.header("Analysis Visualization")

    avg_values = calculate_average_importance(st.session_state.factors)

    if any(avg_values.values()):
        fig = create_radar_chart(avg_values)
        st.plotly_chart(fig, use_container_width=True)

        # --- Exporting ---
        st.subheader("Export Your Analysis")

        # Export Chart
        img_bytes = fig.to_image(format="png", scale=2)
        st.download_button(
            label="Download Chart as PNG",
            data=img_bytes,
            file_name="swot_radar_chart.png",
            mime="image/png"
        )

        # Export Data
        all_factors = []
        for category, items in st.session_state.factors.items():
            for item in items:
                all_factors.append([category, item['name'], item['importance']])

        if all_factors:
            df = pd.DataFrame(all_factors, columns=["Category", "Factor", "Importance"])
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name="swot_analysis_data.csv",
                mime="text/csv",
            )

    else:
        st.info("Add some factors to see the chart.")


if __name__ == "__main__":
    main()
