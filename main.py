import csv
import sys
import string
import secrets
import hashlib
import os

def main():

    if not os.path.exists("master.txt"):
        setup_master_password()

    TRIALS = 0

    while True:
        if not check_master_password():
            print("Incorrect password.")
            TRIALS += 1
            if TRIALS == 3:
                sys.exit("Maximum number of attempts has been exhausted.")
        else:
            break
        

    while True:
        try:
            option = int(input("""Please choose one option:
1. Add new password 
2. Retrieve a password
3. Delete a password
4. See all passwords
5. Create a strong password
6. exit
Which option would you like to choose:  """))

            if option == 1:
                site = input("What is the name of the site? ")
                username = input("What is your username? ")
                password = input("What is your chosen password? ")
                add_entry(site, username, password)

            elif option == 2:
                u = input("What is the site's name: ")
                get_entry(u)

            elif option == 3:
                d = input("What is the site's name whose password you would like to delete: ")
                delete_entry(d)

            elif option == 4:
                list_entries()

            elif option == 5:
                x = generate_password()
                print(f"This is your randomly generated password: {x}")

            elif option == 6:
                break

            else:
                print("\nPlease choose options 1 to 6.\n")

        except ValueError:
            print("Please choose options 1 to 6.")


def setup_master_password():
    pw = input("Create a master password: ")
    hashed = hashlib.sha256(pw.encode()).hexdigest()
    with open("master.txt", "w") as f:
        f.write(hashed)

def check_master_password():
    with open("master.txt", "r") as f:
        stored_hash = f.read().strip()

    attempt = input("Enter master password: ")
    attempt_hash = hashlib.sha256(attempt.encode()).hexdigest()

    return attempt_hash == stored_hash

    
def add_entry(site, username, password):
    try:
        with open("passwords.csv", "a", newline="") as file:
            fieldnames = ["site", "username", "password"]
            writer = csv.DictWriter(file, fieldnames = fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow({'site': site, 'username': username, 'password': password})
        print("\nPassword added!\n")
    except:
        print("An error seems to have occured")


def get_entry(site):
    try:
        with open("passwords.csv", newline = "") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["site"] == site:
                    print(row["password"])
                    return

            print("\nThis site is not in your list of passwords.\n")
    except FileNotFoundError:
        print("\nThere is no passwords saved.\n")

def delete_entry(site):
    try:
        with open("passwords.csv", newline = "") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            for row in rows:
                if row["site"] == site:
                    rows = [row for row in rows if row["site"] != site]

                    with open("passwords.csv", "w", newline="") as file:
                        fieldnames = ["site", "username", "password"]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)

                        writer.writeheader()
                        writer.writerows(rows)
                    print("\npassword deleted!\n")
                    return
                
            print("\nThis site is not in your list of passwords.\n")
    except FileNotFoundError:
        print("\nThere is no passwords saved.\n")


def list_entries():
    try:
        with open("passwords.csv") as file:
            reader = csv.DictReader(file)
            print(list(reader))
    except FileNotFoundError:
        print("\nThere is no passwords saved.\n")      


def generate_password(length = 16):
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password



if __name__ == "__main__":
    main()