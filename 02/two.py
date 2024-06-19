### 此程式是參考老師的範例:https://github.com/ccc112b/py2cs/blob/master/03-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/02-%E5%84%AA%E5%8C%96%E7%AE%97%E6%B3%95/01-%E5%82%B3%E7%B5%B1%E5%84%AA%E5%8C%96%E6%96%B9%E6%B3%95/01-%E5%84%AA%E5%8C%96/01-%E7%88%AC%E5%B1%B1%E6%BC%94%E7%AE%97%E6%B3%95/03-%E9%80%9A%E7%94%A8%E7%9A%84%E7%88%AC%E5%B1%B1%E6%A1%86%E6%9E%B6/tsp.py
### 還有使用ChatGPT來輔助，最後自己有理解過這個程式並自行標註註解
import random  

citys = [  # 定義城市的座標
    (0, 3), (0, 0),
    (0, 2), (0, 1),
    (1, 0), (1, 3),
    (2, 0), (2, 3),
    (3, 0), (3, 3),
    (3, 1), (3, 2)
]

def distance(p1, p2):
    """計算兩個城市之間的距離"""
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5

### citys[path[i]] 取得這個城市的座標
### path[(i + 1) % len(citys)]表示下個城市的索引，如果 i+1 大於等於 len(citys)，則取餘數後再作為索引。
def path_length(path):
    """計算一個路徑的總長度"""
    return sum(distance(citys[path[i]], citys[path[(i + 1) % len(citys)]]) for i in range(len(path))) 

def hill_climbing(citys, b):
    """爬山演算法求解TSP"""
    path = list(range(len(citys)))  ### 初始化一個順序路徑 [0, 1, 2, ..., n-1]
    length = path_length(path)  ### 計算初始路徑的長度
    
    for _ in range(b): ### 重複b次迭代
        index1, index2 = random.sample(range(len(citys)), 2) ### 隨機選取兩個不同的索引
        new_path = path[:]  ### 複製目前的路徑
        
       ### 交換選取的兩個城市的位置
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]
        
        new_length = path_length(new_path)  ### 計算新路徑的長度
        
       ### 如果新路徑比目前的路徑長度更短，則更新最佳路徑和最佳長度
        if new_length < length:
            path, length = new_path, new_length
            
    return path, length  ### 返回最佳路徑和其長度

### 執行爬山演算法找到最佳路徑
best_path, best_length = hill_climbing(citys, b=1000)

### 輸出最佳路徑和其長度
print("Best path:", best_path)
print("Best path length:", best_length)
