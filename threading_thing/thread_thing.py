import threading
import timeit


# Non-threaded function
def calculate_sum(limit):
    result = 0
    for num in range(1, limit + 1):
        result += num
    return result


# Helper function for each thread to calculate the sum
def calculate_chunk(start, end, result_list):
    result = 0
    for num in range(start, end + 1):
        result += num
    result_list.append(result)


# Threading function
def calculate_sum_threading(limit):
    num_threads = 16  # Number of threads to use
    chunk_size = limit // num_threads  # Divide the work into chunks

    # Create a result list to collect the results from each thread
    result_list = []

    # Create and start the threads
    threads = []
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = (i + 1) * chunk_size
        if i == num_threads - 1:  # Handle the last chunk
            end = limit
        t = threading.Thread(target=calculate_chunk, args=(start, end, result_list))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Combine the results from all threads
    result = sum(result_list)
    return result


# Benchmarking using timeit
limit = 10**8  # The limit for the sum

if __name__ == '__main__':
    # Measure the execution time of the non-threaded function
    non_threaded_time = timeit.timeit(lambda: calculate_sum(limit), number=1)

    # Measure the execution time of the threading function
    threading_time = timeit.timeit(lambda: calculate_sum_threading(limit), number=1)

    print("Non-threaded time:", non_threaded_time)
    print("Threading time:", threading_time)