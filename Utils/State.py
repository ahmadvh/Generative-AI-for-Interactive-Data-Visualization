from Utils.Code import Code
from langchain_core.prompts import  HumanMessagePromptTemplate
import traceback
class State:
    def __init__(self , code_object, llm_model, user_prompt, data_sample) -> None:
        self.user_prompt = user_prompt
        self.code = code_object
        self.error = False
        self.model = llm_model
        self.data_sample = data_sample

    def generate_code(self):
        # print(self.code.description)
        template = """
            {context}
            Here is the method:
            {imports}
            {code}
            Ensure any code you provide is using matplotlib and can be executed with all required imports and variables defined. Update the imports if needed.
            Structure your answer with a description of the code solution. call the method `generated_method`.
            Here is the user prompt:
            {user_prompt}
            """
        prompt_template = HumanMessagePromptTemplate.from_template(template = template)
        code_generation_prompt = prompt_template.format_messages(
                                                                context = self.code.description,
                                                                imports = self.code.imports, 
                                                                code = self.code.code,
                                                                user_prompt = self.user_prompt, 
                                                                )
        
        chain = self.model.with_structured_output(Code)
        
        self.code = chain.invoke(code_generation_prompt)
        self.code.code = self.code.code.strip()
        self.code.imports = self.code.imports.strip()
        
        # TODO: making sure that the output structure is correct.
        

    def check_code(self):

        input_count, output_count = self.code.extract_code_components()
        method_name = self.code.method_name

        if(input_count != 1):
            print("Incorrect method input parameter count.")
            self.code.description = self.code.description + f"""
                update the following method. the method should get 1 parameter a dataframe, and return a `fig`.
                {self.code.code}
            """
            self.error = True
            return 
        if(output_count != 1):
            print("Incorrect method output parameter count.")
            self.code.description = self.code.description + f"""
                update the following method. the method should get 1 parameter a dataframe, and return a `fig`. 
                {self.code.code}
            """
            self.error = True
            return 
        

        generated_code = self.code.code + f"\n{method_name}(self.data_sample)"

        try:
            exec(self.code.imports, locals())
        except Exception as e:
            full_error = traceback.format_exc()
            print(f"Error in imports block! {e} {full_error}")
            new_context = f"""
                             The following python code is not exectuable.
                             There is the following error: {e}. 
                             Fix the error by updating the imports section. here is the code:
                             {self.code.imports}
                             {generated_code}
                             """
            self.code.description = new_context + self.code.description 
            self.error = True
            return
        

        try:
            exec(generated_code, locals())
        except Exception as e:
            full_error = traceback.format_exc()
            print(f"Error in code block! {e} {full_error}" )
            new_context = f"""
                             The following python code is not exectuable.
                             There is the following error: {e}. 
                             Update and fix the code block. here is the code:
                             {self.code.imports}
                             {generated_code}
                             """
            self.code.description = self.code.description + new_context
            self.error = True
            return
        
        self.error = False
        print("CODE IS EXECUTED WITH NO ERROR!")
        
    def run(self):
        attempt = 0
        print("Generating Code...")
        while(True):
            attempt += 1 
            if(attempt > 2):
                break
            print("Attempt:" , attempt)
            self.generate_code()
            self.check_code()
            if self.error == False:
                break
        return self.code
        


    
