from flask import Flask, render_template, request
import requests

imt_value = 0
pressure_value = 0

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template("input_form.html")

def imt(weight, height):    
    response_imt = requests.get(f'http://imt-service-container/imt?weight={weight}&height={height}')                               
    imt_value = response_imt.text    
    return imt_value

def pressure(id):   
    response_pressure = requests.get(f'http://pressure-service-container/pressure?id={id}')
    pressure_value = response_pressure.text
    return pressure_value

def save_data(id,age,pressure,weight,height,imt,risk):
    response_data = requests.get(f'http://db-service-container/save_data?id={id}&age={age}&pressure={pressure}&weight={weight}&height={height}&imt={imt}&risk={risk}')
    inserted_user = response_data.text

    return inserted_user

@app.route('/find_data', methods=["POST"])
def find_data():
    id_value = int (request.form["find_id"])
    response_data = requests.get(f'http://db-service-container/find_data?id={id_value}')
    find_user = response_data.text

    return render_template("find_form.html", user=find_user)

@app.route('/', methods=["POST"])

def result():
    try:
        id_value = int (request.form["identifier"])
        age_value = int (request.form["age"])
        weight_value = float (request.form["weight"])
        height_value = float (request.form["height"])
    except ValueError:
        return "Заполнены не все поля!"

    imt_value = float (imt (weight_value, height_value))
    pressure_value = int (pressure(id_value))

    if pressure_value > 140:
        if (imt_value > 35 and age_value > 30):
            risk = 'высокий риск инфаркта' 
        elif (imt_value > 30 and age_value <= 30): 
            risk = 'средний риск инфаркта'
        else:
            risk = 'низкий риск инфаркта'
    elif pressure_value > 130:
        if (imt_value > 40 and age_value >= 25):
            risk = 'высокий риск инфаркта' 
        elif (imt_value > 30 and age_value >= 30): 
            risk = 'средний риск инфаркта'
        else:
            risk = 'низкий риск инфаркта'
    else:
        risk = 'низкий риск инфаркта'   

    save_data(id_value,age_value,pressure_value,weight_value,height_value,imt_value,risk)
    
    return render_template("result_form.html", 
                           imt_result=imt_value, pressure_result=pressure_value, risk_result=risk, age=age_value)

app.run(host='0.0.0.0', port=80)