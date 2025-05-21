from sqlalchemy import text
import pandas as pd
from project.views.ctg.ctg_article_presentations import __get_service__ as service_presentations
import numpy as np

class LoadDataMassive:
    def __init__(self, repository):
        self.repository = repository

    def transform(self, df, config, movement_id):
        df.rename(columns={
            "IDENTIFICADOR": "article_id",
            "CANTIDAD": "quantity",
            "COSTO": "cost",
            "EQUIVALENCIA": "real_quantity_equivalent",
        }, inplace=True)

        # Convertir a numérico y gestionar valores nulos
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        df["cost"] = pd.to_numeric(df["cost"], errors="coerce").fillna(0)
        df["real_quantity_equivalent"] = pd.to_numeric(df["real_quantity_equivalent"], errors="coerce").fillna(1)
        
        # Filtrar artículos que no tienen cantidad ni costo
        df = df[(df["quantity"] > 0) & (df["cost"] > 0)]
        
        # Continuar con el resto de transformaciones
        df["quantity"] = df["quantity"] * df["real_quantity_equivalent"]
        df["cost"] = (df["cost"] / df["quantity"]).round(2)
        df['presentation_id'] = df.apply(
            lambda row: self.get_presentation_id(
                account_id=config['account_id'],
                article_id=row['article_id'],
                equivalence=row['real_quantity_equivalent']
            ),
            axis=1
        )
        df["presentation_id"] = df["presentation_id"].apply(
          lambda x: int(x) if pd.notnull(x) and not np.isnan(x) else None
        )

        df["presentation_id"] = df["presentation_id"].astype("Int64")

        df = df[["article_id", "quantity", "cost", "real_quantity_equivalent", "presentation_id"]]
        df["account_id"] = config['account_id']
        df["movement_id"] = movement_id
        
        
        return df.to_dict(orient="records")

    def insert_bulk(self, data):
        query = text("""
            INSERT INTO inv_movements_details (article_id, quantity, cost, account_id, movement_id, real_quantity_equivalent, presentation_id)
            VALUES (:article_id, :quantity, :cost, :account_id, :movement_id, :real_quantity_equivalent, :presentation_id)
        """)
        self.repository.execute(query, data)
        self.repository.commit()
    
    def get_presentation_id(self, article_id, equivalence, account_id):
        presentation_serv = service_presentations()
        presentation = presentation_serv.compose.repository.query(presentation_serv.compose.model).filter_by(
            article_id=article_id,
            quantity_equivalent=equivalence,
            account_id=account_id
        ).first()
        return presentation.id if presentation else None