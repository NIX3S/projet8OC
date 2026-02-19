from pydantic import BaseModel
from data import InputData
# Boucle pour générer SQLAlchemy columns
for field_name, field_info in InputData.model_fields.items():
    print(f"{field_name} = Column(Float)")
