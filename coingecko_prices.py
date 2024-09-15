import requests
import pandas as pd
from datetime import datetime
import time

# Function to convert date from 'YYYY/MM/DD' to 'DD-MM-YYYY'
def convert_date_format(date_str):
    date_obj = datetime.strptime(date_str, '%Y/%m/%d')
    return date_obj.strftime('%d-%m-%Y')

# Function to get historical price for a specific token and day
def get_historical_price(symbol, date):
    # Convert date to required format (DD-MM-YYYY)
    formatted_date = convert_date_format(date)
    
    # Define the base URL for CoinGecko's API
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/history'
    
    # API request parameters
    params = {
        'date': formatted_date,  # Date in DD-MM-YYYY format
        'localization': 'false'  # Disable localized language response
    }

    # Make the GET request to CoinGecko API
    response = requests.get(url, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()

        try:
            price_data = data['market_data']['current_price']['usd']
            return price_data
        except KeyError:
            return None
    else:
        return None

# Function to process the CSV file, fetch historical prices, and save as a new file
def process_csv(input_file, output_file, delay=10):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Create an empty list to store the prices
    prices = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        symbol = row['symbol']
        date = row['date']

        # Get the historical price for the token on the specified date
        price = get_historical_price(symbol, date)

        # Append the price to the list
        prices.append(price if price is not None else 'No Data')

        # Print the result and delay before making the next request
        print(f"Fetched price for {symbol} on {date}: {price}")

        # Introduce a delay to avoid exceeding rate limits
        time.sleep(delay)

    # Add the 'price' column to the DataFrame
    df['price'] = prices

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Updated data with historical prices saved to {output_file}")

# Example usage:
input_file = 'input.csv'  # Input CSV file with 'YYYY/MM/DD' date format
output_file = 'output_with_prices.csv'  # Output CSV file where updated data will be saved

# Process the CSV file and add the historical pricing information
process_csv(input_file, output_file, delay=10)
