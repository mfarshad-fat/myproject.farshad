from sqlalchemy.orm import Session
from src.allocation.adapters.models import Userjwt

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str) -> Userjwt:
        """
        جستجوی کاربر بر اساس نام کاربری
        """
        return self.db.query(Userjwt).filter(Userjwt.username == username).first()

    def set_user_logged_out(self, username: str) -> bool:
        """
        به‌روزرسانی وضعیت کاربر به 'logged out'
        """
        user = self.get_user_by_username(username)
        if not user:
            return False
        user.is_logged_out = True
        self.db.commit()
        return True
