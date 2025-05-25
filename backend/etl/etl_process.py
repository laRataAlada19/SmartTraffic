import luigi
from warehouse import Warehouse
import pandas as pd
import os
from datetime import datetime

dw = Warehouse()

#path = "/app/data/"
path = "backend/etl/data/"

class ExtractTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(path+'extracted.csv')

    def complete(self):
        # Only consider complete if file exists and was modified recently
        if not os.path.exists(self.output().path):
            return False
        file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(self.output().path))

        print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: file location: {os.path.abspath(self.output().path)}\033[0m")
        return file_age.total_seconds() < 60  # Consider stale after 1 minute

    def run(self):
        os.makedirs(os.path.dirname(self.output().path), exist_ok=True)

        print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Starting extraction...\033[0m")
        dw.connect_db()
        data, updates = dw.extract_data(path)
        dw.close_db()

        if data is not None and not data.empty:
            data.to_csv(self.output().path, index=False, encoding='utf-8')
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Extracted data written successfully\033[0m")
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Updated records: {updates}\033[0m")
        else:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No new data(inserts) to extract. Task will complete with empty output. But if applicable, will still update the dimensions.\033[0m")
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Updated records: {updates}\033[0m")
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
        print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Starting transformation...\033[0m")
        try:
            with self.input().open('r') as f:
                extracted_data = pd.read_csv(f)
        except pd.errors.EmptyDataError:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Extracted file is empty.\033[0m")
            extracted_data = pd.DataFrame()

        # Always run transform_data() even if extracted_data is empty, because self.location_df might not be
        transformed_data, transformed_locations = dw.transform_data(extracted_data)

        if not transformed_data.empty:
            transformed_data.to_csv(self.output().path, index=False, encoding='utf-8')
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Transformed data written successfully.\033[0m")
        else:
            transformed_data.to_csv(self.output().path, index=False, encoding='utf-8')
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No data to transform, empty transformed data file written.\033[0m")
            
        if not transformed_locations.empty:
            transformed_locations.to_csv(path + 'transformed_locations.csv', index=False, encoding='utf-8')
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Transformed locations written successfully\033[0m")
        else:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No new location data to transform.\033[0m")

class LoadTask(luigi.Task):
    def requires(self):
        return TransformTask()

    def complete(self):
        return False  # Always run

    def run(self):
        print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: Starting load process...\033[0m")
        dw.connect_dw()
        
        try:
            with self.input().open('r') as f:
                transformed_data = pd.read_csv(f)
        except pd.errors.EmptyDataError:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: transformed_to_fact_table file is empty. Will only load updated locations if available.\033[0m")
            transformed_data = pd.DataFrame()

        # Always attempt to load updated dimensions
        dw.load_dim_location(transformed_data)
        if not transformed_data.empty:
            dw.load_dim_date(transformed_data)
            dw.load_dim_time(transformed_data)
            dw.load_fact_vehicle_count(transformed_data)
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: All data loaded successfully\033[0m")
        else:
            print(f"\033[92m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CUSTOM: No vehicle count data to load. Only dimension 'location' was updated.\033[0m")

        dw.close_dw()

if __name__ == '__main__':
    # Force clean the output files to ensure fresh run
    for f in [path+'extracted.csv', path+'transformed_to_fact_table.csv', path+'transformed_locations.csv']:
        if os.path.exists(f):
            os.remove(f)
    
    luigi.run(main_task_cls=LoadTask, local_scheduler=True)

# luigid -> para iniciar o servidor 
# http://localhost:8082/ -> para acessar o servidor