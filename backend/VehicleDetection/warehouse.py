import pandas as pd
from config import DB_CONFIG, DW_CONFIG
from sqlalchemy import create_engine, text
import psycopg2
import numpy as np
from sqlalchemy.types import Integer

#pip install sqlalchemy
#pip install pandas

class Warehouse:
    def __init__(self):
        self.engine = None
        self.conn = None
        self.date_df = None
        self.time_df = None
        self.location_df = None

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            print("Conexão com a DB estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar com a BD: {e}")
            self.conn = None
            raise

    def connect_dw(self):
        try:
            self.engine = create_engine(f"postgresql+psycopg2://{DW_CONFIG['user']}:{DW_CONFIG['password']}@{DW_CONFIG['host']}/{DW_CONFIG['dbname']}")
            print("Conexão com o DW estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar com o DW: {e}")
            self.engine = None
            raise

    def close_dw(self):
        try:
            if self.engine:
                self.engine.dispose()
                print("Conexão com o DW encerrada.")
        except Exception as e:
            print(f"Erro ao encerrar a conexão com o DW: {e}")
            raise

    def extract_data(self):
        try:
            query = """
                        select vc.id, vc.car, vc.motorcycle, vc.bike, vc.truck, vc.bus,
                               vc.n, vc.s, vc.e, vc.w, vc.ne, vc.nw, vc.se, vc.sw, 
                               vc.timestamp, vc.location_id, l.location, l.direction
                        from vehicle_counts vc
                        join location l on l.location_id = vc.location_id;
                    """
            with self.conn:
                df = pd.read_sql(query, self.conn)
            
            print("Data extracted from source DB")
            return df
        except Exception as e:
            print(f"Error extracting data from DB: {e}")
            raise

    def transform_data(self, df):
        try:
            df.dropna(inplace=True)  # Remove missing values

            # Transform date and time columns
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df["date"] = df["timestamp"].dt.date
            df["time"] = df["timestamp"].dt.time
            df["hour"] = df["timestamp"].dt.hour
            df["minute"] = df["timestamp"].dt.minute
            df["period"] = df["timestamp"].dt.strftime("%p")  # AM/PM

            # Transform camera direction column
            df["direction"] = df["direction"].astype(str).str.strip().str.upper()
            
            df["direction"] = df["direction"].replace({
                "NORTE": "N", "NORTH": "N", "N": "N",
                "SUL": "S", "SOUTH": "S", "S": "S",
                "LESTE": "E", "EAST": "E", "L": "E", "E": "E",
                "OESTE": "W", "WEST": "W", "W": "W", "O": "W",
                "NORDESTE": "NE", "NORTHEAST": "NE", "NE": "NE",
                "NOROESTE": "NW", "NORTHWEST": "NW", "NW": "NW",
                "SUDESTE": "SE", "SOUTHEAST": "SE", "SE": "SE",
                "SUDOESTE": "SW", "SOUTHWEST": "SW", "SW": "SW"
            })

            df["direction"] = df["direction"].where(df["direction"].isin(["N", "S", "E", "W", "NE", "NW", "SE", "SW"]), "UNKNOWN")

            print("Data transformed successfully")
            print(df.head())
            return df
        except Exception as e:
            print(f"Error transforming data: {e}")
            raise

    def load_dim_date (self, df):
        try:
            self.date_df = df[["date"]].drop_duplicates().rename(columns={"date": "full_date"})
            self.date_df["full_date"] = pd.to_datetime(self.date_df["full_date"], errors="coerce")
            self.date_df["year"] = self.date_df["full_date"].dt.year
            self.date_df["month"] = self.date_df["full_date"].dt.month
            self.date_df["day"] = self.date_df["full_date"].dt.day
            self.date_df["weekday"] = self.date_df["full_date"].dt.strftime("%A")
            # Insert data while handling duplicates
            with self.engine.begin() as conn:
                for _, row in self.date_df.iterrows():
                    conn.execute(
                        text("""
                            INSERT INTO dim_date (full_date, year, month, day, weekday)
                            VALUES (:full_date, :year, :month, :day, :weekday)
                            ON CONFLICT (full_date) DO NOTHING;
                        """),
                        row.to_dict()
                    )

            self.date_df = pd.read_sql("SELECT * FROM dim_date", self.engine)
            print("Loaded dim_date table")
        except Exception as e:
            print(f"Erro ao carregar a tabela dim_date: {e}")
            raise

    def load_dim_time(self, df):
        try:
            self.time_df = df[["time", "hour", "minute", "period"]].drop_duplicates().rename(columns={"time": "full_time"})
            with self.engine.begin() as conn:
                for _, row in self.time_df.iterrows():
                    conn.execute(
                        text("""
                            INSERT INTO dim_time (full_time, hour, minute, period)
                            VALUES (:full_time, :hour, :minute, :period)
                            ON CONFLICT (full_time) DO NOTHING;
                        """),
                        row.to_dict()
                    )

            # Read back with time_id
            self.time_df = pd.read_sql("SELECT time_id, full_time, hour, minute, period FROM dim_time", self.engine)
            print("Loaded dim_time table")
        except Exception as e:
            print(f"Erro ao carregar a tabela dim_time: {e}")
            raise

    def load_dim_location(self, df):
        try:
            # Extract unique camera data
            self.location_df = df[["location", "direction"]].drop_duplicates()

            # Insert data efficiently
            with self.engine.begin() as conn:
                self.location_df.to_sql("dim_location", conn, if_exists="append", index=False)
                
            self.location_df = pd.read_sql("SELECT * FROM dim_location", self.engine)
            print("Loaded dim_location table")
        except Exception as e:
            print(f"Error loading dim_location table: {e}")
            raise

    def load_fact_vehicle_count(self, df):
        try:
            # Convert input data types
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            df["time"] = pd.to_datetime(df["time"], format='%H:%M:%S', errors="coerce").dt.time

            # Ensure dimension tables have proper types
            self.date_df["full_date"] = pd.to_datetime(self.date_df["full_date"], errors="coerce").dt.date
            self.time_df["full_time"] = pd.to_datetime(self.time_df["full_time"].astype(str), format='%H:%M:%S', errors="coerce").dt.time
            self.location_df["location_id"] = self.location_df["location_id"].astype(str)

            # Merge with validation
            fact_df = df.merge(
                self.date_df[["date_id", "full_date"]],
                left_on="date",
                right_on="full_date",
                how="inner"
            ).merge(
                self.time_df[["time_id", "full_time"]],
                left_on="time",
                right_on="full_time",
                how="inner"
            ).merge(
                self.location_df[["location_id", "name"]],
                left_on="location_id",
                right_on="location_id",
                how="inner"
            )

            # Prepare final columns
            fact_df = fact_df[[
                "date_id", "time_id", "location_id",
                "car", "motorcycle", "bike", "truck", "bus",
                "n", "s", "e", "w", "ne", "nw", "se", "sw"
            ]]

            # Insert efficiently
            with self.engine.begin() as conn:
                fact_df.to_sql(
                    "fact_vehicle_counts",
                    conn,
                    if_exists="append",
                    index=False,
                    chunksize=500,
                    method="multi",  # Faster batch insert
                    dtype={
                        'date_id': Integer(),
                        'time_id': Integer(),
                        'camera_id': Integer(),
                        'car': Integer(),
                        'motorcycle': Integer(),
                        'bike': Integer(),
                        'truck': Integer(),
                        'bus': Integer(),
                        'n': Integer(),
                        's': Integer(),
                        'e': Integer(),
                        'w': Integer(),
                        'ne': Integer(),
                        'nw': Integer(),
                        'se': Integer(),
                        'sw': Integer()
                    }
                )

            print("Loaded fact_vehicle_counts table")
            return fact_df
        except Exception as e:
            print(f"Error loading fact table: {str(e)}")
            raise