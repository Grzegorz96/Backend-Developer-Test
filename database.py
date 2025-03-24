from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL
DATABASE_URL = "mysql+mysqlconnector://login:password@localhost/dbname"


# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our classes definitions
Base = declarative_base()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    # Test the connection
    with engine.connect() as connection:
        print("Połączenie z bazą danych MySQL udało się!")
except Exception as e:
    print(f"Połączenie nie powiodło się: {e}")
