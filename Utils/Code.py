from pydantic import BaseModel, Field

class Code(BaseModel):
    """LLM Code output"""
    context: str = Field(description="Description of the generated code. and the input dataframe structure (column Names).")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")