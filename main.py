import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Maximum number of iterations
max_iterations = 6

# Function to call Groq LLaMa 8b to decide number of iterations based on question complexity
def get_iterations_from_groq(user_query):
    groq_response = groq_client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": "You are an AI that evaluates the complexity of problems."
        }, {
            "role": "user",
            "content": f"Determine the number of iterations required to solve the following problem: {user_query}. ONLY RETURN the number, without any other indication, do not exceed {max_iterations} if possible, for example an example answer would be “4”."
        }],
        model="llama3-8b-8192",
    )

    # Extract the number of iterations (assuming the response contains something like: "5")
    response_text = groq_response.choices[0].message.content.strip()

    # Try to extract the number of iterations from the response
    import re
    match = re.search(r'\d+', response_text)
    if match:
        iterations = int(match.group())  # Extract the first number
    else:
        iterations = 1  # Default to 1 iteration if no number found

    return iterations

# Function to create the initial chain of thought using GPT-4o
def create_chain_of_thought(query):
    # GPT-4o is used to generate an initial chain of thought (CoT)
    response = openai_client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": "You are an AI that creates a chain of thought to solve problems step by step. When creating it try to generate the best possible chain of thought and try to realize what a normal model would not realize, try to see hidden data that may be in the problem you are posed in all the data that is offered. For each step remember to say why that would be so or not, always being very exact and specific."
        }, {
            "role": "user",
            "content": f"Create a chain of thought to solve the following problem: {query}"
        }],
        model="gpt-4o",
    )

    cot = response.choices[0].message.content.strip()  # Get the chain of thought
    return cot

# Function to handle the iterative process with GPT-4o
def iterate_with_gpt4o(query, cot, iterations):
    current_answer = None
    current_cot = cot
    for i in range(iterations):
        # Each iteration refines the answer, using the previous answer and current CoT
        response = openai_client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": "You are an AI that iterates over a problem and improves the solution each time. Do not use markdown in responses. You should use this chain of thought to respond: {current_cot}"
            }, {
                "role": "user",
                "content": f"Improve the previous answer and change any data you see wrong to make the answer correct, although in the previous answer data is given as correct, always ask whether this is the case or not: {query}. The previous answer was: {current_answer if current_answer else 'None'}"
            }],
            model="gpt-4o",
        )

        # Get the improved answer from GPT-4o
        current_answer = response.choices[0].message.content.strip()  # Updated answer
        print(f"Iteration {i+1}:\n{current_answer}\n")  # Display iteration result

    return current_answer

# Main function to process user input and execute the entire flow
def main():
    user_query = input("Enter your problem/question: ")

    # Step 1: Get the number of iterations based on query complexity using Groq and LLaMa 8B
    iterations = get_iterations_from_groq(user_query)
    print(f"Number of iterations decided by Groq's LLaMa 8B: {iterations}\n")

    # Step 2: Generate the initial chain of thought using GPT-4o
    cot = create_chain_of_thought(user_query)
    print(f"Initial Chain of Thought from GPT-4o:\n{cot}\n")

    # Step 3: Perform the iterative process based on the complexity and generate the final answer
    final_answer = iterate_with_gpt4o(user_query, cot, iterations)
    print(f"Final refined solution after {iterations} iterations:\n{final_answer}\n")

if __name__ == "__main__":
    main()
