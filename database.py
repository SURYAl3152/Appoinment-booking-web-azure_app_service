from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Azure SQL Server connection string
DATABASE_URL = (
    "mssql+pyodbc://surya:Admin%40123@appionmentdb.database.windows.net:1433/"
    "Appionmentdb?driver=ODBC+Driver+18+for+SQL+Server&Encrypt=yes&"
    "TrustServerCertificate=no&Connection+Timeout=30"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
