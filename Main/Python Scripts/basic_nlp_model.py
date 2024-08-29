import mysql.connector

# Connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@0833",
        database="chatbot_db"
    )

import spacy
from nltk.corpus import stopwords

nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha]
    return tokens

def keyword_matching(cursor, business_id, customer_query):
    query_tokens = preprocess_text(customer_query)
    print(f"Customer Query Tokens: {query_tokens}")

    sql = "SELECT question, answer FROM faqs WHERE business_id = %s"
    cursor.execute(sql, (business_id,))
    faqs = cursor.fetchall()

    best_match = None
    best_score = 0

    for question, answer in faqs:
        question_tokens = preprocess_text(question)
        print(f"Question: {question}")
        print(f"Question Tokens: {question_tokens}")

        match_score = len(set(query_tokens) & set(question_tokens))
        print(f"Match Score: {match_score}")

        if match_score > best_score:
            best_score = match_score
            best_match = answer

    if best_match:
        return best_match
    else:
        return "Sorry, I don't have an answer for that right now. I'll forward your query to our team."



def chatbot():
    # Connect to the database
    db = connect_to_database()
    cursor = db.cursor()

    # Assume we're working with the business "Elite Events"
    business_id = 1  # Assuming Elite Events has business_id = 1
    
    while True:
        customer_query = input("Ask me anything: ")
        response = keyword_matching(cursor, business_id, customer_query)
        print("Chatbot:", response)
        
        # Exit the loop if the customer says 'bye'
        if customer_query.lower() == 'bye':
            break

    cursor.close()
    db.close()

if __name__ == "__main__":
    chatbot()
