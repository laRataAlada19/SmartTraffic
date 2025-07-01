import luigi
from warehouse import Warehouse
import pandas as pd
import os
from datetime import datetime

dw = Warehouse()

#path = "/app/data/"
path = "backend/etl/data/"

def log(message, level="INFO"):
    colors = {
        "INFO": "\033[92m",     # green
        "WARNING": "\033[93m",  # yellow
        "ERROR": "\033[91m",    # red
    }
    color = colors.get(level.upper(), "\033[0m")
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{color}{timestamp} [{level.upper()}] {message}\033[0m\n", end="")

class ExtractTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(path+'extracted.csv')

    def complete(self):
        # Only consider complete if file exists and was modified recently
        if not os.path.exists(self.output().path):
            log(f"ExtractTask: Output file {self.output().path} does not exist.", level="WARNING")
            log(f"ExtractTask: Task will run to extract data.")
            return False
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(self.output().path))

        log(f"ExtractTask: file location: {os.path.abspath(self.output().path)}")
        return file_age.total_seconds() < 60  # Consider stale after 1 minute

    def run(self):
        os.makedirs(os.path.dirname(self.output().path), exist_ok=True)

        log(f"ExtractTask: Starting extraction...")
        dw.connect_db()
        data, updates = dw.extract_data(path)
        dw.close_db()

        if data is not None and not data.empty:
            data.to_csv(self.output().path, index=False, encoding='utf-8')
            log(f"ExtractTask: Extracted data written successfully.")
            log(f"ExtractTask: Updated records: {updates}")
        else:
            log(f"ExtractTask: No new data(inserts) to extract. Task will complete with empty output. But if applicable, will still update the dimensions.", level="WARNING")
            log(f"ExtractTask: Updated records: {updates}")
            # Still touch the output to signal task completion
            pd.DataFrame().to_csv(self.output().path, index=False)

class TransformTask(luigi.Task):
    def requires(self):
        return ExtractTask()

    def output(self):
        return luigi.LocalTarget(path + 'transformed_to_fact_table.csv')

    def complete(self):
        if not os.path.exists(self.output().path):
            return False
        
        input_mtime = os.path.getmtime(self.input().path)
        output_mtime = os.path.getmtime(self.output().path)
        return output_mtime > input_mtime

    def run(self):
        log(f"TransformTask: Starting transformation...")
        try:
            with self.input().open('r') as f:
                extracted_data = pd.read_csv(f)
        except pd.errors.EmptyDataError:
            log(f"TransformTask: Extracted file is empty.", level="WARNING")
            extracted_data = pd.DataFrame()

        # Always run transform_data() even if extracted_data is empty, because self.location_df might not be
        transformed_data, transformed_locations = dw.transform_data(extracted_data)

        if not transformed_data.empty:
            transformed_data.to_csv(self.output().path, index=False, encoding='utf-8')
            log(f"TransformTask: Transformed data written successfully.")
        else:
            transformed_data.to_csv(self.output().path, index=False, encoding='utf-8')
            log(f"TransformTask: No data to transform, empty transformed data file written.", level="WARNING")
            
        if not transformed_locations.empty:
            transformed_locations.to_csv(path + 'transformed_locations.csv', index=False, encoding='utf-8')
            log(f"TransformTask: Transformed locations written successfully.")
        else:
            log(f"TransformTask: No new location data to transform, empty transformed locations file written.", level="WARNING")

class LoadTask(luigi.Task):
    def requires(self):
        return TransformTask()

    def complete(self):
        return False  # Always run

    def run(self):
        log(f"LoadTask: Starting load process...")
        dw.connect_dw()
        
        try:
            with self.input().open('r') as f:
                transformed_data = pd.read_csv(f)
        except pd.errors.EmptyDataError:
            log(f"LoadTask: transformed_to_fact_table file is empty. Will only load updated locations if available.", level="WARNING")
            transformed_data = pd.DataFrame()

        # Always attempt to load updated dimensions
        dw.load_dim_location(transformed_data)
        if not transformed_data.empty:
            dw.load_dim_date(transformed_data)
            dw.load_dim_time(transformed_data)
            dw.load_fact_vehicle_count(transformed_data)
            log(f"LoadTask: Data loaded successfully.")
        else:
            log(f"LoadTask: No vehicle count data to load. Only dimension 'location' was updated.", level="WARNING")

        dw.close_dw()

if __name__ == '__main__':
    # Force clean the output files to ensure fresh run
    for f in [path+'extracted.csv', path+'transformed_to_fact_table.csv', path+'transformed_locations.csv']:
        if os.path.exists(f):
            os.remove(f)
    
    luigi.run(main_task_cls=LoadTask, local_scheduler=True)

# luigid -> para iniciar o servidor 
# http://localhost:8082/ -> para acessar o servidor