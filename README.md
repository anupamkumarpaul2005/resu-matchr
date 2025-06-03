# 🧠 ResuMatchr: AI-Powered Resume Matcher & Optimizer
**ResuMatchr** is a smart, AI-driven platform designed to help job seekers improve their resumes and find the best job matches, while also empowering recruiters to post jobs. Leveraging modern AI tools and semantic search, it brings precision, clarity, and explainability to the job search and hiring process.

## 🚀 Project Overview
Finding the right job or candidate can be overwhelming, especially with countless applications and generic filters. ResuMatchr bridges this gap by combining powerful AI models and vector search to:
- Upload their resume and receive AI-generated suggestions to improve.
- Get predicted job roles based on resume content.
- Find top job matches ranked by both vector similarity and LLM scoring.
- For recruiters: Post jobs and get them instantly available for matchmaking.

The platform is built to be flexible—easy to run with Docker or on your local machine—and designed for real-world usability.

## 🎯 Why ResuMatchr?

> Traditional resume filters often miss the bigger picture.  
> ResuMatchr gives you context, clarity, and confidence—whether you're hiring or applying.

- Goes beyond keyword search by analyzing **semantic meaning**.
- Explains **why** certain jobs match your resume (thanks to local LLMs).
- Provides **LLM-based suggestions** to improve your resume.
- Fast, self-hostable, and free—ideal for students, recruiters, and researchers.

---

## 🛠️ Tech Stack

| Layer            | Technology                                                                 |
|------------------|----------------------------------------------------------------------------|
| Backend          | **FastAPI** (Python)                                                       |
| Frontend         | **Streamlit** (Python)                                                     |
| Resume Parsing   | **LlamaParse** (via Unstructured API), falls back to **PyMuPDF** locally   |
| Language Model   | **LLaMA 3** via [Ollama](https://ollama.com/)                              |
| Embedding Model  | **e5-base** via Sentence Transformers                                      |
| Vector DB        | **PostgreSQL** with `pgvector` extension                                   |
| Semantic Search  | **FAISS**                                                                  |
| Containerization | **Docker** & **Docker Compose**                                            |

> 💡 Ollama must be installed and running locally for both Docker and non-Docker setups.

---

## ⚙️ Installation & Setup
### ✅ Option 1: Run with Docker (Recommended)
> **Requirements:**
> - Docker & Docker Compose
> - Ollama installed locally and running
> - LLaMA 3 pulled via: `ollama pull llama3`

#### 1️⃣ Clone the repository
```bash
$ git clone https://github.com/anupamkumarpaul2005/resu-matchr.git
$ cd resu-matchr
```
#### 2️⃣ Create a .env file in the root directory (keep the URLs same):
```
DATABASE_USER=youruser
DATABASE_PASSWORD=yourpass
DATABASE_DB=yourdb
DATABASE_URL=db:5432
FASTAPI_URL=backend:8000
OLLAMA_URL=host.docker.internal:11434
LLAMA_CLOUD_API_KEY=your_dummy_key_or_remove_if_not_needed
```
#### 3️⃣ Start Ollama serving locally:
```bash
$ ollama serve
```
#### 4️⃣ Start the project
```bash
$ docker compose up --build
```
*Access the UI at http://localhost:8501 in your browser.*

---
### 🧪 Option 2: Run Manually (Without Docker)
> **Requirements:**
> - Python 3.10+
> - PostgreSQL with pgvector enabled
> - Ollama installed locally, running on port 11434
> - LLaMA 3 model pulled via Ollama using `ollama pull llama3`

#### 1️⃣ Set up PostgreSQL database and enable pgvector.
#### 2️⃣ Clone the repository
```bash
$ git clone https://github.com/anupamkumarpaul2005/resu-matchr.git
$ cd resu-matchr
```
#### 3️⃣ Create a .env file in the root directory (keep the URLs same):
```
DATABASE_USER=youruser
DATABASE_PASSWORD=yourpass
DATABASE_DB=yourdb
DATABASE_URL=localhost:5432
FASTAPI_URL=localhost:8000
OLLAMA_URL=localhost:11434
LLAMA_CLOUD_API_KEY=your_dummy_key_or_remove_if_not_needed
```
#### 4️⃣ Start Ollama serving locally:
```bash
$ ollama serve
```
#### 5️⃣ Backend setup:
```bash
$ cd app
$ python3 -m venv venv
$ .venv\Scripts\activate
$ pip install -r requirements.txt
$ uvicorn main:app --host 0.0.0.0 --port 8000
```
#### 6️⃣ Frontend setup:
```bash
$ cd ../ui
$ pip install -r requirements.txt
$ streamlit run Home.py
```
*Access the UI at http://localhost:8501 in your browser.*

---
## 📌 Additional Notes

- 📄 **Populate Job Listings First**:  
  To get meaningful recommendations, make sure to add some job listings through the **Recruiter** page before uploading a resume.  
  If no jobs exist in the system, job matching won’t return useful results.  
  However, resume **feedback generation and role prediction will still work** independently.

- 🧠 **Fallback Parsing Behavior**:  
  The app uses [**LlamaParse**](https://llamaparse.io/) (if available) for structured and intelligent resume parsing.  
  If LlamaParse is not accessible (e.g., no API key or offline), it automatically **falls back to `PyMuPDF`** for basic text extraction.

- 📂 **Resume Format**:  
  Only **PDF resumes** are supported at this time.  
  Please ensure your resume is in PDF format and not a scanned image or Word document.

## 🔮 Future Directions
- Add user accounts and authentication for personalized experiences
- Integrate fine-tuning of the language model on domain-specific data
- Provide more detailed skill gap analytics with upskilling recommendations
- Visualize match insights with interactive dashboards
- Enable resume editing and rewriting suggestions directly in the UI
- Add notifications or alerts for new job matches or candidate applications
- Allow support for other resume formats like LaTeX, Word, scanned image


## 👨‍💻 Contributors
👤 Anupam Kumar Paul  
📌 AI/ML Enthusiast  
🔗 [LinkedIn](https://www.linkedin.com/in/anupamkumarpaul/) | [GitHub](https://github.com/anupamkumarpaul2005)

## 🤝 Contributing & Getting Involved

ResuMatchr is an open-source project with ambitious goals for the future. If you’re interested in helping build any of the planned features or have ideas for improvements, contributions are **very welcome**!

Feel free to open issues, submit pull requests, or start a discussion. Together, we can make ResuMatchr smarter, faster, and more useful for job seekers and recruiters alike.

## License
MIT License - see the [LICENSE](LICENSE) file for details.

---
### 💡 If you like this project, give it a ⭐ on GitHub!
---
