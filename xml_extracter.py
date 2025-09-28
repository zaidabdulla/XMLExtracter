import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import os
import zipfile
import io
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

st.title("📂 Multiple XMLs to AI Insights (OpenRouter)")

uploaded_file = st.file_uploader("Upload ZIP containing XML files", type=["zip"])

def parse_xml(file_content, filename):
    """Parse single XML file and extract tag-value pairs"""
    try:
        tree = ET.parse(io.BytesIO(file_content))
        root = tree.getroot()
    except Exception as e:
        return pd.DataFrame([{"File": filename, "Tag": "ERROR", "Value": str(e)}])

    data = []

    def walk_tree(node, path=""):
        tag_path = f"{path}/{node.tag}" if path else node.tag

        # Capture attributes
        for attr_name, attr_value in node.attrib.items():
            data.append({
                "File": filename,
                "Tag": f"{tag_path}[@{attr_name}]",
                "Value": attr_value
            })

        # Capture text content (if present)
        if node.text and node.text.strip():
            data.append({
                "File": filename,
                "Tag": tag_path,
                "Value": node.text.strip()
            })

        # Recurse for children
        for child in node:
            walk_tree(child, tag_path)

    walk_tree(root)
    return pd.DataFrame(data)

def get_ai_insights(text, filename):
    """Send XML text to OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are an AI assistant that analyzes XML data."},
            {"role": "user", "content": f"Extract key insights from this XML ({filename}):\n\n{text}"}
        ]
    }
    response = requests.post(BASE_URL, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        dfs = []
        ai_results = {}
        for file_name in zip_ref.namelist():
            if file_name.endswith(".xml"):
                file_content = zip_ref.read(file_name)
                df = parse_xml(file_content, file_name)
                dfs.append(df)

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            st.subheader("📑 Extracted XML Data (All Files)")
            st.dataframe(combined_df)

            # --- Download button for Excel ---
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                combined_df.to_excel(writer, index=False, sheet_name="Extracted_XML_Data")
            excel_data = output.getvalue()

            st.download_button(
                label="📥 Download Extracted Data as Excel",
                data=excel_data,
                file_name="extracted_xml_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            if st.button("🔎 Get AI Insights for Each File"):
                with st.spinner("Processing with AI..."):
                    for file_name in zip_ref.namelist():
                        if file_name.endswith(".xml"):
                            xml_text = zip_ref.read(file_name).decode("utf-8")
                            ai_results[file_name] = get_ai_insights(xml_text, file_name)

                st.subheader("🤖 AI Insights")
                for fname, insight in ai_results.items():
                    st.markdown(f"### 📄 {fname}")
                    st.write(insight)
        else:
            st.error("No XML files found in the uploaded ZIP.")
