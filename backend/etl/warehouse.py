import pandas as pd
from config import DB_CONFIG_neon_tech, DATABASE_SCHEMA, WAREHOUSE_SCHEMA
from sqlalchemy import create_engine, text
import psycopg2
import os
import re
from datetime import datetime

#pip install sqlalchemy
#pip install pandas

def dms_to_decimal(coord_str):
    if not isinstance(coord_str, str):
        return None

    # Clean up weird characters to standard DMS symbols
    coord_str = (
        coord_str.strip()
        .replace("º", "°")
        .replace("’", "'")
        .replace("′", "'")
        .replace("″", '"')
    )

    # Match DMS pattern with optional symbols
    dms_pattern = r"(\d+)[°\s]+(\d+)?['\s]*([\d\.]+)?[\"\s]*([NSEW])"
    match = re.match(dms_pattern, coord_str, re.IGNORECASE)

    if match:
        degrees = float(match.group(1))
        minutes = float(match.group(2) or 0)
        seconds = float(match.group(3) or 0)
        direction = match.group(4).upper()

        decimal = degrees + minutes / 60 + seconds / 3600
        if direction in ['S', 'W']:
            decimal *= -1
        return round(decimal, 4)

    # Try to parse directly as float if already in decimal
    try:
        return float(coord_str)
    except ValueError:
        return None

class Warehouse:
    def __init__(self):
        self.engine = None
        self.conn = None
        self.date_df = None
        self.time_df = None
        self.location_df = None

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG_neon_tech)
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Conexão com a DB estabelecida com sucesso!\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Erro ao conectar com a BD: {e}\033[0m")
            self.conn = None
            raise

    def connect_dw(self):
        try:
            self.engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG_neon_tech['user']}:{DB_CONFIG_neon_tech['password']}@{DB_CONFIG_neon_tech['host']}/{DB_CONFIG_neon_tech['dbname']}")
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Conexão com o DW estabelecida com sucesso!\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Erro ao conectar com o DW: {e}\033[0m")
            self.engine = None
            raise

    def close_db(self):
        try:
            if self.conn:
                self.conn.close()
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Conexão com a DB encerrada.\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Erro ao encerrar a conexão com a DB: {e}\033[0m")
            raise

    def close_dw(self):
        try:
            if self.engine:
                self.engine.dispose()
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Conexão com o DW encerrada.\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Erro ao encerrar a conexão com o DW: {e}\033[0m")
            raise

    def get_last_row_id(self, path, table):
        if table == 1:  # vehicle_counts
            file_path = os.path.join(path, 'last_row_id_vehicle_count.txt')
        elif table == 2:  # locations
            file_path = os.path.join(path, 'last_updated_locations.txt')
        else:
            raise ValueError("Invalid table number.")

        if not os.path.exists(file_path):
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No last row ID/time file found. Starting from scratch.\033[0m")
            return 0 if table == 1 else "1970-01-01 00:00:00"

        try:
            with open(file_path, 'r') as f:
                value = f.read().strip()
                return int(value) if table == 1 else value
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Error reading last row ID/time: {e}\033[0m")
            return 0 if table == 1 else "1970-01-01 00:00:00"

    def save_last_row_id(self, path, value, table):
        try:
            os.makedirs(path, exist_ok=True)
            if table == 1: # vehicle_counts
                file_path = os.path.join(path, 'last_row_id_vehicle_count.txt')
            elif table == 2: # locations
                file_path = os.path.join(path, 'last_updated_locations.txt')
            else:
                raise ValueError("Invalid table number.")

            with open(file_path, 'w') as f:
                f.write(str(value))
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Error saving last row ID/time: {e}\033[0m")
            raise

    def extract_data(self, path):
        try:
            # Step 1: Extract from vehicle_counts
            last_id = self.get_last_row_id(path, 1)  # 1 → vehicle_counts
            query_vc = f"""
                SELECT id AS vehicle_count_id, car, motorcycle, bike, truck, bus,
                    n, s, e, w, ne, nw, se, sw, 
                    timestamp, location_id
                FROM {DATABASE_SCHEMA}.vehicle_counts
                WHERE id > {last_id}
            """
            with self.conn:
                vehicle_df = pd.read_sql(query_vc, self.conn)

            if not vehicle_df.empty:
                self.save_last_row_id(path, vehicle_df["vehicle_count_id"].max(), 1)
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: vehicle_counts extracted rows: {len(vehicle_df)}\033[0m")
            else:
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No new vehicle_counts data.\033[0m")

            # Step 2: Extract updated or new locations
            last_updated = self.get_last_row_id(path, 2)  # 2 → locations
            vehicle_location_ids = (
                vehicle_df["location_id"].unique().tolist() if not vehicle_df.empty else []
            )
            vehicle_location_ids_str = ','.join(map(str, vehicle_location_ids)) or "NULL"

            query_loc = f"""
                SELECT location_id, location, direction, updated_at, latitude, longitude
                FROM {DATABASE_SCHEMA}.locations
                WHERE updated_at > '{last_updated}'
                OR location_id IN ({vehicle_location_ids_str})
            """
            location_df_full = pd.read_sql(query_loc, self.conn)

            if not location_df_full.empty:
                most_recent = location_df_full["updated_at"].max()
                self.save_last_row_id(path, most_recent, 2)
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: locations extracted rows:\033[0m", len(location_df_full))
            else:
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No locations data.\033[0m")

            # Step 3: Filter location_df for merging only (those used in vehicle_df)
            if not vehicle_df.empty:
                location_df_filtered = location_df_full[location_df_full["location_id"].isin(vehicle_location_ids)]
                vehicle_df = vehicle_df.merge(
                    location_df_filtered.drop(columns=['updated_at']),
                    on="location_id",
                    how="left"
                )

            # Identify unused (only-updated) location rows not referenced in vehicle_df
            if not location_df_full.empty:
                used_location_ids = vehicle_df["location_id"].unique() if not vehicle_df.empty else []
                extra_location_df = location_df_full[~location_df_full["location_id"].isin(used_location_ids)]
                self.location_df = extra_location_df.drop(columns=["updated_at"])
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Updated locations extracted rows:\033[0m", len(self.location_df))
            else:
                self.location_df = pd.DataFrame()

            if not vehicle_df.empty and not self.location_df.empty:
                return vehicle_df, len(self.location_df)
            elif not vehicle_df.empty and self.location_df.empty:
                return vehicle_df, 0
            elif vehicle_df.empty:
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No new data to process.\033[0m")
                return pd.DataFrame(), len(self.location_df)

        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Error during extraction: {e}\033[0m")
            raise

    def transform_data(self, df):
        try:
            if not df.empty:
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
                    "ESTE": "E", "EAST": "E", "L": "E", "E": "E",
                    "OESTE": "W", "WEST": "W", "W": "W", "O": "W",
                    "NORDESTE": "NE", "NORTHEAST": "NE", "NORTH-EAST": "NE", "NE": "NE",
                    "NOROESTE": "NW", "NORTHWEST": "NW", "NORTH-WEST": "NW", "NW": "NW",
                    "SUDESTE": "SE", "SOUTHEAST": "SE", "SOUTH-EAST": "SE", "SE": "SE",
                    "SUDOESTE": "SW", "SOUTHWEST": "SW", "SOUTH-WEST": "SW", "SW": "SW"
                })
                df["direction"] = df["direction"].where(
                    df["direction"].isin(["N", "S", "E", "W", "NE", "NW", "SE", "SW"]),
                    "UNKNOWN"
                )

                # Transform location latitude and longitude to decimal degrees, example: 40.7128, -74.0060
                df["latitude"] = df["latitude"].apply(dms_to_decimal)
                df["longitude"] = df["longitude"].apply(dms_to_decimal)


            if self.location_df is not None and not self.location_df.empty:
                # Transform camera direction in the direction column from loacation table from DB
                self.location_df["direction"] = self.location_df["direction"].astype(str).str.strip().str.upper()
                self.location_df["direction"] = self.location_df["direction"].replace({
                    "NORTE": "N", "NORTH": "N", "N": "N",
                    "SUL": "S", "SOUTH": "S", "S": "S",
                    "ESTE": "E", "EAST": "E", "L": "E", "E": "E",
                    "OESTE": "W", "WEST": "W", "W": "W", "O": "W",
                    "NORDESTE": "NE", "NORTHEAST": "NE", "NORTH-EAST": "NE", "NE": "NE",
                    "NOROESTE": "NW", "NORTHWEST": "NW", "NORTH-WEST": "NW", "NW": "NW",
                    "SUDESTE": "SE", "SOUTHEAST": "SE", "SOUTH-EAST": "SE", "SE": "SE",
                    "SUDOESTE": "SW", "SOUTHWEST": "SW", "SOUTH-WEST": "SW", "SW": "SW"
                })
                self.location_df["direction"] = self.location_df["direction"].where(
                    self.location_df["direction"].isin(["N", "S", "E", "W", "NE", "NW", "SE", "SW"]),
                    "UNKNOWN"
                )

                # Transform location latitude and longitude to decimal degrees, example: 40.7128, -74.0060
                self.location_df["latitude"] = self.location_df["latitude"].apply(dms_to_decimal)
                self.location_df["longitude"] = self.location_df["longitude"].apply(dms_to_decimal)


            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Data transformed successfully\033[0m")
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Vehicle rows: {len(df)}, Location rows: {len(self.location_df) if self.location_df is not None else 0}\033[0m")

            return df, self.location_df 

        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Error transforming data: {e}\033[0m")
            raise

    def load_dim_date (self, df):
        try:
            self.date_df = df[["date"]].drop_duplicates().rename(columns={"date": "full_date"})
            self.date_df["full_date"] = pd.to_datetime(self.date_df["full_date"], errors="coerce")
            self.date_df["year"] = self.date_df["full_date"].dt.year
            self.date_df["month"] = self.date_df["full_date"].dt.month
            self.date_df["day"] = self.date_df["full_date"].dt.day
            self.date_df["weekday"] = self.date_df["full_date"].dt.strftime("%A")
            
            with self.engine.begin() as conn:
                for _, row in self.date_df.iterrows():
                    conn.execute(
                        text(f"""
                            INSERT INTO {WAREHOUSE_SCHEMA}.dim_date (full_date, year, month, day, weekday)
                            VALUES (:full_date, :year, :month, :day, :weekday)
                            ON CONFLICT (full_date) DO NOTHING;
                        """),
                        row.to_dict()
                    )

            self.date_df = pd.read_sql(f"SELECT * FROM {WAREHOUSE_SCHEMA}.dim_date", self.engine)
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Loaded dim_date table\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Erro ao carregar a tabela dim_date: {e}\033[0m")
            raise

    def load_dim_time(self, df):
        try:
            self.time_df = df[["time", "hour", "minute", "period"]].drop_duplicates().rename(columns={"time": "full_time"})
            with self.engine.begin() as conn:
                for _, row in self.time_df.iterrows():
                    conn.execute(
                        text(f"""
                            INSERT INTO {WAREHOUSE_SCHEMA}.dim_time (full_time, hour, minute, period)
                            VALUES (:full_time, :hour, :minute, :period)
                            ON CONFLICT (full_time) DO NOTHING;
                        """),
                        row.to_dict()
                    )

            self.time_df = pd.read_sql(f"SELECT * FROM {WAREHOUSE_SCHEMA}.dim_time", self.engine)
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Loaded dim_time table\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Erro ao carregar a tabela dim_time: {e}\033[0m")
            raise

    def load_dim_location(self, df):
        try:
            if (df is None or df.empty) and (self.location_df is None or self.location_df.empty):
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No location data to load.\033[0m")
                return
            
            if df is not None and not df.empty:
                combined_df = pd.concat([df, self.location_df]).drop_duplicates(subset=["location_id"], keep="last")
            else:
                combined_df = self.location_df

            # Ensure we have unique location_ids to avoid duplicate checks
            unique_location_ids = combined_df['location_id'].unique()

            if unique_location_ids.size > 0:
                location_ids = tuple(int(id) for id in unique_location_ids)
                
                # Get existing locations from dimension table
                query = f"""
                    SELECT location_id, location, direction, latitude, longitude
                    FROM {WAREHOUSE_SCHEMA}.dim_location
                    WHERE location_id IN %(location_ids)s
                """
                existing = pd.read_sql(
                    query, 
                    self.engine, 
                    params={"location_ids": location_ids}
                )

                # Convert existing locations to a dictionary for fast lookup
                existing_dict = {
                    row["location_id"]: {
                        "location": row["location"],
                        "direction": row["direction"],
                        "latitude": row["latitude"],
                        "longitude": row["longitude"]
                    }
                    for _, row in existing.iterrows()
                }

                new_rows = 0
                updated_rows = 0
                
                with self.engine.begin() as conn:
                    for _, row in combined_df.iterrows():
                        location_id = int(row["location_id"])
                        location = row["location"]
                        direction = row["direction"]
                        latitude = row["latitude"]
                        longitude = row["longitude"]

                        if location_id not in existing_dict:
                            # Insert new location
                            conn.execute(
                                text(f"""
                                    INSERT INTO {WAREHOUSE_SCHEMA}.dim_location (location_id, location, direction, latitude, longitude)
                                    VALUES (:location_id, :location, :direction, :latitude, :longitude)
                                """),
                                {
                                    "location_id": location_id,
                                    "location": location,
                                    "direction": direction,
                                    "latitude": latitude,
                                    "longitude": longitude
                                }
                            )
                            new_rows += 1
                        else:
                            existing_location = existing_dict[location_id]
                            # Update if either location name or direction has changed
                            if (existing_location["location"] != location or 
                                existing_location["direction"] != direction):
                                conn.execute(
                                    text(f"""
                                        UPDATE {WAREHOUSE_SCHEMA}.dim_location
                                        SET location = :location,
                                            direction = :new_direction,
                                            location_old = :old_location,
                                            direction_old = :old_direction
                                        WHERE location_id = :location_id
                                    """),
                                    {
                                        "location_id": location_id,
                                        "location": location,
                                        "new_direction": direction,
                                        "old_location": existing_location["location"],
                                        "old_direction": existing_location["direction"]
                                    }
                                )
                                updated_rows += 1

                skipped_rows = len(combined_df) - new_rows - updated_rows

                # Refresh the in-memory cache
                self.location_df = pd.read_sql(f"SELECT * FROM {WAREHOUSE_SCHEMA}.dim_location", self.engine)
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Loaded dim_location table\033[0m")
                print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: New rows inserted: {new_rows}, Updated: {updated_rows}, Skipped: {skipped_rows}\033[0m")
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Error loading dim_location table: {e}\033[0m")
            raise

    def load_fact_vehicle_count(self, df):
        try:
            # Convert date and time columns to appropriate formats
            df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
            df["time"] = pd.to_datetime(df["time"].astype(str), errors="coerce").dt.time
            
            self.date_df["full_date"] = pd.to_datetime(self.date_df["full_date"], errors="coerce").dt.date
            self.time_df["full_time"] = pd.to_datetime(self.time_df["full_time"].astype(str), format='%H:%M:%S', errors="coerce").dt.time
            
            # Merge dataframes to get the fact data
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

            fact_df.rename(columns={"location_id_y": "location_id"}, inplace=True)

            fact_df = fact_df[[
                "date_id", "time_id", "location_id",
                "car", "motorcycle", "bike", "truck", "bus",
                "n", "s", "e", "w", "ne", "nw", "se", "sw"
            ]]
            
            with self.engine.begin() as conn:
                # Check if the fact table is empty
                existing_combinations = pd.read_sql(
                    f"SELECT date_id, time_id, location_id FROM {WAREHOUSE_SCHEMA}.fact_vehicle_counts", conn
                )
                
                if existing_combinations.empty:
                    # First insertion into an empty fact table
                    print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: First insertion.\033[0m")
                    for _, row in fact_df.iterrows():  # Use fact_df directly here
                        conn.execute(
                            text(f"""
                                INSERT INTO {WAREHOUSE_SCHEMA}.fact_vehicle_counts (
                                    date_id, time_id, location_id,
                                    car, motorcycle, bike, truck, bus,
                                    n, s, e, w, ne, nw, se, sw
                                ) VALUES (
                                    :date_id, :time_id, :location_id,
                                    :car, :motorcycle, :bike, :truck, :bus,
                                    :n, :s, :e, :w, :ne, :nw, :se, :sw
                                );
                            """),
                            row.to_dict()
                        )
                    
                    print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Inserted {len(fact_df)} new records into fact_vehicle_counts\033[0m")
                else:
                    # If the fact table has data, check for conflicts
                    print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Checking for conflicts.\033[0m")
                    
                    # Create a composite key column to check for existing records
                    fact_df['composite_key'] = fact_df['date_id'].astype(str) + '_' + \
                                            fact_df['time_id'].astype(str) + '_' + \
                                            fact_df['location_id'].astype(str)
                    
                    existing_combinations['composite_key'] = existing_combinations['date_id'].astype(str) + '_' + \
                                                            existing_combinations['time_id'].astype(str) + '_' + \
                                                            existing_combinations['location_id'].astype(str)
                    
                    # Identify new records by checking which composite keys are not in the existing combinations
                    new_records = fact_df[~fact_df['composite_key'].isin(existing_combinations['composite_key'])]
                    
                    # Drop the composite_key column for the final insert
                    new_records = new_records.drop(columns=['composite_key'])
                    
                    if not new_records.empty:
                        # Insert new records without conflict (conflict check is already handled)
                        for _, row in new_records.iterrows():
                            conn.execute(
                                text(f"""
                                    INSERT INTO {WAREHOUSE_SCHEMA}.fact_vehicle_counts (
                                        date_id, time_id, location_id,
                                        car, motorcycle, bike, truck, bus,
                                        n, s, e, w, ne, nw, se, sw
                                    ) VALUES (
                                        :date_id, :time_id, :location_id,
                                        :car, :motorcycle, :bike, :truck, :bus,
                                        :n, :s, :e, :w, :ne, :nw, :se, :sw
                                    )
                                    ON CONFLICT (date_id, time_id, location_id) DO NOTHING;
                                """),
                                row.to_dict()
                            )

                        print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Inserted {len(new_records)} new records into fact_vehicle_counts\033[0m")
                    else:
                        print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No new records to insert\033[0m")
            
            return fact_df
        except Exception as e:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Error loading fact table: {str(e)}\033[0m")
            raise
