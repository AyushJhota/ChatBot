import mysql.connector

# Function to connect to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@0833",
        database="chatbot_db"
    )

def interact_with_business():
    conn = connect_to_database()
    cursor = conn.cursor()

    while True:
        business_name = input("Enter the business name (or type 'exit' to quit): ").strip()
        
        if business_name.lower() == 'exit':
            print("Exiting the program.")
            break

        # Check if the business exists
        cursor.execute("SELECT id, name FROM businesses WHERE name=%s", (business_name,))
        business = cursor.fetchone()

        if business:
            print(f"Business Found: {business[1]}")
            business_id = business[0]

            # Ask user if they want to see FAQs
            choice = input("Do you want to see all FAQs? (yes/no): ").strip().lower()
            if choice == 'yes':
                show_faqs(conn, business_id)

            # Loop to keep asking if the user wants to add more FAQs
            while True:
                choice = input("Do you want to add a new FAQ? (yes/no): ").strip().lower()
                if choice == 'yes':
                    add_faq(conn, business_id)
                else:
                    break  # Exit the loop if the user does not want to add more FAQs

            break  # Exit the main loop after handling the business

        else:
            print("Business not found. Please check the name or type 'exit' to quit.")

    conn.close()

def show_faqs(conn, business_id):
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faqs WHERE business_id=%s", (business_id,))
    faqs = cursor.fetchall()
    
    if faqs:
        print("FAQs:")
        for i, faq in enumerate(faqs, start=1):
            print(f"{i}. Q: {faq[0]}")
            print(f"   A: {faq[1]}\n")
    else:
        print("No FAQs found for this business.")

def add_faq(conn, business_id):
    question = input("Enter the FAQ question: ").strip()
    answer = input("Enter the FAQ answer: ").strip()

    cursor = conn.cursor()
    cursor.execute("INSERT INTO faqs (business_id, question, answer) VALUES (%s, %s, %s)", 
                   (business_id, question, answer))
    conn.commit()
    print("FAQ added successfully.")

# Main Function To Interact With The Business
if __name__ == "__main__":
    interact_with_business()
