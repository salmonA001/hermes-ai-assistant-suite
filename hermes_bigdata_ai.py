#!/usr/bin/env python3
"""
Hermes BigData AI - Advanced AI Assistant for Large File and Big Data Processing
Specialized in handling large files, data streaming, map-reduce patterns, and efficient data processing
"""

import os
import sys
import json
import csv
import math
import random
import datetime
import time
import hashlib
from typing import Dict, List, Any, Optional, Tuple, Generator, Iterator
from collections import defaultdict, Counter
import heapq

# ==================== CONFIGURATION ====================

CONFIG = {
    "name": "Hermes BigData AI",
    "version": "2.0.0",
    "creator": "Nous Research (Hermes Framework)",
    "max_history": 50,
    "chunk_size": 10000,  # Process 10K lines at a time for large files
    "sample_size": 1000,  # Sample size for quick analysis
    "temp_dir": "./temp_bigdata",
}

# ==================== MAIN BIG DATA AI CLASS ====================

class HermesBigDataAI:
    """Advanced AI Assistant specialized in big data and large file processing"""
    
    def __init__(self):
        self.name = CONFIG["name"]
        self.version = CONFIG["version"]
        self.creator = CONFIG["creator"]
        self.conversation_history = []
        self.user_name = None
        self.session_start = datetime.datetime.now()
        self.knowledge_base = self._load_knowledge_base()
        self.processed_files = {}  # Cache for file metadata
        
        # Create temp directory if it doesn't exist
        os.makedirs(CONFIG["temp_dir"], exist_ok=True)
        
        # Response templates
        self.greetings = [
            f"Hello! I'm {self.name} v{self.version}, your big data processing specialist. How can I help you with large files and data analysis today?",
            f"Hi there! Ready to tackle large datasets, perform efficient data processing, or just chat about big data concepts. What's on your mind?",
            f"Greetings! I specialize in handling large files, implementing map-reduce patterns, and optimizing data workflows.",
            f"Hey! I'm {self.name}. I can process massive files efficiently, implement streaming algorithms, and help with big data challenges."
        ]
        
        self.farewells = [
            "Goodbye! Thanks for letting me help with your big data challenges. Have a great day!",
            "See you later! Remember I'm here whenever you need assistance with large datasets.",
            "Farewell! Thanks for the conversation. Come back anytime for more big data insights!",
            "Bye for now! I'll be here when you need me for data processing tasks."
        ]
        
        self.jokes = [
            "Why don't scientists trust atoms anymore? Because they make up everything!",
            "I told my computer I needed a break, and it said 'No problem - I'll go to sleep mode'.",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "Why did the database administrator break up with the SQL query? It had too many joins!",
            "How many data scientists does it take to change a light bulb? One, but they'll spend 80% of the time cleaning the data first!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why was the math book sad? Because it had too many problems.",
            "I would tell you a UDP joke, but you might not get it.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem."
        ]
        
        self.quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Data is the new oil. - Clive Humby",
            "Without big data analytics, companies are blind and deaf, wandering out onto the web like deer on a freeway. - Geoffrey Moore",
            "The goal is to turn data into information, and information into insight. - Carly Fiorina",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "In the middle of difficulty lies opportunity. - Albert Einstein",
            "Whether you think you can or you think you can't, you're right. - Henry Ford",
            "The journey of a thousand miles begins with one step. - Lao Tzu",
            "Believe you can and you're halfway there. - Theodore Roosevelt"
        ]
    
    def _load_knowledge_base(self) -> Dict[str, str]:
        """Load the AI's knowledge base focused on big data and data processing"""
        return {
            # Big Data & Data Processing
            "big_data": "Big data refers to extremely large datasets that may be analyzed computationally to reveal patterns, trends, and associations, especially relating to human behavior and interactions.",
            "data_mining": "Data mining is the process of discovering patterns in large data sets involving methods at the intersection of machine learning, statistics, and database systems.",
            "etl": "ETL (Extract, Transform, Load) is a process in database usage and especially in data warehousing that involves extracting data from outside sources, transforming it to fit operational needs, and loading it into the end target.",
            "map_reduce": "MapReduce is a programming model and an associated implementation for processing and generating large data sets with a parallel, distributed algorithm on a cluster.",
            "stream_processing": "Stream processing is a programming paradigm that allows software applications to process a continuous flow of data and detect conditions, usually within a small time period after the receipt of the data.",
            "data_warehouse": "A data warehouse is a system used for reporting and data analysis, and is considered a core component of business intelligence.",
            "data_lake": "A data lake is a system or repository of data stored in its natural/raw format, usually object blobs or files.",
            "nosql": "NoSQL databases provide a mechanism for storage and retrieval of data that is modeled in means other than the tabular relations used in relational databases.",
            "data_pipeline": "A data pipeline is a set of actions that read data from one or more sources, transform it, and write it to a destination.",
            "data_cleaning": "Data cleaning is the process of detecting and correcting (or removing) corrupt or inaccurate records from a record set, table, or database.",
            
            # File Handling & Performance
            "file_i_o": "File I/O (Input/Output) refers to the operations of reading from and writing to files. Efficient file I/O is crucial for processing large files.",
            "buffering": "Buffering is a technique where data is temporarily stored in a buffer (a region of memory) while it is being moved from one place to another, to compensate for differences in speed between devices.",
            "memory_mapping": "Memory-mapped file is a segment of virtual memory that has been assigned a direct byte-for-byte correlation with some portion of a file or file-like resource.",
            "chunking": "Chunking is the process of breaking down large amounts of data into smaller chunks for easier processing, especially when dealing with files that don't fit in memory.",
            "streaming": "Streaming data processing involves processing data continuously as it arrives, rather than in batches, enabling real-time analytics.",
            "compression": "Data compression is the process of encoding information using fewer bits than the original representation, reducing storage size and transmission time.",
            "indexing": "Indexing is a data structure technique to improve the speed of data retrieval operations on a database table at the cost of additional writes and storage space.",
            "partitioning": "Data partitioning is the process of splitting a large database or dataset into smaller, more manageable parts called partitions.",
            
            # Algorithms & Techniques
            "algorithm": "An algorithm is a finite sequence of well-defined instructions, typically to solve a class of problems or to perform a computation.",
            "sorting": "Sorting algorithms arrange elements of a list in a certain order. The most frequently used orders are numerical order and lexicographical order.",
            "searching": "Search algorithms are designed to retrieve an element stored in any data structure where it is stored.",
            "hashing": "Hashing is the process of converting a given key into another value. A hash function is used to generate the new value according to a mathematical algorithm.",
            "caching": "Caching is the process of storing copies of files in a cache, or temporary storage location, so that they can be accessed more quickly.",
            "load_balancing": "Load balancing is the process of distributing a set of tasks over a set of resources, with the aim of making their overall processing more efficient.",
            "parallel_processing": "Parallel processing is the ability to perform multiple operations or tasks simultaneously. The term is used in the context of a single machine with multiple processors.",
            "distributed_computing": "Distributed computing is a field of computer science that studies distributed systems. A distributed system consists of multiple autonomous computers that communicate through a computer network.",
            
            # Specific Formats
            "csv": "CSV (Comma-Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database. Files in the CSV format can be imported to and exported from programs that store data in tables.",
            "json": "JSON (JavaScript Object Notation) is a lightweight data-interchange format that is easy for humans to read and write and easy for machines to parse and generate.",
            "xml": "XML (Extensible Markup Language) is a markup language that defines a set of rules for encoding documents in a format that is both human-readable and machine-readable.",
            "parquet": "Apache Parquet is a columnar storage file format available to any project in the Apache Hadoop ecosystem, based on the columnar storage format of Google's Dremel paper.",
            "avro": "Apache Avro is a row-oriented remote procedure call and data serialization framework developed within Apache's Hadoop project.",
            "orc": "ORC (Optimized Row Columnar) file format provides a highly efficient way to store Hive data. It was designed to overcome limitations of the other Hive file formats.",
            
            # Statistics & Analysis
            "statistics": "Statistics is the discipline that concerns the collection, organization, analysis, interpretation, and presentation of data.",
            "descriptive_statistics": "Descriptive statistics is the discipline of quantitatively describing the main features of a collection of information, or the quantitative description of data itself.",
            "inferential_statistics": "Inferential statistics uses a random sample of data taken from a population to describe and make inferences about the population.",
            "regression_analysis": "Regression analysis is a set of statistical processes for estimating the relationships between a dependent variable and one or more independent variables.",
            "clustering": "Cluster analysis or clustering is the task of grouping a set of objects in such a way that objects in the same group (called a cluster) are more similar to each other than to those in other groups.",
            "classification": "In machine learning and statistics, classification is the problem of identifying to which of a set of categories a new observation belongs, on the basis of a training set of data containing observations whose category membership is known.",
            
            # Performance & Optimization
            "time_complexity": "Time complexity is the computational complexity that describes the amount of computer time it takes to run an algorithm.",
            "space_complexity": "Space complexity is the amount of memory space required by an algorithm to run as a function of the length of the input.",
            "big_o_notation": "Big O notation is a mathematical notation that describes the limiting behavior of a function when the argument tends towards a particular value or infinity.",
            "amortized_analysis": "Amortized analysis is a method for analyzing a given algorithm's time complexity, or how much time a given algorithm takes to execute.",
            "space_time_tradeoff": "A space-time tradeoff in computer science is a situation where an algorithm or data structure exchanges increased space usage with decreased time, or vice versa.",
            "caching": "Caching is storing copies of frequently accessed data in a faster storage layer to reduce access time.",
            "prefetching": "Prefetching is a technique used in computer architecture to speed up the execution of a program by reducing wait times.",
            
            # Machine Learning for Big Data
            "machine_learning": "Machine Learning is a subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed.",
            "deep_learning": "Deep Learning is a subset of machine learning that uses neural networks with many layers to analyze various factors of data.",
            "online_learning": "Online learning is a machine learning method in which data becomes available in a sequential order and is used to update our best predictor for future data at each step.",
            "stochastic_gradient_descent": "Stochastic gradient descent (SGD) is an iterative method for optimizing an objective function with suitable smoothness properties.",
            "feature_engineering": "Feature engineering is the process of using domain knowledge to extract features from raw data via data mining techniques.",
            "model_training": "Model training is the process of teaching a machine learning model to make predictions by exposing it to training data.",
            
            # About Hermes
            "hermes_origin": "Hermes is an AI agent framework created by Nous Research, designed to be extensible, self-improving, and capable of tool use.",
            "hermes_bigdata_capabilities": "Hermes BigData AI specializes in handling large files, implementing efficient data processing algorithms, performing streaming analytics, and providing insights on big data technologies and techniques.",
            "hermes_version": f"This is {self.name} version {self.version}.",
        }
    
    # ==================== CORE FUNCTIONALITY ====================
    
    def _get_current_time(self) -> str:
        """Get current date and time"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_current_date(self) -> str:
        """Get current date"""
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def _get_system_info(self) -> str:
        """Get system information"""
        try:
            import psutil
            uname = os.uname() if hasattr(os, 'uname') else ('Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown')
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            return f"""💻 **System Information**
OS: {uname[0]} {uname[2]} ({uname[3]})
Architecture: {uname[4]}
Processor: {os.cpu_count()} cores
Memory: {memory.total // (1024**3)} GB total, {memory.available // (1024**3)} GB available
Disk: {disk.total // (1024**3)} GB total, {disk.free // (1024**3)} GB free
Python: {sys.version.split()[0]}"""
        except:
            return f"""💻 **System Information**
OS: {sys.platform}
Python: {sys.version.split()[0]}
CPU Cores: {os.cpu_count() or 'Unknown'}"""
    
    def _calculate_expression(self, expression: str) -> str:
        """Safely evaluate a mathematical expression"""
        try:
            # Remove any non-math characters for safety (basic sanitization)
            allowed_chars = set('0123456789+-*/().%^ ')
            cleaned = ''.join(c for c in expression if c in allowed_chars)
            
            # Replace ^ with ** for exponentiation
            cleaned = cleaned.replace('^', '**')
            
            # Add math functions safely
            allowed_names = {
                "abs": abs, "round": round, "min": min, "max": max, "sum": sum,
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "log10": math.log10, "exp": math.exp,
                "pi": math.pi, "e": math.e, "factorial": math.factorial
            }
            
            # Evaluate the expression
            result = eval(cleaned, {"__builtins__": {}}, allowed_names)
            
            # Format the result nicely
            if isinstance(result, float):
                if result.is_integer():
                    return str(int(result))
                else:
                    return f"{result:.6f}".rstrip('0').rstrip('.')
            else:
                return str(result)
                
        except Exception as e:
            return f"Sorry, I couldn't calculate that. Error: {str(e)}"
    
    def _get_knowledge(self, query: str) -> Optional[str]:
        """Retrieve information from knowledge base"""
        query_lower = query.lower().strip()
        
        # Direct lookup
        for key, value in self.knowledge_base.items():
            if key in query_lower or query_lower in key:
                return value
        
        # Pattern matching for common questions
        if any(word in query_lower for word in ['what is', 'what are', 'define', 'definition', 'explain']):
            # Extract the concept being asked about
            for key, value in self.knowledge_base.items():
                if key.replace('_', ' ') in query_lower:
                    return value
        
        return None
    
    def _analyze_large_file(self, file_path: str, analysis_type: str = "basic") -> str:
        """Analyze a large file efficiently using chunking"""
        if not os.path.exists(file_path):
            return f"File '{file_path}' not found."
        
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return f"File '{file_path}' is empty."
            
            # Check if we have cached analysis
            if file_path in self.processed_files:
                cache_time, cached_result = self.processed_files[file_path]
                if (datetime.datetime.now() - cache_time).seconds < 300:  # 5 minute cache
                    return f"📊 **Cached Analysis of {os.path.basename(file_path)}**\n{cached_result}"
            
            start_time = time.time()
            
            if analysis_type == "basic":
                result = self._basic_file_analysis(file_path, file_size)
            elif analysis_type == "line_count":
                result = self._count_lines_efficiently(file_path)
            elif analysis_type == "word_count":
                result = self._count_words_efficiently(file_path)
            elif analysis_type == "sample_analysis":
                result = self._analyze_file_sample(file_path)
            elif analysis_type == "csv_analysis" and file_path.endswith('.csv'):
                result = self._analyze_csv_file(file_path)
            else:
                result = self._basic_file_analysis(file_path, file_size)
            
            # Cache the result
            self.processed_files[file_path] = (datetime.datetime.now(), result)
            
            elapsed = time.time() - start_time
            result += f"\n⏱️ Analysis completed in {elapsed:.2f} seconds"
            
            return result
            
        except Exception as e:
            return f"Error analyzing file: {str(e)}"
    
    def _basic_file_analysis(self, file_path: str, file_size: int) -> str:
        """Perform basic file analysis"""
        # Get file info
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1].lower()
        
        result = f"📊 **File Analysis: {filename}**\n"
        result += f"   Size: {self._format_bytes(file_size)}\n"
        result += f"   Type: {file_ext if file_ext else 'Unknown'} file\n"
        result += f"   Path: {file_path}\n\n"
        
        # Try to read first few lines for text files
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                first_lines = []
                for i in range(5):
                    line = f.readline()
                    if not line:
                        break
                    first_lines.append(line.rstrip('\n\r'))
                
                if first_lines:
                    result += "📄 **First 5 lines:**\n"
                    for i, line in enumerate(first_lines, 1):
                        # Truncate long lines
                        display_line = line[:100] + "..." if len(line) > 100 else line
                        result += f"   {i}. {display_line}\n"
        except:
            result += "📄 **Content preview:** Unable to read as text (possibly binary file)\n"
        
        return result
    
    def _count_lines_efficiently(self, file_path: str) -> str:
        """Count lines in a file efficiently using buffering"""
        try:
            line_count = 0
            with open(file_path, 'rb') as f:
                # Read in chunks to avoid memory issues
                chunk_size = 8192 * 1024  # 8MB chunks
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    line_count += chunk.count(b'\n')
            
            return f"📊 **Line Count: {file_path}**\n   Total lines: {line_count:,}\n   Approximate size: {self._format_bytes(os.path.getsize(file_path))}"
        except Exception as e:
            return f"Error counting lines: {str(e)}"
    
    def _count_words_efficiently(self, file_path: str) -> str:
        """Count words in a file efficiently"""
        try:
            word_count = 0
            line_count = 0
            char_count = 0
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line_count += 1
                    char_count += len(line)
                    words = line.split()
                    word_count += len(words)
            
            return f"""📊 **Word Count: {file_path}**
   Lines: {line_count:,}
   Words: {word_count:,}
   Characters: {char_count:,}
   Average words per line: {word_count/line_count:.1f if line_count > 0 else 0:.1f}"""
        except Exception as e:
            return f"Error counting words: {str(e)}"
    
    def _analyze_file_sample(self, file_path: str, sample_size: int = None) -> str:
        """Analyze a sample of the file for characteristics"""
        if sample_size is None:
            sample_size = CONFIG["sample_size"]
        
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return f"File '{file_path}' is empty."
            
            # Read sample from beginning, middle, and end
            samples = []
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Beginning
                for _ in range(min(sample_size // 3, 100)):
                    line = f.readline()
                    if not line:
                        break
                    samples.append(line.strip())
                
                # Middle
                if file_size > 1024:  # Only if file is reasonably large
                    f.seek(file_size // 2)
                    f.readline()  # Skip partial line
                    for _ in range(min(sample_size // 3, 100)):
                        line = f.readline()
                        if not line:
                            break
                        samples.append(line.strip())
                
                # End
                if file_size > 1024:
                    f.seek(max(0, file_size - 10240))  # Last 10KB
                    lines = f.readlines()
                    for line in lines[-min(sample_size // 3, 100):]:
                        samples.append(line.strip())
            
            if not samples:
                return f"Unable to sample file '{file_path}'"
            
            # Analyze the sample
            total_chars = sum(len(s) for s in samples)
            avg_line_length = total_chars / len(samples) if samples else 0
            
            # Try to detect if it's CSV
            comma_count = sum(s.count(',') for s in samples)
            tab_count = sum(s.count('\t') for s in samples)
            semicolon_count = sum(s.count(';') for s in samples)
            
            likely_delimiter = "comma (,)"
            if tab_count > comma_count:
                likely_delimiter = "tab (\\t)"
            elif semicolon_count > comma_count and semicolon_count > tab_count:
                likely_delimiter = "semicolon (;)"
            
            result = f"📊 **File Sample Analysis: {os.path.basename(file_path)}**\n"
            result += f"   Sample size: {len(samples)} lines\n"
            result += f"   Average line length: {avg_line_length:.1f} characters\n"
            result += f"   Likely delimiter: {likely_delimiter}\n"
            result += f"   File size: {self._format_bytes(file_size)}\n"
            
            # Show sample lines
            result += "\n📄 **Sample lines:**\n"
            for i, line in enumerate(samples[:5], 1):
                display_line = line[:80] + "..." if len(line) > 80 else line
                result += f"   {i}. {display_line}\n"
            
            if len(samples) > 5:
                result += f"   ... and {len(samples) - 5} more sample lines\n"
            
            return result
            
        except Exception as e:
            return f"Error sampling file: {str(e)}"
    
    def _analyze_csv_file(self, file_path: str) -> str:
        """Analyze a CSV file specifically"""
        try:
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                return f"CSV file '{file_path}' is empty."
            
            # Analyze first few rows to determine structure
            rows = []
            columns = []
            sample_rows = 0
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # Try to detect delimiter
                sample = f.read(1024)
                f.seek(0)
                
                sniffer = csv.Sniffer()
                try:
                    dialect = sniffer.sniff(sample)
                    delimiter = dialect.delimiter
                except:
                    delimiter = ','  # Default to comma
                
                reader = csv.reader(f, delimiter=delimiter)
                
                # Get header
                try:
                    headers = next(reader)
                    columns = headers
                except StopIteration:
                    return f"CSV file '{file_path}' appears to be empty or has no header."
                
                # Sample some rows
                for i, row in enumerate(reader):
                    if i >= 100:  # Sample first 100 rows after header
                        break
                    rows.append(row)
                    sample_rows += 1
            
            if not columns:
                return f"Could not determine CSV structure for '{file_path}'"
            
            # Analyze columns
            col_analysis = []
            for col_idx, col_name in enumerate(columns):
                # Collect values for this column from sample
                values = []
                for row in rows:
                    if col_idx < len(row):
                        values.append(row[col_idx])
                
                # Determine column type
                numeric_count = 0
                empty_count = 0
                unique_values = set()
                
                for val in values:
                    if val == '' or val is None:
                        empty_count += 1
                    else:
                        unique_values.add(val)
                        # Try to check if numeric
                        try:
                            float(val)
                            numeric_count += 1
                        except ValueError:
                            pass
                
                total_valid = len(values) - empty_count
                if total_valid > 0:
                    numeric_ratio = numeric_count / total_valid
                    if numeric_ratio > 0.8:
                        col_type = "numeric"
                    elif numeric_ratio > 0.2:
                        col_type = "mixed"
                    else:
                        col_type = "categorical"
                else:
                    col_type = "empty"
                
                col_analysis.append({
                    'name': col_name,
                    'type': col_type,
                    'unique_values': len(unique_values),
                    'empty_count': empty_count,
                    'sample_size': len(values)
                })
            
            # Build result
            result = f"📊 **CSV Analysis: {os.path.basename(file_path)}**\n"
            result += f"   File size: {self._format_bytes(file_size)}\n"
            result += f"   Columns: {len(columns)}\n"
            result += f"   Sampled rows: {sample_rows}\n"
            result += f"   Detected delimiter: '{delimiter}'\n\n"
            
            result += "📋 **Column Analysis:**\n"
            for col in col_analysis:
                result += f"   • {col['name']}: {col['type']}"
                if col['type'] == 'categorical' and col['unique_values'] <= 10:
                    result += f" ({col['unique_values']} unique values)"
                result += f" - {col['empty_count']} empty/{col['sample_size']} sampled\n"
            
            # Show first few rows as example
            if rows:
                result += "\n📄 **Sample data (first 3 rows):**\n"
                header_line = " | ".join(f"{h:<12}" for h in columns[:5])
                result += f"   {header_line}\n"
                result += f"   {'-'*len(header_line)}\n"
                for i, row in enumerate(rows[:3], 1):
                    row_data = " | ".join(str(cell)[:10] for cell in row[:5])
                    result += f"   {i}. {row_data}\n"
            
            return result
            
        except Exception as e:
            return f"Error analyzing CSV file: {str(e)}"
    
    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes into human readable format"""
        if bytes_value == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while bytes_value >= 1024 and i < len(size_names) - 1:
            bytes_value /= 1024.0
            i += 1
        return f"{bytes_value:.1f} {size_names[i]}"
    
    def _map_reduce_word_count(self, file_path: str) -> str:
        """Perform a map-reduce style word count on a text file"""
        try:
            if not os.path.exists(file_path):
                return f"File '{file_path}' not found."
            
            start_time = time.time()
            
            # MAP phase: process chunks and emit (word, 1) pairs
            def map_chunk(chunk: str) -> Dict[str, int]:
                word_counts = defaultdict(int)
                words = re.findall(r'\b\w+\b', chunk.lower())
                for word in words:
                    word_counts[word] += 1
                return dict(word_counts)
            
            # REDUCE phase: combine counts from multiple maps
            def reduce_counts(count1: Dict[str, int], count2: Dict[str, int]) -> Dict[str, int]:
                result = defaultdict(int)
                for k, v in count1.items():
                    result[k] += v
                for k, v in count2.items():
                    result[k] += v
                return dict(result)
            
            # Process file in chunks
            chunk_size = 64 * 1024  # 64KB chunks
            final_counts = defaultdict(int)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    # Map
                    mapped = map_chunk(chunk)
                    
                    # Reduce (in this case, just accumulate)
                    for word, count in mapped.items():
                        final_counts[word] += count
            
            # Get top words
            top_words = sorted(final_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            elapsed = time.time() - start_time
            
            result = f"📊 **MapReduce Word Count: {os.path.basename(file_path)}**\n"
            result += f"   Processing time: {elapsed:.2f} seconds\n"
            result += f"   Unique words found: {len(final_counts):,}\n"
            result += f"   Total word occurrences: {sum(final_counts.values()):,}\n\n"
            
            result += "🔝 **Top 10 Words:**\n"
            for word, count in top_words:
                result += f"   {word}: {count:,} occurrences\n"
            
            return result
            
        except Exception as e:
            return f"Error in MapReduce word count: {str(e)}"
    
    def _process_command(self, user_input: str) -> Optional[str]:
        """Process special commands"""
        command = user_input.strip().lower()
        
        # Help command
        if command in ['help', '?', 'commands']:
            return self._get_help_text()
        
        # Clear screen
        if command in ['clear', 'cls']:
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Screen cleared. How can I assist you with big data processing?"
        
        # Time/date commands
        if command == 'time':
            return f"🕐 Current time: {self._get_current_time()}"
        if command == 'date':
            return f"📅 Today's date: {self._get_current_date()}"
        
        # System info
        if command in ['system', 'sysinfo', 'info']:
            return self._get_system_info()
        
        # Calculator
        if command.startswith('calc '):
            expression = command[5:].strip()
            if not expression:
                return "Please provide a mathematical expression to calculate (e.g., 'calc 2+2*3')"
            result = self._calculate_expression(expression)
            return f"🧮 {expression} = {result}"
        
        # File operations
        if command == 'files':
            return self._list_files()
        if command.startswith('files '):
            directory = command[6:].strip()
            return self._list_files(directory)
        
        if command.startswith('read '):
            filename = command[5:].strip()
            if not filename:
                return "Please specify a filename to read (e.g., 'read data.csv')"
            return self._read_file(filename)
        
        # File analysis commands
        if command.startswith('analyze '):
            parts = command[8:].strip().split()
            if not parts:
                return "Usage: analyze <file_path> [type]\nTypes: basic, lines, words, sample, csv, wordcount"
            
            file_path = parts[0]
            analysis_type = parts[1] if len(parts) > 1 else "basic"
            
            if not os.path.exists(file_path):
                return f"File '{file_path}' not found."
            
            return self._analyze_large_file(file_path, analysis_type)
        
        if command == 'wordcount':
            if len(user_input.split()) < 2:
                return "Usage: wordcount <file_path>"
            file_path = user_input.split()[1]
            if not os.path.exists(file_path):
                return f"File '{file_path}' not found."
            return self._map_reduce_word_count(file_path)
        
        # Dataset analysis (for sample datasets)
        if command.startswith('stats '):
            dataset_name = command[6:].strip()
            if not dataset_name:
                return "Please specify a dataset name (e.g., 'stats employees')"
            # For now, just say we don't have pre-loaded datasets in this version
            return f"I don't have pre-loaded datasets in this BigData version. Use 'analyze <file_path>' to analyze actual files."
        if command == 'datasets':
            return "📊 This BigData version focuses on analyzing actual files rather than pre-loaded datasets.\nUse 'analyze <file_path>' to analyze files on your system."
        
        # Conversation history
        if command == 'history':
            if not self.conversation_history:
                return "No conversation history yet."
            history_text = "📜 **Conversation History:**\n"
            for i, (user_msg, bot_resp) in enumerate(self.conversation_history[-5:], 1):  # Show last 5
                history_text += f"{i}. You: {user_msg[:50]}{'...' if len(user_msg) > 50 else ''}\n"
                history_text += f"   Me: {bot_resp[:50]}{'...' if len(bot_resp) > 50 else ''}\n\n"
            return history_text
        
        # About me
        if command in ['about', 'whoami']:
            return f"""🤖 **About {self.name}**
Version: {self.version}
Created by: {self.creator}
Session started: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}
Specialization: Big data processing, large file handling, efficient algorithms
Currently chatting with: {self.user_name or 'Anonymous'}"""
        
        # Reset conversation
        if command in ['reset', 'clear history']:
            self.conversation_history = []
            return "Conversation history cleared. Fresh start!"
        
        # Performance test
        if command.startswith('benchmark '):
            test_type = command[10:].strip()
            return self._run_benchmark(test_type)
        
        return None  # Not a command, let AI handle it
    
    def _get_help_text(self) -> str:
        """Return help text"""
        return """🤖 **Hermes BigData AI - Available Commands**

**General Chat:**
Just type your question or message normally!

**Utility Commands:**
• `help` or `?` - Show this help message
• `clear` or `cls` - Clear the terminal screen
• `time` - Show current time
• `date` - Show current date
• `system` or `sysinfo` - Show system information
• `history` - Show recent conversation history
• `about` or `whoami` - Information about me
• `reset` or `clear history` - Clear conversation history
• `exit`, `quit`, `bye` - End the conversation

**Calculations:**
• `calc <expression>` - Calculate mathematical expressions
  Examples: `calc 2+2*3`, `calc sqrt(144)`, `calc (5+3)^2`

**File Operations:**
• `files` - List files in current directory
• `files <directory>` - List files in specified directory
• `read <filename>` - Display contents of a text file

**Big Data Analysis:**
• `analyze <file_path> [type]` - Analyze a file
  Types: basic (default), lines, words, sample, csv, wordcount
  Examples: 
    `analyze data.csv`
    `analyze log.txt lines`
    `analyze huge.csv csv`
    `analyze big.txt wordcount`
• `wordcount <file_path>` - Perform MapReduce word count on text file

**Tips:**
• I specialize in handling large files efficiently using chunking and streaming
• For very large files, I use memory-efficient techniques
• Try: "analyze large_file.log lines" to count lines without loading everything into memory
• Ask about: big data concepts, map-reduce, streaming algorithms, data compression
• Example: "What is MapReduce?" or "Explain data streaming"
"""
    
    def process_message(self, user_input: str) -> str:
        """Process user message and generate response"""
        # Store original input for history
        original_input = user_input
        
        # Check if it's a command first
        command_response = self._process_command(user_input)
        if command_response is not None:
            # Store in history
            self.conversation_history.append((original_input, command_response))
            return command_response
        
        # Not a command, process as natural language
        user_input_lower = user_input.lower().strip()
        
        # Handle greetings
        if any(greeting in user_input_lower for greeting in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            response = random.choice(self.greetings)
            if self.user_name:
                response = f"Hello {self.user_name}! " + response[len("Hello!"):]
        
        # Handle farewells
        elif any(farewell in user_input_lower for farewell in ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit']):
            response = random.choice(self.farewells)
        
        # Handle name setting
        elif 'my name is' in user_input_lower or 'i am' in user_input_lower or 'im' in user_input_lower:
            # Simple name extraction
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['is', 'am', 'im'] and i+1 < len(words):
                    # Extract name from remaining words
                    name_parts = words[i+1:]
                    potential_name = ' '.join(name_parts).strip('.,!?')
                    if potential_name and len(potential_name) < 20:  # Reasonable name length
                        self.user_name = potential_name
                        response = f"Nice to meet you, {self.user_name}! How can I assist you with big data today?"
                        break
            else:
                response = "Hello! I'm here to help with big data processing. What's your name?"
        
        # Handle thanks
        elif any(thanks in user_input_lower for thanks in ['thank', 'thanks', 'thx']):
            responses = [
                "You're welcome! Happy to help with your data processing needs.",
                "My pleasure! Let me know if you need assistance with large files or data analysis.",
                "Anytime! That's what I'm here for - helping you tackle big data challenges.",
                "You're very welcome! Feel free to ask more questions about data processing."
            ]
            response = random.choice(responses)
        
        # Handle jokes
        elif 'joke' in user_input_lower or 'funny' in user_input_lower:
            response = f"😄 {random.choice(self.jokes)}"
        
        # Handle quotes/inspiration
        elif any(word in user_input_lower for word in ['quote', 'inspire', 'motivation', 'inspirational']):
            response = f"💫 \"{random.choice(self.quotes)}\""
        
        # Handle knowledge questions
        else:
            knowledge_response = self._get_knowledge(user_input)
            if knowledge_response:
                response = f"📚 {knowledge_response}"
            else:
                # Try to handle as a general question
                response = self._generate_general_response(user_input)
        
        # Store in conversation history
        self.conversation_history.append((original_input, response))
        
        return response
    
    def _generate_general_response(self, user_input: str) -> str:
        """Generate a general response for unrecognized queries"""
        user_lower = user_input.lower()
        
        # Check for question words
        if any(word in user_lower for word in ['what', 'how', 'why', 'when', 'where', 'who', 'which']):
            responses = [
                f"That's an interesting question about '{user_input}'. While I don't have specific information on that topic in my knowledge base, I can help with file analysis, big data concepts, efficient algorithms, or data processing techniques. Would you like help with something else?",
                f"I'm not sure I have detailed information about '{user_input}' in my current knowledge base. However, I'm an expert at handling large files, performing efficient data analysis, explaining map-reduce patterns, and assisting with big data challenges. What would you like to try?",
                f"That's a thoughtful question! My expertise is more focused on big data technologies, file processing optimization, streaming algorithms, and data analysis techniques. Could you rephrase your question or ask about something I might know more about?"
            ]
            return random.choice(responses)
        else:
            # Statement or comment
            responses = [
                f"I see. Thanks for sharing that about '{user_input}'. Is there something specific you'd like me to help you with regarding file processing or data analysis?",
                f"Interesting point about '{user_input}'. Would you like to explore that further in the context of big data, or is there something else I can assist you with?",
                f"Thanks for telling me! If you have any questions or need help with large file processing, data analysis, algorithms, or just want to chat about big data topics, I'm here.",
                f"That's noteworthy! Is there a particular aspect of data processing or file handling you'd like to dive deeper into, or shall we talk about something else?"
            ]
            return random.choice(responses)
    
    def start_chat(self):
        """Start the interactive chat session"""
        # Clear screen for clean start
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 70)
        print(f"🤖 {self.name} v{self.version}")
        print("   Your Big Data Processing Specialist")
        print("=" * 70)
        print("Type 'help' for available commands, or just start chatting!")
        print("Type 'exit', 'quit', or 'bye' to end the conversation.")
        print("-" * 70)
        
        # Initial greeting
        print(f"\n{self.name}: {random.choice(self.greetings)}")
        print("-" * 70)
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("\n> ").strip()
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                    farewell = random.choice(self.farewells)
                    if self.user_name:
                        farewell = f"Goodbye {self.user_name}! {farewell[len('Goodbye!'):]}"
                    print(f"\n{self.name}: {farewell}")
                    break
                
                # Skip empty input
                if not user_input:
                    continue
                
                # Process and get response
                response = self.process_message(user_input)
                
                # Display response
                print(f"\n{self.name}: {response}")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print(f"\n\n{self.name}: Goodbye! (Interrupted)")
                break
            except EOFError:
                # Handle non-interactive environments gracefully
                print(f"\n\n{self.name}: Session ended. Goodbye!")
                break
            except Exception as e:
                print(f"\n{self.name}: Sorry, I encountered an error: {str(e)}")
                print("Please try again or type 'help' for assistance.")

# ==================== MAIN EXECUTION ====================

def main():
    """Main function to start the BigData AI assistant"""
    assistant = HermesBigDataAI()
    assistant.start_chat()

if __name__ == "__main__":
    # Check if we're running in a terminal that supports input
    if not sys.stdin.isatty():
        print("Note: For full interactive experience, run this in a terminal/command prompt.")
        print("Starting in demo mode...\n")
        
        # Demo mode for non-interactive environments
        assistant = HermesBigDataAI()
        print(f"🤖 {assistant.name} v{assistant.version}")
        print("=" * 50)
        print("Demo: Sample interactions")
        print("-" * 50)
        
        # Show a few sample interactions
        samples = [
            "Hello!",
            "What is big data?",
            "Explain MapReduce",
            "How do I analyze a large log file?",
            "Tell me a joke about data",
            "About",
            "Thanks!",
            "Bye"
        ]
        
        for sample in samples:
            print(f"\n> {sample}")
            response = assistant.process_message(sample)
            print(f"{assistant.name}: {response}")
            print("-" * 30)
        
        print("\n💡 To use the full interactive version, run this script in your terminal!")
    else:
        try:
            main()
        except KeyboardInterrupt:
            print("\n\nChatbot terminated by user. Goodbye!")
        except Exception as e:
            print(f"\nFatal error: {str(e)}")
            sys.exit(1)