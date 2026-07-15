#!/usr/bin/env python3
"""
DataSage: Advanced Data Analysis AI Assistant
A comprehensive tool for data processing, analysis, and machine learning
designed to demonstrate big data handling techniques and algorithms.
"""

import os
import sys
import json
import csv
import math
import random
import statistics
import datetime
import time
from typing import List, Dict, Any, Optional, Tuple, Generator
from collections import defaultdict, Counter
import heapq
import bisect

# ==================== DATA GENERATION MODULE ====================

class DataGenerator:
    """Generate synthetic datasets for testing and demonstration"""
    
    @staticmethod
    def generate_csv_data(filename: str, rows: int = 100000, cols: int = 10) -> str:
        """Generate a large CSV file with synthetic data"""
        print(f"Generating {rows:,} rows x {cols} cols dataset...")
        
        headers = [f"col_{i}" for i in range(cols)]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    # Generate different types of data based on column index
                    if col % 4 == 0:  # Integer IDs
                        val = random.randint(1, 1000000)
                    elif col % 4 == 1:  # Floating point measurements
                        val = round(random.uniform(0.0, 1000.0), 4)
                    elif col % 4 == 2:  # Categories
                        val = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])
                    else:  # Dates
                        days_offset = random.randint(0, 365*5)  # 5 years
                        date = datetime.datetime(2020, 1, 1) + datetime.timedelta(days=days_offset)
                        val = date.strftime('%Y-%m-%d')
                    row_data.append(val)
                writer.writerow(row_data)
                
                # Progress indicator for large files
                if row % 10000 == 0 and row > 0:
                    print(f"  Generated {row:,} rows...")
        
        file_size = os.path.getsize(filename)
        print(f"Generated {filename}: {rows:,} rows, {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        return filename
    
    @staticmethod
    def generate_json_data(filename: str, records: int = 50000) -> str:
        """Generate JSON data with nested structures"""
        print(f"Generating {records:,} JSON records...")
        
        data = []
        for i in range(records):
            record = {
                "id": i + 1,
                "timestamp": (datetime.datetime(2020, 1, 1) + 
                             datetime.timedelta(seconds=random.randint(0, 365*24*3600))).isoformat(),
                "user_info": {
                    "user_id": f"user_{random.randint(1000, 9999)}",
                    "age": random.randint(18, 80),
                    "gender": random.choice(["M", "F", "Other"]),
                    "preferences": {
                        "newsletter": random.choice([True, False]),
                        "notifications": random.choice([True, False]),
                        "theme": random.choice(["light", "dark", "auto"])
                    }
                },
                "activity": {
                    "actions": random.randint(0, 100),
                    "duration": round(random.uniform(0.0, 3600.0), 2),
                    "features": [f"feature_{j}" for j in random.sample(range(20), random.randint(1, 5))]
                },
                "metrics": {
                    "score": round(random.uniform(0.0, 100.0), 2),
                    "rating": random.randint(1, 5),
                    "success": random.choice([True, False])
                },
                "tags": [f"tag_{j}" for j in random.sample(range(50), random.randint(0, 8))]
            }
            data.append(record)
            
            # Progress indicator
            if i % 5000 == 0 and i > 0:
                print(f"  Generated {i:,} records...")
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        file_size = os.path.getsize(filename)
        print(f"Generated {filename}: {records:,} records, {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        return filename

# ==================== DATA PROCESSING CORE ====================

class DataProcessor:
    """Efficient data processing utilities for large datasets"""
    
    @staticmethod
    def read_csv_chunked(filename: str, chunk_size: int = 10000) -> Generator[List[List[str]], None, None]:
        """Read CSV file in chunks to handle large files"""
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read header
            
            chunk = []
            for row in reader:
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    yield headers, chunk
                    chunk = []
            
            # Yield remaining rows
            if chunk:
                yield headers, chunk
    
    @staticmethod
    def calculate_statistics(data: List[float]) -> Dict[str, float]:
        """Calculate comprehensive statistics for numeric data"""
        if not data:
            return {}
        
        sorted_data = sorted(data)
        n = len(data)
        
        return {
            'count': n,
            'mean': statistics.mean(data),
            'median': statistics.median(data),
            'mode': statistics.mode(data) if len(set(data)) < n else None,
            'stdev': statistics.stdev(data) if n > 1 else 0.0,
            'variance': statistics.variance(data) if n > 1 else 0.0,
            'min': min(data),
            'max': max(data),
            'range': max(data) - min(data),
            'q1': statistics.quantiles(data, n=4)[0] if n >= 4 else None,
            'q3': statistics.quantiles(data, n=4)[2] if n >= 4 else None,
            'iqr': (statistics.quantiles(data, n=4)[2] - statistics.quantiles(data, n=4)[0]) if n >= 4 else None,
            'sum': sum(data)
        }
    
    @staticmethod
    def correlation_coefficient(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
        
        return numerator / denominator if denominator != 0 else 0.0
    
    @staticmethod
    def linear_regression(x: List[float], y: List[float]) -> Dict[str, float]:
        """Perform simple linear regression"""
        if len(x) != len(y) or len(x) < 2:
            return {'slope': 0.0, 'intercept': 0.0, 'r_squared': 0.0}
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)
        
        # Calculate slope and intercept
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if (n * sum_x2 - sum_x2 - sum_x * sum_x) != 0 else 0.0
        intercept = (sum_y - slope * sum_x) / n
        
        # Calculate R-squared
        y_mean = sum_y / n
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)
        ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0
        
        return {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'predictions': [slope * xi + intercept for xi in x]
        }

# ==================== MACHINE LEARNING BASICS ====================

class SimpleML:
    """Basic machine learning algorithms for demonstration"""
    
    @staticmethod
    def kmeans_clustering(points: List[List[float]], k: int, max_iterations: int = 100) -> Tuple[List[List[float]], List[int]]:
        """Simple K-means clustering implementation"""
        if not points or k <= 0:
            return [], []
        
        # Initialize centroids randomly
        centroids = random.sample(points, k)
        
        for _ in range(max_iterations):
            # Assign points to closest centroid
            clusters = [[] for _ in range(k)]
            for point in points:
                distances = [math.sqrt(sum((p - c) ** 2 for p, c in zip(point, centroid))) for centroid in centroids]
                closest = distances.index(min(distances))
                clusters[closest].append(point)
            
            # Update centroids
            new_centroids = []
            for cluster in clusters:
                if cluster:
                    centroid = [sum(dim) / len(dim) for dim in zip(*cluster)]
                    new_centroids.append(centroid)
                else:
                    # If cluster is empty, reinitialize randomly
                    new_centroids.append(random.choice(points))
            
            # Check for convergence
            if all(abs(c1 - c2) < 0.001 for c1, c2 in zip(centroids, new_centroids)):
                break
                
            centroids = new_centroids
        
        # Assign final labels
        labels = []
        for point in points:
            distances = [math.sqrt(sum((p - c) ** 2 for p, c in zip(point, centroid))) for centroid in centroids]
            labels.append(distances.index(min(distances)))
        
        return centroids, labels
    
    @staticmethod
    def naive_bayes_train(texts: List[str], labels: List[str]) -> Dict[str, Any]:
        """Simple Naive Bayes classifier for text"""
        # Preprocess text
        def tokenize(text):
            return [word.lower().strip('.,!?;:"()[]{}') for word in text.split()]
        
        # Calculate priors
        label_counts = Counter(labels)
        total_docs = len(labels)
        priors = {label: count / total_docs for label, count in label_counts.items()}
        
        # Calculate likelihoods
        vocabulary = set()
        word_counts = defaultdict(lambda: defaultdict(int))
        label_word_counts = defaultdict(int)
        
        for text, label in zip(texts, labels):
            tokens = tokenize(text)
            for token in tokens:
                vocabulary.add(token)
                word_counts[label][token] += 1
                label_word_counts[label] += 1
        
        # Calculate likelihoods with Laplace smoothing
        likelihoods = {}
        vocab_size = len(vocabulary)
        
        for label in label_counts:
            likelihoods[label] = {}
            for word in vocabulary:
                count = word_counts[label].get(word, 0)
                likelihoods[label][word] = (count + 1) / (label_word_counts[label] + vocab_size)
        
        return {
            'priors': priors,
            'likelihoods': likelihoods,
            'vocabulary': vocabulary
        }
    
    @staticmethod
    def naive_bayes_predict(model: Dict[str, Any], text: str) -> str:
        """Predict using trained Naive Bayes model"""
        def tokenize(text):
            return [word.lower().strip('.,!?;:"()[]{}') for word in text.split()]
        
        tokens = tokenize(text)
        best_label = None
        max_prob = float('-inf')
        
        for label in model['priors']:
            # Start with log prior
            log_prob = math.log(model['priors'][label])
            
            # Add log likelihood for each token
            for token in tokens:
                if token in model['vocabulary']:
                    likelihood = model['likelihoods'][label].get(token, 1e-10)  # Small probability for unseen words
                    log_prob += math.log(likelihood)
            
            if log_prob > max_prob:
                max_prob = log_prob
                best_label = label
        
        return best_label

# ==================== FILE HANDLING & UTILITIES ====================

class FileHandler:
    """Efficient file handling utilities"""
    
    @staticmethod
    def get_file_info(filepath: str) -> Dict[str, Any]:
        """Get comprehensive file information"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        stat = os.stat(filepath)
        return {
            "path": filepath,
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 2),
            "size_mb": round(stat.st_size / (1024 * 1024), 2),
            "size_gb": round(stat.st_size / (1024 * 1024 * 1024), 2),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "is_file": os.path.isfile(filepath),
            "is_dir": os.path.isdir(filepath),
            "readable": os.access(filepath, os.R_OK),
            "writable": os.access(filepath, os.W_OK)
        }
    
    @staticmethod
    def count_lines(filename: str) -> int:
        """Efficiently count lines in large file"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except Exception as e:
            return f"Error: {str(e)}"
    
    @staticmethod
    def tail_file(filename: str, lines: int = 10) -> List[str]:
        """Get last N lines from file (efficient for large files)"""
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                # Read from end of file
                total_lines_wanted = lines
                block_size = 1024
                f.seek(0, os.SEEK_END)
                file_size = remaining = f.tell()
                
                lines_found = []
                block = -1
                
                while len(lines_found) < total_lines_wanted and remaining > 0:
                    if block_size > remaining:
                        block_size = remaining
                        seek_pos = 0
                    else:
                        seek_pos = file_size - block_size * abs(block)
                    
                    f.seek(seek_pos)
                    block_data = f.read(block_size)
                    
                    # Count newlines in this block
                    lines_found = block_data.count('\n') + len(lines_found)
                    
                    if lines_found >= total_lines_wanted:
                        # Found enough lines, extract the last 'lines' lines
                        all_lines = block_data.split('\n')
                        return [line for line in all_lines[-(lines+1):-1] if line][-lines:]
                    
                    block -= 1
                    remaining -= block_size
                
                # If we get here, read from beginning
                f.seek(0)
                return f.read().splitlines()[-lines:]
                
        except Exception as e:
            return [f"Error reading file: {str(e)}"]

# ==================== MAIN AI ASSISTANT CLASS ====================

class DataSageAI:
    """Main AI Assistant for Data Science and Big Data operations"""
    
    def __init__(self):
        self.name = "DataSage AI"
        self.version = "2.0.0"
        self.data_processor = DataProcessor()
        self.ml_engine = SimpleML()
        self.file_handler = FileHandler()
        self.conversation_history = []
        self.loaded_datasets = {}
        self.models = {}
        
        # Initialize with some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Create some sample datasets for demonstration"""
        sample_dir = "sample_data"
        if not os.path.exists(sample_dir):
            os.makedirs(sample_dir)
        
        # Create a small CSV sample if none exists
        sample_csv = os.path.join(sample_dir, "sample_data.csv")
        if not os.path.exists(sample_csv):
            print("Generating sample dataset...")
            DataGenerator.generate_csv_data(sample_csv, rows=1000, cols=5)
            self.load_dataset("sample_csv", sample_csv)
    
    def load_dataset(self, name: str, filepath: str, sample_size: Optional[int] = None) -> bool:
        """Load a dataset into memory (with optional sampling for large files)"""
        try:
            if not os.path.exists(filepath):
                print(f"Error: File {filepath} not found")
                return False
            
            file_info = self.file_handler.get_file_info(filepath)
            print(f"Loading dataset: {file_info['size_mb']} MB")
            
            # For very large files, offer sampling
            if file_info['size_mb'] > 100 and sample_size is None:
                response = input(f"File is {file_info['size_mb']} MB. Load a sample? (y/n): ")
                if response.lower() == 'y':
                    sample_size = min(10000, self._estimate_rows(filepath))
                    print(f"Will load sample of {sample_size} rows")
            
            # Load data based on file extension
            if filepath.endswith('.csv'):
                data = self._load_csv(filepath, sample_size)
            elif filepath.endswith('.json'):
                data = self._load_json(filepath, sample_size)
            else:
                print("Unsupported file format. Please use .csv or .json")
                return False
            
            self.loaded_datasets[name] = {
                'data': data,
                'filepath': filepath,
                'loaded_at': datetime.datetime.now().isoformat(),
                'size_info': file_info
            }
            
            print(f"Successfully loaded dataset '{name}' with {len(data) if data else 0} records")
            return True
            
        except Exception as e:
            print(f"Error loading dataset: {str(e)}")
            return False
    
    def _estimate_rows(self, filepath: str) -> int:
        """Estimate number of rows in a CSV file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Read first line to estimate average line length
                first_line = f.readline()
                if not first_line:
                    return 0
                
                avg_line_length = len(first_line.encode('utf-8'))
                file_size = os.path.getsize(filepath)
                estimated_lines = file_size // avg_line_length
                return max(100, estimated_lines)  # Minimum 100 lines
        except:
            return 1000  # Default fallback
    
    def _load_csv(self, filepath: str, sample_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load CSV data into list of dictionaries"""
        data = []
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for i, row in enumerate(reader):
                    if sample_size and i >= sample_size:
                        break
                    data.append(dict(row))
            return data
        except Exception as e:
            print(f"Error reading CSV: {str(e)}")
            return []
    
    def _load_json(self, filepath: str, sample_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """Load JSON data"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    if sample_size:
                        return data[:sample_size]
                    return data
                else:
                    # If it's a single object, wrap in list
                    return [data] if not sample_size else [data][:sample_size]
        except Exception as e:
            print(f"Error reading JSON: {str(e)}")
            return []
    
    def analyze_dataset(self, name: str) -> Dict[str, Any]:
        """Perform comprehensive analysis on a loaded dataset"""
        if name not in self.loaded_datasets:
            return {"error": f"Dataset '{name}' not found"}
        
        dataset = self.loaded_datasets[name]
        data = dataset['data']
        
        if not data:
            return {"error": "Dataset is empty"}
        
        print(f"Analyzing dataset '{name}' ({len(data)} records)...")
        start_time = time.time()
        
        # Basic info
        analysis = {
            'dataset_name': name,
            'record_count': len(data),
            'fields': list(data[0].keys()) if data else [],
            'analysis_time': None
        }
        
        # Analyze each field
        field_analysis = {}
        numeric_fields = []
        
        for field in data[0].keys():
            values = [record.get(field) for record in data if record.get(field) is not None]
            
            # Try to convert to numeric
            numeric_values = []
            for val in values:
                try:
                    if isinstance(val, str):
                        # Try to parse as number
                        num_val = float(val)
                        numeric_values.append(num_val)
                    elif isinstance(val, (int, float)):
                        numeric_values.append(float(val))
                except (ValueError, TypeError):
                    pass  # Not numeric
            
            field_info = {
                'total_values': len(values),
                'non_null_values': len([v for v in values if v is not None and v != '']),
                'null_count': len([v for v in values if v is None or v == '']),
                'unique_values': len(set(str(v) for v in values if v is not None and v != '')) if values else 0
            }
            
            if numeric_values and len(numeric_values) > 1:
                field_info['numeric_stats'] = self.data_processor.calculate_statistics(numeric_values)
                numeric_fields.append((field, numeric_values))
            
            field_analysis[field] = field_info
        
        analysis['field_analysis'] = field_analysis
        
        # Correlation analysis for numeric fields
        if len(numeric_fields) >= 2:
            correlations = {}
            for i, (field1, values1) in enumerate(numeric_fields):
                for j, (field2, values2) in enumerate(numeric_fields[i+1:], i+1):
                    corr = self.data_processor.correlation_coefficient(values1, values2)
                    correlations[f"{field1}_vs_{field2}"] = round(corr, 4)
            
            analysis['correlations'] = correlations
        
        analysis['analysis_time'] = round(time.time() - start_time, 3)
        return analysis
    
    def run_ml_experiment(self, dataset_name: str, target_field: str, algorithm: str = "naive_bayes") -> Dict[str, Any]:
        """Run a machine learning experiment on the dataset"""
        if dataset_name not in self.loaded_datasets:
            return {"error": f"Dataset '{dataset_name}' not found"}
        
        data = self.loaded_datasets[dataset_name]['data']
        if not data:
            return {"error": "Dataset is empty"}
        
        print(f"Running {algorithm} on dataset '{dataset_name}'...")
        start_time = time.time()
        
        # Prepare data
        X = []  # Features
        y = []  # Labels
        
        for record in data:
            # Extract target
            target_val = record.get(target_field)
            if target_val is None:
                continue
            y.append(str(target_val))
            
            # Create feature vector (simplified - in reality would need proper feature engineering)
            feature_vector = []
            for key, value in record.items():
                if key != target_field:
                    # Simple feature extraction: convert to numeric if possible, else hash
                    try:
                        feature_vector.append(float(value))
                    except (ValueError, TypeError):
                        # Hash string values to numbers
                        feature_vector.append(float(hash(str(value)) % 1000))
            
            X.append(feature_vector)
        
        if not X or not y:
            return {"error": "Insufficient data for training"}
        
        # Ensure we have at least 2 classes
        unique_labels = set(y)
        if len(unique_labels) < 2:
            return {"error": "Need at least 2 different classes for classification"}
        
        # Split data (simple 80/20 split)
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        results = {
            'algorithm': algorithm,
            'dataset': dataset_name,
            'target_field': target_field,
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'features_per_sample': len(X[0]) if X else 0,
            'unique_classes': list(unique_labels)
        }
        
        if algorithm == "naive_bayes":
            # Convert features to text-like representation for Naive Bayes demo
            def features_to_text(features):
                return " ".join([f"f{i}_{int(val)}" for i, val in enumerate(features)])
            
            X_train_text = [features_to_text(f) for f in X_train]
            X_test_text = [features_to_text(f) for f in X_test]
            
            # Train model
            model = self.ml_engine.naive_bayes_train(X_train_text, y_train)
            
            # Make predictions
            predictions = []
            for text in X_test_text:
                pred = self.ml_engine.naive_bayes_predict(model, text)
                predictions.append(pred)
            
            # Calculate accuracy
            correct = sum(1 for pred, true in zip(predictions, y_test) if pred == true)
            accuracy = correct / len(y_test) if y_test else 0
            
            results.update({
                'model': model,
                'predictions': predictions[:10],  # Show first 10 predictions
                'actual': y_test[:10],
                'accuracy': round(accuracy, 4),
                'correct_predictions': correct,
                'total_predictions': len(y_test)
            })
        
        results['execution_time'] = round(time.time() - start_time, 3)
        
        # Store model
        model_key = f"{dataset_name}_{target_field}_{algorithm}_{int(time.time())}"
        self.models[model_key] = results
        
        return results
    
    def generate_report(self, analysis_results: Dict[str, Any]) -> str:
        """Generate a human-readable report from analysis results"""
        if "error" in analysis_results:
            return f"❌ Error: {analysis_results['error']}"
        
        report = []
        report.append("=" * 60)
        report.append(f"📊 DATA ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Dataset: {analysis_results.get('dataset_name', 'Unknown')}")
        report.append(f"Records: {analysis_results.get('record_count', 0):,}")
        report.append(f"Analysis Time: {analysis_results.get('analysis_time', 0)}s")
        report.append("")
        
        # Field analysis
        if 'field_analysis' in analysis_results:
            report.append("📋 FIELD ANALYSIS:")
            report.append("-" * 40)
            for field, info in analysis_results['field_analysis'].items():
                report.append(f"  {field}:")
                report.append(f"    Values: {info['total_values']:,} total, {info['non_null_values']:,} non-null, {info['null_count']:,} null")
                report.append(f"    Unique values: {info['unique_values']:,}")
                
                if 'numeric_stats' in info and info['numeric_stats']:
                    stats = info['numeric_stats']
                    report.append(f"    Numeric stats: Mean={stats.get('mean', 0):.2f}, Median={stats.get('median', 0):.2f}, "
                                f"StdDev={stats.get('stdev', 0):.2f}, Min={stats.get('min', 0):.2f}, Max={stats.get('max', 0):.2f}")
                report.append("")
        
        # Correlations
        if 'correlations' in analysis_results and analysis_results['correlations']:
            report.append("🔗 CORRELATIONS:")
            report.append("-" * 40)
            for pair, corr in analysis_results['correlations'].items():
                strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.3 else "Weak"
                direction = "positive" if corr > 0 else "negative" if corr < 0 else "no"
                report.append(f"  {pair}: {corr:+.4f} ({strength} {direction} correlation)")
            report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)
    
    def chat(self):
        """Interactive chat interface"""
        print(f"🤖 {self.name} v{self.version}")
        print("Type 'help' for commands, 'quit' to exit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"{self.name}: Goodbye! Thanks for using DataSage AI.")
                    break
                
                elif user_input.lower() == 'help':
                    self._show_help()
                
                elif user_input.lower() == 'datasets':
                    self._list_datasets()
                
                elif user_input.lower().startswith('load '):
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 2:
                        name = parts[1]
                        filepath = parts[2] if len(parts) > 2 else name
                        self.load_dataset(name, filepath)
                    else:
                        print("Usage: load <name> [filepath]")
                
                elif user_input.lower().startswith('analyze '):
                    parts = user_input.split(' ', 1)
                    if len(parts) == 2:
                        dataset_name = parts[1]
                        result = self.analyze_dataset(dataset_name)
                        print(self.generate_report(result))
                    else:
                        print("Usage: analyze <dataset_name>")
                
                elif user_input.lower().startswith('ml '):
                    parts = user_input.split(' ')
                    if len(parts) >= 3:
                        dataset_name = parts[1]
                        target_field = parts[2]
                        algorithm = parts[3] if len(parts) > 3 else "naive_bayes"
                        result = self.run_ml_experiment(dataset_name, target_field, algorithm)
                        print(json.dumps(result, indent=2))
                    else:
                        print("Usage: ml <dataset_name> <target_field> [algorithm]")
                
                elif user_input.lower() == 'stats':
                    self._show_system_stats()
                
                else:
                    # Default conversational response
                    response = self._get_conversational_response(user_input)
                    print(f"{self.name}: {response}")
                    
            except KeyboardInterrupt:
                print(f"\n{self.name}: Goodbye!")
                break
            except Exception as e:
                print(f"{self.name}: Sorry, I encountered an error: {str(e)}")
    
    def _show_help(self):
        """Display help information"""
        help_text = """
🔧 Available Commands:
  help                    - Show this help message
  datasets                - List loaded datasets
  load <name> [filepath]  - Load a dataset (CSV or JSON)
  analyze <name>          - Analyze a loaded dataset
  ml <name> <target> [alg]- Run ML experiment (algorithms: naive_bayes)
  stats                   - Show system statistics
  quit/exit/bye           - Exit the assistant

💡 Examples:
  load mydata data.csv
  analyze mydata
  ml mydata category naive_bayes
        """
        print(help_text)
    
    def _list_datasets(self):
        """List all loaded datasets"""
        if not self.loaded_datasets:
            print("📂 No datasets loaded")
            return
        
        print("📂 Loaded Datasets:")
        print("-" * 40)
        for name, info in self.loaded_datasets.items():
            size_mb = info['size_info'].get('size_mb', 0)
            records = len(info['data']) if info['data'] else 0
            print(f"  • {name}: {records:,} records ({size_mb:.2f} MB)")
            print(f"    Loaded: {info['loaded_at']}")
            print(f"    File: {info['filepath']}")
            print()
    
    def _show_system_stats(self):
        """Show system and performance statistics"""
        print("💻 System Statistics:")
        print("-" * 40)
        print(f"Loaded datasets: {len(self.loaded_datasets)}")
        print(f"Trained models: {len(self.models)}")
        
        total_records = sum(len(info['data']) for info in self.loaded_datasets.values() if info['data'])
        print(f"Total records in memory: {total_records:,}")
        
        # Memory estimation (rough)
        estimated_mb = total_records * 0.1  # Very rough estimate
        print(f"Estimated memory usage: {estimated_mb:.2f} MB")
        
        print(f"\n{self.name} is ready to help with your data analysis tasks!")
    
    def _get_conversational_response(self, user_input: str) -> str:
        """Generate a conversational response for general queries"""
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return "Hello! I'm DataSage AI, your intelligent data analysis assistant. How can I help you with your data today?"
        
        elif any(word in user_lower for word in ['what', 'who', 'how']):
            if 'data' in user_lower or 'dataset' in user_lower:
                return "I can help you load, analyze, and build models from datasets. Try 'load mydata.csv' to get started!"
            elif 'model' in user_lower or 'ml' in user_lower or 'machine learning' in user_lower:
                return "I support basic machine learning experiments like Naive Bayes classification. Try 'ml dataset target_field' to see it in action!"
            elif 'help' in user_lower:
                return "I'm here to help! Type 'help' to see all available commands."
            else:
                return "That's an interesting question! I specialize in data analysis tasks. Try asking about datasets, analysis, or machine learning."
        
        elif any(word in user_lower for word in ['thanks', 'thank you']):
            return "You're welcome! Is there anything else you'd like to explore with your data?"
        
        else:
            return "I'm designed to help with data analysis tasks. Try commands like 'load', 'analyze', or 'ml' to get started, or type 'help' for a full list of options."

# ==================== MAIN EXECUTION ====================

def main():
    """Main entry point"""
    print("🚀 Initializing DataSage AI Assistant...")
    print("   Loading modules and preparing data science environment...")
    
    # Initialize the AI assistant
    ai = DataSageAI()
    
    # Show startup banner
    print("\n" + "="*60)
    print(f"🎉 {ai.name} v{ai.version} is ready!")
    print("   Advanced Data Analysis & Machine Learning Assistant")
    print("="*60)
    print("💡 Tip: Type 'help' to see available commands")
    print("💡 Try loading the sample dataset: load sample sample_data/sample_data.csv")
    print()
    
    # Start interactive chat
    ai.chat()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Thanks for using DataSage AI.")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        print("Please check your installation and try again.")
        sys.exit(1)