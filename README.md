# Python Profiler

This is a custom Python profiler that provides detailed information about the performance and resource usage of your code. It supports function-level profiling, line-level profiling, memory profiling, CPU usage profiling, and thread/process profiling.

## Features

- **Function-level profiling**: Measures the execution time and number of calls for each function.
- **Line-level profiling**: Provides the execution time, number of calls, and the actual line of code for each line within a function.
- **Memory profiling**: Measures the memory consumption of each function.
- **CPU usage profiling**: Measures the CPU time consumed by each function.
- **Thread and process profiling**: Provides execution time and number of calls for each thread and process.

## Usage

To use the profiler, follow these steps:

1. Import the `Profiler` class from the `profiler` module.
2. Create an instance of the `Profiler` class, optionally specifying the desired profiling options.
3. Apply the `@Profiler()` decorator to the function you want to profile.
4. Run your code as usual.
5. The profiling results will be saved to a JSON file specified by the `output_file` parameter (default: `output.json`).

Example:
```python
from profiler import Profiler

@Profiler(output_file="profile_results.json")
def my_function():
    # Your code here
    pass

my_function()
```

## Interpreting the Output

The profiler generates an output file in JSON format that contains detailed information about the profiled code. Here's how to interpret the different sections of the output file:

### Function Stats

The `function_stats` section provides statistics for each profiled function. It includes the following information:

- `time`: The total execution time of the function in seconds.
- `calls`: The number of times the function was called.
- `lines`: A nested object that contains line-level profiling information for the function.

Each line number is represented as a key, and its corresponding value is an object containing:
- `time`: The total execution time spent on that line in seconds.
- `calls`: The number of times that line was executed.
- `code`: The actual line of code.

Example:
```json
{
  "main_function": {
    "time": 4.858382940292358,
    "calls": 1,
    "lines": {
      "14": {
        "time": 1.7699341773986816,
        "calls": 100001,
        "code": "for _ in range(100000):"
      },
      "15": {
        "time": 0.11131095886230469,
        "calls": 100000,
        "code": "_ = sum(range(1000))"
      }
    }
  }
}
```

### Memory Stats

The `memory_stats` section provides information about the memory consumption of each profiled function. It includes the following information:

- `memory_usage`: The memory consumption of the process at the end of the function execution, measured in bytes.

Example:
```json
{
  "memory_stats": {
    "main_function": {
      "memory_usage": 25853952
    },
    "memory_intensive_function": {
      "memory_usage": 64274432
    }
  }
}
```

### CPU Stats

The `cpu_stats` section provides information about CPU usage for each profiled function. It includes the following information:

- `time`: The total CPU time consumed by the function in seconds.

Example:
```json
{
  "cpu_stats": {}
}
```

### Thread Stats

The `thread_stats` section provides information about the execution time and number of calls for each thread. It includes the following information:

- `time`: The total execution time of the thread in seconds.
- `calls`: The total number of function calls made by the thread.

Example:
```json
{
  "thread_stats": {
    "8273370624": {
      "time": 7.638259649276733,
      "calls": 7
    }
  }
}
```

### Process Stats

The `process_stats` section provides information about the execution time and number of calls for each process. It includes the following information:

- `time`: The total execution time of the process in seconds.
- `calls`: The total number of function calls made by the process.

Example:
```json
{
  "process_stats": {
    "8273370624": {
      "time": 7.638259649276733,
      "calls": 7
    }
  }
}
```

By analyzing the information provided in the output file, you can gain insights into the performance and resource usage of your code. You can identify which functions are taking the most time, which lines of code are being executed frequently, and how much memory is being consumed by each function.

Use this information to optimize your code, identify bottlenecks, and make informed decisions about performance improvements.

## Requirements

- Python 3.x
- `psutil` module (for memory profiling)

Install the required dependencies using:
```bash
pip install psutil
```