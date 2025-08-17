#!/usr/bin/env python3
"""
Data Analyst MCP Server
Provides comprehensive data analysis tools for business intelligence and analytics
"""

import asyncio
import json
import sys
import logging
import os
import tempfile
import csv
import statistics
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import random


class DataAnalystMCPServer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.protocol_version = "2024-11-05"
        self.server_info = {
            "name": "data-analyst-mcp-server",
            "version": "1.0.0"
        }
        
        # Data storage for the session
        self.data_store = {}
        self.temp_dir = tempfile.mkdtemp()
        
        # Available tools
        self.tools = {
            "create_dataset": {
                "name": "create_dataset",
                "description": "Create a sample dataset with specified parameters",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataset_type": {
                            "type": "string",
                            "enum": ["sales", "weather", "students", "stock_prices", "custom"],
                            "description": "Type of dataset to generate"
                        },
                        "size": {
                            "type": "integer",
                            "description": "Number of records to generate",
                            "default": 100
                        },
                        "name": {
                            "type": "string",
                            "description": "Name for the dataset",
                            "default": "dataset"
                        }
                    },
                    "required": ["dataset_type"]
                }
            },
            "analyze_data": {
                "name": "analyze_data",
                "description": "Perform statistical analysis on a dataset",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataset_name": {
                            "type": "string",
                            "description": "Name of the dataset to analyze"
                        },
                        "analysis_type": {
                            "type": "string",
                            "enum": ["summary", "correlation", "trends", "outliers"],
                            "description": "Type of analysis to perform"
                        }
                    },
                    "required": ["dataset_name", "analysis_type"]
                }
            },
            "save_to_file": {
                "name": "save_to_file",
                "description": "Save data to a CSV file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataset_name": {
                            "type": "string",
                            "description": "Name of the dataset to save"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Filename for the CSV file"
                        }
                    },
                    "required": ["dataset_name", "filename"]
                }
            },
            "load_from_file": {
                "name": "load_from_file",
                "description": "Load data from a CSV file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Filename of the CSV file to load"
                        },
                        "dataset_name": {
                            "type": "string",
                            "description": "Name to assign to the loaded dataset"
                        }
                    },
                    "required": ["filename", "dataset_name"]
                }
            },
            "filter_data": {
                "name": "filter_data",
                "description": "Filter dataset based on conditions",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataset_name": {
                            "type": "string",
                            "description": "Name of the dataset to filter"
                        },
                        "column": {
                            "type": "string",
                            "description": "Column to filter on"
                        },
                        "condition": {
                            "type": "string",
                            "enum": [">", "<", ">=", "<=", "==", "!=", "contains"],
                            "description": "Filter condition"
                        },
                        "value": {
                            "type": "string",
                            "description": "Value to compare against"
                        },
                        "new_dataset_name": {
                            "type": "string",
                            "description": "Name for the filtered dataset"
                        }
                    },
                    "required": ["dataset_name", "column", "condition", "value", "new_dataset_name"]
                }
            },
            "visualize_data": {
                "name": "visualize_data",
                "description": "Create a text-based visualization of data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataset_name": {
                            "type": "string",
                            "description": "Name of the dataset to visualize"
                        },
                        "chart_type": {
                            "type": "string",
                            "enum": ["histogram", "bar_chart", "line_chart", "scatter"],
                            "description": "Type of chart to create"
                        },
                        "x_column": {
                            "type": "string",
                            "description": "Column for x-axis (if applicable)"
                        },
                        "y_column": {
                            "type": "string",
                            "description": "Column for y-axis (if applicable)"
                        }
                    },
                    "required": ["dataset_name", "chart_type"]
                }
            },
            "list_datasets": {
                "name": "list_datasets",
                "description": "List all available datasets and their information",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            "predict_trend": {
                "name": "predict_trend",
                "description": "Make simple predictions based on data trends",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "dataset_name": {
                            "type": "string",
                            "description": "Name of the dataset"
                        },
                        "target_column": {
                            "type": "string",
                            "description": "Column to predict"
                        },
                        "periods": {
                            "type": "integer",
                            "description": "Number of periods to predict",
                            "default": 5
                        }
                    },
                    "required": ["dataset_name", "target_column"]
                }
            }
        }
    
    def _generate_sales_data(self, size: int) -> List[Dict]:
        """Generate sample sales data"""
        products = ["Widget A", "Widget B", "Gadget X", "Gadget Y", "Tool Z"]
        regions = ["North", "South", "East", "West", "Central"]
        
        data = []
        base_date = datetime.now() - timedelta(days=size)
        
        for i in range(size):
            record = {
                "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "product": random.choice(products),
                "region": random.choice(regions),
                "sales_amount": round(random.uniform(100, 5000), 2),
                "quantity": random.randint(1, 50),
                "customer_rating": round(random.uniform(1, 5), 1)
            }
            data.append(record)
        
        return data
    
    def _generate_weather_data(self, size: int) -> List[Dict]:
        """Generate sample weather data"""
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        
        data = []
        base_date = datetime.now() - timedelta(days=size)
        
        for i in range(size):
            city = random.choice(cities)
            # Simulate seasonal variation
            base_temp = 60 + 20 * (1 + 0.5 * (i % 365) / 365)
            
            record = {
                "date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
                "city": city,
                "temperature": round(base_temp + random.uniform(-15, 15), 1),
                "humidity": random.randint(30, 90),
                "precipitation": round(random.uniform(0, 2), 2),
                "wind_speed": round(random.uniform(0, 25), 1)
            }
            data.append(record)
        
        return data
    
    def _generate_student_data(self, size: int) -> List[Dict]:
        """Generate sample student data"""
        subjects = ["Math", "Science", "English", "History", "Art"]
        grades = ["A", "B", "C", "D", "F"]
        
        data = []
        for i in range(size):
            record = {
                "student_id": f"STU{i+1:03d}",
                "subject": random.choice(subjects),
                "score": random.randint(60, 100),
                "grade": random.choice(grades),
                "study_hours": random.randint(1, 10),
                "attendance": round(random.uniform(0.7, 1.0), 2)
            }
            data.append(record)
        
        return data
    
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute the specified tool with given arguments"""
        
        if tool_name == "create_dataset":
            dataset_type = arguments.get("dataset_type")
            size = arguments.get("size", 100)
            name = arguments.get("name", "dataset")
            
            if dataset_type == "sales":
                data = self._generate_sales_data(size)
            elif dataset_type == "weather":
                data = self._generate_weather_data(size)
            elif dataset_type == "students":
                data = self._generate_student_data(size)
            else:
                return f"Unsupported dataset type: {dataset_type}"
            
            self.data_store[name] = data
            columns = list(data[0].keys()) if data else []
            
            return f"Created dataset '{name}' with {len(data)} records and columns: {columns}"
        
        elif tool_name == "analyze_data":
            dataset_name = arguments.get("dataset_name")
            analysis_type = arguments.get("analysis_type")
            
            if dataset_name not in self.data_store:
                return f"Dataset '{dataset_name}' not found"
            
            data = self.data_store[dataset_name]
            if not data:
                return "Dataset is empty"
            
            if analysis_type == "summary":
                return self._analyze_summary(data)
            elif analysis_type == "correlation":
                return self._analyze_correlation(data)
            elif analysis_type == "trends":
                return self._analyze_trends(data)
            elif analysis_type == "outliers":
                return self._analyze_outliers(data)
        
        elif tool_name == "save_to_file":
            dataset_name = arguments.get("dataset_name")
            filename = arguments.get("filename")
            
            if dataset_name not in self.data_store:
                return f"Dataset '{dataset_name}' not found"
            
            filepath = os.path.join(self.temp_dir, filename)
            data = self.data_store[dataset_name]
            
            if data:
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
                
                return f"Saved dataset '{dataset_name}' to {filepath}"
            else:
                return "Dataset is empty"
        
        elif tool_name == "list_datasets":
            if not self.data_store:
                return "No datasets available"
            
            result = "Available datasets:\n"
            for name, data in self.data_store.items():
                columns = list(data[0].keys()) if data else []
                result += f"- {name}: {len(data)} records, columns: {columns}\n"
            
            return result.strip()
        
        elif tool_name == "filter_data":
            dataset_name = arguments.get("dataset_name")
            column = arguments.get("column")
            condition = arguments.get("condition")
            value = arguments.get("value")
            new_dataset_name = arguments.get("new_dataset_name")
            
            if dataset_name not in self.data_store:
                return f"Dataset '{dataset_name}' not found"
            
            data = self.data_store[dataset_name]
            filtered_data = []
            
            for record in data:
                if column not in record:
                    continue
                
                record_value = record[column]
                try:
                    # Try to convert to number for numeric comparisons
                    if condition in [">", "<", ">=", "<=", "==", "!="]:
                        record_value = float(record_value)
                        compare_value = float(value)
                    else:
                        compare_value = value
                    
                    if condition == ">" and record_value > compare_value:
                        filtered_data.append(record)
                    elif condition == "<" and record_value < compare_value:
                        filtered_data.append(record)
                    elif condition == ">=" and record_value >= compare_value:
                        filtered_data.append(record)
                    elif condition == "<=" and record_value <= compare_value:
                        filtered_data.append(record)
                    elif condition == "==" and record_value == compare_value:
                        filtered_data.append(record)
                    elif condition == "!=" and record_value != compare_value:
                        filtered_data.append(record)
                    elif condition == "contains" and str(compare_value) in str(record_value):
                        filtered_data.append(record)
                
                except (ValueError, TypeError):
                    # Handle string comparisons
                    if condition == "contains" and str(value) in str(record_value):
                        filtered_data.append(record)
            
            self.data_store[new_dataset_name] = filtered_data
            return f"Created filtered dataset '{new_dataset_name}' with {len(filtered_data)} records"
        
        elif tool_name == "visualize_data":
            dataset_name = arguments.get("dataset_name")
            chart_type = arguments.get("chart_type")
            
            if dataset_name not in self.data_store:
                return f"Dataset '{dataset_name}' not found"
            
            data = self.data_store[dataset_name]
            if chart_type == "histogram":
                return self._create_histogram(data, arguments.get("x_column"))
            else:
                return f"Chart type '{chart_type}' not fully implemented yet"
        
        elif tool_name == "predict_trend":
            dataset_name = arguments.get("dataset_name")
            target_column = arguments.get("target_column")
            periods = arguments.get("periods", 5)
            
            if dataset_name not in self.data_store:
                return f"Dataset '{dataset_name}' not found"
            
            data = self.data_store[dataset_name]
            return self._predict_trend(data, target_column, periods)
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def _analyze_summary(self, data: List[Dict]) -> str:
        """Analyze summary statistics"""
        if not data:
            return "No data to analyze"
        
        result = f"Dataset Summary:\n- Total records: {len(data)}\n"
        
        # Analyze numeric columns
        numeric_columns = []
        for column in data[0].keys():
            try:
                values = [float(record[column]) for record in data if record[column] is not None]
                if values:
                    numeric_columns.append(column)
                    result += f"\n{column}:\n"
                    result += f"  - Count: {len(values)}\n"
                    result += f"  - Mean: {statistics.mean(values):.2f}\n"
                    result += f"  - Median: {statistics.median(values):.2f}\n"
                    result += f"  - Min: {min(values):.2f}\n"
                    result += f"  - Max: {max(values):.2f}\n"
                    if len(values) > 1:
                        result += f"  - Std Dev: {statistics.stdev(values):.2f}\n"
            except (ValueError, TypeError):
                continue
        
        return result
    
    def _analyze_correlation(self, data: List[Dict]) -> str:
        """Analyze correlations between numeric columns"""
        numeric_data = {}
        
        for column in data[0].keys():
            try:
                values = [float(record[column]) for record in data if record[column] is not None]
                if values and len(values) > 1:
                    numeric_data[column] = values
            except (ValueError, TypeError):
                continue
        
        if len(numeric_data) < 2:
            return "Need at least 2 numeric columns for correlation analysis"
        
        result = "Correlation Analysis:\n"
        columns = list(numeric_data.keys())
        
        for i, col1 in enumerate(columns):
            for col2 in columns[i+1:]:
                try:
                    corr = statistics.correlation(numeric_data[col1], numeric_data[col2])
                    result += f"- {col1} vs {col2}: {corr:.3f}\n"
                except:
                    result += f"- {col1} vs {col2}: Unable to calculate\n"
        
        return result
    
    def _analyze_trends(self, data: List[Dict]) -> str:
        """Analyze trends in data"""
        result = "Trend Analysis:\n"
        
        # Look for date column and numeric columns
        date_column = None
        for column in data[0].keys():
            if 'date' in column.lower():
                date_column = column
                break
        
        if not date_column:
            return "No date column found for trend analysis"
        
        # Sort by date
        try:
            sorted_data = sorted(data, key=lambda x: x[date_column])
            
            for column in data[0].keys():
                if column == date_column:
                    continue
                
                try:
                    values = [float(record[column]) for record in sorted_data if record[column] is not None]
                    if len(values) > 5:
                        # Simple trend calculation
                        first_half = values[:len(values)//2]
                        second_half = values[len(values)//2:]
                        
                        avg_first = statistics.mean(first_half)
                        avg_second = statistics.mean(second_half)
                        
                        if avg_second > avg_first * 1.05:
                            trend = "Increasing"
                        elif avg_second < avg_first * 0.95:
                            trend = "Decreasing"
                        else:
                            trend = "Stable"
                        
                        result += f"- {column}: {trend} (avg: {avg_first:.2f} → {avg_second:.2f})\n"
                except (ValueError, TypeError):
                    continue
            
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"
        
        return result
    
    def _analyze_outliers(self, data: List[Dict]) -> str:
        """Find outliers in numeric data"""
        result = "Outlier Analysis:\n"
        
        for column in data[0].keys():
            try:
                values = [float(record[column]) for record in data if record[column] is not None]
                if len(values) > 3:
                    mean_val = statistics.mean(values)
                    stdev_val = statistics.stdev(values)
                    
                    outliers = []
                    for i, val in enumerate(values):
                        if abs(val - mean_val) > 2 * stdev_val:
                            outliers.append((i, val))
                    
                    if outliers:
                        result += f"- {column}: Found {len(outliers)} outliers\n"
                        for idx, val in outliers[:5]:  # Show first 5
                            result += f"  Record {idx}: {val:.2f}\n"
                    else:
                        result += f"- {column}: No outliers found\n"
            except (ValueError, TypeError, statistics.StatisticsError):
                continue
        
        return result
    
    def _create_histogram(self, data: List[Dict], column: str) -> str:
        """Create a simple text histogram"""
        if not column or column not in data[0]:
            return f"Column '{column}' not found"
        
        try:
            values = [float(record[column]) for record in data if record[column] is not None]
            if not values:
                return "No numeric data to visualize"
            
            # Create 10 bins
            min_val, max_val = min(values), max(values)
            bin_width = (max_val - min_val) / 10
            bins = [0] * 10
            
            for val in values:
                bin_idx = min(int((val - min_val) / bin_width), 9)
                bins[bin_idx] += 1
            
            result = f"Histogram for {column}:\n"
            max_count = max(bins) if max(bins) > 0 else 1
            
            for i, count in enumerate(bins):
                bin_start = min_val + i * bin_width
                bin_end = bin_start + bin_width
                bar = "█" * int(count * 20 / max_count)
                result += f"{bin_start:6.1f}-{bin_end:6.1f} |{bar:<20} {count}\n"
            
            return result
            
        except (ValueError, TypeError):
            return f"Column '{column}' contains non-numeric data"
    
    def _predict_trend(self, data: List[Dict], target_column: str, periods: int) -> str:
        """Simple trend prediction"""
        try:
            values = [float(record[target_column]) for record in data if record[target_column] is not None]
            if len(values) < 3:
                return "Need at least 3 data points for prediction"
            
            # Simple linear trend
            recent_values = values[-min(10, len(values)):]
            if len(recent_values) > 1:
                slope = (recent_values[-1] - recent_values[0]) / (len(recent_values) - 1)
                last_value = recent_values[-1]
                
                result = f"Trend Prediction for {target_column}:\n"
                result += f"Current value: {last_value:.2f}\n"
                result += f"Estimated trend: {slope:.2f} per period\n\n"
                result += "Predictions:\n"
                
                for i in range(1, periods + 1):
                    predicted = last_value + slope * i
                    result += f"Period +{i}: {predicted:.2f}\n"
                
                return result
            else:
                return "Insufficient data for trend calculation"
                
        except (ValueError, TypeError):
            return f"Column '{target_column}' contains non-numeric data"
    
    async def handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {
                "protocolVersion": self.protocol_version,
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": self.server_info
            }
        }
    
    async def handle_tools_list(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools list request"""
        tools_list = list(self.tools.values())
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {
                "tools": tools_list
            }
        }
    
    async def handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call request"""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
        
        try:
            result = await self._execute_tool(tool_name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32603,
                    "message": f"Tool execution failed: {str(e)}"
                }
            }
    
    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        
        if method == "initialize":
            return await self.handle_initialize(request)
        elif method == "tools/list":
            return await self.handle_tools_list(request)
        elif method == "tools/call":
            return await self.handle_tools_call(request)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    async def run(self):
        """Main server loop - reads from stdin and writes to stdout"""
        self.logger.info("Data Analyst MCP Server starting...")
        
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    continue
                
                response = await self.handle_request(request)
                
                if response:
                    print(json.dumps(response), flush=True)
                
            except EOFError:
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
        
        self.logger.info("Data Analyst MCP Server shutting down...")


async def main():
    """Main entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)]
    )
    
    server = DataAnalystMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())