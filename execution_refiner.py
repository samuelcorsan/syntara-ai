from utils import execute_code
import re

def refine_with_execution(query, current_cot, iterations, openai_client):
    current_answer = None
    for i in range(iterations):
        # Si es la última iteración, cambia el mensaje para que no use código
        if i == iterations - 1:
            system_message = (
                """Eres un AI que refina soluciones dinámicamente. En esta última iteración, 
                presenta la respuesta final de la mejor manera posible, con todo lo que has razonado antes. Usa todo lo que has aprendido durante las iteraciones previas y cuentale al usuario todo lo que piensas y tu conclusión final."""
            )
        else:
            system_message = (
                """Eres un AI que refina soluciones dinámicamente, utilizando código ejecutable solo cuando sea necesario para obtener información del texto o realizar tareas específicas que lo requieran. Por ejemplo analizar partes de textos, etc, que la IA puede liarse debido a que divide en tokens y no en letras. 
Por ejemplo, si te piden encontrar nombres de comunidades autónomas que terminen en "ia", usarás código para comprobarlo. 
Sin embargo, para otros tipos de respuestas, como explicaciones o análisis que no impliquen procesamiento de datos específicos, no usarás código y proporcionarás la información directamente."""
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
