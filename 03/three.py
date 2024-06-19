from scipy.optimize import linprog

# 目標函數係數
c = [-3, -2, -5]  # 因為 linprog 是求最小化，所以我們把最大化變成最小化(-3x - 2y - 5z)

# 不等式的左邊的係數矩陣
A = [
    [1, 1, 0],  # x + y <= 10
    [2, 0, 1],  # 2x + z <= 9
    [0, 1, 2]   # y + 2z <= 11
]

# 不等式的右邊
b = [10, 9, 11]

# 變數的下限
x_bounds = (0, None)
y_bounds = (0, None)
z_bounds = (0, None)

# 使用 linprog 進行求解
result = linprog(c, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds, z_bounds], method='highs')

# 輸出結果
if result.success:
    print("最佳解是:")
    print(f"x = {result.x[0]:.2f}")
    print(f"y = {result.x[1]:.2f}")
    print(f"z = {result.x[2]:.2f}")
    print(f"最大值 = {-result.fun:.2f}")  # 記得將最小化的結果變回最大化
else:
    print("沒有找到合適的解")
