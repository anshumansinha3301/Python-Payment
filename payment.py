import stripe
import getpass


stripe.api_key = "your_secret_key_here"

users_db = {}

def create_account():
    print("\n--- Create Account ---")
    email = input("Enter your email: ")
    if email in users_db:
        print("Account already exists.")
        return
    password = getpass.getpass("Enter your password: ")
    users_db[email] = {
        "password": password,
        "payment_methods": [],
    }
    print("Account created successfully.")

def access_account():
    print("\n--- Access Account ---")
    email = input("Enter your email: ")
    if email not in users_db:
        print("Account not found.")
        return None
    password = getpass.getpass("Enter your password: ")
    if users_db[email]["password"] != password:
        print("Incorrect password.")
        return None
    return email

def add_payment_method(user_email):
    print("\n--- Add Payment Method ---")
    
    payment_method_id = "pm_card_visa"
    users_db[user_email]["payment_methods"].append(payment_method_id)
    print(f"Payment method {payment_method_id} added.")

def create_payment_intent(amount, currency="usd", payment_method_types=["card"]):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=payment_method_types,
        )
        return payment_intent
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def pay(user_email):
    print("\n--- Make a Payment ---")
    if not users_db[user_email]["payment_methods"]:
        print("No payment methods available. Please add a payment method first.")
        return

    amount = int(input("Enter amount in cents (e.g., 5000 for $50.00): "))
    payment_intent = create_payment_intent(amount)
    if payment_intent:
        print(f"Created PaymentIntent: {payment_intent.id}")

       
        payment_method_id = users_db[user_email]["payment_methods"][0]
        try:
            confirmed_intent = stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method=payment_method_id,
            )
            print(f"Payment successful! PaymentIntent ID: {confirmed_intent.id}")
        except Exception as e:
            print(f"An error occurred during payment confirmation: {e}")

def main():
    while True:
        print("\n--- Payment Gateway ---")
        print("1. Create Account")
        print("2. Access Account")
        print("3. Make a Payment")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            user_email = access_account()
            if user_email:
                print("Access granted.")
                while True:
                    print("\n--- Account Menu ---")
                    print("1. Add Payment Method")
                    print("2. Make a Payment")
                    print("3. Log Out")
                    account_choice = input("Choose an option: ")

                    if account_choice == "1":
                        add_payment_method(user_email)
                    elif account_choice == "2":
                        pay(user_email)
                    elif account_choice == "3":
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            print("Please access your account first.")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
