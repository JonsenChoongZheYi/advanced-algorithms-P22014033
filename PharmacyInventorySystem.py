import time

# ENTITY CLASS – Medicine
class Medicine:
    """Represents a pharmacy product."""
    def __init__(self, medID, medName, medType, quantity, price):
        self.id = medID
        self.name = medName
        self.type = medType          # e.g., tablet, syrup, supplement
        self.quantity = quantity
        self.price = price

    def display(self):
        print(f"ID: {self.id:<6} | {self.name:<12} | Type: {self.type:<10} | "
              f"Price: RM{self.price:>8.2f} | Stock: {self.quantity:<6}")


# HASH TABLE with LINEAR PROBING (Open Addressing)
class HashTable:
    def __init__(self, initial_capacity=10):
        self.capacity = initial_capacity
        self.table = [None] * self.capacity   # each slot stores (key, value) or None
        self.size = 0                         # number of stored items
        self.load_factor_threshold = 0.7      # resize when size/capacity > 0.7

# abs() to avoid negative index results
    def hashKey(self, key):
        return abs(hash(key)) % self.capacity

# Double the table size and rehash all existing entries.
    def _resize(self):

        old_table = self.table
        old_capacity = self.capacity
        # Double the capacity
        self.capacity = old_capacity * 2
        self.table = [None] * self.capacity
        self.size = 0   # we will re-insert, so reset size

        # Re-insert every non‑None entry from the old table
        for slot in old_table:
            if slot is not None:
                key, value = slot
                self.insert(key, value)   # insert will update self.size

# insert / update the key-value pair
# if the load factor >= 0.7, resize the table first
    def insert(self, key, value):
        # Check load factor and resize if necessary
        if self.size / self.capacity > self.load_factor_threshold:
            self._resize()

        index = self.hashKey(key)
        start = index

        # Probe linearly until we find an empty slot or the key itself
        while self.table[index] is not None:
            if self.table[index][0] == key:
                # Key exists: update value
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity
            if index == start:
                raise Exception("Hash Table is full (should not happen after resizing)")

        # Insert into empty slot
        self.table[index] = (key, value)
        self.size += 1

    def search(self, key):
        """
        Search for a key and return the associated value.
        Returns None if the key is not found.
        """
        index = self.hashKey(key)
        start = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
            if index == start:
                break
        return None

#delete key-value pair
    """
            Delete a key-value pair.
            Uses the 'rehash following cluster' method to avoid tombstones.
            Returns True if deletion was successful, False otherwise.
            """
    def delete(self, key):
        index = self.hashKey(key)
        start = index

        while self.table[index] is not None:
            if self.table[index][0] == key:
                break
            index = (index + 1) % self.capacity
            if index == start:
                return False   # key not found
        else:
            return False       # reached an empty slot without finding key

        # Remove the element
        self.table[index] = None
        self.size -= 1

        # Rehash all subsequent elements in the cluster
        next_idx = (index + 1) % self.capacity
        while self.table[next_idx] is not None:
            # Save the key and value
            k, v = self.table[next_idx]
            # Remove it temporarily
            self.table[next_idx] = None
            self.size -= 1
            # Re-insert it (this will place it in the correct position,
            # possibly filling the hole we created)
            self.insert(k, v)
            # Move to the next slot
            next_idx = (next_idx + 1) % self.capacity

        return True

# list all the Medicine objects which stored in the table
    def displayMedicines(self):
        result = []
        for slot in self.table:
            if slot is not None:
                result.append(slot[1])   # value is the Medicine object
        return result

    def __len__(self):
        """Return the number of items stored."""
        return self.size



# PHARMACY SYSTEM
class PharmacySystem:
    def __init__(self):
        # Use a larger initial capacity (20) to reduce early collisions
        self.database = HashTable(initial_capacity=10)

    def displayMedicines(self):
        """Display all medicine records."""
        if len(self.database) == 0:
            print("No medicine records in Pharmacy Inventory System.")
            return
        print("\n--- Medicine Records ----")
        print(f"{'ID':<10} | {'Name':<13} | {'Type':<15} | {'Price (RM)':<17} | {'Stock':<6}")
        print("-" * 80)
        for med in self.database.displayMedicines():
            med.display()
        print()

    def searchMedicine(self, medicineID):
        """Search for a medicine by its ID. Returns Medicine object or None."""
        return self.database.search(medicineID)

    def addMedicine(self, medicine):
        """Add a new medicine to the inventory."""
        self.database.insert(medicine.id, medicine)
        print(f"Medicine {medicine.id} is added into Pharmacy Inventory System records.")

    def deleteMedicine(self, medicineID):
        """Delete a medicine by its ID. Returns success/failure."""
        if self.database.delete(medicineID):
            print(f"Medicine {medicineID} is deleted from record.")
        else:
            print(f"Unable to find medicine {medicineID}.")


# COMMAND-LINE MENU
def pharmacyMenu():
    print("\n===== Pharmacy Inventory System =====")
    print("1. Display all medicines")
    print("2. Search medicines by ID")
    print("3. Add medicine records")
    print("4. Delete medicine records")
    print("5. Exit")


# =====================================================================
# PERFORMANCE COMPARISON (Hash Table vs. Array)
# =====================================================================
def performanceComparison():
    """
    Compares the average search time of the hash table (linear probing)
    against a linear search in a one-dimensional array.
    It measures search times for both existing and non-existing keys separately.
    """
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON: Hash Table (linear probing) vs. Array (linear search)")
    print("=" * 70)

    # ---------- Prepare the same data set ----------
    num_items = 1000   # use a larger set to magnify the difference
    medicines = []
    for i in range(1, num_items + 1):
        medicines.append(Medicine(i, f"Medicine_{i}", "tablet", 100, 10.0))

    # Insert into Hash Table (with a sufficiently large capacity)
    ht = HashTable(initial_capacity=num_items * 2)   # avoid resizing during insert
    for med in medicines:
        ht.insert(med.id, med)

    # Insert into Array (list)
    array = medicines[:]   # copy

    # Choose search keys: 100 existing and 100 non-existing
    existing_keys = list(range(1, 101))
    non_existing_keys = list(range(num_items + 1, num_items + 101))
    all_keys = existing_keys + non_existing_keys

    repetitions = 1000   # repeat the whole set of searches to get measurable times

    # ---------- Helper for array linear search ----------
    def array_search(arr, key):
        for med in arr:
            if med.id == key:
                return med
        return None

    # ---------- Measure Hash Table search ----------
    start_ht = time.perf_counter()
    for _ in range(repetitions):
        for key in all_keys:
            _ = ht.search(key)
    end_ht = time.perf_counter()
    ht_total_time = (end_ht - start_ht) * 1000   # in ms

    # ---------- Measure Array search ----------
    start_arr = time.perf_counter()
    for _ in range(repetitions):
        for key in all_keys:
            _ = array_search(array, key)
    end_arr = time.perf_counter()
    arr_total_time = (end_arr - start_arr) * 1000

    # ---------- Detailed breakdown: existing vs non-existing ----------
    # We need separate measurements for existing and non-existing.
    # Run again for hash table existing keys only
    start_ht_existing = time.perf_counter()
    for _ in range(repetitions):
        for key in existing_keys:
            _ = ht.search(key)
    end_ht_existing = time.perf_counter()
    ht_existing_time = (end_ht_existing - start_ht_existing) * 1000

    # Non-existing keys for hash table
    start_ht_non = time.perf_counter()
    for _ in range(repetitions):
        for key in non_existing_keys:
            _ = ht.search(key)
    end_ht_non = time.perf_counter()
    ht_non_time = (end_ht_non - start_ht_non) * 1000

    # Array existing
    start_arr_existing = time.perf_counter()
    for _ in range(repetitions):
        for key in existing_keys:
            _ = array_search(array, key)
    end_arr_existing = time.perf_counter()
    arr_existing_time = (end_arr_existing - start_arr_existing) * 1000

    # Array non-existing
    start_arr_non = time.perf_counter()
    for _ in range(repetitions):
        for key in non_existing_keys:
            _ = array_search(array, key)
    end_arr_non = time.perf_counter()
    arr_non_time = (end_arr_non - start_arr_non) * 1000

    # ---------- Print results ----------
    total_searches = repetitions * len(all_keys)
    print(f"\nTotal searches performed: {total_searches:,} "
          f"({repetitions} repetitions × {len(all_keys)} keys)")
    print(f"Data size: {num_items} records\n")

    print("--- Overall times ---")
    print(f"Hash Table (linear probing) total time: {ht_total_time:.2f} ms")
    print(f"Array (linear search)           total time: {arr_total_time:.2f} ms")
    print(f"▶ Hash Table is {arr_total_time / ht_total_time:.2f} times faster than Array.\n")

    print("--- Breakdown: Existing Keys ---")
    print(f"Hash Table existing search time: {ht_existing_time:.2f} ms")
    print(f"Array existing search time:      {arr_existing_time:.2f} ms")
    print(f"Hash Table is {arr_existing_time / ht_existing_time:.2f}× faster for existing keys.")

    print("\n--- Breakdown: Non-Existing Keys ---")
    print(f"Hash Table non-existing search time: {ht_non_time:.2f} ms")
    print(f"Array non-existing search time:      {arr_non_time:.2f} ms")
    print(f"Hash Table is {arr_non_time / ht_non_time:.2f}× faster for non-existing keys.")

    print("\nExplanation:")
    print("- Hash Table: average search is O(1) because the key is hashed and only a few probes are needed.")
    print("- Array: linear search is O(n) because it must scan from the start until the key is found or the end is reached.")
    print("- For non-existing keys, the array must scan all elements, while the hash table stops at the first empty slot.")
    print("- The performance gap grows as the data size increases.")



# MAIN PROGRAM
def main():
    system = PharmacySystem()

    # Insert some predefined sample records
    sample_meds = [
        Medicine(101, "Panadol", "tablet", 100, 10.00),
        Medicine(102, "Cough Syrup", "syrup", 80, 15.50),
        Medicine(103, "Vitamin C", "supplement", 200, 8.75),
    ]
    for med in sample_meds:
        system.addMedicine(med)

    print("Welcome to Pharmacy Inventory System\n")

    while True:
        pharmacyMenu()
        try:
            choice = int(input("Enter choice: "))
            if choice == 1:
                system.displayMedicines()
            elif choice == 2:
                searchID = int(input("Enter medicine ID to search: "))
                med = system.searchMedicine(searchID)
                if med:
                    med.display()
                else:
                    print("Medicine not found.")
            elif choice == 3:
                print("\nPlease insert the medicine information below:")
                medID = int(input("Medicine ID: "))
                medName = input("Name: ")
                medType = input("Type (tablet, syrup, supplement): ")
                try:
                    quantity = int(input("Quantity: "))
                    if quantity <= 0:
                        raise ValueError("Quantity must be a positive integer.")
                except ValueError as e:
                    print(f"Error: {e}")
                    continue  # go back to menu without adding
                try:
                    price = float(input("Price: "))
                    if price <= 0:
                        raise ValueError("Price must be a positive number.")
                except ValueError as e:
                    print(f"Error: {e}")
                    continue

                new_med = Medicine(medID, medName, medType, quantity, price)
                system.addMedicine(new_med)
            elif choice == 4:
                deleteID = int(input("Enter medicine ID to delete: "))
                system.deleteMedicine(deleteID)   # note: renamed method
            elif choice == 5:
                print("Exiting System. Thank you for using!")
                break
            else:
                print("Invalid input. Please enter 1-5.\n")
        except ValueError:
            print("Error: Invalid input. Please enter numbers only.\n")
        except Exception as e:
            print(f"Unexpected error: {e}\n")

    # After the user exits, run the performance comparison
    performanceComparison()


if __name__ == "__main__":
    main()