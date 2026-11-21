from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from app.database import engine, SessionLocal, Base
from app.models import Lead
from app.schemas import LeadCreate, LeadResponse, LeadStatusUpdate

app = FastAPI(title="LeadFlow AI")

Base.metadata.create_all(bind=engine)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
def home():
    return {"message": "LeadFlow AI Running"}


# 1. Create a lead
@app.post("/api/v1/leads", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):

    existing_lead = db.query(Lead).filter(
        Lead.email == lead.email
    ).first()

    if existing_lead:
        raise HTTPException(
            status_code=409,
            detail="This email already exists"
        )

    new_lead = Lead(**lead.model_dump())

    try:
        db.add(new_lead)
        db.commit()
        db.refresh(new_lead)

        return new_lead

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Lead already exists"
        )




# 2. Retrieve all leads
@app.get("/api/v1/leads", response_model=list[LeadResponse])
def get_leads(db: Session = Depends(get_db)):

    return db.query(Lead).all()



# 4. Count leads
@app.get("/api/v1/leads/count")
def count_leads(db: Session = Depends(get_db)):

    total = db.query(Lead).count()

    return {"total_leads": total}


# 3. Retrieve lead by ID
@app.get("/api/v1/leads/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):

    lead = db.query(Lead).filter(
        Lead.id == lead_id
    ).first()

    if not lead:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return lead

@app.put("/api/v1/leads/{lead_id}", response_model=LeadResponse)
def update_lead_status(
    lead_id: int,
    lead_update: LeadStatusUpdate,
    db: Session = Depends(get_db)
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()

    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.status = lead_update.status

    db.commit()
    db.refresh(lead)

    return lead
