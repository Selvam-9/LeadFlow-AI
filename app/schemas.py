from pydantic import BaseModel, EmailStr, ConfigDict
from app.models import LeadStatus


class LeadStatusUpdate(BaseModel):
    status: LeadStatus

class LeadCreate(BaseModel):

    first_name : str
    email : EmailStr
    phone : str | None=None
    country : str | None=None
    course : str | None=None

class LeadResponse(BaseModel):
    id : int
    first_name : str
    email : EmailStr
    phone : str | None
    country : str | None
    course : str | None
    status : str



model_config = ConfigDict(from_attributes=True)
