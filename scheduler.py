import os
import subprocess
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone
import sys

def run_ingestion():
    print(f"[{datetime.now()}] Starting scheduled data ingestion...")
    try:
        # Run the ingestion script
        result = subprocess.run([sys.executable, "run_ingestion.py"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[{datetime.now()}] Data ingestion completed successfully.")
            print(result.stdout)
        else:
            print(f"[{datetime.now()}] Error in data ingestion:")
            print(result.stderr)
    except Exception as e:
        print(f"[{datetime.now()}] Exception occurred during ingestion: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    ist = timezone('Asia/Kolkata')
    
    # Schedule the job every day at 10:30 AM IST
    scheduler.add_job(run_ingestion, 'cron', hour=10, minute=30, timezone=ist)
    
    print(f"Scheduler started. Job will run daily at 10:30 AM IST.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
