import sys
import time
import threading
import traceback
import json
import linecache
import os
import psutil
from collections import defaultdict
from functools import wraps

class Profiler:
    def __init__(self, inline_profiling=True, memory_profiling=True, output_file="profile_stats.json"):
        self.inline_profiling = inline_profiling
        self.memory_profiling = memory_profiling
        self.output_file = output_file
        self.function_stats = defaultdict(lambda: {"time": 0, "calls": 0, "lines": defaultdict(lambda: {"time": 0, "calls": 0, "code": ""})})
        self.memory_stats = defaultdict(lambda: {"memory_usage": 0})
        self.cpu_stats = defaultdict(lambda: {"time": 0})
        self.thread_stats = defaultdict(lambda: {"time": 0, "calls": 0})
        self.process_stats = defaultdict(lambda: {"time": 0, "calls": 0})

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.start()
            result = func(*args, **kwargs)
            self.stop()
            self.save_stats()
            return result
        return wrapper

    def start(self):
        sys.settrace(self.trace_calls)
        threading.settrace(self.trace_calls)

    def stop(self):
        sys.settrace(None)
        threading.settrace(None)

    def trace_calls(self, frame, event, arg):
        if event == "call":
            code = frame.f_code
            function_name = code.co_name
            thread_id = threading.get_ident()
            process_id = threading.current_thread().ident

            self.function_stats[function_name]["calls"] += 1
            self.thread_stats[thread_id]["calls"] += 1
            self.process_stats[process_id]["calls"] += 1

            frame.f_locals["_start_time"] = time.time()

        elif event == "return":
            code = frame.f_code
            function_name = code.co_name
            thread_id = threading.get_ident()
            process_id = threading.current_thread().ident

            start_time = frame.f_locals.get("_start_time", None)
            if start_time is not None:
                duration = time.time() - start_time
                self.function_stats[function_name]["time"] += duration
                self.thread_stats[thread_id]["time"] += duration
                self.process_stats[process_id]["time"] += duration

        elif event == "line" and self.inline_profiling:
            code = frame.f_code
            function_name = code.co_name
            line_number = frame.f_lineno
            filename = code.co_filename

            self.function_stats[function_name]["lines"][line_number]["calls"] += 1
            self.function_stats[function_name]["lines"][line_number]["code"] = linecache.getline(filename, line_number).strip()

            start_time = frame.f_locals.get("_line_start_time", None)
            if start_time is not None:
                duration = time.time() - start_time
                self.function_stats[function_name]["lines"][line_number]["time"] += duration

            frame.f_locals["_line_start_time"] = time.time()

        if self.memory_profiling:
            if event == "return":
                code = frame.f_code
                function_name = code.co_name
                process = psutil.Process(os.getpid())
                memory_info = process.memory_info()
                self.memory_stats[function_name]["memory_usage"] = memory_info.rss

        return self.trace_calls

    def save_stats(self):
        stats = {
            "function_stats": self.function_stats,
            "memory_stats": self.memory_stats,
            "cpu_stats": self.cpu_stats,
            "thread_stats": self.thread_stats,
            "process_stats": self.process_stats
        }

        with open(self.output_file, "w") as f:
            json.dump(stats, f, indent=4)