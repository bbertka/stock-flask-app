#!/usr/bin/python3

from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

def get_stock_price(symbol):
    try:
        # Query the stock data from Yahoo Finance
        stock_data = yf.Ticker(symbol)

        # Get the most recent stock price
        stock_price = stock_data.history(period='1d')['Close'].iloc[-1]

        return stock_price

    except Exception as e:
        print("Error:", str(e))
        return None

@app.route('/stock-price', methods=['GET'])
def stock_price():
    try:
        # Get the stock symbol from the query parameters
        stock_symbol = request.args.get('symbol')

        # Query the stock price
        price = get_stock_price(stock_symbol)
        if price:
            response = {
                'symbol': stock_symbol,
                'price': price
            }
            return jsonify(response), 200
        else:
            return jsonify({'error': 'Failed to retrieve the price.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
