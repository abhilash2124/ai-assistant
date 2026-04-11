# 🚀 RAG-based AI System (Qdrant + Groq)

## 📌 Overview

This project is a basic implementation of a **Retrieval-Augmented Generation (RAG)** system.

It demonstrates how to combine:

* Embeddings
* Vector Database
* LLM (Large Language Model)

to build an AI system that can **understand and answer questions based on given data**.

---

## 🧠 What I Learned

* How to convert text into embeddings using Sentence Transformers
* How to store and search embeddings using Qdrant (vector database)
* How semantic search works (meaning-based search, not keyword-based)
* How to connect retrieved data with an LLM using Groq API
* Basics of prompt engineering to control AI responses

---

## ⚙️ Tech Stack

* Python
* Qdrant (Vector Database)
* Sentence Transformers (Embeddings)
* Groq API (LLM - LLaMA 3.1)

---

## 🔄 How It Works

1. Convert text into embeddings
2. Store embeddings in Qdrant
3. Convert user query into embedding
4. Retrieve similar data using semantic search
5. Send retrieved context to LLM
6. Generate final answer

---

## 🧪 Example Flow

**Input:**

```
coding is fun
```

**Retrieved Context:**

```
I love coding  
I enjoy programming
```

**AI Output:**

```
The statement aligns with the context as coding and programming are associated with enjoyment.
```

---

## 🚀 Current Status

* Basic RAG pipeline implemented
* Semantic search working
* LLM integration completed

---

## 🔜 Next Steps

* Use real data (PDF / Resume)
* Build API using FastAPI
* Add frontend (React)
* Extend to AI Agent system

---

## ⚠️ Note

API keys are stored securely using environment variables (.env file) and are not included in the repository.

---
