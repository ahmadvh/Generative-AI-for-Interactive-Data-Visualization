from Utils.Code import Code
from langchain_core.prompts import  HumanMessagePromptTemplate

class State:
    def __init__(self , code_object, llm_model, user_prompt) -> None:
        self.user_prompt = user_prompt
        self.code = code_object
        self.error = False
        self.model = llm_model
        


    def generate_code(self):
        template = """
            {context}
            Here is the method:
            {imports}
            {code}
            Ensure any code you provide is using matplotlib and can be executed with all required imports and variables defined. Update the imports if needed.
            Structure your answer with a description of the code solution.
            Here is the user prompt:
            {user_prompt}
            """
        prompt_template = HumanMessagePromptTemplate.from_template(template = template)
        code_generation_prompt = prompt_template.format_messages(
                                                                context = self.code.context,
                                                                imports = self.code.imports, 
                                                                code = self.code.code,
                                                                user_prompt = self.user_prompt, 
                                                                )
        
        chain = self.model.with_structured_output(Code)
        
        self.code = chain.invoke(code_generation_prompt)

        # TODO: making sure that the output structure is correct.
        

    def check_code(self):
        generated_code = self.code.code + "\ngenerated_method(data)"
        imports_block = self.code.imports
        context = self.code.context

        try:
            eval(imports_block)
        except Exception as e:
            print("CODE NOT EXECUTABLE!")
            new_context = f"""
                             The following python code is not exectuable.
                             There is the following error: {e}. 
                             Fix the error by updating the imports section. here is the code:
                             {imports_block}
                             {generated_code}
                             """
            self.code.context = context + new_context
            self.error = True
            # self.write_logs(f"{e}")
            


        try:
            eval(generated_code)
        except Exception as e:
            print("CODE NOT EXECUTABLE!")
            new_context = f"""
                             The following python code is not exectuable.
                             There is the following error: {e}. 
                             Update and fix the code block. here is the code:
                             {imports_block}
                             {generated_code}
                             """
            self.code.context = context + new_context
            self.error = True
            # self.write_logs(f"{e}")

        self.error = False
        
        print("CODE IS EXECUTED WITH NO ERROR!")
        
    def run(self):
        print("Generating Code...")
        while(True):
            print("New Attempt...")
            self.generate_code()
            self.check_code()
            if self.error == False:
                break
        

    
   