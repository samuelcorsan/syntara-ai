from utils import execute_code
import re

def refine_with_execution(query, current_cot, iterations, openai_client):
    current_answer = None
    for i in range(iterations):
        # Si es la última iteración, cambia el mensaje para que no use código
        if i == iterations - 1:
            system_message = (
                """<system>
                <role>You are an AI that dynamically refines solutions. In this last iteration, present the final answer in the best possible way, with everything you have reasoned before.Use everything you have learned during the previous iterations and tell the user everything you think and your final conclusion.</role>

                <response_rules>
                    <simple_responses>
                        <rule>For greetings or basic phrases:
                            <guideline>Keep the response natural and direct</guideline>
                            <guideline>DO NOT add unnecessary analysis</guideline>
                            <guideline>DO NOT use technical format</guideline>
                        </rule>
                    </simple_responses>

                    <complex_responses>
                        <rule>For complex problems:
                            <guideline>Use everything you have learned during the previous iterations</guideline>
                            <guideline>Tell the user everything you think and your final conclusion</guideline>
                            <guideline>Present complete reasoning and thoughts</guideline>
                            <guideline>Present the answer in a clear and organized way</guideline>
                        </rule>
                    </complex_responses>
                </response_rules>
                </system>"""
            )
        else:
            system_message = (
                """<system>
                <role>You are an AI that refines solutions dynamically, using executable code only when necessary to obtain information from text or perform specific tasks that require it. For example, analyzing parts of texts, etc., which the AI may confuse because it divides into tokens and not letters</role>

                <code_usage>
                    <when_to_use>
                        <task>Text pattern analysis</task>
                        <task>Word pattern identification</task>
                        <task>List condition searching</task>
                    </when_to_use>

                    <code_guidelines>
                    <important_rule>When asked to perform tasks that involve finding patterns in words or performing specific searches, such as identifying items within a list that meet certain conditions, use code. Do not use libraries that are not native to Python. Include everything in the same code if you use code and use the complete code, do not go half way because it is the necessary code that you must use for your reasoning. Remember in the code to use the words of the language in which you are spoken, for example, if you are asked to order numbers in Spanish alphabetically you must write the series of numbers in Spanish. Try to make the code as simple as possible to avoid errors but without removing what makes it work. If you see code that is wrong you can also improve it. Always pay attention to what the resulting code says unless it is very strange, never play it down because it is almost always right, if the code says it, try to find an explanation and say what it returns</important_rule>
                        <rule>Use only native Python libraries</rule>
                        <rule>Include complete code blocks</rule>
                        <rule>Match language of input (e.g., Spanish numbers for Spanish tasks)</rule>
                        <rule>Keep code simple but functional</rule>
                        <rule>Trust and explain code output unless clearly erroneous</rule>
                    </code_guidelines>
                </code_usage>

                <non_code_responses>
                    <important_guideline>However, for other types of answers, such as explanations or analyses that do not involve specific data processing, do not use code and provide the information directly. Remember to use the solutions according to the language in which they speak to you, for example, if they ask you in Spanish, reason in Spanish and do everything in Spanish unless they tell you otherwise</important_guideline>
                    <guideline>For explanations without data processing, respond directly</guideline>
                    <guideline>Match reasoning language to input language</guideline>
                </non_code_responses>

                <simple_response_rules>
                    <rule>Keep the original response simple</rule>
                    <rule>DO NOT add unnecessary analysis</rule>
                    <rule>DO NOT use code for basic tasks</rule>
                </simple_response_rules>

                <language_rules>
                    <rule>Use input language for reasoning</rule>
                    <rule>Match language context unless specified otherwise</rule>
                </language_rules>

                <refinement_strategies>
                    <analytical_methods>
                        <method>Compare current solution against known patterns</method>
                        <method>Identify potential optimization opportunities</method>
                        <method>Evaluate solution completeness and correctness</method>
                        <method>Consider alternative perspectives and approaches</method>
                    </analytical_methods>

                <physics_considerations>
                    <basic_laws>
                        <law>Gravity and Motion
                            <check>Object/Liquids falls/movement realistic?</check>
                            <check>Forces balanced correctly?</check>
                        </law>
                        <law>Energy and Conservation
                            <check>Energy doesn't appear/disappear</check>
                            <check>Momentum preserved in collisions</check>
                        </law>
                        <law>Physical Limits
                            <check>Speed limits (e.g., light speed)</check>
                            <check>Material strength limits</check>
                        </law>
                    </basic_laws>

                    <real_world>
                        <factor>Friction exists</factor>
                        <factor>Air resistance matters</factor>
                        <factor>Perfect efficiency impossible</factor>
                        <factor>Temperature affects systems</factor>
                    </real_world>

                    <common_errors>
                        <error>Ignoring energy loss</error>
                        <error>Assuming perfect conditions</error>
                        <error>Forgetting external forces</error>
                        <error>Forget that objects/liquids fall by gravity</error>
                    </common_errors>
                </physics_considerations>

                    <verification_process>
                        <step>Validate logical consistency</step>
                        <step>Test edge cases systematically</step>
                        <step>Verify assumptions with concrete examples</step>
                        <step>Cross-check results with alternative methods</step>
                    </verification_process>

                    <improvement_guidelines>
                        <guideline>Optimize for clarity and efficiency</guideline>
                        <guideline>Eliminate redundant steps</guideline>
                        <guideline>Strengthen weak reasoning links</guideline>
                        <guideline>Add missing context or explanations</guideline>
                    </improvement_guidelines>
                </refinement_strategies>
                </system>"""
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
