# 🏦 SEC Financial Data Lakehouse & RAG Pipeline

**An end-to-end Big Data project that ingests unstructured SEC 10-K filings, processes them with Apache Spark, and powers an AI-driven financial analysis dashboard.**

> **Status:** ✅ Complete | **Tech Stack:** Docker, Spark, MinIO, DuckDB, Streamlit, Google Gemini
---

## 🚀 How It Works
This project implements a modern **"Lakehouse"** architecture to solve the problem of analyzing messy legal documents.

1.  **Ingest:** A Python script fetches raw 10-K HTML reports from the **SEC EDGAR Archives**.
2.  **Store:** Raw files are saved to **MinIO** (S3-compatible object storage).
3.  **Process:** **Apache Spark** reads the HTML, cleans tags, **redacts PII** (emails/phones), and chunks text for AI.
4.  **Analyze:** **DuckDB** queries the processed Parquet files in milliseconds.
5.  **Intelligence (RAG):** **Google Gemini Pro** acts as a reasoning engine, answering user questions based *only* on the retrieved financial data.

<img width="680" height="700" alt="RAG pipline flow" src="https://github.com/user-attachments/assets/7f013a41-eb6d-411a-b222-1d784ad775dd" />

## 🛠️ Tech Stack
* **Infrastructure:** Docker & Docker Compose
* **Storage:** MinIO (Object Storage)
* **Processing:** Apache Spark (PySpark)
* **Query Engine:** DuckDB (OLAP)
* **UI/Visualization:** Streamlit
* **GenAI Model:** gemini-2.5-flash

---

## 📸 Project Snapshots

StreamLit Dashboard:
<img width="1919" height="938" alt="Screenshot 2026-01-25 133806" src="https://github.com/user-attachments/assets/d6574dae-ad73-428e-a0ee-2933f4cff26a" />

<img width="1917" height="946" alt="Screenshot 2026-01-25 133651" src="https://github.com/user-attachments/assets/6be023a4-6c71-4052-a008-1e375c43c776" />

<img width="1919" height="939" alt="Screenshot 2026-01-25 133715" src="https://github.com/user-attachments/assets/a2657979-67e6-4995-a815-c9001976ed85" />

<img width="940" height="460" alt="image" src="https://github.com/user-attachments/assets/aceb0040-966f-40f0-9a1c-fbdc5c455e24" />

MinIO HomePage:
<img width="1919" height="962" alt="Screenshot 2026-01-25 134823" src="https://github.com/user-attachments/assets/02194b67-9a8b-41d9-a9a4-a411a53fe656" />

Apache Spark:
<img width="1919" height="972" alt="Screenshot 2026-01-25 143551" src="https://github.com/user-attachments/assets/a916791a-3f6c-44a7-8985-068a530ef93a" />



---

## ⚡ Quick Start

**1. Prerequisites**
* Docker Desktop installed
* Python 3.9+ installed

**2. Setup Infrastructure**
```bash
git clone [https://github.com/aniketsingh15/compliance-llm-pipeline.git](https://github.com/aniketsingh15/compliance-llm-pipeline.git)
cd compliance-llm-pipeline
docker-compose up -d
