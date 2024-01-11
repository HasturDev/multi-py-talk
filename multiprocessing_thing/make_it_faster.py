import multiprocessing
import timeit


# Non-threaded function
def calculate_sum(limit):
    result = 0
    for num in range(1, limit + 1):
        result += num
    return result


# Helper function for each process to calculate the sum
def calculate_chunk(start, end, result_queue):
    result = 0
    for num in range(start, end + 1):
        result += num
    result_queue.put(result)


# Multiprocessing function
def calculate_sum_multiprocessing(limit):
    num_processes = 16  # Number of processes to use
    chunk_size = limit // num_processes  # Divide the work into chunks

    # Create a result queue to collect the results from each process
    result_queue = multiprocessing.Queue()

    # Create and start the processes
    processes = []
    for i in range(num_processes):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        if i == num_processes - 1:  # Handle the last chunk
            end = limit
        p = multiprocessing.Process(target=calculate_chunk, args=(start, end, result_queue))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

    # Collect the results from the result queue
    results = []
    while not result_queue.empty():
        result = result_queue.get()
        results.append(result)

    # Combine the results from all processes
    result = sum(results)
    return result


# Benchmarking using timeit
limit_binary = bin(10**8)  # The limit for the sum in binary

if __name__ == '__main__':
    # Measure the execution time of the non-threaded function
    non_threaded_time = timeit.timeit(lambda: calculate_sum(int(limit_binary, 2)), number=1)

    # Measure the execution time of the multiprocessing function
    multiprocessing_time = timeit.timeit(lambda: calculate_sum_multiprocessing(int(limit_binary, 2)), number=1)

    print("Non-threaded time:", non_threaded_time)
    print("Multiprocessing time:", multiprocessing_time)