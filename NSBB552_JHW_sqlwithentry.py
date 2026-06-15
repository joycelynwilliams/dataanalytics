import sqlite3
import csv
import datetime

# Helper function to print the database contents nicely
def display_database(cursor):
    cursor.execute("SELECT * FROM superpowers")
    rows = cursor.fetchall()
    
    print("\n" + "="*90)
    print(f"{'Superpower':<20} | {'First Name':<12} | {'Last Name':<15} | {'Age':<3} | {'Country':<12} | {'Food':<15}")
    print("-" * 90)
    
    if not rows:
        print("Database is currently empty.")
    else:
        for row in rows:
            # row[6] is the date_added, which we can skip in this compact view, or you can add it
            print(f"{row[0]:<20} | {row[1]:<12} | {row[2]:<15} | {row[3]:<3} | {row[4]:<12} | {row[5]:<15}")
    print("="*90 + "\n")

def manage_superpowers():
    # Define your exact folder path
    folder_path = "/Users/joycelynwilliams/Desktop/coding/"
    
    original_csv = folder_path + 'Superpower-FirstName-LastName-Age-FavoriteCountry-FavoriteFood.csv'
    db_file = folder_path + 'superpowers.db'
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    

    # Create the table with a new 'date_added' column
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS superpowers (
            superpower TEXT,
            first_name TEXT,
            last_name TEXT,
            age INTEGER,
            fav_country TEXT,
            fav_food TEXT,
            date_added TEXT
        )
    ''')

    # 1. Load the original CSV into the database if the table is empty
    cursor.execute("SELECT COUNT(*) FROM superpowers")
    if cursor.fetchone()[0] == 0:
        print(f"Loading original data from {original_csv}...")
        try:
            with open(original_csv, 'r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cursor.execute('''
                        INSERT INTO superpowers 
                        (superpower, first_name, last_name, age, fav_country, fav_food, date_added)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (row['superpower'], row['first_name'], row['last_name'], 
                          row['age'], row['fav_country'], row['fav_food'], 'Original File'))
            conn.commit()
        except FileNotFoundError:
            print(f"Warning: {original_csv} not found. Starting with an empty database.")

    # Show the current database contents BEFORE any user input
    print("\n--- Current Database Contents ---")
    display_database(cursor)

    session_changes = 0

    # 2. Start the interactive command loop
    while True:
        cmd = input("Enter command (type 'add' to insert, 'view' to see data, 'quit' to save & exit): ").strip().lower()
        
        if cmd == 'add':
            sp = input("Superpower: ")
            fname = input("First Name: ")
            lname = input("Last Name: ")
            
            while True:
                try:
                    age = int(input("Age (number): "))
                    break
                except ValueError:
                    print("Please enter a valid number.")
                    
            country = input("Favorite Country: ")
            food = input("Favorite Food: ")
            
            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            changes_before = conn.total_changes
            
            cursor.execute('''
                INSERT INTO superpowers 
                (superpower, first_name, last_name, age, fav_country, fav_food, date_added)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sp, fname, lname, age, country, food, current_date))
            conn.commit()
            
            # Track changes
            changes_made = conn.total_changes - changes_before
            session_changes += changes_made
            print(f"\n-> Successfully added {fname}! Total changes made this session: {session_changes}")
            
            # Show the updated database contents AFTER the new entry is made
            print("\n--- Updated Database Contents ---")
            display_database(cursor)

        elif cmd == 'view':
            display_database(cursor)

        elif cmd == 'quit':
            # 3. Export everything to a new CSV sheet
            today_str = datetime.datetime.now().strftime("%Y-%m-%d")
            new_csv_filename = folder_path + f"superpowers_updated_{today_str}.csv"
            
            print(f"\nExporting your database to a new sheet: {new_csv_filename}...")
            cursor.execute("SELECT * FROM superpowers")
            all_rows = cursor.fetchall()
            
            with open(new_csv_filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['superpower', 'first_name', 'last_name', 'age', 'fav_country', 'fav_food', 'date_added'])
                writer.writerows(all_rows)
            
            print("Export complete. Goodbye!")
            break
            
        else:
            print("Command not recognized. Please type 'add', 'view', or 'quit'.")

    conn.close()

if __name__ == "__main__":
    manage_superpowers()