import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG_neon_tech, DATABASE_SCHEMA,direction_summary
from datetime import datetime
from collections import Counter

class Database:
    def __init__(self):
        self.connection = None

    def log(self, message, level="INFO"):
        colors = {
            "INFO": "\033[92m",     # green
            "WARNING": "\033[93m",  # yellow
            "ERROR": "\033[91m",    # red
        }
        color = colors.get(level.upper(), "\033[0m")
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"{color}{timestamp} [{level.upper()}] {message}\033[0m\n", end="")

    def connect(self):
        try:
            self.connection = psycopg2.connect(**DB_CONFIG_neon_tech)
            self.log("Conexão com o banco de dados estabelecida com sucesso.")
        except Exception as e:
            self.log(f"Erro ao conectar ao banco de dados: {e}", level="ERROR")
            self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()
            self.log("Conexão com o banco de dados fechada.")

    def execute_query(self, query, params=None):
        try:
            if not self.connection:
                self.log("Conexão com o banco de dados não está disponível.", level="ERROR")
                return None
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.log(f"Erro ao executar a query: {e}", level="ERROR")
            return None
    
    def exists_result(self, timestamp, location_id):
        try:
            query = f"""
                SELECT COUNT(*) FROM {DATABASE_SCHEMA}.vehicle_counts 
                WHERE timestamp = %s AND location_id = %s
            """
            
            result = self.execute_query(query, (timestamp, location_id))

            return result[0]['count'] > 0 
        except Exception as e:
            self.log(f"Erro ao verificar a existência de resultados: {e}", level="ERROR")
            return False
        
    def get_location_direction(self, location_id):
        try:
            print(f"Obtendo direção para a localização id: {location_id}")
            query = f"""
                SELECT direction FROM {DATABASE_SCHEMA}.locations 
                WHERE location_id = %s
            """
            
            result = self.execute_query(query, (location_id,))

            # Retornar a direção, se encontrada
            if result:
                return result[0]['direction'].upper()  # A direção está no primeiro índice do resultado
            else:
                self.log(f"Nenhuma direção encontrada para a localização id '{location_id}'", level="WARNING")
                return None
        except Exception as e:
            self.log(f"Erro ao obter a direção da localização: {e}", level="ERROR")
            return None

    def verify_id(self,location_id):
        query = f"""
            SELECT location_id FROM {DATABASE_SCHEMA}.locations WHERE location_id = %s
        """
        id = self.execute_query(query, (location_id,))
        if id:
            return id[0]['location_id']  # buscar so o id
        else:
            print(f"Nenhuma localização encontrada com id '{location_id}'.")
            return None

    def save_results_to_bd(self, class_counter, total_class_counter, timestamp, location_id):
        try:
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
                    %s, %s)
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
                timestamp,
                location_id
            )

            self.execute_query(query, params)
            self.log(f"Resultados salvos no banco de dados para a localização id '{location_id}' com timestamp '{timestamp}'.")
        except Exception as e:
            self.log(f"Erro ao salvar resultados para a localização id '{location_id}' no banco de dados: {e}", level="ERROR")
            return False
        return True