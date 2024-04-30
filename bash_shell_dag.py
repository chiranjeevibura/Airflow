from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 29),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'run_unix_script',
    default_args=default_args,
    description='A DAG to run a Unix shell script',
    schedule_interval=timedelta(days=1),  # Run the DAG daily
)

# Define the task
run_script_task = BashOperator(
    task_id='run_unix_script',
    bash_command='/path/to/your/script.sh',  # Specify the path to your shell script
    dag=dag,
)

# Define task dependencies
run_script_task
