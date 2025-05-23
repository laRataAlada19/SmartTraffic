import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG_neon_tech, DATABASE_SCHEMA,direction_summary
from datetime import datetime
from collections import Counter

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG_neon_tech)
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.connection = None

    def execute_query(self, query, params=None):
        if not self.connection:
            print("Conexão não estabelecida. Chame o método connect() primeiro.")
            return None
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            print(f"Erro ao executar a query: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")
    
    def exists_result(self, timestamp, camera):
        try:
            conn = psycopg2.connect(**DB_CONFIG_neon_tech)
            cur = conn.cursor()

            query = f"""
            SELECT COUNT(*) FROM {DATABASE_SCHEMA}.vehicle_counts 
            WHERE timestamp = %s AND location_id = 8
            """
            cur.execute(query, (timestamp, camera))
            result = cur.fetchone()[0]
            
            cur.close()
            conn.close()

            return result > 0
        except Exception as e:
            print(f"Erro ao verificar existência de dados: {e}")
            return False

    def save_results_to_bd(self, class_counter, total_class_counter, timestamp, camera):
        try:
            from collections import Counter

            self.connect()

            # Inicializa os contadores de direção
            final_directions = {"N": 0, "S": 0, "E": 0, "W": 0, "NE": 0, "NW": 0, "SE": 0, "SW": 0}

            # Conta a direção mais comum de cada track
            for track_id, direction in direction_summary.items():
                if direction:
                    final_directions[direction] += 1

            # Atualiza o total acumulado por tipo de veículo
            for vehicle_type, count in class_counter.items():
                total_class_counter[vehicle_type] += count
                
            query = f"""
                INSERT INTO {DATABASE_SCHEMA}.vehicle_counts (
                    car, motorcycle, bike, truck, bus,
                    n, s, e, w, ne, nw, se, sw,
                    timestamp, location_id
                ) VALUES (%s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, 3)
            """

            params = (
                class_counter.get("car", 0),
                class_counter.get("motorcycle", 0),
                class_counter.get("bike", 0),
                class_counter.get("truck", 0),
                class_counter.get("bus", 0),
                final_directions["N"],
                final_directions["S"],
                final_directions["E"],
                final_directions["W"],
                final_directions["NE"],
                final_directions["NW"],
                final_directions["SE"],
                final_directions["SW"],
                timestamp
            )

            self.execute_query(query, params)
            self.close()
            print(f"[{timestamp}] Dados salvos para câmara '{camera}' com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar resultados no banco de dados: {e}")