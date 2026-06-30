<div align="center">

# 🩺 Patient-Centric Dashboard

**A full-stack healthcare analytics platform that turns raw patient data into a clear, visual story.**

Built to help non-technical users — patients and clinicians alike — understand vitals, trends, and risk at a glance.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey)](#-license)

</div>

---

## 📖 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Dashboard Walkthrough](#-dashboard-walkthrough)
- [API Endpoints](#-api-endpoints)
- [Team](#-team)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## 🩻 About the Project

The **Patient-Centric Dashboard** is a full-stack healthcare analytics application designed to give patients an easy-to-understand view of their health records, vital signs, and clinical analytics — without needing to interpret raw lab data themselves.

It was developed as part of the **Patient-Centric Dashboard** initiative, with a focus on simplifying healthcare data visualization for non-technical, everyday users.

The system is split into two independent layers:

- A **FastAPI backend** that handles data access, analytics, and risk computation.
- A **Streamlit frontend** that turns that data into an interactive, visual dashboard.

---

## ✨ Features

| Category | Capabilities |
|---|---|
| 🔐 **Access** | Secure patient dashboard, patient lookup |
| 📊 **Analytics** | Clinical risk assessment, trend analysis, health score gauge |
| 📈 **Visualization** | Interactive Plotly charts, blood glucose trend visualization |
| ❤️ **Vitals** | Latest vital signs, patient health summary |
| 🧮 **Comparison** | Reference population comparison |
| 💻 **Experience** | Responsive Streamlit interface, CSV export |
| ⚙️ **Backend** | FastAPI REST API, PostgreSQL (Supabase) database |

---

## 🛠 Technology Stack

<table>
<tr>
<td valign="top" width="33%">

**Frontend**
- Streamlit
- Plotly
- Pandas

</td>
<td valign="top" width="33%">

**Backend**
- FastAPI
- SQLAlchemy
- PostgreSQL
- Supabase

</td>
<td valign="top" width="33%">

**Language**
- Python 3.10+

</td>
</tr>
</table>

---

## 📂 Project Structure

```
patient-health-dashboard/
│
├── backend/
│   ├── analytics/          # Risk scoring, trend & anomaly logic
│   ├── api/                # FastAPI route definitions
│   ├── models/              # ORM / data models
│   ├── repository/          # Database access layer
│   ├── services/             # Business logic
│   ├── utils/                 # Shared helpers
│   ├── config.py             # App configuration
│   ├── database.py           # DB connection/session setup
│   ├── main.py                # FastAPI app entrypoint
│   └── requirements.txt
│
├── frontend/
│   ├── assets/               # Static assets (images, icons)
│   ├── api.py                 # Backend API client
│   ├── streamlit_app.py       # Streamlit app entrypoint
│   └── utils.py                # Frontend helpers
│
├── data/                       # Sample / seed data
├── notebooks/                   # Exploratory analysis notebooks
├── saved_models/                 # Trained model artifacts
├── tests/                         # Unit & integration tests
└── README.md
```

---

##  Getting Started

### Prerequisites

- Python 3.10 or higher
- pip
- A PostgreSQL database (Supabase recommended)
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/<your-repository-link>.git
cd patient-health-dashboard
```

---

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=your_database_connection_string
```

Run the backend server:

```bash
uvicorn backend.main:app --reload
```

| Resource | URL |
|---|---|
| API base | `http://127.0.0.1:8000` |
| Swagger docs | `http://127.0.0.1:8000/docs` |

---

### Frontend Setup

Open a new terminal:

```bash
cd frontend
pip install streamlit requests pandas plotly
streamlit run streamlit_app.py
```

The dashboard will be available at:

```
http://localhost:8501
```

> 💡 **Tip:** Run the backend first — the frontend will display a connection status indicator and won't load patient data until the API is reachable.

---

## 🖥 Dashboard Walkthrough

| Section | What it shows |
|---|---|
| **Patient Login** | Search and load a patient by ID |
| **Patient Information** | Age, gender, and identifying details |
| **Latest Vitals** | Most recent readings (glucose, BMI, blood pressure, etc.) |
| **Clinical Summary** | Plain-language summary of the patient's current status |
| **Health Score** | Single 0–100 indicator combining risk, trend, and anomalies |
| **Risk Classification** | Low / Medium / High risk banding |
| **Trend Analysis** | Direction of change across recent readings |
| **Glucose Trend Chart** | Interactive time-series of blood glucose |
| **Population Comparison** | Patient values vs. reference population |
| **CSV Download** | Export the current vitals snapshot |

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Root / API status |
| `/health` | GET | Health check |
| `/patients` | GET | List all patients |
| `/patients/{patient_id}` | GET | Patient summary |
| `/patients/{patient_id}/analytics` | GET | Patient analytics (risk, trend, anomalies) |
| `/dashboard/{patient_id}` | GET | Complete dashboard payload (overview + analytics + history) |

Full interactive documentation is available via Swagger at `/docs` once the backend is running.

---

## 👥 Team

**MedTech Innovators**

| Name |
|---|
| Asna S B |
| Shreya B |
| Dana Arif M A |

---

## 🔭 Future Enhancements

- 🤖 AI-powered health recommendations
- 🔮 Predictive risk analysis
- 📄 PDF medical report generation
- 📅 Appointment integration
- 🔑 Multi-user authentication
- 🩺 Doctor-facing dashboard
- 🏥 Electronic Health Record (EHR) integration

---

## 📜 License

This project was developed for **academic purposes** as part of a healthcare analytics initiative.

---

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [Supabase](https://supabase.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

<div align="center">

Made with ❤️ by **MedTech Innovators**

</div>
