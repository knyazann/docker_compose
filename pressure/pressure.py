import random
from flask import Flask

app = Flask(__name__)

@app.route('/pressure')
def calculate_pressure():
    
    pressure_value = random.randint(95, 165) 
    return f"{pressure_value}"

app.run(host='0.0.0.0', port=80)
