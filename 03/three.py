## 使用ChatGPT來輔助，最後自己有理解過這個程式並自行標註註解
from scipy.optimize import linprog
### 定義目標函數的係數向量 c，這裡是最小化 -3x - 2y - 5z
c = [-3, -2, -5]  

### 系統不等式的係數矩陣 A
A = [
    [1, 1, 0],  # x + y <= 10
    [2, 0, 1],  # 2x + z <= 9
    [0, 1, 2]   # y + 2z <= 11
]

### 系統不等式的右側常數向量 b
b = [10, 9, 11]

### x, y, z 的界限條件，為了防止有負數存在或是解空間可能是無限大的問題，x、y、z必須大於0
x_bounds = (0, None) 
y_bounds = (0, None)  
z_bounds = (0, None) 

### 使用 linprog 函數求解線性規劃問題，method='highs': 指定使用內建的 Highs solver ，A_ub受到linprog 函數的規則限制
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds, z_bounds], method='highs')

###檢查最佳解是否找到
if result.success:
    print("最佳解是:")
    print(f"x = {result.x[0]:.2f}")
    print(f"y = {result.x[1]:.2f}")
    print(f"z = {result.x[2]:.2f}")
### 將 result.fun（最小化目標函數的值）取負號，轉換為最大化目標函數的值，將最大化目標函數的值格式化為兩位小數
    print(f"最大值 = {-result.fun:.2f}")  
else:
    print("沒有找到合適的解")
