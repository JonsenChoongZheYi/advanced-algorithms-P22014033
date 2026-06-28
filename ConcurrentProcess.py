import threading
import time

# ---------- Factorial function (iterative) ----------
def factorial(n):
    """Return n! (iterative, O(n) time)."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# ---------- Thread worker ----------
def thread_work(n, results, index):
    """Compute factorial(n) and store in results[index]."""
    results[index] = factorial(n)

# ---------- Multithreaded run for one round ----------
# run factorial computation on numbers using separate threads
def run_multithreaded(numbers):
    results = [0] * len(numbers)
    threads = []

    # Record start time before starting any thread
    start = time.perf_counter_ns()

    # Create and start threads
    # loop through the list with an index tracker
    for i, n in enumerate(numbers):
        t = threading.Thread(target=thread_work, args=(n, results, i))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end = time.perf_counter_ns()
    elapsed = end - start
    return elapsed, results

# ---------- Sequential run for one round ----------
# run factorial computation sequentially
def run_sequential(numbers):
    start = time.perf_counter_ns()
    for n in numbers:
        _ = factorial(n)
    end = time.perf_counter_ns()
    return end - start

# ---------- Main execution ----------
def main():
    numbers = [50, 100, 200]
    rounds = 10

    print("=" * 70)
    print("MULTITHREADED FACTORIAL COMPUTATION (3 threads)")
    print("=" * 70)
    multithreaded_times = []
    for r in range(1, rounds + 1):
        elapsed, _ = run_multithreaded(numbers)
        multithreaded_times.append(elapsed)
        print(f"Round {r:2d}: {elapsed:>12,} ns")

    avg_mt = sum(multithreaded_times) / rounds
    print(f"\nAverage time (multithreaded): {avg_mt:>12,.2f} ns\n")

    print("=" * 70)
    print("SEQUENTIAL FACTORIAL COMPUTATION")
    print("=" * 70)
    sequential_times = []
    for r in range(1, rounds + 1):
        elapsed = run_sequential(numbers)
        sequential_times.append(elapsed)
        print(f"Round {r:2d}: {elapsed:>12,} ns")

    avg_seq = sum(sequential_times) / rounds
    print(f"\nAverage time (sequential): {avg_seq:>12,.2f} ns\n")

    # Compare
    print("=" * 70)
    print("COMPARISON")
    print("=" * 70)
    print(f"Multithreaded average : {avg_mt:>12,.2f} ns")
    print(f"Sequential average    : {avg_seq:>12,.2f} ns")
    print(f"Difference (MT - Seq): {avg_mt - avg_seq:>12,.2f} ns")
    if avg_mt > avg_seq:
        print("Multithreading is slower due to thread overhead (GIL).")
    else:
        print("Multithreading is slightly faster (possible due to scheduling quirks).")
    print("In CPython, CPU‑bound threading does not give parallel speed‑up; "
          "the GIL serialises execution. The overhead makes it slightly slower.")

if __name__ == "__main__":
    main()