from dotenv import load_dotenv
load_dotenv()

def get_iterations_from_groq(user_query, groq_client, max_iterations=6):
    groq_response = groq_client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"""<system>
            <role>You are an AI that evaluates the complexity of problems. Analyze the problem</role>

            <evaluation_rules>
              <mathematical_physics>
                <rule>Require more iterations due to common AI limitations</rule>
              </mathematical_physics>

              <response_guidelines>
                <simple_cases>
                  <rule>Return 1 for:
                    - Simple greetings (like "hello", "hi", etc.)
                    - Basic conversational phrases
                    - Direct questions than require direct response (like "how are you?", "thank you", etc.)
                    - DO NOT add reasoning to basic conversational phrases, simple greetings or direct questions, only provide a direct response
                    - Adapts the reasoning of the iteration to a direct response
                  </rule>
                </simple_cases>

                <complexity_analysis>
                    <dimensions>
                        <dimension>Conceptual complexity (abstract reasoning required)</dimension>
                        <dimension>Computational complexity (processing steps needed)</dimension>
                        <dimension>Domain knowledge requirements</dimension>
                        <dimension>Interdependency of components</dimension>
                    </dimensions>

                    <scaling_factors>
                        <factor>Number of variables or parameters</factor>
                        <factor>Depth of nested logic or conditions</factor>
                        <factor>Required precision level</factor>
                        <factor>Error margin tolerance</factor>
                    </scaling_factors>

                    <iteration_requirements>
                        <requirement>Verification depth needed</requirement>
                        <requirement>Solution refinement complexity</requirement>
                        <requirement>Edge case coverage needed</requirement>
                        <requirement>Optimization requirements</requirement>
                    </iteration_requirements>
                </complexity_analysis>

                <complex_cases>
                  <rule>Return a number between 2 and {max_iterations} for:
                    - Mathematical problems
                    - Physics calculations
                    - Complex analysis problems
                  </rule>
                </complex_cases>
              </response_guidelines>
            </evaluation_rules>

            <output_format>
              <instruction>ONLY RETURN the number, without any other indication.</instruction>
            </output_format>
            </system>"""
        }, {
            "role": "user",
            "content": f"Determine the number of iterations required to solve the following problem: {user_query}."
        }],
        model="llama3-8b-8192",
    )

    response_text = groq_response.choices[0].message.content.strip()

    import re
    match = re.search(r'\d+', response_text)
    if match:
        return int(match.group())
    else:
        return 1
