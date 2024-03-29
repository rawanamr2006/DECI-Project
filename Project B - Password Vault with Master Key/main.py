# Setup & Imports 
import getpass, hashlib, os
from cryptography.fernet import Fernet

# Some Variables
run = True
takingInput = True
loginAttempts = 0

# Functions

def createMasterKey():
    new_master_key = bytes(getpass.getpass("Input your new master key to be created(hidden, type anyway): "), "utf-8")
    hashed_key = hashlib.sha256(new_master_key).hexdigest()

    master_key_file = open("master_key.key", "x")
    master_key_file.write(hashed_key)

    master_key_file.close()

def isKeyValid():
    master_key = bytes(getpass.getpass("\nInput your master key to authenticate: \n"), "utf-8")
    hashed_key = hashlib.sha256(master_key).hexdigest()

    with open("master_key.key", "r") as real_key_file:
        real_master_key = real_key_file.read()

    return real_master_key == hashed_key

def authenticate():
    global loginAttempts, takingInput, run

    if isKeyValid():
        print("\nAuthentication Success !\n")

        while takingInput:
            prompt = input("\nPress 'i' to input new password record or 'r' to retreive stored data or 'q' to quit ('i' or 'r' or 'q'): ")

            if prompt == "q":
                takingInput = False
            elif prompt == "i":
                takeInput()
            elif prompt == "r":
                retreivePassword()
            else:
                print("\nInvalid option !! try a valid one ...")
    else:
        loginAttempts += 1
        if loginAttempts <= 4:
            print("\nInvalid Key, Try again...")
            authenticate()
        else:
            print("Login attempts Exceeded the Limit and you are locked out ! Try again Later..")
            run = False

def takeInput():
    print("\nFill the following fields to store your password: \n")
    domain = input("Domain/website: ")
    username = input("username: ")
    password = bytes(getpass.getpass("Password(hidden, type anyway): "), "utf-8")

    key = Fernet.generate_key()
    f = Fernet(key)

    encrypted_passwd = f.encrypt(password)
    hashed_passwd = hashlib.sha256(password).hexdigest()

    record = ":".join([domain,username,key.decode("utf-8"),encrypted_passwd.decode("utf-8") ,hashed_passwd])
    
    with open("vault.vlt", "a") as vault:
        vault.write("\n" + record)

    vault.close()
        
def retreivePassword():
    requested_domain = input("\nDomain: ")
    found = False
    with open("vault.vlt", "r") as vault:
        for line in vault.readlines()[1:]:
            domain,username,key,encrypted_passwd ,hashed_passwd = line.split(":")
            
            if domain == requested_domain:
                f = Fernet(key)
                passwd = f.decrypt(bytes(encrypted_passwd, "utf-8"))

                print("\nCredentials for", domain, "\nUsername: ", username, "\nPassword: ", passwd.decode("utf-8"))
                found = True

        if not found: 
            print("\nDidn't find the domain you requested, Search for a valid domain...")

    vault.close()


# Main Loop

while run:
    state = input("Press 'k' for master key creation. If already done press 'a' to authenticate or 'q' to quit ('k' or 'a' or 'q'): ")

    if state == "q":
        run = False
    
    # Master Key Creation and Hashing
    elif state == "k":
        if os.path.exists("master_key.key"):
            print("Already Exists.\nYou have already created a master key.")
            authenticate()
        else:
            createMasterKey()

    # Authentication and key verification        
    elif state == "a":  
        authenticate()
    
    else:
        print("\nInvalid option !! try a valid one ...")

    # Securely Storing Passwords ( Taking User Input , Password Encryption , Password Hashing and Storage )
    # Retrieving Passwords ( Implementing a functon , after successful authN , Decrepting Passwords )
