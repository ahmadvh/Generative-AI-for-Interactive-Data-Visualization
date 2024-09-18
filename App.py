from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import Utils.DataLoader as DataLoader 
from Utils.Code import Code
from Utils.State import State

# import the api key (The key name most be: `OPENAI_API_KEY`)
load_dotenv(dotenv_path='apikey.env')
# set up the model
model = ChatOpenAI(temperature=0, model="gpt-4o")

data = DataLoader.load_data("product_sales_dataset.csv")

base_code = Code(
                context = """
                        We have a product sales dataset. Heres a description of the columns in this dataframe:
                        Date: The date on which the sales data for the products was recorded, formatted as YYYY-MM-DD.
                        Product_Category: The category to which the product belongs. This could include various categories like "Art & Crafts" or others.
                        Product_Name: The name of the product sold. Each row corresponds to a specific product such as "Barrel O' Slime" or "Etch A Sketch."
                        Product_Cost: The cost to produce or acquire the product. This is the amount spent on each unit of the product.
                        Product_Price: The selling price of the product. This is the price at which the product is sold to customers.
                        Items_Sold: The quantity of the product sold on the specified date.
                        Product_Profit: The total profit generated from the sales of the product. This value is the difference between the selling price and the product cost, multiplied by the number of items sold. It represents the gross profit from that product's sales.
                        Act like a data scientist and data visualization engineer. write a Python method called `generated_method` based on matplotlib to create a visualization based on user input.
                        The method should take a dataframe as input and return a figure.
                """,
                imports="",
                code = 
                """
                        def generated_method(dataframe):
                            return figure
                """.strip(),
                 )


while True:
    user_prompt = input("What do you want?")

    state = State(
        base_code,
        model,
        user_prompt
    )

    state.run()

    print(
        state.code.context  
    )
    base_code = state.code
    exec(state.code.imports, globals())
    exec(state.code.code, globals())

    fig = generated_method(data)
    fig.savefig("output.png") 