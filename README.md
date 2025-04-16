# 🗓️ Appointment Booking App

This is a simple full-stack web app for booking appointments, built with **FastAPI** on the backend and plain **HTML/CSS/JS** on the frontend. It's deployed on **Azure App Service**, and everything is automated using **GitHub Actions**.

---

## ✨ What It Does

- Lets users book appointments with their name, email, and preferred date/time.
- Stores appointment data in an Azure SQL database.
- Backend built using FastAPI (async and fast 🚀)
- CI/CD pipeline using GitHub Actions to deploy every push to `main`
- Hosted on Azure with Gunicorn + Uvicorn for production

---

## 🛠 Tech Used

- **FastAPI** (Python 3.11)
- **HTML/CSS/JavaScript**
- **Azure App Service (Linux)** for deployment
- **Azure SQL Database** (with SQLAlchemy + pyodbc)
- **GitHub Actions** for CI/CD
- **Gunicorn** with Uvicorn workers (for async ASGI)

---

## 🧱 Folder Structure
 ├── main.py # FastAPI app entry ├── models.py # Database + schema models ├── database.py # SQLAlchemy engine setup ├── static/ │ ├── index.html # UI │ ├── style.css # Styling │ └── script.js # JS logic ├── requirements.txt # Python dependencies └── .github/ └── workflows/ └── deploy.yml # CI/CD pipeline config
﻿
---

## 🚀 How It Deploys

This project uses GitHub Actions to zip the app and push it to Azure every time you push to the `main` branch.

Make sure this is the **startup command** in Azure:

```bash
gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0


---

Let me know if you want me to drop this into your repo automatically or help link your live site!
