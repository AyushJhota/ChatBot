import mysql.connector

# Function to connect to the database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mysql@0833",
        database="chatbot_db"
    )

# Function to add a new business
def add_business(cursor, business_name, business_type, business_description):
    sql = "INSERT INTO businesses (business_name, business_type, business_description) VALUES (%s, %s, %s)"
    values = (business_name, business_type, business_description)
    cursor.execute(sql, values)
    return cursor.lastrowid  # Return the ID of the newly added business

# Function to add a new FAQ
def add_faq(cursor, business_id, question, answer):
    sql = "INSERT INTO faqs (business_id, question, answer) VALUES (%s, %s, %s)"
    values = (business_id, question, answer)
    cursor.execute(sql, values)

# Main function to add businesses and FAQs interactively
def main():
    # Connect to the database
    db = connect_to_database()
    cursor = db.cursor()

    # Loop to add multiple businesses
    while True:
        print("\n--- Add a New Business ---")
        business_name = input("Enter Business Name: ")
        business_type = input("Enter Business Type: ")
        business_description = input("Enter Business Description: ")

        # Add the business to the database
        business_id = add_business(cursor, business_name, business_type, business_description)
        print(f"Business '{business_name}' added with ID {business_id}.")

        # Loop to add multiple FAQs for the business
        while True:
            print("\n--- Add a FAQ for the Business ---")
            question = input("Enter a common customer question: ")
            answer = input("Enter the response to this question: ")

            add_faq(cursor, business_id, question, answer)
            print("FAQ added.")

            more_faqs = input("Do you want to add another FAQ for this business? (yes/no): ").lower()
            if more_faqs != "yes":
                break

        more_businesses = input("Do you want to add another business? (yes/no): ").lower()
        if more_businesses != "yes":
            break

    # Commit the changes and close the connection
    db.commit()
    cursor.close()
    db.close()

    print("\nAll data has been successfully added to the database.")

if __name__ == "__main__":
    main()
