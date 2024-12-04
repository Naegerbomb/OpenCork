#HashForge is HF.py
#HashBash will be HB.py
#This module is meant to locally ingest PII and hash it with a unique salt, for inclusion in a shared (open) database.
#HashBash will generate a hash for a given PII, and then search the database for a matching hash.

import hashlib
import os
import sqlite3
from datetime import datetime
import csv
import argon2

# Database file
DB_FILE = "secure_database.db"

# Initialize the database
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            age_verified TEXT NOT NULL,
            initials TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Standardize and validate data
def standardize_data(first_name, middle_initial, last_name, dob, address):
    first_name = first_name.strip().title()
    middle_initial = middle_initial.strip().upper() if middle_initial else ""
    last_name = last_name.strip().title()
    dob = datetime.strptime(dob.strip(), "%m-%d-%Y").strftime("%m-%d-%Y")
    address = address.strip().title()
    return first_name, middle_initial, last_name, dob, address

# Generate hash with unique salt
def generate_hash(data, salt):
    ph = argon2.PasswordHasher()
    combined = data + salt
    return ph.hash(combined)

# Check for duplicates
def is_duplicate(first_name, middle_initial, last_name, dob, address):
    # Standardize inputs
    first_name, middle_initial, last_name, dob, address = standardize_data(
        first_name, middle_initial, last_name, dob, address
    )
    
    # Format data for hashing
    formatted_data = f"{first_name}|{middle_initial}|{last_name}|{dob}|{address}"
    
    # Open database connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT hash, salt FROM entries")
    rows = cursor.fetchall()
    conn.close()
    
    # Instantiate PasswordHasher
    ph = argon2.PasswordHasher()
    
    # Check for existing hash
    for db_hash, db_salt in rows:
        try:
            ph.verify(db_hash, formatted_data + db_salt)
            return True  # Duplicate found
        except argon2.exceptions.VerifyMismatchError:
            continue
    
    return False  # No duplicate found

# Add an entry to the database (PII excluded)
def add_entry_to_database(first_name, middle_initial, last_name, dob, address):
    print(f"Debug: Adding entry for {first_name} {middle_initial} {last_name}, DOB: {dob}, Address: {address}")
    if is_duplicate(first_name, middle_initial, last_name, dob, address):
        print("Duplicate entry found. Skipping addition.")
        return
    
    # Standardize inputs
    first_name, middle_initial, last_name, dob, address = standardize_data(
        first_name, middle_initial, last_name, dob, address
    )
    
    # Generate unique salt
    salt = os.urandom(16).hex()
    
    # Format data for hashing
    formatted_data = f"{first_name}|{middle_initial}|{last_name}|{dob}|{address}"
    print(f"Formatted data (password): {formatted_data}")
    hash_value = generate_hash(formatted_data, salt)
    
    # Extract metadata: initials only
    initials = f"{first_name[0]}{middle_initial}{last_name[0]}"
    
    # Determine age verification status
    birth_date = datetime.strptime(dob, "%m-%d-%Y")
    age = (datetime.now() - birth_date).days // 365
    age_verified = "Yes" if age >= 18 else "No"
    print(f"Debug: Calculated age for {first_name} {last_name} is {age}. Age Verified: {age_verified}")
    
    # Add to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entries (hash, salt, age_verified, initials)
        VALUES (?, ?, ?, ?)
    """, (hash_value, salt, age_verified, initials))
    conn.commit()
    conn.close()
    print(f"Entry added for customer: {initials}")

# Manual input
def manual_input():
    print("Enter customer data:")
    first_name = input("First Name: ")
    middle_initial = input("Middle Initial: ")
    last_name = input("Last Name: ")
    dob = input("Date of Birth (MM-DD-YYYY): ")
    address = input("Address: ")
    print(f"Debug: Received manual input - {first_name} {middle_initial} {last_name}, DOB: {dob}, Address: {address}")
    add_entry_to_database(first_name, middle_initial, last_name, dob, address)

# Batch input from CSV
def batch_input_from_csv(file_path):
    try:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Debug: Processing CSV line - {row['First Name']} {row.get('Middle Initial', '')} {row['Last Name']}, DOB: {row['DOB']}, Address: {row['Address']}")
                add_entry_to_database(
                    row["First Name"], 
                    row.get("Middle Initial", ""), 
                    row["Last Name"], 
                    row["DOB"], 
                    row["Address"]
                )
    except Exception as e:
        print(f"Error processing CSV: {e}")

# View database contents (no PII displayed)
def view_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, hash, salt, age_verified, initials FROM entries")
    rows = cursor.fetchall()
    conn.close()
    
    print("\nDatabase Entries:")
    for row in rows:
        print(f"ID: {row[0]}, Hash: {row[1]}, Salt: {row[2]}, Age Verified: {row[3]}, Initials: {row[4]}")

# Main program
def main():
    initialize_database()
    while True:
        print("\nMenu:")
        print("1. Add entry manually")
        print("2. Import entries from CSV")
        print("3. View database")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            manual_input()
        elif choice == "2":
            file_path = input("Enter CSV file path: ").strip()
            batch_input_from_csv(file_path)
        elif choice == "3":
            view_database()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
