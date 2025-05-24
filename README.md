# GPT-Powered Todoist Productivity Assistant

This is a Streamlit-based productivity assistant that connects your [Todoist](https://todoist.com/) task list with [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4). It analyzes your tasks and suggests ways to improve organization, balance, clarity, priorities, and deadlines—right from your browser.

---

## ✨ Features

- 📋 Pulls your **active Todoist tasks**, including project, section, labels, priorities, and due dates  
- 🤖 Uses GPT-4o to **analyze your task list and suggest improvements**  
- ✅ Lets you **approve suggestions one by one**  
- 🔐 Password-protected to prevent unauthorized access  
- ☁️ Runs both **locally** and on **Streamlit Cloud**  
- ⚙️ Designed with clean, modular Python code  

---

## 🔧 Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/chatgpt-todoist-assistant.git
cd chatgpt-todoist-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file in the project root

```env
OPENAI_API_KEY=your-openai-api-key
TODOIST_API_TOKEN=your-todoist-api-token
```

Make sure your `.env` file is listed in `.gitignore`.

---

## 🚀 Run Locally

```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deploy to Streamlit Cloud

1. Push your repo to GitHub  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)  
3. Click **Create App** and select your GitHub repo  
4. Set your secrets in **Manage App → Secrets**:

```toml
OPENAI_API_KEY = "your-openai-api-key"
TODOIST_API_TOKEN = "your-todoist-api-token"
APP_PASSWORD = "your-password"
```

---

## 🔐 Security Notes

- Secrets are never stored in code—only in `.env` or `st.secrets`
- Password gate prevents unauthorized use
- `.env` is excluded from GitHub using `.gitignore`

---

## 📁 File Structure

```
chatgpt-todoist-assistant/
├── streamlit_app.py        # UI logic and user flow
├── openai_api.py           # GPT integration
├── todoist_api.py          # Todoist API logic
├── config.py               # Securely loads API keys from env or secrets
├── requirements.txt        # Dependencies
├── .env                    # Local environment vars (excluded from Git)
├── .gitignore
└── README.md
```

---

## 🛣 Roadmap

- [x] GPT-powered task analysis
- [x] Approve/reject suggestion loop
- [x] Streamlit Cloud deployment
- [x] Password protection
- [ ] Write suggestions back to Todoist
- [ ] Create/edit priorities, projects, and labels
- [ ] Demo mode with sample data

---

## 👨‍💻 Author

Built by **[Your Name]**  
GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

## 📝 License

MIT License – Use freely, improve openly.
