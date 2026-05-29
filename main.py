from fastapi import FastAPI, Form
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi.responses import HTMLResponse, RedirectResponse

from database import engine, Base, SessionLocal
from models import Ticket

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
def home(search: str = "", status: str = ""):
    db: Session = SessionLocal()

    query = db.query(Ticket)

    # Search
    if search:
        query = query.filter(
            or_(
                Ticket.ticket_id.contains(search),
                Ticket.customer_name.contains(search),
                Ticket.customer_email.contains(search),
                Ticket.subject.contains(search),
                Ticket.description.contains(search)
            )
        )

    # Filter by status
    if status:
        query = query.filter(
            Ticket.status == status
        )

    tickets = query.all()

    result = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<div class="container mt-4">

<h1 class="mb-4">Support CRM</h1>

<a href="/create">
    <button class="btn btn-primary mb-3">
        Create New Ticket
    </button>
</a>

<h2>All Tickets</h2>

<form method="get" action="/" class="mb-3">
    <input type="text"
           name="search"
           placeholder="Search tickets">

    <button type="submit" class="btn btn-success">
        Search
    </button>
</form>

<a href="/?status=Open">
    <button class="btn btn-outline-primary">
        Open Tickets
    </button>
</a>

<a href="/?status=In Progress">
    <button class="btn btn-outline-warning">
        In Progress
    </button>
</a>

<a href="/?status=Closed">
    <button class="btn btn-outline-danger">
        Closed Tickets
    </button>
</a>

<a href="/">
    <button class="btn btn-outline-secondary">
        All Tickets
    </button>
</a>

<br><br>
"""

    if len(tickets) == 0:
        result += "<p>No tickets found.</p>"

    for ticket in tickets:
        result += f"""
        <div class="card mb-3">
            <div class="card-body">

                <h3>
                    <a href="/ticket/{ticket.ticket_id}">
                        {ticket.subject}
                    </a>
                </h3>

                <p><strong>Ticket ID:</strong> {ticket.ticket_id}</p>

                <p><strong>Customer:</strong> {ticket.customer_name}</p>

                <p><strong>Email:</strong> {ticket.customer_email}</p>

                <p>{ticket.description}</p>

                <p>
                    <strong>Status:</strong>
                    {ticket.status}
                </p>

                <p>
                    <strong>Created:</strong>
                    {ticket.created_at}
                </p>
<a href="/edit-ticket/{ticket.ticket_id}">
    <button class="btn btn-primary">
        Edit Ticket
    </button>
</a>

<br><br>
                <form method="post"
                      action="/close-ticket/{ticket.ticket_id}">
                    <button class="btn btn-danger"
                            type="submit">
                        Close Ticket
                    </button>
                </form>

                <br>

                <form method="post"
                      action="/progress-ticket/{ticket.ticket_id}">
                    <button class="btn btn-warning"
                            type="submit">
                        Mark In Progress
                    </button>
                </form>

            </div>
        </div>
        """

    db.close()
    return result


@app.get("/ticket/{ticket_id}", response_class=HTMLResponse)
def ticket_detail(ticket_id: int):

    db = SessionLocal()

    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        db.close()
        return "<h2>Ticket Not Found</h2>"

    result = f"""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<div class="container mt-4">

    <h1>{ticket.subject}</h1>

    <p><strong>Ticket ID:</strong> {ticket.ticket_id}</p>

    <p><strong>Customer:</strong> {ticket.customer_name}</p>

    <p><strong>Email:</strong> {ticket.customer_email}</p>

    <p><strong>Description:</strong></p>

    <p>{ticket.description}</p>

    <p><strong>Status:</strong> {ticket.status}</p>

    <p><strong>Created:</strong> {ticket.created_at}</p>

    <a href="/">
        <button class="btn btn-secondary">
            Back
        </button>
    </a>

</div>
"""

    db.close()
    return result
@app.get("/create", response_class=HTMLResponse)
def create_form():
    return """
    <h2>Create Ticket</h2>

    <form method="post" action="/create">

        <input type="text"
               name="customer_name"
               placeholder="Customer Name">

        <br><br>

        <input type="email"
               name="customer_email"
               placeholder="Customer Email">

        <br><br>

        <input type="text"
               name="subject"
               placeholder="Subject">

        <br><br>

        <textarea name="description"
                  placeholder="Ticket Description"></textarea>

        <br><br>

        <button type="submit">
            Create Ticket
        </button>

    </form>
    """
@app.post("/create")
def create_ticket(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...)
):
    db = SessionLocal()

    ticket = Ticket(
        customer_name=customer_name,
        customer_email=customer_email,
        subject=subject,
        description=description
    )

    db.add(ticket)
    db.commit()

    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )
@app.get("/edit-ticket/{ticket_id}", response_class=HTMLResponse)
def edit_ticket_form(ticket_id: int):

    db = SessionLocal()

    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        db.close()
        return "<h2>Ticket Not Found</h2>"

    result = f"""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<div class="container mt-4">

<h2>Edit Ticket</h2>

<form method="post" action="/edit-ticket/{ticket.ticket_id}">

<label>Customer Name</label>
<input type="text"
       class="form-control"
       name="customer_name"
       value="{ticket.customer_name}">

<br>

<label>Customer Email</label>
<input type="email"
       class="form-control"
       name="customer_email"
       value="{ticket.customer_email}">

<br>

<label>Subject</label>
<input type="text"
       class="form-control"
       name="subject"
       value="{ticket.subject}">

<br>

<label>Description</label>
<textarea class="form-control"
          name="description"
          rows="5">{ticket.description}</textarea>

<br>

<button class="btn btn-success"
        type="submit">
    Update Ticket
</button>

<a href="/">
    <button type="button"
            class="btn btn-secondary">
        Cancel
    </button>
</a>

</form>

</div>
"""

    db.close()

    return result


@app.post("/edit-ticket/{ticket_id}")
def update_ticket(
    ticket_id: int,
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...)
):

    db = SessionLocal()

    ticket = db.query(Ticket).filter(
        Ticket.ticket_id == ticket_id
    ).first()

    if ticket:

        ticket.customer_name = customer_name
        ticket.customer_email = customer_email
        ticket.subject = subject
        ticket.description = description

        db.commit()

    db.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )