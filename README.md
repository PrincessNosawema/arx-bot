# Arx-bot

**Arx-bot** is a hybrid **arXiv research document retrieval** and **intelligent chatbot assistant** that lets you:
- Search academic papers from [arXiv.org](https://arxiv.org)  
- Rank results based on semantic and temporal relevance  
- View summaries, authors, abstracts, and direct PDF links  
- Chat with an AI assistant that can answer questions using the retrieved papers as reference

It runs as:
1. **A Web Application** via Flask
2. **A Desktop Application** via PyQt5 + Embedded WebView

---

## ✨ Features

- **arXiv Search Integration**  
  Uses the [`arxiv`](https://pypi.org/project/arxiv/) Python package to query and fetch PDFs from arXiv.

- **Automated PDF Download & Parsing**  
  Downloads and extracts full text from paper PDFs using `PyPDF2`.

- **Advanced Document Ranking**  
  Combines:
  - **TF-IDF relevance scoring**
  - **Semantic similarity** via `sentence-transformers`
  - **Query expansion** using `nltk.wordnet`
  - **Temporal relevance weighting**

- **Integrated Chatbot**  
  Powered by Google Gemini (`google-genai`) for:
  - Contextual Q&A using retrieved papers
  - Intelligent fallback when answer is not in the papers

- **Dual UI Support**  
  - **Web mode**: Flask server with HTML/CSS/JS frontend  
  - **Desktop mode**: PyQt5 app embedding the web interface

- **Responsive Frontend**  
  - Video background  
  - Interactive hover effects for results  
  - Collapsible chatbot panel  

---

## 📂 Project Structure

```

root/
├── app.py                 # Flask web server entry point
├── desktop_ui.py          # Desktop app entry point (PyQt5)
├── requirements.txt       # Dependencies
├── features/              # Core functional modules
│   ├── arxiv_client.py    # arXiv search, download, text extraction
│   ├── chatbot.py         # Chatbot integration with Gemini
│   ├── llm.py             # Ranking, query expansion, semantic search
├── static/                # Static assets (CSS, JS, video)
│   ├── bg.mp4
│   ├── script.js
│   ├── style.css
├── templates/             # HTML templates for Flask
│   ├── index.html
│   ├── result.html
└── full_text.txt          # Generated after search (stores retrieved doc summaries)

```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/PrincessNosawema/arx-bot
cd arx-bot
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Activate:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

You **must** set your Google Gemini API key for the chatbot to work.

#### macOS/Linux

```bash
export GEMINI_API_KEY="your_api_key_here"
```

#### Windows (PowerShell)

```powershell
setx GEMINI_API_KEY "your_api_key_here"
```

---

## 🚀 Usage

You can run **either Web Mode** or **Desktop Mode**.

### **Run Web Mode**

```bash
python app.py
```

* Opens the Flask server on `http://127.0.0.1:5000/`
* Default browser auto-opens

### **Run Desktop Mode**

```bash
python desktop_ui.py
```

* Opens a PyQt5 window with embedded web UI
* Flask runs in a background thread

---

## 🔍 How It Works

1. **User Search**

   * Input query & number of results
   * System fetches up to 3× requested results from arXiv

2. **Data Processing**

   * Downloads PDFs, extracts text
   * Stores summaries in `full_text.txt`

3. **Ranking**

   * Expands query with synonyms
   * Calculates:

     * TF-IDF similarity
     * Semantic similarity (BERT embeddings)
     * Temporal relevance
   * Returns top N documents

4. **Chatbot Interaction**

   * Reads `full_text.txt`
   * Answers questions using Gemini
   * Formats response with HTML tags

---

## 🖥️ Tech Stack

**Backend**

* Python 3.10+
* Flask
* arxiv
* requests
* PyPDF2
* nltk
* scikit-learn
* sentence-transformers
* google-genai

**Frontend**

* HTML5, CSS3, JavaScript
* Video background (`bg.mp4`)
* Responsive layout

**Desktop**

* PyQt5
* PyQtWebEngine

---

## ⚠️ Troubleshooting

* **No API Key Error**
  Ensure `GEMINI_API_KEY` is set in your environment.

* **PDF Download Failures**
  Some arXiv PDFs may not allow extraction — they’ll be skipped.

* **Slow Response Times**
  Initial embedding downloads from `sentence-transformers` may take time.

* **Desktop Mode Not Starting**
  Install PyQtWebEngine along with PyQt5:

  ```bash
  pip install PyQt5 PyQtWebEngine
  ```

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

* [arXiv.org](https://arxiv.org) for providing open-access academic papers
* [Sentence Transformers](https://www.sbert.net/)
* [Google Gemini](https://ai.google/)
* [PyPDF2](https://pypdf2.readthedocs.io/)