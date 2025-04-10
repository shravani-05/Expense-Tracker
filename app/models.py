from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String)
    email = Column(String, unique=True)

    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    amount = Column(Float)
    date = Column(Date)
    user_email = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # ✅ this line requires users.id

    user = relationship("User", back_populates="expenses")


class Budget(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    amount = Column(Float)
    month = Column(String)
    user_email = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="budgets")
