import csv

def main():
    option = int(input("""Please choose one option:
1. Add new password 
2. Retrieve a password
3. Delete a password
4. See all passwords
5. Create a strong password
Which option would you like to choose:  """))

    if option == 1:

        site = input("What is the name of the site? ")
        username = input("What is your username? ")
        password = input("What is your chosen password? ")
        add_entry(site, username, password)
        print("password added!")

    elif option == 2:
        u = input("What is the site's name: ")
        get_entry(u)

    elif option == 3:
        d = input("What is the site's name whose password you would like to delete: ")
        delete_entry(d)

    elif option == 4:
        list_entries()

    elif option == 5:
        generate_password()
    

def add_entry(site, username, password):
    with open("passwords.csv", "a", newline="") as file:
        fieldnames = ["site", "username", "password"]
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow({'site': site, 'username': username, 'password': password})

def get_entry(site):
    with open("passwords.csv", newline = "") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["site"] == site:
                print(row["password"])

def delete_entry(site):
    with open("passwords.csv", newline = "") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    rows = [row for row in rows if row["site"] != site]

    with open("passwords.csv", "w", newline="") as file:
        fieldnames = ["site", "username", "password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(rows)

def list_entries():
    ...

def generate_password(length, use_symbols=True):
    ...



if __name__ == "__main__":
    main()