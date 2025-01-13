from transformers import GPT2LMHeadModel, GPT2Tokenizer

class ArticleWritingAgent:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def perceive(self):
        user_topic = input("Enter the topic for the article: ").strip()
        return user_topic

    def reason(self, user_topic):
        inputs = self.tokenizer.encode(f"Write an article about {user_topic}.", return_tensors="pt")
        outputs = self.model.generate(
            inputs,
            max_length=300,
            min_length=150,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_k=50,
            top_p=0.9
        )
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_text

    def act(self, user_topic, generated_text):
        print("\nGenerated Article:\n")
        print(generated_text)
        save = input("\nDo you want to save the article? (yes/no): ").strip().lower()
        if save == "yes":
            filename = f"{user_topic.replace(' ', '_')}_article.txt"
            with open(filename, "w") as file:
                file.write(generated_text)
            print(f"\nArticle saved as {filename}")

# Initialize the agent
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
agent = ArticleWritingAgent(model, tokenizer)

# Run the agent loop
while True:
    topic = agent.perceive()
    if topic.lower() == "exit":
        print("Exiting agent. Goodbye!")
        break
    article = agent.reason(topic)
    agent.act(topic, article)
