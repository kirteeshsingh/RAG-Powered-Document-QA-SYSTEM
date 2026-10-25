# 🤖 RAG-Powered Document Q&A System

![GitHub Repo stars](https://img.shields.io/github/stars/kirteeshsingh/RAG-Powered-Document-Q-A-System?style=social)
![GitHub forks](https://img.shields.io/github/forks/kirteeshsingh/RAG-Powered-Document-Q-A-System?style=social)
![License](https://img.shields.io/github/license/kirteeshsingh/RAG-Powered-Document-Q-A-System)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## 🎯 Project Description

This project is a **Retrieval-Augmented Generation (RAG) system** that enables users to upload PDF documents and ask intelligent, context-aware questions.

Unlike traditional chatbots, this system retrieves relevant information from documents before generating responses, ensuring **high accuracy and reduced hallucination**.

---

## 🧠 How It Works (Architecture)

```mermaid
graph TD

A[User Uploads PDF] --> B[Text Extraction]
B --> C[Chunking]
C --> D[Embeddings via Cohere]
D --> E[Store in Pinecone]

F[User Query] --> G[Convert to Embedding]
G --> H[Similarity Search in Pinecone]
H --> I[Relevant Chunks Retrieved]
I --> J[LLM Cohere]
J --> K[Final Answer to User]
````

---

## ✨ Key Features

* 📄 PDF ingestion and intelligent chunking
* 🧠 Semantic search using vector embeddings
* ⚡ Fast retrieval with Pinecone
* 💬 Context-aware answer generation

---

## 🛠️ Tech Stack

* **Backend:** Python
* **LLM & Embeddings:** Cohere
* **Vector Database:** Pinecone

---

## 📦 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/kirteeshsingh/RAG-Powered-Document-Q-A-System
cd RAG-Powered-Document-Q-A-System
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add API Keys 🔑

* Cohere → [https://cohere.com](https://cohere.com)
* Pinecone → [https://www.pinecone.io](https://www.pinecone.io)

Configure these in your application.

---

### 5️⃣ Run the App

```bash
cd src
python app.py
```

---

## 📁 Project Structure

```bash
.
├── src/
│   ├── app.py
│   ├── vectorstore.py
│   ├── chatbot.py
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚧 Future Enhancements

* 🌍 Multi-language document support
* 📚 Multi-document querying
* ☁️ Cloud deployment (AWS/GCP)
* 💾 Chat history export
* 🔄 Support for multiple vector databases

---

## 🤝 Contributing

```bash
git checkout -b feature-name
git commit -m "Added feature"
git push origin feature-name
```

Open a Pull Request 🚀

---

## 📜 License

Apache License

---

## 👨‍💻 Author

**Kirteesh Akhil Singh**
B.Tech CSE | DevOps Enthusiast

---

## ⭐ Support

If you like this project:

👉 Give it a ⭐ on GitHub
👉 Share it with others
