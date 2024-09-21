from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import Utils.DataLoader as DataLoader 
from Utils.Code import Code
from Utils.State import State
import matplotlib.pyplot as plt
plt.switch_backend('TkAgg')
import warnings
from pydantic.json_schema import PydanticJsonSchemaWarning

# Suppress the specific PydanticJsonSchemaWarning warnings
warnings.filterwarnings("ignore", category=PydanticJsonSchemaWarning)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

state = None
data = None 

# Import the API key (The key name must be: `OPENAI_API_KEY`)
load_dotenv(dotenv_path='apikey.env')

# Set up the model
model = ChatOpenAI(temperature=0, model="gpt-4")

data = DataLoader.load_data("product_sales_dataset.csv")

# Define base code
init_code = Code(
    description="""
        We have a product sales dataset. Here's a description of the columns in this dataframe:
        Date: The date on which the sales data for the products was recorded, formatted as YYYY-MM-DD.
        Product_Category: The category to which the product belongs. This could include various categories like "Art & Crafts" or others.
        Product_Name: The name of the product sold. Each row corresponds to a specific product such as "Barrel O' Slime" or "Etch A Sketch."
        Product_Cost: The cost to produce or acquire the product. This is the amount spent on each unit of the product.
        Product_Price: The selling price of the product. This is the price at which the product is sold to customers.
        Items_Sold: The quantity of the product sold on the specified date.
        Product_Profit: The total profit generated from the sales of the product. This value is the difference between the selling price and the product cost, multiplied by the number of items sold. It represents the gross profit from that product's sales.
        Act like a data scientist and data visualization engineer. Write a Python method called `generated_method` based on matplotlib to create a visualization based on user input.
        The method should take a dataframe as input and return a figure.
    """,
    imports="",
    code="""
        def generated_method(dataframe):
            return fig
    """.strip(),
)

states = []

while True:
    user_input = input("Enter prompt:")

    state = State(
        code_object = init_code,
        user_prompt = user_input,
        llm_model = model,
        data_sample= data.head(3)
    )
    
    init_code = state.run()
    
    code_str = init_code.imports.strip() + '\n' + init_code.code.strip()
    exec(code_str, globals())
    
    fig = generated_method(data)
    
    fig.savefig("output_figure.png")
    # plt.close('all') 
    fig.show()

    states.append(state)
    
    