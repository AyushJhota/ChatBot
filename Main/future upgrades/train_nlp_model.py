import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import mysql.connector
import joblib
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC

# Fetch Data From Database
def fetch_business_data(business_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@0833",
        database="chatbot_db"
    )
    query = f"SELECT question, answer FROM faqs WHERE business_id = %s"
    df = pd.read_sql_query(query, conn, params=(business_id,))
    conn.close()
    return df

# Train The NLP Model
def train_nlp_model(df):
    X = df['question']
    y = df['answer']

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a pipeline that includes TF-IDF Vectorizer and Logistic Regression
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', LogisticRegression())
    ])

    # Train the model
    pipeline.fit(X_train, y_train)

    # Evaluate the model
    accuracy = pipeline.score(X_test, y_test)
    print(f'Model Accuracy: {accuracy*100:.2f}%')

    # Save the trained model
    joblib.dump(pipeline, 'business_bot_model.pkl')
    print("Model saved as business_bot_model.pkl")
    
    return pipeline

# Main Function To Train The Model
def main(business_id):
    df = fetch_business_data(business_id)
    if df.empty:
        print(f"No FAQs found for business ID {business_id}.")
        return
    print(f"Training model for Business ID: {business_id}")
    train_nlp_model(df)



# Example pipeline with SVM
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('classifier', SVC())
])

# Parameters to tune
parameters = {
    'tfidf__max_features': [500, 1000, 5000],
    'tfidf__ngram_range': [(1, 1), (1, 2), (1, 3)],
    'classifier__C': [0.1, 1, 10],
    'classifier__kernel': ['linear', 'rbf']
}

# Perform Grid Search
grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best parameters and accuracy
print("Best Parameters:", grid_search.best_params_)
print(f"Best Accuracy: {grid_search.best_score_ * 100:.2f}%")

# Save the best model
joblib.dump(grid_search.best_estimator_, 'business_bot_model.pkl')


# Example: Train the model for business with ID 1
if __name__ == "__main__":
    main(business_id=1)
