import luigi
from warehouse import Warehouse
import pandas as pd
import os
from datetime import datetime

dw = Warehouse()

path = "backend/VehicleDetection/data/"

class ExtractTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(path+'extracted.csv')

    def complete(self):
        # Only consider complete if file exists and was modified recently
        if not os.path.exists(self.output().path):
            return False
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(self.output().path))

        print(f"CUSTOM: file location: {os.path.abspath(self.output().path)}")
        return file_age.total_seconds() < 60  # Consider stale after 1 minute

    def run(self):
        os.makedirs(os.path.dirname(self.output().path), exist_ok=True)

        print("CUSTOM: Starting extraction...")
        dw.connect_db()
        data = dw.extract_data()
        dw.close_db()

        if data is not None and not data.empty:
            data.to_csv(self.output().path, index=False, encoding='utf-8')
            print("CUSTOM: Extracted data written successfully")
        else:
            raise Exception("CUSTOM: No data extracted!")

class TransformTask(luigi.Task):
    def requires(self):
        return ExtractTask()

    def output(self):
        return luigi.LocalTarget(path+'transformed.csv')

    def complete(self):
        # Only complete if output exists and is newer than input
        if not os.path.exists(self.output().path):
            return False
        
        input_mtime = os.path.getmtime(self.input().path)
        output_mtime = os.path.getmtime(self.output().path)
        return output_mtime > input_mtime

    def run(self):
        print("CUSTOM: Starting transformation...")
        with self.input().open('r') as f:
            extracted_data = pd.read_csv(f)

        transformed_data = dw.transform_data(extracted_data)
        
        if transformed_data is not None and not transformed_data.empty:
            transformed_data.to_csv(self.output().path, index=False, encoding='utf-8')
            print("CUSTOM: Transformed data written successfully")
        else:
            raise Exception("CUSTOM: Transformation failed!")

class LoadTask(luigi.Task):
    def requires(self):
        return TransformTask()

    def complete(self):
        # LoadTask has no output, so it should always run
        return False

    def run(self):
        print("CUSTOM: Starting load process...")
        dw.connect_dw()
        
        with self.input().open('r') as f:
            transformed_data = pd.read_csv(f)

        if transformed_data is not None and not transformed_data.empty:
            dw.load_dim_date(transformed_data)
            dw.load_dim_time(transformed_data)
            dw.load_dim_location(transformed_data)
            dw.load_fact_vehicle_count(transformed_data)
            print("CUSTOM: Data loaded successfully")
        else:
            raise Exception("CUSTOM: No data to load!")
        
        dw.close_dw()

if __name__ == '__main__':
    # Force clean the output files to ensure fresh run
    for f in [path+'extracted.csv', path+'transformed.csv']:
        if os.path.exists(f):
            os.remove(f)
    
    luigi.run(main_task_cls=LoadTask, local_scheduler=True)

# luigid -> para iniciar o servidor 
# http://localhost:8082/ -> para acessar o servidor