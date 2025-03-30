import streamlit as st
import pandas as pd
import requests
import json

# Set your OpenRouter API key from Streamlit secrets
api_key = st.secrets["OPENROUTER_API_KEY"]

# Page title
st.title("🛠️ DispoCheck: NC Description Review Tool (Powered by Gemini)")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Custom question input
question = st.text_input("Question has no role to play")

# Run analysis button
if uploaded_file and question:
    df = pd.read_csv(uploaded_file)

    # Check required columns
    if "Disposition" not in df.columns or "NC_Description" not in df.columns:
        st.error("CSV must contain 'Disposition' and 'NC_Description' columns.")
    else:
        st.info("Running Gemini analysis, please wait...")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "DispoCheck Streamlit"
        }

        answers = []

        for _, row in df.iterrows():
            prompt = f""" Disposition given: {row['Disposition']}
NC Description: {row['NC_Description']}
Based on the NC Description, what should the correct disposition be?

Respond with one of the following options only: Repair, Use As Is, or Scrap.

Respond with only one word and nothing else.
"""

            payload = {
                "model": "google/gemini-pro",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=json.dumps(payload)
                )

                answer = response.json()["choices"][0]["message"]["content"].strip()
                clean_answer = answer.split()[0]  # take only the first word
                answers.append(clean_answer)

            except Exception as e:
                st.error(f"API error: {e}")
                answers.append("Error")

        df["AI_Answer"] = answers
        st.success("✅ Analysis complete!")

        st.write(df)

        # Download updated CSV
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Download CSV with AI Answers",
            data=csv,
            file_name="updated_dispo_data.csv",
            mime="text/csv"
        )

