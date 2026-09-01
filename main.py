def main():
    site = input("What is the name of the site? ")
    username = input("What is your username? ")
    password = input("What is your chosen password? ")
    add_entry(site, username, password)

def add_entry(site, username, password):
    passwords = {}

    passwords["site: "] = site
    passwords["username: "] = username
    passwords["password: "] = password
    print(passwords)

def get_entry(site):
    ...

def delete_entry(site):
    ...

def list_entries():
    ...

def generate_password(length, use_symbols=True):
    ...



if __name__ == "__main__":
    main()