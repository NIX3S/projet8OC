from sqlalchemy import create_engine, Column, Integer, Float, DateTime,String, ForeignKey, text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

# ------------------------------------------------------
# Charger .env depuis le dossier du script
# ------------------------------------------------------
env_path = Path(__file__).resolve().parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)

# PostgreSQL config via env
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "5345")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "scoring_ml")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

# ------------------------------------------------------
# Table des inputs
# ------------------------------------------------------
class MLInput(Base):
    __tablename__ = "ml_inputs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Toutes les colonnes de InputData
    CNT_CHILDREN = Column(Float)
    AMT_INCOME_TOTAL = Column(Float)
    AMT_CREDIT = Column(Float)
    AMT_ANNUITY = Column(Float)
    NAME_TYPE_SUITE = Column(Float)
    NAME_INCOME_TYPE = Column(Float)
    NAME_EDUCATION_TYPE = Column(Float)
    NAME_FAMILY_STATUS = Column(Float)
    NAME_HOUSING_TYPE = Column(Float)
    REGION_POPULATION_RELATIVE = Column(Float)
    DAYS_BIRTH = Column(Float)
    DAYS_EMPLOYED = Column(Float)
    DAYS_REGISTRATION = Column(Float)
    OWN_CAR_AGE = Column(Float)
    FLAG_WORK_PHONE = Column(Float)
    FLAG_CONT_MOBILE = Column(Float)
    FLAG_PHONE = Column(Float)
    FLAG_EMAIL = Column(Float)
    OCCUPATION_TYPE = Column(Float)
    CNT_FAM_MEMBERS = Column(Float)
    REGION_RATING_CLIENT = Column(Float)
    WEEKDAY_APPR_PROCESS_START = Column(Float)
    HOUR_APPR_PROCESS_START = Column(Float)
    LIVE_REGION_NOT_WORK_REGION = Column(Float)
    REG_CITY_NOT_LIVE_CITY = Column(Float)
    REG_CITY_NOT_WORK_CITY = Column(Float)
    LIVE_CITY_NOT_WORK_CITY = Column(Float)
    ORGANIZATION_TYPE = Column(Float)
    EXT_SOURCE_1 = Column(Float)
    EXT_SOURCE_2 = Column(Float)
    EXT_SOURCE_3 = Column(Float)
    APARTMENTS_AVG = Column(Float)
    BASEMENTAREA_AVG = Column(Float)
    YEARS_BEGINEXPLUATATION_AVG = Column(Float)
    YEARS_BUILD_AVG = Column(Float)
    COMMONAREA_AVG = Column(Float)
    ELEVATORS_AVG = Column(Float)
    ENTRANCES_AVG = Column(Float)
    FLOORSMAX_AVG = Column(Float)
    FLOORSMIN_AVG = Column(Float)
    LANDAREA_AVG = Column(Float)
    LIVINGAPARTMENTS_AVG = Column(Float)
    LIVINGAREA_AVG = Column(Float)
    NONLIVINGAPARTMENTS_AVG = Column(Float)
    NONLIVINGAREA_AVG = Column(Float)
    FONDKAPREMONT_MODE = Column(Float)
    HOUSETYPE_MODE = Column(Float)
    WALLSMATERIAL_MODE = Column(Float)
    OBS_30_CNT_SOCIAL_CIRCLE = Column(Float)
    DEF_30_CNT_SOCIAL_CIRCLE = Column(Float)
    DEF_60_CNT_SOCIAL_CIRCLE = Column(Float)
    DAYS_LAST_PHONE_CHANGE = Column(Float)
    FLAG_DOCUMENT_3 = Column(Float)
    FLAG_DOCUMENT_5 = Column(Float)
    FLAG_DOCUMENT_6 = Column(Float)
    FLAG_DOCUMENT_8 = Column(Float)
    FLAG_DOCUMENT_11 = Column(Float)
    FLAG_DOCUMENT_18 = Column(Float)
    AMT_REQ_CREDIT_BUREAU_WEEK = Column(Float)
    AMT_REQ_CREDIT_BUREAU_MON = Column(Float)
    AMT_REQ_CREDIT_BUREAU_QRT = Column(Float)
    AMT_REQ_CREDIT_BUREAU_YEAR = Column(Float)
    OWN_CAR_AGE_na = Column(Float)
    EXT_SOURCE_1_na = Column(Float)
    EXT_SOURCE_2_na = Column(Float)
    EXT_SOURCE_3_na = Column(Float)
    BASEMENTAREA_AVG_na = Column(Float)
    LANDAREA_AVG_na = Column(Float)
    OCCUPATION_TYPE_na = Column(Float)
    AMT_CREDIT_SUM_sum = Column(Float)
    AMT_CREDIT_SUM_mean = Column(Float)
    AMT_CREDIT_SUM_max = Column(Float)
    AMT_CREDIT_SUM_min = Column(Float)
    AMT_CREDIT_SUM_DEBT_sum = Column(Float)
    AMT_CREDIT_SUM_DEBT_mean = Column(Float)
    AMT_CREDIT_SUM_DEBT_min = Column(Float)
    AMT_CREDIT_SUM_LIMIT_sum = Column(Float)
    AMT_CREDIT_SUM_LIMIT_mean = Column(Float)
    AMT_CREDIT_SUM_LIMIT_min = Column(Float)
    AMT_ANNUITY_sum_x = Column(Float)
    AMT_ANNUITY_mean_x = Column(Float)
    AMT_ANNUITY_min_x = Column(Float)
    AMT_CREDIT_MAX_OVERDUE_sum = Column(Float)
    CREDIT_DAY_OVERDUE_sum = Column(Float)
    CREDIT_DAY_OVERDUE_mean = Column(Float)
    CNT_CREDIT_PROLONG_sum = Column(Float)
    CNT_CREDIT_PROLONG_mean = Column(Float)
    DAYS_CREDIT_min = Column(Float)
    DAYS_CREDIT_max = Column(Float)
    DAYS_CREDIT_mean = Column(Float)
    DAYS_CREDIT_ENDDATE_min = Column(Float)
    DAYS_CREDIT_ENDDATE_max = Column(Float)
    DAYS_CREDIT_ENDDATE_mean = Column(Float)
    DAYS_ENDDATE_FACT_min = Column(Float)
    DAYS_ENDDATE_FACT_max = Column(Float)
    DAYS_ENDDATE_FACT_mean = Column(Float)
    DAYS_CREDIT_UPDATE_min = Column(Float)
    DAYS_CREDIT_UPDATE_max = Column(Float)
    DAYS_CREDIT_UPDATE_mean = Column(Float)
    months_balance_min_min = Column(Float)
    months_balance_max_max = Column(Float)
    status_0_sum_sum = Column(Float)
    status_1_sum_sum = Column(Float)
    status_2_sum_sum = Column(Float)
    status_5_sum_sum = Column(Float)
    status_C_sum_sum = Column(Float)
    status_X_sum_sum = Column(Float)
    credit_active_Active_sum = Column(Float)
    credit_active_Closed_sum = Column(Float)
    credit_active_Sold_sum = Column(Float)
    AMT_ANNUITY_sum_y = Column(Float)
    AMT_ANNUITY_mean_y = Column(Float)
    AMT_ANNUITY_max_y = Column(Float)
    AMT_ANNUITY_min_y = Column(Float)
    AMT_APPLICATION_mean = Column(Float)
    AMT_APPLICATION_max = Column(Float)
    AMT_APPLICATION_min = Column(Float)
    AMT_DOWN_PAYMENT_sum = Column(Float)
    AMT_DOWN_PAYMENT_mean = Column(Float)
    AMT_DOWN_PAYMENT_min = Column(Float)
    AMT_GOODS_PRICE_min = Column(Float)
    DAYS_DECISION_min = Column(Float)
    DAYS_DECISION_max = Column(Float)
    DAYS_DECISION_mean = Column(Float)
    DAYS_FIRST_DRAWING_min = Column(Float)
    DAYS_FIRST_DRAWING_mean = Column(Float)
    DAYS_FIRST_DUE_min = Column(Float)
    DAYS_FIRST_DUE_max = Column(Float)
    DAYS_FIRST_DUE_mean = Column(Float)
    DAYS_LAST_DUE_min = Column(Float)
    DAYS_LAST_DUE_max = Column(Float)
    DAYS_LAST_DUE_mean = Column(Float)
    NAME_CONTRACT_TYPE_Consumer_loans_sum = Column(Float)
    NAME_CONTRACT_TYPE_Revolving_loans_sum = Column(Float)
    NAME_CONTRACT_STATUS_Canceled_sum = Column(Float)
    NAME_CONTRACT_STATUS_Refused_sum = Column(Float)
    NAME_CONTRACT_STATUS_Unused_offer_sum = Column(Float)
    MONTHS_BALANCE_max_x = Column(Float)
    CNT_INSTALMENT_sum = Column(Float)
    CNT_INSTALMENT_mean = Column(Float)
    CNT_INSTALMENT_max = Column(Float)
    CNT_INSTALMENT_min = Column(Float)
    CNT_INSTALMENT_FUTURE_min = Column(Float)
    SK_DPD_sum_x = Column(Float)
    SK_DPD_DEF_sum_x = Column(Float)
    pos_status_Active_sum = Column(Float)
    pos_status_Completed_sum = Column(Float)
    pos_status_Demand_sum = Column(Float)
    pos_status_Returned_to_the_store_sum = Column(Float)
    pos_status_Signed_sum = Column(Float)
    MONTHS_BALANCE_min_y = Column(Float)
    MONTHS_BALANCE_max_y = Column(Float)
    AMT_BALANCE_sum = Column(Float)
    AMT_BALANCE_mean = Column(Float)
    AMT_BALANCE_min = Column(Float)
    AMT_CREDIT_LIMIT_ACTUAL_sum = Column(Float)
    AMT_CREDIT_LIMIT_ACTUAL_mean = Column(Float)
    AMT_DRAWINGS_ATM_CURRENT_sum = Column(Float)
    AMT_DRAWINGS_ATM_CURRENT_mean = Column(Float)
    AMT_DRAWINGS_ATM_CURRENT_max = Column(Float)
    AMT_DRAWINGS_CURRENT_sum = Column(Float)
    AMT_DRAWINGS_CURRENT_mean = Column(Float)
    AMT_DRAWINGS_CURRENT_max = Column(Float)
    AMT_DRAWINGS_CURRENT_min = Column(Float)
    AMT_DRAWINGS_OTHER_CURRENT_sum = Column(Float)
    AMT_DRAWINGS_OTHER_CURRENT_mean = Column(Float)
    AMT_DRAWINGS_OTHER_CURRENT_max = Column(Float)
    AMT_DRAWINGS_POS_CURRENT_sum = Column(Float)
    AMT_DRAWINGS_POS_CURRENT_mean = Column(Float)
    AMT_DRAWINGS_POS_CURRENT_max = Column(Float)
    AMT_DRAWINGS_POS_CURRENT_min = Column(Float)
    AMT_INST_MIN_REGULARITY_min = Column(Float)
    AMT_PAYMENT_CURRENT_mean = Column(Float)
    AMT_PAYMENT_CURRENT_max = Column(Float)
    AMT_PAYMENT_CURRENT_min = Column(Float)
    AMT_PAYMENT_TOTAL_CURRENT_min = Column(Float)
    CNT_DRAWINGS_ATM_CURRENT_sum = Column(Float)
    CNT_DRAWINGS_ATM_CURRENT_mean = Column(Float)
    CNT_DRAWINGS_ATM_CURRENT_max = Column(Float)
    CNT_DRAWINGS_ATM_CURRENT_min = Column(Float)
    CNT_DRAWINGS_CURRENT_sum = Column(Float)
    CNT_DRAWINGS_CURRENT_mean = Column(Float)
    CNT_DRAWINGS_CURRENT_max = Column(Float)
    CNT_DRAWINGS_CURRENT_min = Column(Float)
    CNT_DRAWINGS_OTHER_CURRENT_sum = Column(Float)
    CNT_DRAWINGS_OTHER_CURRENT_mean = Column(Float)
    CNT_DRAWINGS_OTHER_CURRENT_max = Column(Float)
    CNT_DRAWINGS_POS_CURRENT_min = Column(Float)
    CNT_INSTALMENT_MATURE_CUM_sum = Column(Float)
    CNT_INSTALMENT_MATURE_CUM_min = Column(Float)
    cc_status_Completed_sum = Column(Float)
    cc_status_Sent_proposal_sum = Column(Float)
    SK_DPD_sum_y = Column(Float)
    SK_DPD_DEF_sum_y = Column(Float)
    DAYS_INSTALMENT_max = Column(Float)
    DAYS_INSTALMENT_mean = Column(Float)
    AMT_INSTALMENT_sum = Column(Float)
    AMT_INSTALMENT_mean = Column(Float)
    AMT_INSTALMENT_max = Column(Float)
    AMT_INSTALMENT_min = Column(Float)
    AMT_CREDIT_SUM_DEBT_mean_na = Column(Float)
    AMT_CREDIT_SUM_LIMIT_mean_na = Column(Float)
    AMT_ANNUITY_mean_x_na = Column(Float)
    AMT_CREDIT_MAX_OVERDUE_mean_na = Column(Float)
    months_balance_min_min_na = Column(Float)
    AMT_DOWN_PAYMENT_mean_na = Column(Float)
    NAME_CONTRACT_TYPE_Cash_loans = Column(Float)
    CODE_GENDER_F = Column(Float)
    CODE_GENDER_M = Column(Float)
    FLAG_OWN_CAR_N = Column(Float)
    FLAG_OWN_REALTY_N = Column(Float)
    EMERGENCYSTATE_MODE_Unknown = Column(Float)
        
    outputs = relationship("MLOutput", back_populates="input_row")

# ------------------------------------------------------
# Table des outputs
# ------------------------------------------------------
class MLOutput(Base):
    __tablename__ = "ml_outputs"

    id = Column(Integer, primary_key=True)
    input_id = Column(Integer, ForeignKey("ml_inputs.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    prediction = Column(Float)

    input_row = relationship("MLInput", back_populates="outputs")


#-------------------------------------------------------
#Monitoring
#-------------------------------------------------------
class APILogs(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    endpoint = Column(String)
    latency_ms  = Column(Float)
    status_code   = Column(Integer)
    error_message   = Column(String)
    inference_time_ms = Column(Float)
    cpu_usage = Column(Float)
    

class MLMetrics (Base):
    __tablename__ = "ml_metrics"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_count  = Column(Integer)
    avg_latency   = Column(Float)
    anomaly_count    = Column(Integer)
    drift_score    = Column(Float)

    


# ------------------------------------------------------
# Création de la DB et des tables
# ------------------------------------------------------
def main():
    # Connexion par défaut pour créer DB si elle n'existe pas
    engine_default = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/postgres")
    with engine_default.connect() as conn:
        conn.execute(text("COMMIT"))
        result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"))
        exists = result.scalar() is not None
        if not exists:
            print(f"Database '{DB_NAME}' does not exist. Creating...")
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
            print(f"Database '{DB_NAME}' created!")

    # Connexion à la vraie DB pour créer les tables
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    print("Tables créées avec succès !")

if __name__ == "__main__":
    main()
