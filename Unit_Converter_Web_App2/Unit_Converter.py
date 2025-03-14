import webbrowser
import threading
from flask import Flask, request, render_template

app = Flask(__name__, static_folder='static')

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

threading.Timer(1.25, open_browser).start() # Timer delay to allow Flask to start

def convert_length(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value # If same unit, return the same value
    conversion_factors = {
        'millimeter': 0.001, 'centimeter': 0.01, 'meter': 1, 'kilometer': 1000,
        'inch': 0.0254, 'foot': 0.3048, 'yard': 0.9144, 'mile': 1609.34
    }
    return value * (conversion_factors[from_unit] / conversion_factors[to_unit])

def convert_weight(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value # If same unit, return the same value
    conversion_factors = {
        'milligram': 0.001, 'gram': 1, 'kilogram': 1000, 'ounce': 28.3495, 'pound': 453.592
    }
    return value * (conversion_factors[from_unit] / conversion_factors[to_unit])

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value # If same unit, return the same value
    if from_unit == 'Celsius':
        return value * 9/5 + 32 if to_unit == 'Fahrenheit' else value + 273.15
    if from_unit == 'Fahrenheit':
        return (value - 32) * 5/9 if to_unit == 'Celsius' else (value - 32) * 5/9 + 273.15
    if from_unit == 'Kelvin':
        return value - 273.15 if to_unit == 'Celsius' else (value - 273.15) * 9/5 + 32
    return value

@app.route('/')
def home():
    return render_template('index.html', result=None)

@app.route('/convert', methods=['POST'])
def convert():
    value = float(request.form['value'])
    from_unit = request.form['from_unit']
    to_unit = request.form['to_unit']
    category = request.form['category']

    if category == 'length':
        result = convert_length(value, from_unit, to_unit)
    elif category == 'weight':
        result = convert_weight(value, from_unit, to_unit)
    elif category == 'temperature':
        result = convert_temperature(value, from_unit, to_unit)
    else:
        result = "Invalid category"

    return render_template('index.html', result=result, value=value, from_unit=from_unit, to_unit=to_unit, category=category)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)