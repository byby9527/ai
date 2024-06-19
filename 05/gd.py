## 和使用ChatGPT來輔助，最後自己有理解過這個程式並自行標註註解
import numpy as np
from engine import Value

def gradientDescendent(f, p0, lr=0.01, tol=1e-5, max_iters=10000):
    ### lr -> 制每次更新參數時的步長大小
    ### tol -> 容差，當梯度的範數小於10^-5，梯度下降算法將停止運行
    p = p0.copy()  # 複製初始參數以避免修改原始值
    for _ in range(max_iters):  ### 進行最大迭代次數的循環
        grad = compute_gradient(f, p)  ### 計算當前位置的梯度
        
        if np.linalg.norm(grad) < tol:  ### 檢查梯度的範數是否小於設定的容差
            break
        
        p = update_parameters(p, grad, lr)  ### 使用梯度更新參數
    
    return p  ### 返回最終收斂的參數值


def compute_gradient(f, p):
    grad = []
    fp = f(p)  ### 計算函數在當前參數位置的值
    fp.backward()  ### 計算函數對各個參數的梯度
    for param in p:
        grad.append(param.grad)  ### 將各個參數的梯度收集起來
    return np.array(grad)  ### 返回梯度向量


def update_parameters(p, grad, lr):
    p_updated = [param - lr * g for param, g in zip(p, grad)] ### 根據梯度和學習率更新參數
    return p_updated  ###返回更新後的參數值


def f(p):
    x, y, z = p
    return (x-1)**2 + (y-2)**2 + (z-3)**2 ###回傳多變量二次函數


if __name__ == "__main__":
    p = [Value(0), Value(0), Value(0)]  ### 初始化三個參數值為0，使用自定義的 Value 類型
    result = gradientDescendent(f, p)  ### 梯度下降法最小化函數 f
    print(result)  ### 輸出最終的參數值
    print(f(result)) ### 輸出最小化函數後的結果值

