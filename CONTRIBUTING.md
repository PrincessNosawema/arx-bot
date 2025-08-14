# Contributing to **Arx-bot**

Thank you for your interest in contributing to **Arx-bot**!  
We welcome improvements, bug fixes, new features, and documentation enhancements.

Please take a moment to review these guidelines before you start.

---

## 📌 Code of Conduct
By participating in this project, you agree to uphold our standards of respectful and constructive communication.

---

## 📂 Project Structure Overview

```

root/
├── app.py                 # Flask server entry point
├── desktop_ui.py          # Desktop app entry point
├── features/              # Core backend modules
│   ├── arxiv_client.py
│   ├── chatbot.py
│   ├── llm.py
├── static/                # Frontend assets (CSS, JS, media)
├── templates/             # HTML templates
└── requirements.txt

```

Understanding the structure will help you place your contributions in the right place.

---

## 🛠 Development Setup

1. **Fork** this repository  
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/PrincessNosawema/arx-bot
   cd arx-bot
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```
4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
5. **Set environment variables** (for chatbot integration):

   ```bash
   export GEMINI_API_KEY="your_api_key_here"  # macOS/Linux
   setx GEMINI_API_KEY "your_api_key_here"    # Windows PowerShell
   ```

---

## 🧩 Contribution Types

* **🐛 Bug Fixes**
  Locate the issue, fix it, and ensure it’s covered by tests or verified manually.

* **💡 New Features**
  Propose the feature in an issue **before** starting work to align with project goals.

* **📖 Documentation**
  Improve README, inline comments, or user instructions.

* **🎨 UI/UX Improvements**
  Enhance CSS, JS, and HTML for better usability and accessibility.

---

## 📜 Coding Guidelines

* **Python**

  * Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
  * Use `logging` instead of `print` where possible
  * Keep functions small and focused

* **JavaScript**

  * Use `const` and `let` (avoid `var`)
  * Keep DOM selectors efficient
  * Avoid inline event handlers — use `addEventListener`

* **HTML/CSS**

  * Keep templates clean and semantic
  * Use external stylesheets/scripts (no inline styles unless unavoidable)

---

## 🔄 Git Workflow

1. **Create a branch** for your work:

   ```bash
   git checkout -b feature/<feature-name>
   # or
   git checkout -b fix/<bug-name>
   ```

2. **Commit changes** with clear messages:

   ```
   feat: add semantic search improvement
   fix: resolve PDF extraction error
   docs: update README usage section
   ```

3. **Push to your fork**:

   ```bash
   git push origin feature/<feature-name>
   ```

4. **Open a Pull Request**

   * Describe what you changed and why
   * Link any related issues (e.g., `Closes #12`)

---

## ✅ Pull Request Checklist

Before submitting:

* [ ] Code follows the style guide
* [ ] No unused imports or variables
* [ ] Tested locally in **both Web and Desktop modes**
* [ ] No breaking changes unless approved

---

## 🧪 Testing Your Changes

* **Web Mode**

  ```bash
  python app.py
  ```

  Visit: `http://127.0.0.1:5000`

* **Desktop Mode**

  ```bash
  python desktop_ui.py
  ```

Verify:

* Search works
* Results are ranked and displayed
* Chatbot responds with relevant answers

---

## 📬 Getting Help

If you have questions:

* Open a GitHub **Discussion** for general queries
* Open a **GitHub Issue** for bugs or feature requests

---

**Thank you for contributing!**
Your work helps make **Arx-bot** more powerful and useful for the research community.