# Reasoner-O1: Iterative AI Chain of Thought Model

**Reasoner-O1** is an experimental AI system that combines OpenAI's GPT-4o and Groq's LLaMa 8B to provide an innovative iterative problem-solving approach. The system uses a chain of thought (CoT) generation strategy, refining solutions over multiple iterations until the most accurate answer is reached. This approach aims to address complex queries that require multiple steps of reasoning, allowing the AI to progressively improve its answers.

### Current Status: Beta

This project is in the **Beta** stage, meaning it’s still under active development. We are continuously working to improve its functionality and effectiveness. **Your feedback and suggestions are greatly appreciated!** If you have any ideas for improvements, please feel free to submit issues or pull requests.

### Features:
- **Iterative Problem Solving**: The system makes use of multiple GPT-4o models, each building on the previous iteration to improve the solution.
- **Chain of Thought (CoT)**: The initial problem is broken down into a logical chain of thought by the first GPT-4o model.
- **Dynamic Iteration Calculation**: Groq's LLaMa 8B model determines how many iterations the AI should go through based on the problem's complexity.
- **Refinement Process**: Each GPT-4o model iteration improves the answer progressively, incorporating the previous model's output.
- **Environment-Based Configuration**: Sensitive data such as API keys are stored securely in a `.env` file.

### How It Works:

1. **User Query**: The user enters a problem or question they want solved.
   
2. **Complexity Evaluation (Groq)**: The **Groq LLaMa 8B** model evaluates the problem's complexity and determines the number of iterations needed for the solution. For example, simple queries may only require one iteration, while complex problems may require more.

3. **Initial Chain of Thought (CoT)**: The **GPT-4o** model is used to create the first chain of thought, which breaks down the problem into smaller, manageable steps.

4. **Iterative Refinement**: Starting from the initial CoT, each subsequent GPT-4o iteration improves the solution, referencing the previous output and iterating over the problem until the correct answer is reached.

5. **Final Answer**: Once all iterations are completed, the last GPT-4o model provides the final, most refined solution.

### Installation and Setup

To get started with the Reasoner-O1 project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/samuelcorsan/reasoner-o1.git
   cd reasoner-o1
   ```

2. **Install Dependencies**:
   The project requires several Python libraries to interact with the APIs and manage environment variables. Install them using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**:
   Create a `.env` file in the root directory of the project and add your Groq and OpenAI API keys:

   ```
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

4. **Run the Application**:
   Execute the Python script to begin solving problems interactively:
   
   ```bash
   python main.py
   ```

### Example Use Case

**Example Question**: "How many 'r' letters are there in 'strawberry'?"

1. **Groq's Evaluation**: The LLaMa 8B model from Groq decides that this problem only requires a single iteration due to its simplicity.
2. **Initial Chain of Thought**: GPT-4o creates a step-by-step breakdown of how to count the "r"s.
3. **Iterative Refinement**: Since it's a simple problem, no iterations are required beyond the initial response. The final answer would be returned directly.
   
For more complex queries, multiple iterations might be necessary to refine the answer, making the system adaptable to a wide range of problems.

### How to Configure the Maximum Iterations Based on Cost Considerations
The `max_iterations` variable of the Reasoner-O1 project allows setting a limit on the maximum number of iterations that the system can perform when solving a problem, i.e. on the maximum number of iterations that LLaMa 8b will choose based on the complexity of the problem. This feature provides flexibility, especially considering the cost of using API services such as OpenAI and Groq, which charge based on the number of requests, tokens used and computation time.

In the beginning of the file you can change the maximum number of iterations that 8b will decide to use:
```python
   max_iterations = 5  # Set a maximum limit for iterations
```

### Why Limit Iterations?
Each iteration requires an API call to GPT-4o and Groq. These calls consume resources, and depending on the complexity of the problem, the number of iterations can quickly add up. Limiting the number of iterations helps control the costs associated with these API calls, especially for users with limited budgets or when experimenting with multiple queries.

### Why is it in Beta?

The Reasoner-O1 project is currently in beta, and we are refining its functionality. Although it’s already operational, the number of iterations and the overall model accuracy can be improved through further testing and feedback. We encourage contributions and feedback to make this system even better.

### Contributing

We are open to any contributions! Whether you have ideas for improvement, bug fixes, or new features, please feel free to open an issue or submit a pull request.

Here’s how you can contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Push your changes and open a pull request.

### License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

### Notes:
- **Iterative Refinement**: The more complex the problem, the more iterations are needed. The system can handle problems ranging from simple queries (e.g., "How many 'r' in strawberry?") to more complex, multi-step questions.
- **Customizability**: The number of iterations can be controlled through Groq’s API, making it adaptive to different problem complexities.
- **Improvement**: As this is a beta project, ongoing refinement and improvements are expected, especially with the iteration count and GPT-4o's response accuracy.
