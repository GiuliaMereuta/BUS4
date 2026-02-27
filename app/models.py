from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime

class User(db.Model):
    user_id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    first_name: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    last_name: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    email: so.Mapped[str] = so.mapped_column(unique=True, nullable=False, index=True)
    password: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    role: so.Mapped[str] = so.mapped_column(nullable=False, index=True)

    def __repr__(self):
        return f'<Login {self.user_id}, {self.last_name}, {self.first_name}, {self.email}, {self.role}>'

class HealthRecord(db.Model):
    record_id: so.Mapped[int] = so.mapped_column(primary_key=True, nullable=False, index=True)
    patient_id: so.Mapped[int] = so.mapped_column(unique=True, nullable=False, index=True)
    date: so.Mapped[datetime] = so.mapped_column(sa.DATE, nullable=False, index=True)
    status: so.Mapped[str] = so.mapped_column(nullable=False, index=True)


