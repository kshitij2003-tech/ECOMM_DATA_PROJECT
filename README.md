# E-Commerce Data Pipeline (A-SDLC Demo)

This project demonstrates a simple analytics-focused pipeline for an e-commerce dataset using Python, SQLModel, and SQLite. It generates synthetic data, loads it into a relational database, and produces a spending leaderboard via terminal visualization.

## Install Dependencies

1. Create and activate a virtual environment (optional but recommended).
2. Install requirements:

```bash
pip install -r requirements.txt
```

## Run the Pipeline

1. **Generate** sample data files:
   ```bash
   python src/generate_data.py
   ```
2. **Ingest** the CSV files into SQLite:
   ```bash
   python src/ingest_data.py
   ```
3. **Analyze** top spenders:
   ```bash
   python src/analyze_data.py
   ```


   SAMPLE OUTPUT SCREENSHOT -
   <img width="1920" height="1080" alt="REFERENCE SCREENSHOT OF CURSOR" src="https://github.com/user-attachments/assets/d4acaed8-ceac-4165-b5bb-f9f1ef4af0b8" />


## Tech Stack

- SQLModel
- Rich
- Faker
- SQLite

## Why This Approach?

Using SQLModel provides type-safe models that map directly to database tables, reducing errors compared to raw SQL strings. Schema validation, relationships, and query construction are all handled in Python, making the pipeline easier to reason about and maintain.

