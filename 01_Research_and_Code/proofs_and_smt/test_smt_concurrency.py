import z3
import time
import concurrent.futures
import math

def evaluate_token_constraint(thread_id, token_id, has_cui, is_encrypted, is_verified):
    start_time = time.perf_counter()
    
    # Thread-isolated z3 context to prevent C++ native memory access violations
    ctx = z3.Context()
    solver = z3.Solver(ctx=ctx)
    
    CUI = z3.Bool('HasCUI', ctx=ctx)
    Encrypted = z3.Bool('IsEncryptedEnclave', ctx=ctx)
    Verified = z3.Bool('IsVerifiedSession', ctx=ctx)
    
    policy = z3.Implies(CUI, z3.And(Encrypted, Verified))
    solver.add(policy)
    solver.add(CUI == has_cui)
    solver.add(Encrypted == is_encrypted)
    solver.add(Verified == is_verified)
    
    result = solver.check()
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    
    if result == z3.sat:
        logit_mod = 0.0
    else:
        logit_mod = float('-inf')
        
    return {
        'thread_id': thread_id,
        'sat_status': str(result),
        'logit_mod': logit_mod,
        'latency_ms': elapsed_ms
    }

def run_test(num_threads=100):
    print(f"[+] Running SMT Concurrency Harness with {num_threads} parallel isolated threads...")
    futures = []
    start = time.perf_counter()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            f = executor.submit(evaluate_token_constraint, i, 1000 + i, (i % 2 == 0), True, (i % 4 != 0))
            futures.append(f)
            
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
    total_ms = (time.perf_counter() - start) * 1000.0
    latencies = [r['latency_ms'] for r in results]
    avg_lat = sum(latencies) / len(latencies)
    violations = sum(1 for r in results if r['logit_mod'] == float('-inf'))
    
    print("\n================ SMT CONCURRENCY RESULTS ================")
    print(f"Threads Executed    : {len(results)}")
    print(f"Violations Blocked  : {violations} (Logit Mod = -inf)")
    print(f"Average Latency     : {avg_lat:.3f} ms")
    print(f"Total Execution Time: {total_ms:.3f} ms")
    print("========================================================\n")

if __name__ == "__main__":
    run_test(100)
