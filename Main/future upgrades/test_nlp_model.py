import joblib

def load_model_and_test():
    # Load the trained model
    model = joblib.load('business_bot_model.pkl')
    
    while True:
        question = input("Ask a question (type 'exit' to stop): ").strip()
        if question.lower() == 'exit':
            break
        
        # Predict the answer
        answer = model.predict([question])[0]
        print(f"Answer: {answer}")

if __name__ == "__main__":
    load_model_and_test()
