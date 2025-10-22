"""
Admin Log model for Bridge Exchange
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from database import Base

class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, nullable=False, index=True)
    action = Column(String(100), nullable=False)  # freeze_user, refund, adjust_balance, etc.
    target_user_id = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    meta = Column(JSON, nullable=True)  # Additional action data
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AdminLog(id={self.id}, admin_id={self.admin_id}, action={self.action}, target_user_id={self.target_user_id})>"
