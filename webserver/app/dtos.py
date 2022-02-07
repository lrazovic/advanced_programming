from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: Optional[int]
    
    email: str
    name: Optional[str]
    access_token: Optional[str]
    refresh_token: Optional[str]