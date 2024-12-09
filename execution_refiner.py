from utils import execute_code
import re

def refine_with_execution(query, current_cot, iterations, openai_client):
    current_answer = None
    for i in range(iterations):
        # Si es la última iteración, cambia el mensaje para que no use código
        if i == iterations - 1:
            system_message = (
                """You are an AI that dynamically refines solutions. In this last iteration, present the final answer in the best possible way, with everything you have reasoned before. Use everything you have learned during the previous iterations and tell the user everything you think and your final conclusion."""
            )
        else:
            system_message = (
                """You are an AI that refines solutions dynamically, using executable code only when necessary to obtain information from text or perform specific tasks that require it. For example, analyzing parts of texts, etc., which the AI may confuse because it divides into tokens and not letters. 
When asked to perform tasks that involve finding patterns in words or performing specific searches, such as identifying items within a list that meet certain conditions, use code. Do not use libraries that are not native to Python. Include everything in the same code if you use code and use the complete code, do not go half way because it is the necessary code that you must use for your reasoning. Remember in the code to use the words of the language in which you are spoken, if you are asked to order numbers in Spanish alphabetically you must write the series of numbers in Spanish. Try to make the code as simple as possible to avoid errors but without removing what makes it work. If you see code that is wrong you can also improve it. Always pay attention to what the resulting code says unless it is very strange, never play it down because it is almost always right, if the code says it, try to find an explanation and say what it returns.
However, for other types of answers, such as explanations or analyses that do not involve specific data processing, do not use code and provide the information directly. Remember to use the solutions according to the language in which they speak to you, if they ask you in Spanish, reason in Spanish and do everything in Spanish unless they tell you otherwise."""
            )
        
        # Generar la respuesta del modelo
        response = openai_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": (
                        f"Refina esta solución al problema: {query}. "
                        f"Respuesta previa: {current_answer if current_answer else 'None'}. "
                        f"Cadena de pensamiento: {current_cot}"
                    ),
                },
            ],
            model="gpt-4o",
        )

        current_answer = response.choices[0].message.content.strip()

        # Si es una iteración que no es la última, verificar si hay código y ejecutarlo
        code_match = re.search(r"```python\n(.*?)```", current_answer, re.DOTALL)
        if code_match:
                code_snippet = code_match.group(1)
                execution_result = execute_code(code_snippet)

                if "result" in execution_result:
                    print(f"Resultado de la ejecución: {execution_result['result']}")
                    current_cot += (
                        f"\nSe ejecutó el código y devolvió: {execution_result['result']}"
                    )
                elif "error" in execution_result:
                    print(f"Error en la ejecución: {execution_result['error']}")
        
        print(f"Iteración {i + 1}:\n{current_answer}\n")

    return current_answer
