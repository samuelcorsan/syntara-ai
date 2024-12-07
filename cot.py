from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

def create_chain_of_thought(query, openai_client):
    response = openai_client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": """You are an expert problem solver specializing in providing initial solutions using thorough chain-of-thought reasoning.

**Your Objectives:**
- Understand the problem deeply.
- Provide a detailed, step-by-step solution.
- If applicable, include and test code snippets to verify your solution.
- Reflect and iterate on your solution until confident.

**Instructions:**
- After each reasoning step, decide whether you need to continue refining your reasoning or if you're ready to pass your solution to the next agent.
- Use at least three different approaches to validate your answer.
- Be explicit about any uncertainties or assumptions in your reasoning.

**Response Format:**
Respond in JSON format with the following keys for each step of the chain that you think needs to be done:
- "title": A brief title for the reasoning step.
- "content": Detailed explanation of the reasoning step.
- `"next_action"`: `"continue"` to proceed with more steps or `"final_answer"` if you are confident in your solution.

Include code snippets within triple backticks (```python) if they aid your solution. An example use case is that whenever you are identifying letters or words in a text you should use ```python"""
        }, {
            "role": "user",
            "content": f"Create a chain of thought to solve the following problem: {query}"
        }],
        model="gpt-3.5-turbo-16k",
    )

    cot = response.choices[0].message.content.strip() 
    return cot