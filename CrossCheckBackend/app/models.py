from app import db
import sqlalchemy.orm as so
import sqlalchemy as sa
from datetime import datetime

class User(db.Model):
    user_id: so.Mapped[int] = so.mapped_column(primary_key=True, index=True)
    name: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    username: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    password: so.Mapped[str] = so.mapped_column(nullable=False, index=True)
    role: so.Mapped[str] = so.mapped_column(nullable=False, index=True)

class HealthRecord(db.Model):
    record_id: so.Mapped[int] = so.mapped_column(primary_key=True, nullable=False, index=True)
    patient_id: so.Mapped[int] = so.mapped_column(unique=True, nullable=False, index=True)
    date: so.Mapped[datetime] = so.mapped_column(sa.DATE, nullable=False, index=True)
    status: so.Mapped[str] = so.mapped_column(nullable=False, index=True)


