#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Student database
students = {}

def register():
    print("Registration Form")
    print("------------------")
    print("REGISTER TO LNCT")
    name = input("Enter your name: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return register()
    email = input("Enter your email: ")
    phone = input("Enter your phone number: ")
    address = input("Enter your address: ")
    city = input("Enter your city: ")
    state = input("Enter your state: ")
    country = input("Enter your country: ")
    pincode = input("Enter your pincode: ")

    student = {
        "name": name,
        "username": username,
        "password": password,
        "email": email,
        "phone": phone,
        "address": address,
        "city": city,
        "state": state,
        "country": country,
        "pincode": pincode
    }

    students[username] = student
    print("Registration successful!")
    print("welcome to LNCT")


def login():
    print("Login Form")
    print("-----------")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in students and students[username]["password"] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid username or password. Please try again.")
        return login()

def show_profile(username):
    print("Profile")
    print("-------")
    student = students[username]
    for key, value in student.items():
        print(f"{key.capitalize()}: {value}")

def update_profile(username):
    print("Update Profile")
    print("--------------")
    student = students[username]
    print("Enter new details (press enter to skip):")
    for key in student.keys():
        if key not in ["username", "password"]:
            new_value = input(f"{key.capitalize()}: ")
            if new_value:
                student[key] = new_value
    students[username] = student
    print("Profile updated successfully!")

def main():
    while True:
        print("Student System")
        print("--------------")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                while True:
                    print("Dashboard")
                    print("---------")
                    print("1. Show Profile")
                    print("2. Update Profile")
                    print("3. Logout")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        show_profile(username)
                    elif choice == "2":
                        update_profile(username)
                    elif choice == "3":
                        print("Logged out successfully!")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 


# In[ ]:




