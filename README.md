# XMLExtracter
To Decode XML and display values against each tag, get AI Insights as well

# 📂 XML to AI Insights (Streamlit + OpenRouter)

This Streamlit app lets you upload a **ZIP file of multiple XMLs**, extract their **tag–value pairs**, view them in a table, download the results to **Excel**, and generate **AI-powered insights** using the [OpenRouter API](https://openrouter.ai/).

---

## 🚀 Features
- Upload a ZIP file containing multiple **XML files**.
- Parse and extract **Tag–Value pairs** recursively.
- Combined table with columns: **File | Tag | Value**.
- 📥 Download results into an Excel file (`.xlsx`).
- 🔎 Get **AI insights** for each XML file via OpenRouter.

---

## 📦 Installation

1. Clone this repo or copy the `app.py` script.
2. Install dependencies:
   ```bash
   pip install streamlit pandas openpyxl requests python-dotenv
   ```

---

## 🔑 Setup OpenRouter API Key

1. Sign up at [OpenRouter](https://openrouter.ai/) and get an API key.  
2. Create a `.env` file in the project root with:
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   ```

---

## ▶️ Run the App

Start the Streamlit server:

```bash
streamlit run app.py
```

The app will open in your browser (default: `http://localhost:8501`).

---

## 📂 Usage

1. Upload a **ZIP file** containing one or more `.xml` files.
2. View the extracted **Tag–Value pairs** in an interactive table.
3. Click **📥 Download Extracted Data as Excel** to export results.
4. (Optional) Click **🔎 Get AI Insights for Each File** to let the AI analyze each XML file.

---

## 📝 Example Output

### Extracted Table (inside Streamlit)

| File       | Tag         | Value      |
|------------|-------------|------------|
| data1.xml  | root/name   | John Doe   |
| data1.xml  | root/age    | 34         |
| data2.xml  | order/id    | 1001       |
| data2.xml  | order/item  | Laptop     |

### Excel Export
- A single sheet named **`Extracted_XML_Data`** with all parsed XML data.

### AI Insights Example
```
📄 data1.xml
- Contains user details: name, age, and address.

📄 data2.xml
- Represents an order with ID 1001 for item "Laptop".
```

---

## ⚙️ Configuration
- Default model: `openai/gpt-4o-mini`.  
- To change models, update `payload["model"]` in the script.

---

## 📌 Notes
- Only `.zip` uploads are supported (must contain `.xml` files).
- Malformed XML files will show an `ERROR` row in the extracted data.
- Ensure your API key has sufficient quota in OpenRouter.

---

