import hashlib
import sqlite3
import csv
from datetime import datetime
import argon2

# Database file location (ensure this points to the existing database)
DB_FILE = "OpenAgeCheck.db"

# Standardize and validate data
def standardize_data(first_name, middle_initial, last_name, dob, address):
    first_name = first_name.strip().title()
    middle_initial = middle_initial.strip().upper() if middle_initial else ""
    last_name = last_name.strip().title()
    dob = datetime.strptime(dob.strip(), "%m-%d-%Y").strftime("%m-%d-%Y")
    address = address.strip().title()
    return first_name, middle_initial, last_name, dob, address

# Generate hash with provided data and salt
def generate_hash(data, salt):
    ph = argon2.PasswordHasher()
    combined = data + salt
    return ph.hash(combined)

# Verify if a hash exists in the database and return the age verified status
def verify_hash_in_database(first_name, middle_initial, last_name, dob, address):
    # Standardize inputs
    first_name, middle_initial, last_name, dob, address = standardize_data(
        first_name, middle_initial, last_name, dob, address
    )
    
    # Format data for hashing
    formatted_data = f"{first_name}|{middle_initial}|{last_name}|{dob}|{address}"
    
    # Open database connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT hash, salt, age_verified FROM entries")
    rows = cursor.fetchall()
    conn.close()
    
    # Instantiate PasswordHasher
    ph = argon2.PasswordHasher()
    
    # Check each entry in the database
    for row in rows:
        db_hash, db_salt, age_verified = row
        try:
            ph.verify(db_hash, formatted_data + db_salt)
            print(f"Debug: Found matching entry for {first_name} {last_name}. Age Verified: {age_verified}")
            return age_verified  # Return "Yes" or "No" from the database
        except argon2.exceptions.VerifyMismatchError:
            continue
    
    print(f"Debug: No matching entry found for {first_name} {last_name}")
    return None  # If no match is found

# Manual verification
def manual_verification():
    print("Enter customer data to verify:")
    first_name = input("First Name: ")
    middle_initial = input("Middle Initial: ")
    last_name = input("Last Name: ")
    dob = input("Date of Birth (MM-DD-YYYY): ")
    address = input("Address: ")
    status = verify_hash_in_database(first_name, middle_initial, last_name, dob, address)
    print(f"Age Verified: {status}")

# Batch verification from CSV
def batch_verification_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            results = []
            for row in reader:
                first_name = row["First Name"]
                middle_initial = row.get("Middle Initial", "")
                last_name = row["Last Name"]
                dob = row["DOB"]
                address = row["Address"]
                
                status = verify_hash_in_database(first_name, middle_initial, last_name, dob, address)
                if status is None:
                    status = "No (not in database)"
                results.append({
                    "First Name": first_name,
                    "Middle Initial": middle_initial,
                    "Last Name": last_name,
                    "Age Verified": status
                })
            
            # Print results
            print("\nVerification Results:")
            for result in results:
                print(f"{result['First Name']} {result['Middle Initial']} {result['Last Name']}: Age Verified = {result['Age Verified']}")
    except Exception as e:
        print(f"Error processing CSV: {e}")

# Main entry point for standalone execution
if __name__ == "__main__":
    print("Standalone Age Verification Module: checker.py")
    print("===============================================")
    print("\nMenu:")
    print("1. Verify customer manually")
    print("2. Verify customers from CSV")
    choice = input("Choose an option (1 or 2): ").strip()
    
    if choice == "1":
        manual_verification()
    elif choice == "2":
        file_path = input("Enter CSV file path: ").strip()
        batch_verification_from_csv(file_path)
    else:
        print("Invalid option. Exiting.")