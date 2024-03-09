import random

citys = [
    (0,3),(0,0),
    (0,2),(0,1),
    (1,0),(1,3),
    (2,0),(2,3),
    (3,0),(3,3),
    (3,1),(3,2)
]

# 定義距離函數，計算兩個城市之間的距離
def distance(p1, p2):
    return ((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)**0.5

# 計算路徑的長度
def path_length(path):
    return sum(distance(citys[path[i]], citys[path[(i+1)%len(citys)]]) for i in range(len(path)))


def hill_climbing(citys, b):
    path = list(range(len(citys)))  
    length = path_length(path)  
    for _ in range(b):
        index1, index2 = random.sample(range(len(citys)), 2)  
        new_path = path[:]  # 複製目前的路徑
        new_path[index1], new_path[index2] = new_path[index2], new_path[index1]  # 交換城市位置
        new_length = path_length(new_path)  # 計算新路徑的長度
        # 如果新路徑比目前路徑更短，則更新目前路徑
        if new_length < length:
            path, length = new_path, new_length
    return path, length


best_path, best_length = hill_climbing(citys, b=1000)
print("Best path:", best_path)
print("Best path length:", best_length)

