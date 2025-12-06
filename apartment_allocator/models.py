from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    budget = Column(Float, nullable=False)
    preferences = Column(String(200))
    
    units = relationship("Unit", back_populates="customer")
    

    
    @classmethod
    def create(cls, session, name, budget, preferences=None):
        if not name or len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        if budget <= 0:
            raise ValueError("Budget must be positive")
        
        customer = cls(name=name.strip(), budget=budget, preferences=preferences)
        session.add(customer)
        session.commit()
        return customer
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, customer_id):
        return session.query(cls).filter(cls.id == customer_id).first()
    
    def delete(self, session):
        session.delete(self)
        session.commit()
    


class Unit(Base):
    __tablename__ = 'units'
    
    id = Column(Integer, primary_key=True)
    unit_number = Column(String(20), nullable=False, unique=True)
    floor = Column(Integer, nullable=False)
    unit_type = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(20), default='Available')
    customer_id = Column(Integer, ForeignKey('customers.id'))
    
    customer = relationship("Customer", back_populates="units")
    

    
    @property
    def is_available(self):
        return self.status == 'Available'
    
    @classmethod
    def create(cls, session, unit_number, floor, unit_type, price):
        if not unit_number or len(unit_number.strip()) == 0:
            raise ValueError("Unit number cannot be empty")
        if floor < 1:
            raise ValueError("Floor must be positive")
        if price <= 0:
            raise ValueError("Price must be positive")
        
        existing = session.query(cls).filter(cls.unit_number == unit_number.strip()).first()
        if existing:
            raise ValueError(f"Unit {unit_number} already exists")
        
        unit = cls(unit_number=unit_number.strip(), floor=floor, unit_type=unit_type, price=price)
        session.add(unit)
        session.commit()
        return unit
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, unit_id):
        return session.query(cls).filter(cls.id == unit_id).first()
    
    @classmethod
    def find_by_unit_number(cls, session, unit_number):
        return session.query(cls).filter(cls.unit_number == unit_number).first()
    
    def allocate_to_customer(self, session, customer):
        if not self.is_available:
            raise ValueError("Unit is not available")
        if customer.budget < self.price:
            raise ValueError("Customer budget insufficient")
        
        self.customer_id = customer.id
        self.status = 'Allocated'
        session.commit()
    
    def delete(self, session):
        session.delete(self)
        session.commit()
    
