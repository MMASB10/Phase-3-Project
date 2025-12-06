#!/usr/bin/env python3
from .database import init_db, get_session
from .models import Customer, Unit

def display_menu():
    print("\n" + "="*50)
    print("🏢 APARTMENT UNIT ALLOCATOR")
    print("="*50)
    print("1. Customer Management")
    print("2. Unit Management")
    print("3. Exit")
    print("-"*50)

def customer_menu():
    print("\n📋 CUSTOMER MANAGEMENT")
    print("-"*30)
    print("1. Create Customer")
    print("2. View All Customers")
    print("3. Find Customer by ID")
    print("4. View Customer's Units")
    print("5. Delete Customer")
    print("6. Back to Main Menu")
    print("-"*30)

def unit_menu():
    print("\n🏠 UNIT MANAGEMENT")
    print("-"*30)
    print("1. Create Unit")
    print("2. View All Units")
    print("3. Find Unit by ID")
    print("4. Allocate Unit to Customer")
    print("5. Delete Unit")
    print("6. Back to Main Menu")
    print("-"*30)

def get_input(prompt, input_type=str):
    while True:
        try:
            value = input(prompt)
            if input_type != str:
                value = input_type(value)
                if input_type in [int, float] and value <= 0:
                    raise ValueError("Value must be positive")
            return value
        except ValueError as e:
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            exit()

def handle_customer_management():
    session = get_session()
    
    while True:
        customer_menu()
        choice = get_input("Choose an option: ")
        
        try:
            if choice == "1":
                name = get_input("Enter customer name: ")
                budget = get_input("Enter budget: ", float)
                preferences = get_input("Enter preferences (optional): ")
                preferences = preferences if preferences.strip() else None
                
                customer = Customer.create(session, name, budget, preferences)
                print(f"✅ Customer '{customer.name}' created with ID {customer.id}")
                
            elif choice == "2":
                customers = Customer.get_all(session)
                if not customers:
                    print("📭 No customers found")
                else:
                    print(f"\n📋 Found {len(customers)} customers:")
                    for customer in customers:
                        print(f"  ID: {customer.id} | Name: {customer.name} | Budget: ${customer.budget:,.0f}")
                        
            elif choice == "3":
                customer_id = get_input("Enter customer ID: ", int)
                customer = Customer.find_by_id(session, customer_id)
                if customer:
                    print(f"\n👤 Customer Details:")
                    print(f"  ID: {customer.id}")
                    print(f"  Name: {customer.name}")
                    print(f"  Budget: ${customer.budget:,.0f}")
                    print(f"  Preferences: {customer.preferences or 'None'}")
                else:
                    print("❌ Customer not found")
                    
            elif choice == "4":
                customer_id = get_input("Enter customer ID: ", int)
                customer = Customer.find_by_id(session, customer_id)
                if customer:
                    if customer.units:
                        print(f"\n🏠 Units for {customer.name}:")
                        for unit in customer.units:
                            print(f"  {unit.unit_number} | Floor {unit.floor} | {unit.unit_type} | ${unit.price:,.0f}")
                    else:
                        print(f"📭 No units allocated to {customer.name}")
                else:
                    print("❌ Customer not found")
                    
            elif choice == "5":
                customer_id = get_input("Enter customer ID to delete: ", int)
                customer = Customer.find_by_id(session, customer_id)
                if customer:
                    if customer.units:
                        print("❌ Cannot delete customer with allocated units")
                    else:
                        confirm = get_input(f"Delete customer '{customer.name}'? (y/N): ")
                        if confirm.lower() == 'y':
                            customer.delete(session)
                            print("✅ Customer deleted")
                        else:
                            print("❌ Deletion cancelled")
                else:
                    print("❌ Customer not found")
                    
            elif choice == "6":
                break
            else:
                print("❌ Invalid option")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            session.rollback()
    
    session.close()

def handle_unit_management():
    session = get_session()
    
    while True:
        unit_menu()
        choice = get_input("Choose an option: ")
        
        try:
            if choice == "1":
                unit_number = get_input("Enter unit number: ")
                floor = get_input("Enter floor: ", int)
                unit_type = get_input("Enter unit type (e.g., 1BR, 2BR): ")
                price = get_input("Enter price: ", float)
                
                unit = Unit.create(session, unit_number, floor, unit_type, price)
                print(f"✅ Unit '{unit.unit_number}' created")
                
            elif choice == "2":
                units = Unit.get_all(session)
                if not units:
                    print("📭 No units found")
                else:
                    print(f"\n🏠 Found {len(units)} units:")
                    for unit in units:
                        customer_info = f" | Customer: {unit.customer.name}" if unit.customer else ""
                        print(f"  {unit.unit_number} | Floor {unit.floor} | {unit.unit_type} | ${unit.price:,.0f} | {unit.status}{customer_info}")
                        
            elif choice == "3":
                unit_id = get_input("Enter unit ID: ", int)
                unit = Unit.find_by_id(session, unit_id)
                if unit:
                    print(f"\n🏠 Unit Details:")
                    print(f"  ID: {unit.id}")
                    print(f"  Number: {unit.unit_number}")
                    print(f"  Floor: {unit.floor}")
                    print(f"  Type: {unit.unit_type}")
                    print(f"  Price: ${unit.price:,.0f}")
                    print(f"  Status: {unit.status}")
                    if unit.customer:
                        print(f"  Customer: {unit.customer.name}")
                else:
                    print("❌ Unit not found")
                    
            elif choice == "4":
                unit_number = get_input("Enter unit number: ")
                unit = Unit.find_by_unit_number(session, unit_number)
                if not unit:
                    print("❌ Unit not found")
                    continue
                    
                if not unit.is_available:
                    print("❌ Unit is not available")
                    continue
                    
                customer_id = get_input("Enter customer ID: ", int)
                customer = Customer.find_by_id(session, customer_id)
                if not customer:
                    print("❌ Customer not found")
                    continue
                    
                unit.allocate_to_customer(session, customer)
                print(f"✅ Unit {unit.unit_number} allocated to {customer.name}")
                
            elif choice == "5":
                unit_id = get_input("Enter unit ID to delete: ", int)
                unit = Unit.find_by_id(session, unit_id)
                if unit:
                    confirm = get_input(f"Delete unit '{unit.unit_number}'? (y/N): ")
                    if confirm.lower() == 'y':
                        unit.delete(session)
                        print("✅ Unit deleted")
                    else:
                        print("❌ Deletion cancelled")
                else:
                    print("❌ Unit not found")
                    
            elif choice == "6":
                break
            else:
                print("❌ Invalid option")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            session.rollback()
    
    session.close()

def main():
    print("🏢 Initializing Apartment Unit Allocator...")
    init_db()
    
    while True:
        display_menu()
        choice = get_input("Choose an option: ")
        
        if choice == "1":
            handle_customer_management()
        elif choice == "2":
            handle_unit_management()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    main()