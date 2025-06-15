# AidAgent — Crisis Response on Autopilot

AidAgent is an intelligent crisis response platform designed to automate and streamline disaster management and humanitarian aid coordination. Leveraging AI-driven alerts, user-generated help requests, donation tracking, and community discussion forms, AidAgent aims to accelerate response times and enhance collaboration during crises.

---

## Features

* **User**: Register and manage users with wallet-based identities.
* **Alerts**: Receive and update real-time crisis alerts with detailed resources like food, shelter, and helpline information.
* **Help Requests**: Submit and track help requests linked to alerts.
* **Donations**: Track crypto and fiat donations related to specific requests or alerts.
* **Charities**: Manage charity organizations connected to alerts.
* **Discussion Forms**: Enable community members to discuss and coordinate aid efforts through message boards linked to alerts.
* **AI Integration**: Use AI to fetch and update alert details automatically.

---

## Tech Stack

* **Backend**: FastAPI, Python 3.9+
* **Database**: MongoDB with Beanie ODM
* **AI Integration**: AI LLM and Livefeed
* **Async HTTP Client**: `httpx` or native async support
* **Deployment**: Uvicorn ASGI server

---

## Project Structure

* `models/` — Beanie Document models for User, Alert, Donation, Charity, Form, etc.
* `schemas/` — Pydantic schemas for request validation and response models
* `services/` — Async service modules handling CRUD operations and business logic
* `routes/` — FastAPI routers for API endpoints
* `app.py` — FastAPI app initialization and router registration
* `config/` — Database and external API configuration and initialization

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/aidagent.git
cd aidagent
```

2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set environment variables

```bash
export MONGODB_URI="your-mongodb-connection-string"
```

5. Run the app

```bash
uvicorn app:app --reload
```

---

## Usage

* API is available at `http://localhost:8000/`
* Access endpoints like:

  * `/users/` — Manage users
  * `/alerts/` — View and update crisis alerts
  * `/donations/` — Track donations
  * `/charities/` — Manage charity organizations
  * `/forms/alert/{alert_id}` — View or post messages in discussion forms

Refer to the API docs at `http://localhost:8000/docs` for interactive exploration.

---
## License

MIT License © 2025 Your Name or Organization
