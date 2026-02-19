import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from create_db import DATABASE_URL, MLMetrics, MLInput, APILogs
from scipy.stats import ks_2samp

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def compute_drift_metrics(reference_csv="data/training_data.csv"):
    db = SessionLocal()
    drift_score = 0.0
    
    try:
        # 1. Charger données
        reference = pd.read_csv(reference_csv)
        production = pd.read_sql(db.query(MLInput).statement, db.bind)
        
        print(f"📊 Reference: {len(reference)} lignes | Production: {len(production)} lignes")
        
        if len(production) < 5:
            print("⚠️ Production trop petite → drift=0")
        elif reference.empty:
            print("⚠️ Reference vide → drift=0")
        else:
            # 2. ✅ FORCER COLONNES IDENTIQUES À 100%
            common_cols = reference.columns.intersection(production.columns)
            print(f"🔍 {len(common_cols)} colonnes communes total")
            
            # 3. Filtrer NUMÉRIQUES dans LES DEUX DataFrames
            ref_numeric_cols = reference[common_cols].select_dtypes(include=[np.number]).columns.tolist()
            prod_numeric_cols = production[common_cols].select_dtypes(include=[np.number]).columns.tolist()
            
            # ✅ INTERSECTION STRICTE = MÊMES COLONNES NUMÉRIQUES
            numeric_cols = list(set(ref_numeric_cols) & set(prod_numeric_cols))
            print(f"📈 {len(numeric_cols)} colonnes numériques IDENTIQUES")
            
            if numeric_cols:
                # 4. ✅ SÉLECTION SYNCHRONE (même ordre)
                ref_data = reference[numeric_cols]
                cur_data = production[numeric_cols]
                
                print(f"✅ Shapes OK: ref={ref_data.shape} | cur={cur_data.shape}")
                
                # 5. Vérification variance (seuil doux pour 8 lignes)
                valid_cols = []
                for col in numeric_cols:
                    ref_std = ref_data[col].std()
                    cur_std = cur_data[col].std()
                    ref_n = ref_data[col].notna().sum()
                    cur_n = cur_data[col].notna().sum()
                    
                    # Seuil adapté aux petites données
                    if (pd.notna(ref_std) and ref_std > 0 and 
                        pd.notna(cur_std) and cur_std > 0 and 
                        ref_n > 5 and cur_n >= 1):  # ≥1 pour production
                        valid_cols.append(col)
                
                print(f"✅ {len(valid_cols)}/{len(numeric_cols)} colonnes drift OK")
                
                if valid_cols:
                    # 6. CALCUL DRIFT (KS-test robuste)
                    ref_final = ref_data[valid_cols].dropna()
                    cur_final = cur_data[valid_cols].dropna()
                    
                    drift_count = 0
                    for col in valid_cols:
                        ref_vals = ref_final[col].dropna()
                        cur_vals = cur_final[col].dropna()
                        
                        if len(ref_vals) > 1 and len(cur_vals) > 0:
                            try:
                                stat, p_value = ks_2samp(ref_vals, cur_vals)
                                if p_value < 0.1:  # Seuil 10% pour petites données
                                    drift_count += 1
                            except:
                                pass  # Ignore erreurs rares
                    
                    drift_score = drift_count / len(valid_cols)
                    print(f"🎯 Drift: {drift_count}/{len(valid_cols)} ({drift_score:.1%})")
            
            else:
                print("⚠️ Aucune colonne numérique commune")

        # 7. Métriques opérationnelles
        error_count = db.query(APILogs).filter(APILogs.status_code >= 400).count()
        logs = db.query(APILogs).all()
        latencies = []
        for log in logs:
            lat = getattr(log, 'latency_ms', None)
            if lat is not None and pd.notna(lat) and isinstance(lat, (int, float)):
                latencies.append(float(lat))
        
        avg_latency = np.mean(latencies) if latencies else 0.0
        anomaly_count = int(production.isnull().sum().sum())

        # 8. SAUVEGARDE
        # metric_entry = MLMetrics(
        #     timestamp=datetime.utcnow(),
        # #     error_count=int(error_count),
        #     avg_latency=float(avg_latency),
        #     anomaly_count=anomaly_count,
        #     drift_score=float(drift_score)
        # )
        # b.add(metric_entry)
        # db.commit()
        
        print(f"✅ TERMINÉ | Drift: {drift_score:.1%} | Erreurs: {error_count} | Latence: {avg_latency:.0f}ms")
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        print(f"  → Type: {type(e).__name__}")
        db.rollback()
        drift_score = 0.0
    finally:
        db.close()
    
    return drift_score

if __name__ == "__main__":
    compute_drift_metrics()
