import time
import random
import threading

from detailed_profiler import Profiler

# The @Profiler decorator is used to profile the 'main_function'
# It enables inline profiling and memory profiling by default
# The profiling results will be saved to "profile_stats.json"
@Profiler(output_file="profile_stats.json")
def main_function():

    # Perform some CPU-intensive operations
    for _ in range(100000):
        _ = sum(range(1000))

    # Call nested functions
    nested_function_1()
    nested_function_2()

    # Perform memory allocations
    memory_intensive_function()

    # Simulate some delay
    time.sleep(1)

def nested_function_1():

    # Perform some CPU-intensive operations
    for _ in range(50000):
        _ = sum(range(500))

    # Simulate some delay
    time.sleep(0.5)

def nested_function_2():

    # Perform some CPU-intensive operations
    for _ in range(30000):
        _ = sum(range(300))

    # Simulate some delay
    time.sleep(0.3)

def memory_intensive_function():

    # Allocate a large list
    large_list = [random.random() for _ in range(1000000)]

    # Perform some operations on the list
    _ = sum(large_list)
    _ = min(large_list)
    _ = max(large_list)

def worker_function():

    # Perform some CPU-intensive operations
    for _ in range(80000):
        _ = sum(range(800))

    # Simulate some delay
    time.sleep(0.8)

if __name__ == "__main__":
    # Create multiple threads to simulate concurrent execution
    threads = []
    for _ in range(3):
        thread = threading.Thread(target=worker_function)
        threads.append(thread)
        thread.start()

    main_function()

    for thread in threads:
        thread.join()