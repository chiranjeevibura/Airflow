from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Define functions for tasks

def produce_output():
    # Logic to produce output
    output_data = "Hello, world!"
    return output_data

def consume_output(**kwargs):
    # Access output produced by the previous task
    ti = kwargs['ti']
    output_data = ti.xcom_pull(task_ids='produce_output')
    print("Output from the previous task:", output_data)
    # Use the output_data in this task as needed

# Define DAG parameters
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'xcom_example_dag',
    default_args=default_args,
    description='Example DAG demonstrating the use of XCom',
    schedule_interval=timedelta(days=1),  # Run the DAG daily
    start_date=datetime(2024, 1, 1),
    catchup=False,  # Don't run past DAG runs
)

# Define tasks
produce_output_task = PythonOperator(
    task_id='produce_output',
    python_callable=produce_output,
    dag=dag
)

consume_output_task = PythonOperator(
    task_id='consume_output',
    python_callable=consume_output,
    provide_context=True,  # Allow access to the context parameter
    dag=dag
)

# Define task dependencies
produce_output_task >> consume_output_task
