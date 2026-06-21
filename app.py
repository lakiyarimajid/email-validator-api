from fastapi import FastAPI
from pydantic import BaseModel
import dns.resolver
import re
import uvicorn

app = FastAPI()

def is_valid_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

DISPOSABLE = {'tempmail.com', 'mailinator.com', 'yopmail.com', '10minutemail.com'}

def check_email(email):
    if not is_valid_format(email):
        return {"email": email, "valid": False, "reason": "Invalid email format"}
    
    domain = email.split('@')[1]
    
    if domain in DISPOSABLE:
        return {"email": email, "valid": False, "reason": "Disposable email"}
    
    try:
        dns.resolver.resolve(domain, 'MX')
        return {"email": email, "valid": True, "reason": "Valid email"}
    except:
        return {"email": email, "valid": False, "reason": "Invalid domain"}

class EmailInput(BaseModel):
    email: str

@app.post("/validate")
async def validate(data: EmailInput):
    return check_email(data.email)

@app.get("/")
async def home():
    return {"message": "Email Validator API", "docs": "/docs"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
