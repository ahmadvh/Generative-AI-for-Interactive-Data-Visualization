from pydantic import BaseModel, Field
import ast, astor

class Code(BaseModel):
    """LLM Code output"""
    description: str = Field(description="Description of the generated code and the input dataframe structure (column Names).")
    imports: str = Field(description="Code block import statements")
    code: str = Field(description="Code block not including import statements")
    method_name: str = None
    # Getter for description
    @property
    def description(self):
        return self.description
    
    # Setter for description
    @description.setter
    def description(self, value: str):
        self.description = value
    
    # Getter for imports
    @property
    def imports(self):
        return self.imports
    
    # Setter for imports
    @imports.setter
    def imports(self, value: str):
        self.imports = value
    
    # Getter for code
    @property
    def code(self):
        return self.code
    
    # Setter for code
    @code.setter
    def code(self, value: str):
        self.code = value

    def extract_code_components(self):
        input_args_count = 0
        output_vars_count = 0

        # Parse the method string into an AST (Abstract Syntax Tree)
        parsed = ast.parse(self.code)
    
        # Walk through the AST nodes
        for node in ast.walk(parsed):
            if isinstance(node, ast.FunctionDef):
                # Extract method name
                self.method_name =  node.name
                
                # Update the method name
                if(self.method_name != "generated_method"):
                    self.update_method_name()

                # Count input arguments (excluding 'self' for class methods)
                input_args_count = len(node.args.args)
                
            elif isinstance(node, ast.Return):
                # If it's a return statement, check how many values are being returned
                if isinstance(node.value, ast.Tuple):  # If returning a tuple
                    output_vars_count = len(node.value.elts)
                else:  # Single return value
                    output_vars_count = 1

        # Return as a tuple
        return input_args_count, output_vars_count
        
    def update_method_name(self):
         # Parse the code into an AST
        parsed = ast.parse(self.code)
        
        # Traverse the AST and find the function definition node
        for node in ast.walk(parsed):
            if isinstance(node, ast.FunctionDef):
                # Update the method name to 'generated_method'
                node.name = 'generated_method'
        
        # Convert the AST back to source code and update self.code
        self.code = astor.to_source(parsed)
        