import json
prompt = """
You are a career assistant. Given the user's resume and a job description, do the following:

1. Rate how well the resume matches the job (0 to 100).
2. List any critical missing skills.
3. Give feedback on how to improve for this role.

RESUME:
Anupam Sharma  
Email: anupam.sharma@email.com | Phone: +91-98XXXXXXX  
LinkedIn: linkedin.com/in/anupam-sharma | GitHub: github.com/anupam-sharma  

EDUCATION  
Indian Institute of Information Technology Guwahati (IIITG)  
B.Tech in Computer Science and Engineering, 2022 – Present  
Relevant Courses: Machine Learning, Data Structures, Algorithms, Operating Systems  

SKILLS  
Languages: Python, Java, C, SQL  
Libraries: scikit-learn, TensorFlow, PyTorch, CatBoost, XGBoost, Pandas, NumPy  
Tools: Git, Docker, FastAPI, Firebase, Android Studio, Linux, FAISS, OpenCV  
Concepts: Machine Learning, Deep Learning, NLP, Computer Vision, MLOps  

PROJECTS  

AI Resume Matcher & Optimizer – FastAPI, FAISS, LLMs  
- Developed a web app that parses resumes, matches with job descriptions using vector search (FAISS)  
- Integrated LLM-based feedback system using Ollama for resume improvement suggestions  

Skin Disease Classifier – TensorFlow, CNN  
- Built and trained a deep CNN model to classify 5 common skin conditions with 85% accuracy  

Music-to-Song Search Tool – Python, librosa  
- Implemented a melody-based audio search prototype using signal processing and cosine similarity  

EXPERIENCE  
Open Source Contributor – Various Projects  
- Contributed bug fixes and documentation to ML repos on GitHub  

ACHIEVEMENTS  
- Secured top 5% in Kaggle Playground Series  
- Completed DeepLearning.AI Specialization (3/5 courses)  

JOB:
AI Engineer Intern  
We are looking for an AI Engineer Intern to assist in building scalable machine learning pipelines and production-level APIs.
The role involves working with LLMs, embedding-based retrieval, model deployment, and fast prototyping of AI tools.  
Python, TensorFlow, PyTorch, Transformers, FastAPI, Docker, MLOps  
Internship  
Artificial Intelligence  
LLMs, vector search, resume matching, backend, GitHub portfolio, Deep Learning

Return your answer as strict JSON. Do not include any text outside the JSON.
Return a JSON like:
{
  "llm_score": ...,
  "missing_skills": [...],
  "feedback": "..."
}
"""
print(json.dumps({"prompt": prompt}))

response="Here is my response in JSON format:\n\n{\n  \"llm_score\": 85,\n  \"missing_skills\": [\"Transformers\"],\n  \"feedback\": \"To improve for this role, Anupam should focus on building more experience with LLMs and embedding-based retrieval. Additionally, they could expand their GitHub portfolio to include more projects showcasing their AI engineering skills.\"\n}"
output = response.strip()
start = output.find('{')
end = output.rfind('}') + 1
json_part = output[start:end]
#print(json.loads(json_part))
