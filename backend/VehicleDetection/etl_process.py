import luigi
from warehouse import Warehouse
import pandas as pd
import os

#pip install luigi
#pip install pandas

dw = Warehouse()

class ExtractTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget('data/extracted.csv') 

    def run(self):
        # Ensure the directory exists
        output_path = os.path.dirname(self.output().path)
        os.makedirs(output_path, exist_ok=True)

        dw.connect_db()
        data = dw.extract_data()
        
        if data is not None and not data.empty:
            with open(self.output().path, 'w', encoding='utf-8') as f:
                data.to_csv(f, index=False)
                print(f"DEBUG: Extracted data written successfully")
        else:
            print("DEBUG: No data to write to file.")
        
class TransformTask(luigi.Task):
    def requires(self):
        return ExtractTask()

    def output(self):
        return luigi.LocalTarget('data/transformed.csv')
    
    def run(self):
        with self.input().open('r') as f:
            extracted_data = pd.read_csv(f)

        extracted_data = dw.transform_data(extracted_data)
        
        if extracted_data is not None and not extracted_data.empty:
            with open(self.output().path, 'w', encoding='utf-8') as f:
                extracted_data.to_csv(f, index=False)
                print(f"DEBUG: Transformed data written successfully")
        else:
            print("DEBUG: No transformed data to write to file.")
        
class LoadTask(luigi.Task):
    def requires(self):
        return TransformTask()

    def run(self):
        dw.connect_dw()
        
        with self.input().open('r') as f:
            transformed_data = pd.read_csv(f)

        if transformed_data is not None and not transformed_data.empty:
            dw.load_dim_date(transformed_data)
            dw.load_dim_time(transformed_data)
            dw.load_dim_location(transformed_data)
            loaded_data = dw.load_fact_vehicle_count(transformed_data)
            #print(f"DEBUG: Loaded Data: \n{loaded_data}")
            print("INFO: Data loaded successfully")
        else:
            print("DEBUG: No data to load.")
        
        dw.close_dw()
        
if __name__ == '__main__':
    luigi.run(main_task_cls=LoadTask)

# luigid -> para iniciar o servidor 
# http://localhost:8082/ -> para acessar o servidor