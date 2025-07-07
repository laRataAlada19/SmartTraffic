from etl_process import ExtractTask, TransformTask, LoadTask
import os

def test_ExtractTask():
    task = ExtractTask()
    
    # output taks test
    assert task.output().path == 'backend/etl/data/extracted.csv', "Output path should be 'backend/etl/data/extracted.csv'"

    # complete task test
    if os.path.exists(task.output().path):
        os.remove(task.output().path)
        
    assert not task.complete(), "Task should not be complete if output file does not exist"

test_ExtractTask()