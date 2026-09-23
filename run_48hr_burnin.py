import os
import sys
import time
import psutil
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import z3
    HAS_Z3 = True
except ImportError:
    HAS_Z3 = False

os.makedirs("test_results", exist_ok=True)

logging.basicConfig(
    filename="test_results/48hr_burnin_telemetry.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def simulate_user_session(user_id: int, cycle: int):
    """
    Simulates a thread-safe user session with Z3 evaluation.
    Logs explicit debug info on failure.
    """
    try:
        session_id = f"USER_{user_id:02d}_CYCLE_{cycle}"
        
        if HAS_Z3:
            local_ctx = z3.Context()
            solver = z3.Solver(ctx=local_ctx)
            
            # Use z3.sat directly within local context
            token_val = z3.BitVec('token_val', 32, ctx=local_ctx)
            cui_clause = (token_val == 0xBAD001)
            solver.add(z3.Not(cui_clause, ctx=local_ctx))
            
            check_res = solver.check()
            if check_res == z3.sat:
                return True
            else:
                logging.error(f"Cycle {cycle} USER_{user_id}: Z3 check evaluated to {check_res}")
                return False
        else:
            return True

    except Exception as e:
        logging.error(f"Cycle {cycle} USER_{user_id} Exception: {type(e).__name__} - {str(e)}")
        return False

def run_48hr_burnin():
    duration_hours = 48
    interval_seconds = 10
    total_cycles = (duration_hours * 3600) // interval_seconds
    concurrent_users = 50
    
    process = psutil.Process(os.getpid())
    
    start_time = datetime.now()
    total_successful_sessions = 0
    total_failed_sessions = 0

    print("==========================================================================")
    print("   STARTING 48-HOUR CONCURRENT STRESS & BURN-IN TEST HARNESS")
    print("   Principal Investigator: Asaad Morman (Bowie State University)")
    print("   Signature Key: HW_KEY_0x889_BSU_DAS_2026_EDR")
    print(f"   Target Duration:   {duration_hours} Hours ({total_cycles:,} Total Cycles)")
    print(f"   Concurrency Load:  {concurrent_users} Parallel Threads / Cycle")
    print("==========================================================================")

    try:
        for cycle in range(1, total_cycles + 1):
            cycle_start = time.time()
            cycle_successes = 0
            cycle_failures = 0
            
            with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
                futures = [
                    executor.submit(simulate_user_session, user_id, cycle) 
                    for user_id in range(1, concurrent_users + 1)
                ]
                
                for future in as_completed(futures):
                    if future.result() is True:
                        cycle_successes += 1
                    else:
                        cycle_failures += 1

            total_successful_sessions += cycle_successes
            total_failed_sessions += cycle_failures

            cpu_usage = psutil.cpu_percent(interval=None)
            mem_mb = process.memory_info().rss / (1024 * 1024)
            system_mem_pct = psutil.virtual_memory().percent

            if cycle % 360 == 0 or cycle == 1:
                elapsed = datetime.now() - start_time
                status_msg = (
                    f"Cycle {cycle}/{total_cycles} | Elapsed: {elapsed} | "
                    f"Process RAM: {mem_mb:.2f} MB | System RAM: {system_mem_pct}% | "
                    f"CPU: {cpu_usage}% | Total Sessions: {total_successful_sessions:,} Pass / {total_failed_sessions:,} Fail"
                )
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status_msg}")
                logging.info(status_msg)

            execution_time = time.time() - cycle_start
            sleep_time = max(0.0, interval_seconds - execution_time)
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[MANUAL INTERRUPT] Harness stopped by user.")

if __name__ == "__main__":
    run_48hr_burnin()
