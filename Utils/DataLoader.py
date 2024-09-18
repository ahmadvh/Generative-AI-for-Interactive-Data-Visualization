import pandas as pd 

def load_data(file_path):
    product_sales_data = pd.read_csv("product_sales_dataset.csv")
    product_sales_data = calculate_product_profit(product_sales_data, 'Product_Price', 'Product_Cost','Items_Sold')
    return product_sales_data

def calculate_product_profit(df, price_col, cost_col, items_sold_col):
    df['Product_Profit'] = (df[price_col] - df[cost_col]) * df[items_sold_col]
    return df

