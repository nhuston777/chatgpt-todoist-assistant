```markdown
# GPT-Powered Todoist Productivity Assistant

This assistant connects your [Todoist](https://todoist.com/) task list with [OpenAI GPT-4o](https://platform.openai.com/docs/models/gpt-4) to help you get organized, prioritize intelligently, and streamline your workflow. It supports multiple modes: Streamlit UI, terminal-based CLI, and a Dockerized deployment.

---

## ✨ Features

- 📋 Pulls your **active Todoist tasks** with full metadata (project, section, labels, priorities, due dates)
- 🤖 Uses GPT-4o to **summarize tasks and suggest improvements**
- ✅ CLI and Streamlit modes both support **suggestion-by-suggestion approval**
- 🔐 Password-protected Streamlit UI
- 🐳 Docker support for containerized CLI execution
- ⚙️ Modular code structure for future API integration (coming soon)

---

## 🧠 Project Modes

This branch supports two ways to interact with the assistant:

---

### 🖥️ 1. CLI Mode (Terminal-Based)

Run the assistant in a traditional command-line interface.

- **Entry point:** `main.py`
- **Run with Docker:**
  ```bash
  docker run -it --env-file .env gpt-todoist-backend
  ```
- **Run locally:**
  ```bash
  python main.py
  ```

---

### 🌐 2. Streamlit UI Mode (Web-Based)

Launch an interactive web app for reviewing and approving suggestions visually.

- **Entry point:** `streamlit_app.py`
- **Run locally:**
  ```bash
  streamlit run streamlit_app.py
  ```

> ⚙️ **Note:** The Dockerfile is currently set to run CLI mode by default.

---

## 🐳 Docker Setup

### Build the image:
```bash
docker build -t gpt-todoist-backend .
```

### Run interactively:
```bash
docker run -it --env-file .env gpt-todoist-backend
```

> Make sure to include a `.dockerignore` with `.env` to avoid baking secrets into the image.

---

## 🔧 Local Setup (No Docker)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/chatgpt-todoist-assistant.git
cd chatgpt-todoist-assistant
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your `.env` file

```env
OPENAI_API_KEY=your-openai-api-key
TODOIST_API_TOKEN=your-todoist-api-token
APP_PASSWORD=your-password  # optional for Streamlit
```

Ensure `.env` is listed in `.gitignore`.

---

## ☁️ Deploy to Streamlit Cloud

1. Push your repo to GitHub  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)  
3. Click **Create App** and link your GitHub repo  
4. Add your secrets under **Manage App → Secrets**:

```toml
OPENAI_API_KEY = "your-openai-api-key"
TODOIST_API_TOKEN = "your-todoist-api-token"
APP_PASSWORD = "your-password"
```

---

## 🔐 Security Notes

- `.env` is excluded from Git using `.gitignore`
- Password required for Streamlit access
- Secrets are only stored in environment variables or Streamlit secrets, never in code

---

## 📁 File Structure

```
chatgpt-todoist-assistant/
├── main.py                # CLI assistant
├── streamlit_app.py       # Streamlit UI logic
├── openai_api.py          # GPT integration
├── todoist_api.py         # Todoist API handling
├── config.py              # Env variable loader
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker image definition (CLI entrypoint)
├── .dockerignore          # Prevents secrets & build bloat
├── .gitignore             # Git exclusions
└── README.md
```

---

## 🛣 Roadmap

- [x] GPT-powered task analysis
- [x] Approve/reject suggestion loop
- [x] Streamlit UI + password
- [x] CLI mode for interactive terminal users
- [x] Dockerized CLI deployment
- [ ] REST API with FastAPI
- [ ] Suggestion editing and direct Todoist writeback
- [ ] Support for creating projects, priorities, and labels
- [ ] Demo mode with sample data

---

## 👨‍💻 Author

Built by **[Your Name]**  
GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

---

## 📝 License

MIT License – Use freely, improve openly.
```
