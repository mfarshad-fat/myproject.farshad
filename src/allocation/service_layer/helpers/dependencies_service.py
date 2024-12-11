from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.allocation.adapters.connector.postgres import get_db
from src.allocation.service_layer.helpers.jwt_auth import get_current_user
from src.allocation.domain.entities import TokenData

class DependencyService:
    def __init__(self, request: Request, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
        self.request = request
        self.db = db
        self.current_user = current_user
