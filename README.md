# Vector-JIRA-AI-Agent

🚀 **Introducing the JIRA AI Agent Project!** 🌟

## 🔍 Problem Statement
In the fast-paced world of technical support, repetitive issues consume valuable time for developers and support engineers. **JIRA AI Agent** solves this problem by leveraging historical data to efficiently resolve queries, enabling teams to focus on critical and high-priority tasks.

---

## 🎯 Features
- ✅ Matches incoming queries with historical Jira tickets.
- ✅ Suggests resolutions or attaches relevant documents automatically.
- ✅ Integrates easily with any frontend technology.
- ✅ Uses `ngrok` for HTTPS routing to handle Jira webhooks.
- ✅ Provides customizable configurations for team-specific Jira projects.

---

## 💻 Tech Stack
- **Backend:** Python Flask with Redis and Celery for task management.
- **Frontend:** Built using Streamlit but supports other frontend technologies.
- **Database:** Locally hosted Weaviate in a Docker container for semantic embeddings.

### AI Integration
- **Embedding Generation:** Weaviate integrated Cohere.
- **Contextual Suggestions:** Ollama (TinyLLaMA), hosted locally in a Docker container.

### Routing
- **ngrok** for secure HTTPS routing.

### Hosting
- **Azure Virtual Machine**.

---

## 🌐 Live Demo
👉 **Try it here**
https://jira-agent.streamlit.app/

---

## 🔗 Key Highlights
- **Batch Processing:** Optimized webhook management for handling ticket data.
- **Semantic Search:** Efficient retrieval using embeddings stored in Weaviate.
- **Cost-Effective:** Ideal for teams with low-to-moderate traffic.
- **Automation:** Processes Jira tickets automatically when transitioned to "Closed."
- **Scalable Design:** Flexibility to integrate with different frontends.

---

## 🛠️ Workflow

### Database Integration
- Weaviate stores semantic embeddings for tickets and incidents.
- Webhooks trigger updates when Jira tickets transition to "Closed," saving the ticket data.

### Embedding Generation
- Cohere generates embeddings for each ticket.
- The embeddings are stored in Weaviate for efficient query resolution.

### AI-Powered Query Resolution
- Locally hosted Ollama (TinyLLaMA) provides context-aware suggestions based on embeddings and historical data.

### Frontend Interaction
- Streamlit connects to the backend API for querying and displaying results.

### HTTPS Routing
- `ngrok` is used for secure HTTPS communication required for Jira webhooks.

---

## 📁 Configuration Requirements
To run this project, create a `.env` file with the following variables:

```env

# Jira Configuration
JIRA_URL=""
JIRA_USERNAME=""
JIRA_API_TOKEN=""

COHERE_API_KEY = ""
```

---

## ✨ Future Scope
- 🚀 Scale the project to handle production-level traffic.
- 🤖 Explore more advanced AI models for enhanced resolution accuracy.
- 📊 Add analytics to visualize ticket trends and resolutions.

---

## 📢 Feedback and Support
We welcome your thoughts, suggestions, or queries! Please feel free to leave feedback or connect with us for further discussions.

---

## 🌟 How to Set Up Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/vector-jira-ai-agent.git
```

### 2. Navigate to the project directory
```bash
cd vector-jira-ai-agent
```

### 3. Install the required dependencies
```bash
pip install -r requirements.txt
```

### 4.1. Start Docker container for Weaviate
```bash
docker-compose up
```
### 4.2. Start Docker container for Ollama
You can choose any model of your choice(*Change config of Weaviate acordingly)


### 5. Run the Flask backend
```bash
backend/start_server.sh
```

### 6. Start ngrok for HTTPS routing
```bash
ngrok http 5000
```

### 7. Access the application
- **Localhost:** http://localhost:5000
- **ngrok URL:** Your ngrok-provided URL

---

## 💡 Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
