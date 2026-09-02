# 🔐 SecurePass — Python Password Manager

A secure command-line password manager built in Python with **encrypted local storage, password-based key derivation, secure password generation, and master-password authentication**.

The project was built to explore practical applications of Python, cryptography, file handling, and secure credential management.

---

## ✨ Features

* 🔑 **Master password authentication**

  * Protects access to the password manager
  * Limits authentication attempts to 3
  * Master password is never stored directly

* 🔒 **Encrypted password database**

  * Password entries are encrypted before being written to disk
  * Uses **Fernet symmetric encryption**
  * Password data is never stored as plaintext in `passwords.csv`

* 🧂 **Salted key derivation**

  * Generates a unique cryptographic salt during setup
  * Uses **PBKDF2-HMAC with SHA-256** to derive the encryption key from the master password

* 🎲 **Secure password generation**

  * Uses Python's `secrets` module rather than the standard `random` module
  * Generates passwords containing uppercase letters, lowercase letters and numbers

* 📁 **CSV-based storage**

  * Simple and portable local database
  * Automatically encrypted before being saved

* 🛠️ **CRUD functionality**

  * Add passwords
  * Retrieve passwords
  * Delete passwords
  * View stored entries

* ⚡ **Command-line interface**

  * Lightweight
  * No external database required
  * Runs locally

---

## 🏗️ How It Works

The application follows a simple security architecture:

```text
                   ┌─────────────────┐
                   │  Master Password │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │     PBKDF2      │
                   │   + SHA-256     │
                   │   + Random Salt │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Derived Key    │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │     Fernet      │
                   │    Encryption   │
                   └────────┬────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  passwords.csv   │
                  │  (Encrypted)     │
                  └──────────────────┘
```

### Encryption flow

When the user creates their master password:

1. A random 16-byte salt is generated.
2. The master password is processed using PBKDF2-HMAC-SHA256.
3. A 32-byte encryption key is derived.
4. The key is encoded into a Fernet-compatible format.
5. The password database is encrypted using Fernet.

When the user logs in:

1. The master password is entered.
2. The stored salt is retrieved.
3. PBKDF2 derives the encryption key again.
4. The resulting key is used to initialise Fernet.
5. The encrypted database can then be decrypted.

---

## 🔐 Security

Security was a core consideration when designing this project.

### Fernet Encryption

The password database is encrypted using Fernet symmetric authenticated encryption.

Instead of storing:

```text
Google,myemail@gmail.com,password123
```

the file contains encrypted ciphertext.

### PBKDF2

The encryption key is **derived from the user's master password** rather than being hard-coded into the application.

```python
PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100_000
)
```

A random salt ensures that identical master passwords do not automatically produce identical derived keys across installations.

### Secure Randomness

Password generation uses Python's cryptographically secure `secrets` module:

```python
secrets.choice(alphabet)
```

rather than `random.choice()`.

---

## 🖥️ Application Menu

When launched, SecurePass provides the following options:

```text
Please choose one option:

1. Add new password
2. Retrieve a password
3. Delete a password
4. See all passwords
5. Create a strong password
6. Exit
```

### Add a password

Stores a website, username and password in the encrypted database.

### Retrieve a password

Searches the encrypted database for a specific website and displays the corresponding password.

### Delete a password

Removes the selected website and its credentials from the database.

### Generate a password

Creates a random password using a cryptographically secure random number generator.

---

## 📂 Project Structure

```text
SecurePass/
│
├── password_manager.py
├── master.txt
├── passwords.csv
└── README.md
```

### `password_manager.py`

Contains the complete password manager application, including:

* Authentication
* Key derivation
* Encryption/decryption
* CSV management
* Password generation
* Command-line interface

### `master.txt`

Stores the information required to verify the master password and the cryptographic salt.

### `passwords.csv`

Contains the encrypted password database.

**The contents of this file should never be committed to GitHub.**

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/SecurePass.git
cd SecurePass
```

### 2. Install the dependency

```bash
pip install cryptography
```

Or, if a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python password_manager.py
```

On the first launch, you will be prompted to create a master password.

---

## ⚠️ Important Security Notice

This project is primarily an **educational and portfolio project** demonstrating the implementation of cryptographic concepts in Python.

It has **not been independently audited or penetration tested** and should not be considered equivalent to established production password managers.

For example, further improvements could include:

* Stronger password hashing/KDF configuration
* Secure password input using `getpass`
* Automatic database backups
* Password-update functionality
* Improved secret/key management
* More robust error handling
* Memory protection for sensitive values
* Secure deletion considerations
* Security testing and auditing

**Never commit ****`master.txt`**** or ****`passwords.csv`**** to a public repository.**

A suitable `.gitignore` would include:

```gitignore
master.txt
passwords.csv
__pycache__/
*.pyc
```

---

## 🧠 What I Learned

This project helped me develop practical experience with:

### Python

* Functions and modular programming
* Exception handling
* File I/O
* CSV processing
* List comprehensions
* String manipulation
* Command-line applications

### Cybersecurity

* Symmetric encryption
* Password-based key derivation
* Cryptographic salts
* Secure random number generation
* Authentication
* Secure credential storage

### Software Engineering

* Breaking a larger application into reusable functions
* Managing application state
* Designing a command-line interface
* Handling invalid user input
* Thinking about security when designing software

---

## 🛣️ Future Improvements

Potential future versions could introduce:

* [ ] Secure password input with `getpass`
* [ ] Password update functionality
* [ ] Username retrieval
* [ ] Search functionality
* [ ] Password strength analysis
* [ ] Configurable password generation
* [ ] Improved authentication hashing
* [ ] Stronger PBKDF2 configuration
* [ ] Automated tests
* [ ] Logging and structured error handling
* [ ] More sophisticated CLI interface
* [ ] Secure backup/export functionality
* [ ] Security audit and penetration testing

---

## 📊 Technologies

| Technology      | Purpose                            |
| --------------- | ---------------------------------- |
| **Python**      | Core application                   |
| **CSV**         | Local data representation          |
| **Fernet**      | Symmetric authenticated encryption |
| **PBKDF2-HMAC** | Password-based key derivation      |
| **SHA-256**     | Cryptographic hashing              |
| **secrets**     | Secure password generation         |
| **Base64**      | Fernet key encoding                |

---

## 👨‍💻 Author

**Gurleen Singh**

Built as a personal project to strengthen my understanding of **Python, cybersecurity, cryptography and software engineering**.

---

## ⭐ If you found this project useful

Feel free to explore the code, suggest improvements, or use the project as a learning resource.

**Built with Python 🐍**
