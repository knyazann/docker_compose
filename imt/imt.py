from flask import Flask, request

app = Flask(__name__)

@app.route('/imt')
def calculate_imt():
    weight = request.args.get('weight')
    if weight and weight != '':
        weight = request.args.get('weight', default=1, type=float)
        height = request.args.get('height', default=1, type=float) / 100

        imt_value = round(weight / height**2, 2)

        return f"{imt_value}"
    else:
        return "error"   

app.run(host='0.0.0.0', port=80)

