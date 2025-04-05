import pandas as pd
from config import DB_CONFIG, DW_CONFIG
from sqlalchemy import create_engine, text
import psycopg2

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
            print("CUSTOM: Conexão com a DB estabelecida com sucesso!")
        except Exception as e:
            print(f"CUSTOM: Erro ao conectar com a BD: {e}")
            self.conn = None
            raise

    def connect_dw(self):
        try:
            self.engine = create_engine(f"postgresql+psycopg2://{DW_CONFIG['user']}:{DW_CONFIG['password']}@{DW_CONFIG['host']}/{DW_CONFIG['dbname']}")
            print("CUSTOM: Conexão com o DW estabelecida com sucesso!")
        except Exception as e:
            print(f"CUSTOM: Erro ao conectar com o DW: {e}")
            self.engine = None
            raise

    def close_db(self):
        try:
            if self.conn:
                self.conn.close()
                print("CUSTOM: Conexão com a DB encerrada.")
        except Exception as e:
            print(f"CUSTOM: Erro ao encerrar a conexão com a DB: {e}")
            raise

    def close_dw(self):
        try:
            if self.engine:
                self.engine.dispose()
                print("CUSTOM: Conexão com o DW encerrada.")
        except Exception as e:
            print(f"CUSTOM: Erro ao encerrar a conexão com o DW: {e}")
            raise

    def extract_data(self):
        try:
            query = """
                        select vc.id, vc.car, vc.motorcycle, vc.bike, vc.truck, vc.bus,
                               vc.n, vc.s, vc.e, vc.w, vc.ne, vc.nw, vc.se, vc.sw, 
                               vc.timestamp, l.location, l.direction
                        from vehicle_counts vc
                        join location l on l.location_id = vc.location_id;
                    """
            with self.conn:
                df = pd.read_sql(query, self.conn)

            print("CUSTOM: Data extracted from source DB")
            return df
        except Exception as e:
            print(f"CUSTOM: Error extracting data from DB: {e}")
            raise

    def transform_data(self, df):
        try:
            df.dropna(inplace=True)  # Remove missing values
            
            # Convert timestamp to datetime and extract date, time, hour, minute, and period(AM/PM)
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df["date"] = df["timestamp"].dt.date
            df["time"] = df["timestamp"].dt.time
            df["hour"] = df["timestamp"].dt.hour
            df["minute"] = df["timestamp"].dt.minute
            df["period"] = df["timestamp"].dt.strftime("%p")

            # Transform camera direction in the direction column from loacation table from DB
            df["direction"] = df["direction"].astype(str).str.strip().str.upper()
            df["direction"] = df["direction"].replace({
                "NORTE": "N", "NORTH": "N", "N": "N",
                "SUL": "S", "SOUTH": "S", "S": "S",
                "LESTE": "E", "EAST": "E", "L": "E", "E": "E",
                "OESTE": "W", "WEST": "W", "W": "W", "O": "W",
                "NORDESTE": "NE", "NORTHEAST": "NE", "NORTH-EAST": "NE", "NE": "NE",
                "NOROESTE": "NW", "NORTHWEST": "NW", "NORTH-WEST": "NW", "NW": "NW",
                "SUDESTE": "SE", "SOUTHEAST": "SE", "SOUTH-EAST": "SE", "SE": "SE",
                "SUDOESTE": "SW", "SOUTHWEST": "SW", "SOUTH-WEST": "SW", "SW": "SW"
            })
            df["direction"] = df["direction"].where(df["direction"].isin(["N", "S", "E", "W", "NE", "NW", "SE", "SW"]), "UNKNOWN")

            print("CUSTOM: Data transformed successfully")
            return df
        except Exception as e:
            print(f"CUSTOM: Error transforming data: {e}")
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
            print("CUSTOM: Loaded dim_date table")
        except Exception as e:
            print(f"CUSTOM: Erro ao carregar a tabela dim_date: {e}")
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
            print("CUSTOM: Loaded dim_time table")
        except Exception as e:
            print(f"CUSTOM: Erro ao carregar a tabela dim_time: {e}")
            raise

    def load_dim_location(self, df):
        try:
            self.location_df = df[["location", "direction"]].drop_duplicates()

            with self.engine.begin() as conn:
                for _, row in self.location_df.iterrows():
                    conn.execute(
                        text("""
                            INSERT INTO dim_location (location, direction)
                            VALUES (:location, :direction)
                        """), 
                        {
                            "location": row["location"],
                            "direction": row["direction"]
                        }
                    )
                        
            self.location_df = pd.read_sql("SELECT * FROM dim_location", self.engine)
        except Exception as e:
            print(f"CUSTOM: Error loading dim_location table: {e}")
            raise

    def load_fact_vehicle_count(self, df):
        try:
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            df["time"] = pd.to_datetime(df["time"], format='%H:%M:%S', errors="coerce").dt.time
            
            self.date_df["full_date"] = pd.to_datetime(self.date_df["full_date"], errors="coerce").dt.date
            self.time_df["full_time"] = pd.to_datetime(self.time_df["full_time"].astype(str), format='%H:%M:%S', errors="coerce").dt.time
            
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
                self.location_df[["location_id", "location"]],
                left_on="location",
                right_on="location",
                how="inner"
            )
            
            fact_df = fact_df[[
                "date_id", "time_id", "location_id",
                "car", "motorcycle", "bike", "truck", "bus",
                "n", "s", "e", "w", "ne", "nw", "se", "sw"
            ]]
            
            with self.engine.begin() as conn:
                existing_combinations = pd.read_sql("SELECT date_id, time_id, location_id FROM fact_vehicle_counts", conn)
                
                fact_df['composite_key'] = fact_df['date_id'].astype(str) + '_' + \
                                        fact_df['time_id'].astype(str) + '_' + \
                                        fact_df['location_id'].astype(str)
                
                existing_combinations['composite_key'] = existing_combinations['date_id'].astype(str) + '_' + \
                                                        existing_combinations['time_id'].astype(str) + '_' + \
                                                        existing_combinations['location_id'].astype(str)
                
                new_records = fact_df[~fact_df['composite_key'].isin(existing_combinations['composite_key'])]
                
                new_records = new_records.drop(columns=['composite_key'])
                
                if not new_records.empty:
                    new_records.to_sql(
                        "fact_vehicle_counts",
                        conn,
                        if_exists="append",
                        index=False,
                        chunksize=500,
                        method="multi"
                    )
                    print(f"CUSTOM: Inserted {len(new_records)} new records into fact_vehicle_counts")
                else:
                    print("CUSTOM: No new records to insert - all combinations already exist")

            return fact_df
        except Exception as e:
            print(f"CUSTOM: Error loading fact table: {str(e)}")
            raise