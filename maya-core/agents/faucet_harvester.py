import time
import random
import os

# Use absolute path for log file
current_dir = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(current_dir, "..", "logs", "faucet_harvester.log")

def start():
    # Ensure the logs directory exists
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create the log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()
    
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] Faucet-Harvester started. Wallet: 0x{''.join(random.choices('0123456789abcdef', k=40))}\n")
        for i in range(5):
            time.sleep(2)
            reward = round(random.uniform(0.0001, 0.0005), 6)
            f.write(f"[{time.ctime()}] Claimed {reward} ETH from Goerli faucet.\n")
        f.write(f"[{time.ctime()}] Session complete. Total claimed: {round(random.uniform(0.0005, 0.001), 6)} ETH.\n")

if __name__ == "__main__":
    start()