import time
import random
import datetime
import threading
import sys

class ServerLogSimulator:
    def __init__(self, log_file="testlog.log"):
        self.log_file = log_file
        self.running = False
        
        # Sample log messages that might appear in server logs
        self.log_messages = [
            "INFO: User authentication successful for user_id: {user_id}",
            "INFO: Database connection established",
            "INFO: Processing request to /api/users/{user_id}",
            "INFO: Cache hit for key: session_{session_id}",
            "INFO: File uploaded successfully: {filename}",
            "WARNING: High memory usage detected: {memory}%",
            "WARNING: Slow query detected: {query_time}ms",
            "WARNING: Rate limit approaching for IP: {ip}",
            "ERROR: Database connection timeout",
            "ERROR: Failed to process payment for order: {order_id}",
            "ERROR: File not found: {filename}",
            "INFO: Server health check passed",
            "INFO: Backup completed successfully",
            "INFO: New user registration: {email}",
            "INFO: Session expired for user: {user_id}",
            "WARNING: Disk space low: {disk_space}GB remaining",
            "INFO: API request completed in {response_time}ms",
            "ERROR: Network timeout for external service",
            "INFO: Background job completed: data_cleanup",
            "WARNING: SSL certificate expires in {days} days"
        ]
        
        # Sample data for placeholders
        self.sample_data = {
            'user_id': lambda: random.randint(1000, 9999),
            'session_id': lambda: ''.join(random.choices('abcdef0123456789', k=8)),
            'filename': lambda: random.choice(['upload.pdf', 'image.jpg', 'document.docx', 'data.csv']),
            'memory': lambda: random.randint(70, 95),
            'query_time': lambda: random.randint(500, 3000),
            'ip': lambda: f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            'order_id': lambda: f"ORD{random.randint(10000, 99999)}",
            'email': lambda: f"user{random.randint(100,999)}@example.com",
            'disk_space': lambda: random.randint(5, 50),
            'response_time': lambda: random.randint(50, 500),
            'days': lambda: random.randint(7, 30)
        }
    
    def generate_log_entry(self):
        """Generate a single log entry with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        message_template = random.choice(self.log_messages)
        
        # Replace placeholders with sample data
        message = message_template
        for key, generator in self.sample_data.items():
            if f"{{{key}}}" in message:
                message = message.replace(f"{{{key}}}", str(generator()))
        
        return f"[{timestamp}] {message}"
    
    def write_log_entry(self):
        """Write a single log entry to the file"""
        log_entry = self.generate_log_entry()
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')
                f.flush()  # Ensure immediate write to disk
            print(f"Logged: {log_entry}")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def start_logging(self, duration=60):
        """Start the logging process for specified duration (seconds)"""
        self.running = True
        print(f"Starting server log simulation for {duration} seconds...")
        print(f"Writing to: {self.log_file}")
        print("Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        
        try:
            while self.running and (time.time() - start_time) < duration:
                self.write_log_entry()
                
                # Random interval between 0.5 to 5 seconds (irregular timing)
                sleep_time = random.uniform(0.5, 5.0)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print("\nLogging stopped by user")
        
        self.running = False
        print(f"\nLogging completed. Check {self.log_file} for entries.")
    
    def stop_logging(self):
        """Stop the logging process"""
        self.running = False

def main():
    # Create simulator instance
    simulator = ServerLogSimulator("testlog.log")
    
    # You can customize the duration (in seconds)
    duration = 3000  # Run for 30 seconds by default
    
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print("Invalid duration. Using default 30 seconds.")
    
    # Start logging
    simulator.start_logging(duration)

if __name__ == "__main__":
    main()