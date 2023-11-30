from flask import Flask, jsonify
import mysql.connector
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app = Flask(__name__)
config = {
  "user": os.environ.get("CONTRACT_USER") or "wedeliver",
  "password": os.environ.get("CONTRACT_PASSWORD") or "We@2468",
  "host": os.environ.get("CONTRACT_HOST") or "db4free.net",
  "port": os.environ.get("CONTRACT_PORT") or "3306",
  "database": os.environ.get("CONTRACT_DATABASE") or "WeDeliver",
  'auth_plugin': 'mysql_native_password'
}
print(config,flush=True)
print("---3--",flush=True)
print(os.environ.get("CONTRACT_USER"),flush=True)

def contracts_data():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT customer_id, vehicle_id, lease_start_date, lease_end_date, price_per_day '
                   ' FROM contracts_data')
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

@app.route('/')
def index():
    return jsonify({'Contracts Data': contracts_data()})

@app.route("/api/sayHello")
def hello():
    return "Hello, Welcome to Contract Service"

@app.route('/api/get_current_contracts', methods=['GET'])
def get_current_contracts():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(dictionary=True)
    query = ("select * from (SELECT customer_id, vehicle_id, price_per_day, "
             " DATEDIFF(if(lease_end_date > LAST_DAY(NOW()),LAST_DAY(NOW()),lease_end_date )"
             " ,if(lease_start_date > LAST_DAY(NOW()),lease_start_date,DATE_FORMAT(NOW(), '%Y-%m-01') )) "
             " AS number_of_days " 
             " FROM contracts_data )as t where t.number_of_days > 0; ")
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    data = {'invoices_num': 0}
    if results:
        data['invoices_num'] = len(results)
        data['invoices'] = results
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)