# app.py
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random
import time

app = Flask(__name__)


class MockScanner:
    def __init__(self):
        self.scanning = False
        self.scan_count = 0
        self.products = [
            {'name': 'Venta Glove', 'price': 90.00, 'color': 'Black'},
            {'name': 'Beta Jacket', 'price': 600.00, 'color': 'Dynasty'},
            {'name': 'Atom LT Hoody', 'price': 260.00, 'color': 'Black'}
        ]
        self.sizes = ['XS', 'S', 'M', 'L', 'XL']
        self.statuses = [
            'Scanning',
            'Found Stock',
            'Attempting Purchase',
            'Purchase Failed',
            'Purchase Success'
        ]
        self.current_data = None

    def generate_mock_data(self):
        if not self.scanning:
            return None

        self.scan_count += 1
        product = random.choice(self.products)

        # Simulate different scenarios
        if self.scan_count % 10 == 0:  # Every 10th scan finds stock
            status = 'Found Stock'
            stock = random.randint(1, 3)
        elif self.scan_count % 50 == 0:  # Every 50th scan attempts purchase
            status = random.choice(['Purchase Success', 'Purchase Failed'])
            stock = 1
        else:
            status = 'Scanning'
            stock = 0

        self.current_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'product': product['name'],
            'size': random.choice(self.sizes),
            'price': product['price'],
            'color': product['color'],
            'stock': stock,
            'status': status
        }
        return self.current_data


scanner = MockScanner()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start_scan', methods=['POST'])
def start_scan():
    try:
        data = request.json
        if not data.get('urls'):
            return jsonify({'message': 'Product URL is required'}), 400

        scanner.scanning = True
        return jsonify({
            'message': 'Scanning started',
            'data': data
        })
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/stop_scan', methods=['POST'])
def stop_scan():
    scanner.scanning = False
    scanner.scan_count = 0
    return jsonify({'message': 'Scanning stopped'})


@app.route('/get_status')
def get_status():
    if scanner.scanning:
        return jsonify(scanner.generate_mock_data())
    return jsonify({'status': 'Not scanning'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8487, debug=True)