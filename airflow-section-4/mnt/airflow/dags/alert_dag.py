from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


def on_success_dag(dict):
    print("on success dag")
    print(dict)

def on_failure_dag(dict):
    print("on failure dag")
    print(dict)

def on_success_task(dict):
    print("on success task")
    print(dict)

def on_failure_task(dict):
    print("on failure task")
    print(dict)


default_args = {
    'start_date': datetime(2020, 4, 12),
    'owner': 'Airflow',
    'retries': 3,
    'retries_delay': timedelta(seconds=10),
    'emails': ['myemail@email.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'on_failure_callback': on_failure_task,
    'on_success_callback': on_success_task
    }


with DAG(dag_id='alert_dag',
         schedule_interval="0 0 * * *",
         default_args=default_args,
         catchup=True,
         on_failure_callback=on_failure_dag,
         on_success_callback=on_success_dag) as dag:
    
    # Task 1
    t1 = BashOperator(task_id='t1',
                      bash_command="exit 1")
    # t1 = BashOperator(task_id='t1', bash_command="echo 'first task'")
    
    # Task 2
    t2 = BashOperator(task_id='t2',
                      bash_command="echo 'second task'")

    t1 >> t2