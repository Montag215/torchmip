import cvxpy as cp
import numpy as np
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: torchmip.py <arg1> <arg2>")
        return
    
    # Define the grid size
    N, M = int(sys.argv[1]), int(sys.argv[2])  # Example grid size, can be modified

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
    problem.solve(solver=cp.GLPK_MI)

    # Display results
    print("Torch placement:")
    solution = torch.value.round()
    #print(solution)

    for i in range(N):
        for j in range(M):
            if solution[i,j]:
                print('X',end='')
            else:
                print('.',end='')
        print()

if __name__ == "__main__":
    main()