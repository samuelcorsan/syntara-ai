from dotenv import load_dotenv
load_dotenv()

def get_iterations_from_groq(user_query, groq_client, max_iterations=6):
    groq_response = groq_client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"You are an AI that evaluates the complexity of problems. Analyze the problem and if it is a mathematical problem or one that requires physics it requires more iterations because conventional AI usually fails. ONLY RETURN the number, without any other indication, do not exceed {max_iterations} if possible, for example an example answer would be “4”."
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
