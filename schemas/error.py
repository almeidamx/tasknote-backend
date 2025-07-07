from pydantic import BaseModel

class ErrorSchema(BaseModel):
    message: str  

class MensagemSchema(BaseModel):
    message: str
    id: int
