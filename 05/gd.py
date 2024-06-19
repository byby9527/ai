import numpy as np
from engine import Value

def gradientDescendent(f, p0, lr=0.01, tol=1e-5, max_iters=10000):
    p = p0.copy()
    for _ in range(max_iters):
        grad = compute_gradient(f, p)
        
        if np.linalg.norm(grad) < tol:
            break
        
        p = update_parameters(p, grad, lr)
    
    return p

def compute_gradient(f, p):
    grad = []
    fp = f(p)
    fp.backward()
    for param in p:
        grad.append(param.grad)
    return np.array(grad)

def update_parameters(p, grad, lr):
    p_updated = [param - lr * g for param, g in zip(p, grad)]
    return p_updated

def f(p):
    x, y, z = p
    return (x-1)**2 + (y-2)**2 + (z-3)**2

if __name__ == "__main__":
    p = [Value(0), Value(0), Value(0)]
    result = gradientDescendent(f, p)
    print(result)
    print(f(result))
