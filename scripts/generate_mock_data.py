import os
import csv
import random
from datetime import datetime, timedelta
import argparse

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

CSV_PATH = os.path.join(DATA_DIR, 'mock_retail_data.csv')

# Mock data options
categories = ['Beverages', 'Snacks', 'Personal Care']
subcategories = {
    'Beverages': ['Soda', 'Juice', 'Water'],
    'Snacks': ['Chips', 'Cookies', 'Nuts'],
    'Personal Care': ['Soap', 'Shampoo', 'Toothpaste']
}
skus = {
    'Soda': ['SODA001', 'SODA002', 'SODA003'],
    'Juice': ['JUICE001', 'JUICE002', 'JUICE003'],
    'Water': ['WATER001', 'WATER002', 'WATER003'],
    'Chips': ['CHIPS001', 'CHIPS002', 'CHIPS003'],
    'Cookies': ['COOKIES001', 'COOKIES002', 'COOKIES003'],
    'Nuts': ['NUTS001', 'NUTS002', 'NUTS003'],
    'Soap': ['SOAP001', 'SOAP002', 'SOAP003'],
    'Shampoo': ['SHAMPOO001', 'SHAMPOO002', 'SHAMPOO003'],
    'Toothpaste': ['TOOTH001', 'TOOTH002', 'TOOTH003']
}
promocodes = ['PROMO10', 'PROMO20', 'PROMO30', '']

parser = argparse.ArgumentParser(description='Generate mock retail data CSV.')
parser.add_argument('--start-date', type=str, default=None, help='Start date (YYYY-MM-DD)')
parser.add_argument('--end-date', type=str, default=None, help='End date (YYYY-MM-DD)')
parser.add_argument('--rows', type=int, default=500, help='Number of rows to generate')
args = parser.parse_args()

if args.start_date and args.end_date:
    start_dt = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(args.end_date, '%Y-%m-%d')
    delta = (end_dt - start_dt).days
    dates = [(start_dt + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta + 1)]
else:
    dates = [(datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

stores = ['FreshMart', 'UrbanGrocer', 'MarketPlace', 'GreenLeaf', 'ShopEase']
brands = ['Sunshine Foods', 'PureLeaf', 'Snackify', 'GlowCare', 'DailyFresh', 'CrunchyBite', 'AquaPure']

rows = []
for _ in range(args.rows):
    date = random.choice(dates)
    store = random.choice(stores)
    category = random.choice(categories)
    subcategory = random.choice(subcategories[category])
    brand = random.choice(brands)
    sku = random.choice(skus[subcategory])
    sales = round(random.uniform(5, 500), 2)
    units = random.randint(1, 50)
    customers = random.randint(1, 20)
    promocode = random.choice(promocodes)
    rows.append([
        date, store, category, subcategory, brand, sku, sales, units, customers, promocode
    ])

with open(CSV_PATH, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['date', 'store', 'category', 'subcategory', 'brand', 'sku', 'sales', 'units', 'customers', 'promocode'])
    writer.writerows(rows)

print(f"Mock data written to {CSV_PATH}")
