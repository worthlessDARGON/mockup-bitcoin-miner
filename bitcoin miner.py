#!/usr/bin/env python3
"""
Live Bitcoin Miner Mock
Generates a continuous fake Bitcoin mining log to a file and stdout.
Logs are written to `miner.log` in real-time.
Press Ctrl+C to stop.
"""
import hashlib
import random
import time
import signal
import sys
import json
from datetime import datetime


def sha256d(data: bytes) -> str:
    return hashlib.sha256(hashlib.sha256(data).digest()).hexdigest()


def format_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def main():
    pool = "mockpool.example:3333"
    worker = "miner01"
    log_file = "miner.log"
    
    stop_requested = False
    
    def signal_handler(signum, frame):
        nonlocal stop_requested
        stop_requested = True
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    start_time = time.time()
    with open(log_file, "w", encoding="utf-8") as f:
        # Initial setup logs
        startup_logs = [
            f"[{format_ts(start_time)}] Miner: starting (worker={worker})",
            f"[{format_ts(start_time)}] Stratum: connecting to {pool}...",
            f"[{format_ts(start_time + 0.1)}] Stratum: connected, difficulty=2.00",
            f"[{format_ts(start_time + 0.2)}] Job: new block template received",
        ]
        
        for log_line in startup_logs:
            print(log_line)
            f.write(log_line + "\n")
        
        # GPU hashrate logs
        gpu_hrs = [random.uniform(50, 120) for _ in range(4)]
        for i, hr in enumerate(gpu_hrs):
            log_line = f"[{format_ts(start_time + 0.3 + i * 0.05)}] GPU{i}: {hr:.2f} MH/s"
            print(log_line)
            f.write(log_line + "\n")
        
        f.flush()
        
        # Main mining loop
        accepted = 0
        rejected = 0
        attempt = 0
        
        try:
            while not stop_requested:
                ts = time.time()
                nonce = random.getrandbits(32)
                payload = f"{pool}|{worker}|{nonce}|{attempt}".encode()
                h = sha256d(payload)
                
                # 5% accept rate + bonus for lucky hashes
                is_accepted = random.random() < 0.05 or h.startswith("00")
                
                if is_accepted:
                    accepted += 1
                    log_line = f"[{format_ts(ts)}] ✓ Share Accepted: nonce=0x{nonce:08x} hash={h[:32]}... diff=2.000"
                else:
                    rejected += 1
                    reason = random.choice(["low-diff", "stale", "invalid"])
                    log_line = f"[{format_ts(ts)}] ✗ Share Rejected ({reason}): nonce=0x{nonce:08x} hash={h[:32]}..."
                
                print(log_line)
                f.write(log_line + "\n")
                
                # Status report every 10 attempts
                if (attempt + 1) % 10 == 0:
                    total_hr = sum(random.uniform(50, 120) for _ in range(4))
                    status_line = f"[{format_ts(ts)}] Status: {total_hr:.2f} MH/s | Accepted: {accepted} | Rejected: {rejected}"
                    print(status_line)
                    f.write(status_line + "\n")
                
                f.flush()
                time.sleep(0.5)
                attempt += 1
        
        except KeyboardInterrupt:
            pass
        
        # Final stop message
        end_time = time.time()
        runtime = end_time - start_time
        final_line = f"[{format_ts(end_time)}] Miner: stopping (runtime: {runtime:.1f}s, accepted: {accepted}, rejected: {rejected})"
        print(final_line)
        f.write(final_line + "\n")
        f.flush()


if __name__ == "__main__":
    main()
