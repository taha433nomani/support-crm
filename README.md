##Support CRM System

##Tech Stack

* FastAPI
* SQLite
* SQLAlchemy ORM
* Jinja2
* HTML/CSS
* Bootstrap

##Features

* Create Tickets
* View All Tickets
* Search Tickets
* Filter Tickets by Status
* View Ticket Details
* Edit Tickets
* Update Ticket Status (Open, In Progress, Closed)

##Local Setup Instructions

##1. Clone the Repository

git clone https://github.com/taha433nomani/support-crm.git

##2. Open Project in VS Code

cd support-crm
code .

##3. Create Virtual Environment

python -m venv venv

##4. Activate Virtual Environment

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

##5. Install Dependencies

pip install -r requirements.txt

##6. Run the Application

uvicorn main:app --reload

##7. Open in Browser

http://127.0.0.1:8000

The application will now be running locally.

##Project Structure

support-crm/
│
├── main.py
├── models.py
├── database.py
├── requirements.txt
├── support_crm.db
│
└── templates/

##Deployment

The application is deployed on Render.
## Live Demo

 https://support-crm-f55p.onrender.com/
