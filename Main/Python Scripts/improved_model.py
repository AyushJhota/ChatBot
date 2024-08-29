import mysql.connector
import spacy
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings

# Suppress specific sklearn warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# Load spacy model
nlp = spacy.load('en_core_web_sm')
stop_words = set(stopwords.words('english'))  # Convert to set for better performance

# Connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@0833",
        database="chatbot_db"
    )

# Preprocess text
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha]
    return tokens

# Expand keywords using synonyms from WordNet
def expand_keywords(tokens):
    expanded_tokens = set(tokens)
    for token in tokens:
        for syn in wordnet.synsets(token):
            for lemma in syn.lemmas():
                expanded_tokens.add(lemma.name())
    return list(expanded_tokens)

# Keyword matching with refined logic
def keyword_matching(cursor, business_id, customer_query):
    query_tokens = preprocess_text(customer_query)
    query_tokens = expand_keywords(query_tokens)
    print(f"Customer Query Tokens: {query_tokens}")

    sql = "SELECT question, answer FROM faqs WHERE business_id = %s"
    cursor.execute(sql, (business_id,))
    faqs = cursor.fetchall()

    questions = [faq[0] for faq in faqs]
    answers = [faq[1] for faq in faqs]

    # Vectorize questions and the customer query using TF-IDF
    vectorizer = TfidfVectorizer(tokenizer=lambda text: preprocess_text(text), stop_words=list(stop_words))
    vectors = vectorizer.fit_transform(questions + [' '.join(query_tokens)])

    # Calculate cosine similarity between the query and each question
    cosine_similarities = cosine_similarity(vectors[-1], vectors[:-1])
    best_match_idx = np.argmax(cosine_similarities)

    best_score = cosine_similarities[0, best_match_idx]
    print(f"Best Match Score: {best_score}")

    if best_score > 0.2:  # Adjust threshold based on testing
        return answers[best_match_idx]
    else:
        return "Sorry, I don't have an answer for that right now. I'll forward your query to our team."

# Main chatbot function
def chatbot():
    # Connect to the database
    db = connect_to_database()
    cursor = db.cursor()

    business_id = 1  # Assume we're working with the business "Elite Events"
    
    while True:
        customer_query = input("Ask me anything: ")
        response = keyword_matching(cursor, business_id, customer_query)
        print("Chatbot:", response)
        
        if customer_query.lower() == 'bye':
            break

    cursor.close()
    db.close()

if __name__ == "__main__":
    chatbot()
