import cvxpy as cp
import numpy as np
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: torchmip_tbl.py <arg1>")
        return
    sqr = int(sys.argv[1])
    tbl = np.zeros((sqr,sqr))

    

    for N in np.arange(sqr)+1:
        for M in np.arange(N)+1:

            # Define the grid size

            torch = cp.Variable((N, M), boolean=True)  # 1 if there's a torch, 0 otherwise

            # Define constraints
            constraints = []

            # Ensure every block is lit by at least one torch within L1 distance 6
            for i in range(N):
                for j in range(M):
                    # Create a coverage constraint
                    coverage = []
                    for di in range(-6, 7):
                        for dj in range(-6, 7):
                            if abs(di) + abs(dj) <= 6:
                                ni, nj = i + di, j + dj
                                if 0 <= ni < N and 0 <= nj < M:
                                    coverage.append(torch[ni, nj])
                    constraints.append(cp.sum(coverage) >= 1)  # Every block must be lit

            # Objective: Minimize the number of torches placed
            objective = cp.Minimize(cp.sum(torch))

            # Solve the MIP problem
            problem = cp.Problem(objective, constraints)
            problem.solve()

            # Display results
            #print("Torch placement:")
            solution = torch.value.round()
            #print(solution)
            tbl[N-1,M-1] = np.sum(solution)
            tbl[M-1,N-1] = np.sum(solution)
    for i in range(sqr+1):
        print(i,end='\t')
    print()
    for i in range(sqr):
        print(i+1,end='\t')
        for j in range(sqr):
            print(int(tbl[i,j]),end='\t')
        print()

if __name__ == "__main__":
    main()