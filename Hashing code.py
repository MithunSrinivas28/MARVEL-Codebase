import hashlib
import os

# File to store hashed passwords
PASSWORD_FILE = "passwords.txt"

def hash_password(password):
    """Hashes a password using SHA-256 and returns the hex digest."""
    salt = os.urandom(32)  # Generate a random 32-byte salt
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex() + ":" + hashed.hex()  # Store salt and hash together

def save_password(username, hashed_password):
    """Saves the hashed password to a file."""
    with open(PASSWORD_FILE, "a") as file:
        file.write(f"{username}:{hashed_password}\n")

def load_passwords():
    """Loads stored passwords into a dictionary."""
    passwords = {}
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            for line in file:
                username, stored_hash = line.strip().split(":", 1)
                passwords[username] = stored_hash
    return passwords

def verify_password(username, password):
    """Verifies if the entered password matches the stored hash."""
    passwords = load_passwords()
    
    if username not in passwords:
        return False  # User not found
    
    stored_salt, stored_hash = passwords[username].split(":")
    salt = bytes.fromhex(stored_salt)
    new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()
    
    return new_hash == stored_hash  # Return True if passwords match

def register():
    """Registers a new user with a hashed password."""
    username = input("Enter a username: ").strip()
    passwords = load_passwords()

    if username in passwords:
        print("Username already exists! Choose a different one.")
        return
    
    password = input("Enter a password: ").strip()
    hashed_password = hash_password(password)
    save_password(username, hashed_password)
    print("User registered successfully!")

def login():
    """Authenticates a user by verifying their password."""
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()

    if verify_password(username, password):
        print("Login successful!")
    else:
        print("Invalid username or password.")

def main():
    """Main menu loop."""
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
