#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import os
import random
from datetime import datetime


USERS_FILE = "students.json"
SCORES_FILE = "quiz_scores.json"
QUESTIONS_FILE = "quiz_questions.json"


DEFAULT_ADMIN = {"username": "admin", "password": "admin123"}

def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)



def register():
    users = load_json(USERS_FILE, [])
    print("\n--- Registration ---")
    name = input("Enter your name: ")
    username = input("Enter your username: ")

    for u in users:
        if u["username"] == username:
            print("Username already exists. Try another.")
            return

    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")
    if password != confirm_password:
        print("Passwords do not match. Try again.")
        return

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
        "pincode": pincode,
        "role": "student"
    }

    users.append(student)
    save_json(USERS_FILE, users)
    print("Registration successful!\n")

def login():
    users = load_json(USERS_FILE, [])
    print("\n--- Login ---")
    username = input("Username: ")
    password = input("Password: ")

    # Check admin
    if username == DEFAULT_ADMIN["username"] and password == DEFAULT_ADMIN["password"]:
        print("Admin login successful!\n")
        return {"username": "admin", "role": "admin"}

    for u in users:
        if u["username"] == username and u["password"] == password:
            print(f"Welcome {u['name']}!\n")
            return u

    print("Invalid credentials.\n")
    return None

def show_profile(user):
    print("\n--- Profile ---")
    for k, v in user.items():
        if k != "password":
            print(f"{k.capitalize()}: {v}")
    print()

def update_profile(user):
    users = load_json(USERS_FILE, [])
    print("\n--- Update Profile ---")
    for field in ["name", "email", "phone", "address", "city", "state", "country", "pincode"]:
        cur = user.get(field, "")
        new_val = input(f"{field.capitalize()} ({cur}): ")
        if new_val:
            user[field] = new_val

    for i, u in enumerate(users):
        if u["username"] == user["username"]:
            users[i] = user
            break
    save_json(USERS_FILE, users)
    print("Profile updated successfully!\n")


def load_questions():
    return load_json(QUESTIONS_FILE, {
        "DSA": [],
        "DBMS": [],
        "PYTHON": []
    })

def save_questions(data):
    save_json(QUESTIONS_FILE, data)

def add_question():
    questions = load_questions()
    print("\n--- Add Quiz Question ---")
    print("Categories: DSA, DBMS, PYTHON")
    cat = input("Enter category: ").upper()
    if cat not in questions:
        print("Invalid category.")
        return

    q_text = input("Question: ")
    options = []
    for i in range(4):
        opt = input(f"Option {i+1}: ")
        options.append(opt)
    correct = input("Enter correct option number (1-4): ")

    if not correct.isdigit() or not (1 <= int(correct) <= 4):
        print("Invalid correct option number.")
        return

    question = {
        "question": q_text,
        "options": options,
        "answer": options[int(correct) - 1]
    }
    questions[cat].append(question)
    save_questions(questions)
    print("Question added successfully!\n")

def attempt_quiz(user):
    questions = load_questions()
    print("\n--- Quiz Categories ---")
    print("1. DSA\n2. DBMS\n3. PYTHON")
    choice = input("Select category number: ")

    if choice == "1":
        cat = "DSA"
    elif choice == "2":
        cat = "DBMS"
    elif choice == "3":
        cat = "PYTHON"
    else:
        print("Invalid choice.")
        return

    q_list = questions[cat]
    if not q_list:
        print("No questions in this category yet.\n")
        return

    random.shuffle(q_list)
    selected = q_list[:5]
    score = 0

    for i, q in enumerate(selected, start=1):
        print(f"\nQ{i}. {q['question']}")
        for j, opt in enumerate(q["options"], start=1):
            print(f"{j}. {opt}")
        ans = input("Your answer (1-4): ")
        if ans.isdigit() and 1 <= int(ans) <= 4:
            chosen = q["options"][int(ans) - 1]
            if chosen == q["answer"]:
                print(" Correct!")
                score += 1
            else:
                print(f"Incorrect! Correct answer: {q['answer']}")
        else:
            print("Invalid input. Skipped question.")

    print(f"\nQuiz Complete! You scored {score}/{len(selected)}.\n")
    record_score(user["username"], cat, score, len(selected))

def record_score(username, category, score, total):
    scores = load_json(SCORES_FILE, [])
    scores.append({
        "username": username,
        "category": category,
        "score": score,
        "total": total,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_json(SCORES_FILE, scores)

def view_my_scores(username):
    scores = load_json(SCORES_FILE, [])
    user_scores = [s for s in scores if s["username"] == username]
    if not user_scores:
        print("No quiz records found.\n")
        return
    print("\n--- Your Quiz Scores ---")
    for s in user_scores:
        print(f"{s['datetime']} | {s['category']} | {s['score']}/{s['total']}")
    print()

def view_all_scores():
    scores = load_json(SCORES_FILE, [])
    if not scores:
        print("No quiz attempts yet.\n")
        return
    print("\n--- All Quiz Scores ---")
    for s in scores:
        print(f"{s['datetime']} | {s['username']} | {s['category']} | {s['score']}/{s['total']}")
    print()

def view_all_users():
    users = load_json(USERS_FILE, [])
    print("\n--- Registered Students ---")
    for u in users:
        print(f"{u['username']} - {u['name']} - {u['email']}")
    print()


def student_dashboard(user):
    while True:
        print("Student Dashboard")
        print("-----------------")
        print("1. Show Profile")
        print("2. Update Profile")
        print("3. Attempt Quiz")
        print("4. View My Scores")
        print("5. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            show_profile(user)
        elif choice == "2":
            update_profile(user)
        elif choice == "3":
            attempt_quiz(user)
        elif choice == "4":
            view_my_scores(user["username"])
        elif choice == "5":
            print("Logged out.\n")
            break
        else:
            print("Invalid choice.\n")

def admin_dashboard():
    while True:
        print("Admin Dashboard")
        print("----------------")
        print("1. Add Quiz Question")
        print("2. View All Scores")
        print("3. View All Students")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_question()
        elif choice == "2":
            view_all_scores()
        elif choice == "3":
            view_all_users()
        elif choice == "4":
            print("Admin logged out.\n")
            break
        else:
            print("Invalid choice.\n")


def main():
    while True:
        print("STUDENT SYSTEM WITH QUIZ MODULE")
        print("-------------------------------")
        print("1. Register")
        print("2. Login (Student/Admin)")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                if user["username"] == "admin":
                    admin_dashboard()
                else:
                    student_dashboard(user)
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()


# In[ ]:




