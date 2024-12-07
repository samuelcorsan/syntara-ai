# main.py
from iterations import get_iterations_from_groq
from cot import create_chain_of_thought
from execution_refiner import refine_with_execution
from clients import openai_client, groq_client

# Maximum number of iterations
max_iterations = 6

def main():
    user_query = input("Enter your problem/question: ")

    # Gets the number of iterations to use based on the complexity of the problem
    iterations = get_iterations_from_groq(user_query, groq_client, max_iterations=max_iterations)

    # Create a thought string based on the user's query using the OpenAI client.
    cot = create_chain_of_thought(user_query, openai_client)

    # Refines the final answer using execution, chain of thought and iterations.
    final_answer = refine_with_execution(user_query, cot, iterations, openai_client)

    # Prints the final refined solution after iterations
    print(f"Final refined solution after {iterations} iterations:\n{final_answer}\n")

if __name__ == "__main__":
    main()
