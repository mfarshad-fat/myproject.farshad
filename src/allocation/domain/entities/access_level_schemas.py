from pydantic import BaseModel

class AcceclevelBase(BaseModel) :
    accec_name : str

class Acceclevelread(AcceclevelBase) :
    accec_id : str
    class config:
        orm_mode = True