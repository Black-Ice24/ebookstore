# Compulsory Task 

# Import sqlite 
import sqlite3

try: 
    # Creates or open a file with SQLite3 DB called 'ebookstore'
    db = sqlite3.connect('ebookstore')

    # Create a cursor object to make changes to the dataase 
    cursor = db.cursor() # Get a cursor object

    # Create the table in the database if it doesn't already exist 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books(
            id INTEGER, 
            Title TEXT,
            Author TEXT,
            Qty INTEGER,
            PRIMARY KEY (id))
    ''')

    # Starting data for table 
    starting_data = [
        (3001, "A Tale of Two Cities", 'Charles Dickens', 30),
        (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
        (3003, "The Lion, the Witch and the Wardrobe", 'C. S. Lewis', 25),
        (3004, "The Lord of the Rings", 'J.R.R Tolkien', 37),
        (3005, "Alice in Wonderland", 'Lewis Carroll', 12),
    ]

    
    # Insert the starting data into the table - don't insert starting data if already in table
    cursor.executemany(''' 
        INSERT OR IGNORE INTO books(id, Title, Author, Qty) VALUES(?,?,?,?)''',
        starting_data)

    # Commit the change
    db.commit()

    
except Exception as e:
    print("Sorry, something went wrong!")
    raise e 




# Function that checks what the last id is in the database and suggests another one
def id_already_exists():
    cursor.execute('''SELECT id FROM books ORDER BY id DESC''')
    id_reminder = cursor.fetchone()[0]

    print("\n \nUnfortunately this id already exists in the database\n")
    print(f"Please enter a different id (Perhaps try id {id_reminder + 1})?\n")


# Function that checks if id is in the database 
def check_id(input_id):
    list_of_ids = []
    # Check ID is in database 
    cursor.execute('''SELECT id FROM books''')
    for row in cursor:
        list_of_ids.append(row[0])

    if input_id not in list_of_ids:
        print("\nSorry, the ID you have selected is not in the database\n")
        return False 
    else:
        return True 


# Function that takes a list of the search results and prints them out 
def search_results(search_result):

    # Print search results to user or notify if search was empty 
    if not search_result:
        print("\nThere are no books matching your search!\n")

        return True 
        
    else:
        print("\n-- SEARCH RESULTS --\n")

        for count, book_result in enumerate(search_result): 
            id = book_result[0]
            title = book_result[1]
            author = book_result[2]
            qty = book_result[3]

            print(f"Book: {count + 1}\n")

            print(f"ID: {id}")
            print(f"TITLE: {title}")
            print(f"AUTHOR: {author}")
            print(f"QTY: {qty}\n")

        return True 
                    
    
        


run_loop = True 


# While loop that will return user to main menu after they have carried out their decision
while run_loop:

    # Display main menu 
    print("--- MAIN MENU ---\n")
    print("1. Enter book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Search books")
    print("0. Exit\n")

    try: 
        # Request user input 
        user_input = int(input("Choose from the above options (Enter the desired number): "))
    except ValueError as v: 
        print("\nPlease try again and make sure you have entered a valid number from 0 -4\n")
        continue


    # Enter book
    if user_input == 1: 

        book_loop = True 

        while book_loop:

            try: 

                print("\n--ENTER BOOK--")
                
                # Request user details for book 
                enter_id = input("\nPlease enter the ID of the book you would like to enter: ")
                enter_title = input("\nPlease enter the TITLE of the book you would like to enter: ")
                enter_author = input("\nPlease enter the AUTHOR of the book you would like to enter: ")


                # Ensure the user enters a number for QTY - else request the user to try again 
                try: 
                    enter_qty = int(input("\nPlease enter QTY of the book you would like to enter: "))

                except ValueError as v:
                    print("\nError: Make sure that the QTY of the book is entered as a number! Please try again\n")
                    continue


                # Insert book into database
                cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                            VALUES(?,?,?,?)''', (enter_id, enter_title, enter_author, enter_qty))
                
                # Commit the change
                db.commit()

                # Notify user that book was successfully added to the database
                print(f'\nThe book was successfully entered into the database!\n')

                break 

            # Notify the user if id they selected already exists in database and suggest another id
            except sqlite3.IntegrityError as e: 
                id_already_exists()


                

          
    # Update book
    elif user_input == 2: 

        run_update_loop = True

        while run_update_loop:

            print("\n--UPDATE BOOK--\n")

            try: 
                # Request user to input id of the book they would like to update 
                update_id = int(input("Enter the ID of the book you would like to update: "))

                # Check if id is in database and request another id if it is 
                if check_id(update_id):
                    pass
                else: 
                    continue
            

                # Request which field the user would like to update 
                update_choice = int(input("\nWould you like to update:\n1. id\n2. Title\n3. Author \n4. Qty\nPlease enter a number: "))

            # Catch error if user enters an invalid character 
            except ValueError as v: 
                print("Please make sure you have entered a number! Please try again")
                continue


            


                
            # User would like to update ID -- 
            if update_choice == 1:
                
                try:
                    # Request the new ID user would like to change id to 
                    new_id = int(input("\nEnter the new id: "))
                except ValueError as v: 
                    print("Please make sure you have entered a number! Please try again")
                    continue


                try:
                    # Update database
                    cursor.execute('''UPDATE books SET id = ? WHERE id = ? ''',
                    (new_id, update_id))

                    print("\nID has been updated!\n")

                    # Commit the change
                    db.commit()

        
                  # Notify the user if id they selected already exists in database and suggest another id
                except sqlite3.IntegrityError as e: 

                    id_already_exists()


            # User would like to update TITLE -- 
            elif update_choice == 2:

                new_title = input("\nEnter the new title: ")

                # Update database
                cursor.execute('''UPDATE books SET Title = ? WHERE id = ? ''',
                (new_title, update_id))

                print("\nTITLE has been updated!\n")
                # Commit the change
                db.commit()

            # User would like to update AUTHOR
            elif update_choice == 3:

                new_author = input("\nEnter the new author: ")

                # Update database
                cursor.execute('''UPDATE books SET Author = ? WHERE id = ? ''',
                (new_author, update_id))

                print("\nAUTHOR has been updated!\n")

                # Commit the change
                db.commit()

            # User would like to update QTY
            elif update_choice == 4:

                try: 
                    new_qty = int(input("\nEnter the new qty: "))

                # Ensure that user inputs a number and not an invalid character 
                except ValueError as v:
                    print("\nError: Make sure that the QTY of the book is entered as a number! Please try again\n")
                    continue

                # Update database 
                cursor.execute('''UPDATE books SET Qty = ? WHERE id = ? ''',
                (new_qty, update_id))

                print("\nQTY has been updated!\n")
                # Commit the change
                db.commit()

            else:
                # Notify user of invalid input 
                print("\nInvalid input. Please enter a number from 1 - 4\n")
                continue

            continue_update = input("Would you like to update another book? (Y/N): ")

            if continue_update == "Y":
                continue
            elif continue_update == "N":
                break 



    # Delete book
    elif user_input == 3: 

        delete_loop = True 

        while delete_loop:

            # Request id of book user would like to delete 
            try:
                id_of_book_to_delete = int(input("Please enter the id of the book you would like to delete: "))

                # Check if id is in the database 
                if check_id(id_of_book_to_delete):
                    pass
                else: 
                    continue

            # Ensure user input is a number 
            except ValueError as v: 
                print("Please make sure you have entered a number! Please try again")
                continue

            # Confirm users choice 
            confirm = input(f"Are sure you would like to delete book with id {id_of_book_to_delete} from the database (Y/N)? ")

            # If user confirms deletion then delete from database 
            if confirm == 'Y':
                cursor.execute('''DELETE FROM books WHERE id = ? ''', (id_of_book_to_delete,))

                print("\nBook has been deleted!\n")
                # Commit the change
                db.commit()
                break 

            # If user decides not to delete then return to main menu 
            if confirm == 'N':
                print("You will be returned to the main menu")
                break 

            # Catch invalid inputs 
            else: 
                print("Invalid input. Please try again")
                continue 



    # Search books
    elif user_input == 4:

        search_loop = True 

        while search_loop:

            print("\n-- SEARCH BOOKS -- ")
            try:
                # Request how user would like to search for books 
                search_by_choice = int(input("\nHow would you like to search for books?\n1. id\n2. Title\n3. Author\nPlease enter a number: "))

            # Ensure user input is a number 
            except ValueError as v: 
                print("Please make sure you have entered a number! Please try again")
                continue

            if search_by_choice == 1:

                try: 
                    search_id = int(input("\nPlease enter the id number of the book you would like to search: "))

                # Ensure user input is a number 
                except ValueError as v: 
                    print("Please make sure you have entered a number! Please try again")
                    continue

                # Select books by id
                cursor.execute('''SELECT * FROM books WHERE id =? ''', (search_id,))
                list_of_books = cursor.fetchall()
                
                # Print search results and return to main menu 
                if search_results(list_of_books):
                    break

            elif search_by_choice == 2:

                search_title = input("Please enter the Title: ")

                # Select books by id
                cursor.execute('''SELECT * FROM books WHERE Title =? ''', (search_title,))
                list_of_books = cursor.fetchall()

                # Print search results and return to main menu 
                if search_results(list_of_books):
                    break

            elif search_by_choice == 3:

                search_author = input("Please enter the Author: ")

                # Select books by id
                cursor.execute('''SELECT * FROM books WHERE Author =? ''', (search_author,))
                list_of_books = cursor.fetchall()

                # Print search results and return to main menu 
                if search_results(list_of_books):
                    break

            else:
                print("\nInvalid input. Please enter a number from 1 - 3")
            

    # Exit the bookstore
    elif user_input == 0:
        print("\nYou are now exiting the ebookstore.\n")
        break 


    else:
        print("\nInvalid input. Please enter a number from 0-4\n")



