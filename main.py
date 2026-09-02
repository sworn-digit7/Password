import csv
import sys
import string
import secrets
import hashlib
import os
import io
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

FERNET = None  # set globally once the master password is verified


def derive_key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100_000)
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


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
    salt = os.urandom(16)
    hashed = hashlib.sha256(pw.encode()).hexdigest()
    with open("master.txt", "w") as f:
        f.write(hashed + "\n" + salt.hex())


def check_master_password():
    global FERNET
    with open("master.txt", "r") as f:
        stored_hash, salt_hex = f.read().strip().split("\n")
    salt = bytes.fromhex(salt_hex)

    attempt = input("Enter master password: ")
    attempt_hash = hashlib.sha256(attempt.encode()).hexdigest()

    if attempt_hash == stored_hash:
        FERNET = Fernet(derive_key(attempt, salt))
        return True
    return False


def load_rows():
    """Decrypts passwords.csv and returns its rows as a list of dicts."""
    if not os.path.exists("passwords.csv"):
        return []
    with open("passwords.csv", "rb") as f:
        encrypted = f.read()
    if not encrypted:
        return []
    decrypted = FERNET.decrypt(encrypted).decode()
    reader = csv.DictReader(io.StringIO(decrypted))
    return list(reader)


def save_rows(rows):
    """Writes rows back to passwords.csv, encrypted."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["site", "username", "password"])
    writer.writeheader()
    writer.writerows(rows)
    encrypted = FERNET.encrypt(output.getvalue().encode())
    with open("passwords.csv", "wb") as f:
        f.write(encrypted)


def add_entry(site, username, password):
    try:
        rows = load_rows()
        for row in rows:
            if row["site"] == site:
                print("\nThis site already has a password, if you wish to update this password please first delete it.\n")
                return
        rows.append({"site": site, "username": username, "password": password})
        save_rows(rows)
        print("\nPassword added!\n")
    except Exception:
        print("An error seems to have occured")


def get_entry(site):
    rows = load_rows()
    for row in rows:
        if row["site"] == site:
            print(row["password"])
            return
    print("\nThis site is not in your list of passwords.\n")


def delete_entry(site):
    rows = load_rows()
    for row in rows:
        if row["site"] == site:
            rows = [r for r in rows if r["site"] != site]
            save_rows(rows)
            print("\npassword deleted!\n")
            return
    print("\nThis site is not in your list of passwords.\n")


def list_entries():
    rows = load_rows()
    print(rows)


def generate_password(length=16):
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