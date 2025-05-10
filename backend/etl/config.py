
#DW_CONFIG = {
 #   "dbname": "warehouse_vehicle_count_db",
  # "password": "123",
   # "port": "5432",
    #"host": "host.docker.internal"
#}

#DB_CONFIG = {
 #   "dbname": "vehicle_detection",
  #  "user": "user",
   # "password": "123",
    #"port": "5432",
    #"host": "host.docker.internal"
#}

DB_CONFIG_neon_tech = {
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_o1YqvCrGuK5O",
    "port": "5432",
    "host": "ep-damp-sunset-a2kojsnk-pooler.eu-central-1.aws.neon.tech"
}

DATABASE_SCHEMA = "vehicle_detection"
WAREHOUSE_SCHEMA = "warehouse_vehicle_count_db"


#postgresql://neondb_owner:npg_o1YqvCrGuK5O@ep-damp-sunset-a2kojsnk-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require