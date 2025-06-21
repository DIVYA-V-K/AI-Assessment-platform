# AI-Based Assessment System

This project presents an intelligent assessment platform that automates question generation, intelligent answer evaluation, plagiarism detection, and secure proctoring using modern NLP and deep learning techniques. It aims to transform how subjective and coding assessments are created, evaluated, and delivered—ideal for EdTech, campus recruitment, and adaptive learning.

---

## Features

- ✅ Automatic question generation (topic or PDF-based) using FLAN-T5
- ✅ Intelligent answer evaluation with LLM-as-a-Judge and semantic similarity
- ✅ Structured, detailed feedback
- ✅ Plagiarism detection using Sentence Transformers
- ✅ Proctoring: tab-switch & browser monitoring
- ✅ Code editor for programming-based answers
- ✅ Clean, multi-page Streamlit interface

---

##  Project Structure

```
AI-ASSESSMENT-COPY/
├── app.py                    # Main Streamlit app
├── main.py                   # CLI test for the evaluation pipeline
├── ai_expert_panel.py        # LLM-based feedback module
├── answer_classifier.py      # Ideal answer & similarity scoring
├── evaluator.py              # Core evaluation engine
├── curriculum_mapping.py     # Maps Q&A to topics
├── pdf_processor.py          # PDF text extraction
├── plagiarism_checker.py     # Embedding-based plagiarism check
├── proctoring.py             # JS-based tab switching detection
├── question_generator.py     # FLAN-T5-based question generation
├── serpapi_search.py         # Google SERP API integration
├── auth.py                   # (Optional) Authentication logic
├── pages/                    # Streamlit multi-page views
├── .env                      # API keys & environment variables
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignored files in version control
├── assets/, share/, bin/     # Resources, temp data, virtualenv (optional)
```

---

##  Technologies Used

- **Frontend**: Streamlit
- **Backend Models**: Hugging Face Transformers (FLAN-T5, SentenceTransformer)
- **Plagiarism**: all-mpnet-base-v2 embeddings
- **Code Editor**: `streamlit-ace`
- **Search**: SERP API
- **Proctoring**: JavaScript event tracking
- **Language**: Python 3.10+

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ai-assessment-copy.git
cd ai-assessment-copy
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file and add your API keys:

```env
OPENAI_API_KEY=your_openai_key
SERPAPI_KEY=your_serpapi_key
```

5. **Run the Streamlit app**

```bash
streamlit run app.py
```

---

##  Sample Program Execution

- Navigate to the `app.py` homepage.
- Choose to:
  - Enter a **topic** or upload a **PDF**
  - Click **Generate Questions**
- Answer questions in text or code editor
- The system will:
  - Generate **ideal answers**
  - Use LLM to **evaluate your responses**
  - Check **plagiarism**
  - Show **detailed feedback & scores**

---

## 📊 Optional: Test via CLI

You can test the core evaluation pipeline manually using:

```bash
python main.py
```

This runs a question, your answer, and prints the ideal answer, similarity, and LLM feedback directly.

---

##  Deployment

- ✅ Local (default)
- 🔜 Streamlit Cloud / Hugging Face Spaces (ready to extend)
- 🔐 Supports modular API deployment via FastAPI (future enhancement)

---

##  Future Enhancements

- Code execution & grading
- Adaptive learning via Reinforcement Learning
- MongoDB integration for user analytics
- User login + performance dashboards
- RAG + FAISS-based question recommendations

---

##  Contributing

We welcome contributions! Please fork the repo and submit a pull request. For major changes, open an issue first to discuss your idea.

---

## 📄License

MIT License. See `LICENSE` file for more details.

---

## Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [SentenceTransformers](https://www.sbert.net/)
- [Streamlit](https://streamlit.io/)
- [SERP API](https://serpapi.com/)
- [Google FLAN-T5](https://huggingface.co/google/flan-t5-large)

---

 *Built for modern AI-powered education and assessment.*
