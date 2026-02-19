from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import DATABASE_URL, MLMetrics

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

db = SessionLocal()

db.query(MLMetrics).delete()
db.commit()

print("Table MLMetrics vidée ✅")

db.close()
