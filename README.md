# Projeto Informático 2 - SmartTraffic

## 📝 Descrição
O **SmartTraffic** é um sistema inteligente para **detecção, rastreamento e análise de veículos**, utilizando visão computacional e machine learning. Os dados são armazenados numa base de dados relacional e num data warehouse, permitindo análises avançadas através de dashboards interativos.

## 🚀 Funcionalidades Principais
- 🎥 Detecção em tempo real de veículos (carros, motas, camiões, autocarros, bicicletas, etc.)
- 🧭 Análise de direção e velocidade dos veículos
- ⚠️ Alerta de excesso de velocidade
- 💾 Armazenamento em base de dados operacional e data warehouse
- 📊 Dashboard analítico para visualização de métricas e tendências

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.12** (Flask, YOLOv8, OpenCV, Psycopg2)
- **Laravel** (API RESTful)
- **PostgreSQL** (Base de dados operacional e Data Warehouse)

### Frontend
- **Vue.js 3** + Pinia
- **Leaflet** (Mapas interativos)
- **Chart.js** (Visualização de dados)

### Infraestrutura
- **Docker** + Docker Compose
- **ETL** automatizado (para processamento e integração de dados)

## ✅ Requisitos

### Ambiente de Desenvolvimento
- Docker 20 ou superior
- Docker Compose 2+
- Node.js 16 ou superior
- Python 3.8+
- PostgreSQL 15+

### Ambiente de Produção
- GPU NVIDIA (recomendado para melhor performance do YOLO)
- Mínimo 8GB de RAM

## 🔧 Instalação

```bash
git clone https://github.com/laRataAlada19/SmartTraffic.git
cd projeto_informatico2

# Iniciar os containers
docker compose up -d
```

## 🗂 Estrutura da Base de Dados Operacional

```sql
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    direction VARCHAR(50) NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE vehicle_counts (
    id SERIAL PRIMARY KEY,
    car INT,
    motorcycle INT,
    bike INT,
    truck INT,
    bus INT,
    n INT,
    s INT,
    e INT,
    w INT,
    ne INT,
    nw INT,
    se INT,
    sw INT,
    timestamp TIMESTAMP,
    location_id INT NOT NULL,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_location_modtime
BEFORE UPDATE ON locations
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## 🧱 Estrutura do Data Warehouse

```sql
CREATE TABLE dim_location (
    location_id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    location_old VARCHAR(100),
    direction VARCHAR(50) NOT NULL,
    direction_old VARCHAR(50)
);

CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    full_time TIME UNIQUE NOT NULL,
    hour INT,
    minute INT,
    period VARCHAR(10)
);

CREATE TABLE dim_date (
    date_id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT,
    month INT,
    day INT,
    weekday VARCHAR(20)
);

CREATE TABLE fact_vehicle_counts (
    id SERIAL PRIMARY KEY,
    date_id INT NOT NULL,
    time_id INT NOT NULL,
    location_id INT NOT NULL,
    car INT DEFAULT 0,
    motorcycle INT DEFAULT 0,
    bike INT DEFAULT 0,
    truck INT DEFAULT 0,
    bus INT DEFAULT 0,
    n INT DEFAULT 0,
    s INT DEFAULT 0,
    e INT DEFAULT 0,
    w INT DEFAULT 0,
    ne INT DEFAULT 0,
    nw INT DEFAULT 0,
    se INT DEFAULT 0,
    sw INT DEFAULT 0,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id)
);
```

## ⚙️ Processo ETL

Para monitorizar o processo ETL:
```bash
docker exec -it etl bash
tail -f /var/log/cron_etl.log
```

## 🌐 Aplicações Disponíveis

| Aplicação         | URL                     |
|-------------------|--------------------------|
| Backend (API)     | http://localhost:8000    |
| Frontend (Vue.js) | http://localhost:8001    |

## 📦 Instalação de Dependências

### Frontend
```bash
npm install vue@3 pinia vue-router axios leaflet @vue-leaflet/vue-leaflet chart.js vue-chartjs dayjs xlsx html2canvas jspdf
```

### Backend (Python)
```bash
pip install ultralytics opencv-python flask flask-cors psycopg2-binary numpy
```

### Backend (Laravel)
```bash
composer require fruitcake/laravel-cors
```

### Câmaras (Servidor local)
```bash
pip install flask flask-cors
```

## 🐳 Comandos Docker Úteis

| Comando                              | Descrição                                |
|--------------------------------------|------------------------------------------|
| `docker compose up --build`          | Reconstruir e iniciar os containers      |
| `docker exec -it vehicle_detection bash` | Aceder ao container da deteção       |
| `docker logs -f etl`                 | Ver os logs do processo ETL              |
