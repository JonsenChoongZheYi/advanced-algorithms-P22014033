import time
import random
from datetime import datetime, timedelta

# Entity Class: Transaction
class Transaction:
    def __init__(self, trans_id, customer, product, amount, date):
        self.transactionID = trans_id
        self.customerName = customer
        self.productName = product
        self.amount = amount
        self.transactionDate = date

    def __str__(self):
        return (f"{self.transactionID:<6} | {self.customerName:<12} | {self.productName:<12} | "
                f"RM{self.amount:>8.2f} | {self.transactionDate}")

    # For sorting by different attributes, we define a key function
    def get_id(self):
        return self.transactionID

    def get_amount(self):
        return self.amount

    def get_date(self):
        return self.transactionDate


# Merge Sort (Divide and Conquer)
merge_sort_recursion_count = 0   # global counter

def merge_sort(arr, key_func, left, right):
    """
    Sorts arr[left:right] using Merge Sort.
    Divide: split array into two halves.
    Conquer: recursively sort each half.
    Combine: merge the two sorted halves.
    """
    global merge_sort_recursion_count
    merge_sort_recursion_count += 1   # count each recursive call

    if left < right:
        mid = (left + right) // 2

        # Divide
        merge_sort(arr, key_func, left, mid)
        merge_sort(arr, key_func, mid + 1, right)

        # Combine (merge)
        merge(arr, key_func, left, mid, right)

#Conquer & Combine: merge two sorted subarrays arr[left:mid] and arr[mid+1:right]
def merge(arr, key_func, left, mid, right):
    # Create temporary arrays
    left_part = arr[left:mid+1]
    right_part = arr[mid+1:right+1]

    i = j = 0
    k = left

    # Merge while both parts have elements
    while i < len(left_part) and j < len(right_part):
        if key_func(left_part[i]) <= key_func(right_part[j]):
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    # Copy remaining elements from left_part (if any)
    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    # Copy remaining elements from right_part (if any)
    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1

# Wrapper to simplify call
def sort_transactions(transactions, key_func=lambda t: t.transactionID):
    global merge_sort_recursion_count
    merge_sort_recursion_count = 0   # reset counter
    start_time = time.perf_counter()
    merge_sort(transactions, key_func, 0, len(transactions) - 1)
    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000   # ms
    return elapsed, merge_sort_recursion_count

# Binary Search (Divide and Conquer)
# Sorted array by transactionID
# Divide: the compare target wu=ith middle element
# Conquer: recurse on left or right half.
def binary_search(arr, target_id, left, right):
    if left > right:
        return -1   # not found

    mid = (left + right) // 2
    if arr[mid].transactionID == target_id:
        return mid
    elif target_id < arr[mid].transactionID:
        return binary_search(arr, target_id, left, mid - 1)
    else:
        return binary_search(arr, target_id, mid + 1, right)

def binary_search_wrapper(transactions, target_id):
    start_time = time.perf_counter()
    index = binary_search(transactions, target_id, 0, len(transactions) - 1)
    end_time = time.perf_counter()
    elapsed = (end_time - start_time) * 1000   # ms
    return index, elapsed

# Linear Search
def linear_search(transactions, target_id):
    start_time = time.perf_counter()
    for i, t in enumerate(transactions):
        if t.transactionID == target_id:
            end_time = time.perf_counter()
            return i, (end_time - start_time) * 1000
    end_time = time.perf_counter()
    return -1, (end_time - start_time) * 1000

# Sample Dataset
def generate_transactions(n):
    """
    Generate n random transactions with unsorted IDs.
    """
    customers = ["Amaris", "Abel", "Lucas", "Blakely", "Sincere", "Aurora", "Duncan", "Frankie", "Joelle", "Mekhi",
                 "Erin", "Rebert", "Boone", "Rohan", "Cleo"]
    products = ["Pants", "Phone", "Tablet", "Powerbank", "Fan", "Pipe", "Shoes", "Handbag", "Clock", "Bed"]
    transactions = []
    # Create a set of unique IDs (random)
    ids = random.sample(range(1000, 9999), n)   # random unique IDs
    for i in range(n):
        cid = ids[i]
        customer = random.choice(customers)
        product = random.choice(products)
        amount = round(random.uniform(10.0, 999.99), 2)
        # random date in last 30 days
        date = datetime.now() - timedelta(days=random.randint(0, 30))
        date_str = date.strftime("%Y-%m-%d")
        transactions.append(Transaction(cid, customer, product, amount, date_str))
    return transactions

# Menu System
def display_transactions(transactions, title="Transactions"):
    print(f"\n--- {title} ---")
    if not transactions:
        print("No transactions.")
        return
    # Print header
    print(f"{'ID':<6} | {'Customer':<12} | {'Product':<12} | {'Amount':<10} | {'Date':<10}")
    print("-" * 62)  # optional separator
    # Print each transaction
    for t in transactions:
        print(t)
    print(f"Total: {len(transactions)} records")

def main():
    # Generate initial dataset of 15 transactions (unsorted by ID)
    print("Generating 15 random transactions...")
    transactions = generate_transactions(15)
    print("Initial unsorted list:")
    display_transactions(transactions, "Unsorted Initial Dataset")

    # Store sorted state for later (to avoid re‑sorting)
    sorted_by_id = transactions[:]   # we'll sort this copy
    is_sorted = False

    # Counters for recursion calls (for optional display)
    recursive_call_count = 0

    while True:
        print("\n" + "="*60)
        print("     DIVIDE & CONQUER - TRANSACTION MANAGER")
        print("="*60)
        print("1. Display all transactions (current order)")
        print("2. Sort transactions by ID using Merge Sort (D&C)")
        print("3. Search transaction by ID using Binary Search (D&C)")
        print("4. Search transaction by ID using Linear Search (comparison)")
        print("5. Insert new transaction dynamically")
        print("6. Sort by amount")
        print("7. Sort by date")
        print("8. Show time complexity table")
        print("9. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            display_transactions(transactions, "Current Transactions")

        elif choice == '2':
            # Sort by transactionID
            print("\n--- Sorting by Transaction ID using Merge Sort ---")
            print("Before sorting:")
            print(f"{'ID':<6} | {'Customer':<12} | {'Product':<12} | {'Amount':<10} | {'Date':<10}")
            for t in transactions[:15]:
                print(t)
            elapsed, count = sort_transactions(transactions, key_func=lambda t: t.transactionID)
            is_sorted = True
            print(f"\nAfter sorting:")
            print(f"{'ID':<6} | {'Customer':<12} | {'Product':<12} | {'Amount':<10} | {'Date':<10}")
            for t in transactions[:15]:
                print(t)
            print(f"Merge Sort completed in {elapsed:.4f} ms")
            print(f"Number of recursive calls: {count}")
            recursive_call_count = count

        elif choice == '3':
            if not is_sorted:
                print("Warning: Transactions are not sorted by ID. Sorting now...")
                sort_transactions(transactions, key_func=lambda t: t.transactionID)
                is_sorted = True
            try:
                target = int(input("Enter transaction ID to search: "))
                idx, elapsed = binary_search_wrapper(transactions, target)
                if idx != -1:
                    print(f"Found at index {idx}:")
                    print(transactions[idx])
                else:
                    print(f"Transaction ID {target} not found.")
                print(f"Binary Search completed in {elapsed:.4f} ms")
            except ValueError:
                print("Invalid ID. Please enter an integer.")

        elif choice == '4':
            # Linear search (works on unsorted or sorted)
            try:
                target = int(input("Enter transaction ID to search: "))
                idx, elapsed = linear_search(transactions, target)
                if idx != -1:
                    print(f"Found at index {idx}:")
                    print(transactions[idx])
                else:
                    print(f"Transaction ID {target} not found.")
                print(f"Linear Search completed in {elapsed:.4f} ms")
            except ValueError:
                print("Invalid ID.")

        elif choice == '5':
            # Insert dynamic transaction
            print("\n--- Insert New Transaction ---")
            try:
                # Generate a random new ID not present
                existing_ids = {t.transactionID for t in transactions}
                new_id = random.randint(1000, 9999)
                while new_id in existing_ids:
                    new_id = random.randint(1000, 9999)
                customer = input("Customer name: ")
                product = input("Product name: ")
                try:
                    amount= float(input("Amount: "))
                    if amount <= 0:
                        raise ValueError("Amount must be a positive integer.")
                except ValueError as e:
                    print(f"Error: {e}")
                    continue  # go back to menu without adding
                date_str = input("Date (YYYY-MM-DD): ")
                # Validate date format
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    print("Invalid date format. Using today's date.")
                    date_str = datetime.now().strftime("%Y-%m-%d")
                new_trans = Transaction(new_id, customer, product, amount, date_str)
                transactions.append(new_trans)
                print(f"Transaction {new_id} inserted.")
                is_sorted = False   # because we added at end, list unsorted again
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '6':
            # Sort by amount
            print("\n--- Sorting by Amount using Merge Sort ---")
            elapsed, count = sort_transactions(transactions, key_func=lambda t: t.amount)
            print("Sorted by amount:")
            print(f"{'ID':<6} | {'Customer':<12} | {'Product':<12} | {'Amount':<10} | {'Date':<10}")
            for t in transactions[:15]:
                print(t)
            print(f"Sort by amount completed in {elapsed:.4f} ms")
            print(f"Number of recursive calls: {count}")

        elif choice == '7':
            # Sort by date (optional)
            print("\n--- Sorting by Date using Merge Sort ---")
            elapsed, count = sort_transactions(transactions, key_func=lambda t: t.transactionDate)
            print("Sorted by date:")
            print(f"{'ID':<6} | {'Customer':<12} | {'Product':<12} | {'Amount':<10} | {'Date':<10}")
            for t in transactions[:15]:
                print(t)
            print(f"Sort by date completed in {elapsed:.4f} ms")
            print(f"Number of recursive calls: {count}")

        elif choice == '8':
            # Time complexity analysis table (optional)
            print("\n" + "="*60)
            print("        TIME COMPLEXITY ANALYSIS")
            print("="*60)
            print("Algorithm          | Time Complexity (Big-O) | Measured (ms for current dataset)")
            print("--------------------|-------------------------|----------------------------------")
            temp = transactions[:]
            # Measure Merge Sort on copy
            start = time.perf_counter()
            sort_transactions(temp, key_func=lambda t: t.transactionID)
            sort_time = (time.perf_counter() - start) * 1000

            # Measure Binary Search (use first ID in sorted list)
            if temp:
                target_id = temp[0].transactionID
                _, bin_time = binary_search_wrapper(temp, target_id)
                # Measure Linear Search on the same target
                _, lin_time = linear_search(temp, target_id)
            else:
                bin_time = 0
                lin_time = 0

            print(f"Merge Sort           | O(n log n)             | {sort_time:.4f} ms")
            print(f"Binary Search        | O(log n)               | {bin_time:.4f} ms")
            print(f"Linear Search        | O(n)                   | {lin_time:.4f} ms")

        elif choice == '9':
            print("Exiting Transaction System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()