from flask import Flask, request
import pymongo

# устанавливаем соединение с MongoDB, 27017 - стандартный порт
db_client = pymongo.MongoClient("mongodb://mongodb-container:27017/")  # или так MongoClient('localhost', 27017)

# подключаемся к БД patientsdb, если её нет, то будет создана
patients_db = db_client["patientsdb"] 

# получаем колекцию из нашей БД, если её нет, то будет создана
# Коллекция - это группа документов, которая хранится в БД MongoDB (эквалент таблицы в ркляционных базах)
collection = patients_db["parameters"]

imt_value = 0
pressure_value = 0

app = Flask(__name__)

@app.route('/save_data')
def save ():
    
    id = int (request.args.get('id'))
    age = int (request.args.get('age'))
    pressure = int (request.args.get('pressure'))
    weight = float (request.args.get('weight'))
    height = float (request.args.get('height'))
    imt = float (request.args.get('imt'))
    risk = request.args.get('risk') 

    if collection.find_one({'ID': id}) is None:
        user = {
            'ID': id,
            'age': age,
            'pressure': pressure,
            'weight': weight,
            'height': height,
            'imt': imt,
            'risk': risk
        }
        insert_result = collection.insert_one(user)  # добавляет одну запись в коллекцию collection
    else:  
        insert_result = collection.update_one({'ID': id}, { '$set': {
            'age': age,
            'pressure': pressure,
            'weight': weight,
            'height': height,
            'imt': imt,
            'risk': risk
                        }}
        )
    return insert_result["ID"]

@app.route('/find_data')
def find ():
    id = int (request.args.get('id'))
    user = collection.find_one({'ID': id}, {'_id': False})
    return f'{user}'

app.run(host='0.0.0.0', port=80)