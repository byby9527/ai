### 此程式是參考老師的範例:https://github.com/ccc112b/py2cs/tree/master/03-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/02-%E5%84%AA%E5%8C%96%E7%AE%97%E6%B3%95/01-%E5%82%B3%E7%B5%B1%E5%84%AA%E5%8C%96%E6%96%B9%E6%B3%95/01-%E5%84%AA%E5%8C%96/01-%E7%88%AC%E5%B1%B1%E6%BC%94%E7%AE%97%E6%B3%95/04-%E7%88%AC%E5%B1%B1%E7%89%A9%E4%BB%B6%E5%B0%8E%E5%90%91%E6%A1%86%E6%9E%B6
### 和使用ChatGPT來輔助，最後自己有理解過這個程式並自行標註註解
import random

def generate_initial_schedule(courses, slots):
    schedule = {}  ### 初始化空的課程表
    for course in courses:
        if course['hours'] > 0:  ### 確保課程的上課時數大於0
            time_slots = random.sample(slots, course['hours'])  ### 隨機選擇課程所需的時段
            schedule[(course['teacher'], course['name'])] = time_slots  ###將課程分配的時段加入課程表
    return schedule  ### 返回初始課程表

def get_neighbors(schedule, slots):
    neighbors = []  ### 初始化空的鄰居課程表列表
    for key in schedule.keys():
        for _ in range(3):  ### 產生3個鄰居課程表
            new_schedule = schedule.copy()  ### 複製當前課程表
            new_slots = random.sample(slots, len(schedule[key]))  ### 為當前課程重新隨機選擇時段
            new_schedule[key] = new_slots  ### 更新課程表
            neighbors.append(new_schedule)  ###將新的課程表加入鄰居列表
    return neighbors  ### 返回鄰居課程表列表

def height(schedule, teachers):
    conflicts = 0  ### 初始化衝突計數
    teacher_slots = {teacher: set() for teacher in teachers} ### 每位老師的上課時段集合
    all_slots = set()  ### 所有課程的時段集合
    
    for (teacher, _), time_slots in schedule.items():
        for slot in time_slots:
            if slot in teacher_slots[teacher]:
                conflicts += 1  ### 如果老師同一時間段有多節課，增加衝突計數
            else:
                teacher_slots[teacher].add(slot)  ### 將時段加入老師的上課時段集合
                
            if slot in all_slots:
                conflicts += 1  ### 如果同一時間段有多節課，增加衝突計數
            else:
                all_slots.add(slot)  ### 將時段加入所有課程的時段集合
    
    return -conflicts  ### 返回衝突數的負值，目標是最小化衝突

def hill_climbing(x, height, neighbor, max_fail=10000):
    fail = 0 ### 初始化失敗計數
    while True:
        nx = random.choice(neighbor(x))  ### 隨機選擇一個鄰居課程表
        if height(nx) > height(x):  ### 如果新課程表的衝突更少，表示負的衝突數
            x = nx  ### 更新當前課程表
            fail = 0  ### 重置失敗計數
        else:
            fail += 1  ### 增加失敗計數
            if fail > max_fail:  ### 如果失敗次數超過最大值
                return x  ### 返回當前最佳課程表

### 初始課程表
courses = [
    {'teacher': ' ', 'name':' ', 'hours': -1},
    {'teacher': '甲', 'name':'機率', 'hours': 2},
    {'teacher': '甲', 'name':'線代', 'hours': 3},
    {'teacher': '甲', 'name':'離散', 'hours': 3},
    {'teacher': '乙', 'name':'視窗', 'hours': 3},
    {'teacher': '乙', 'name':'科學', 'hours': 3},
    {'teacher': '乙', 'name':'系統', 'hours': 3},
    {'teacher': '乙', 'name':'計概', 'hours': 3},
    {'teacher': '丙', 'name':'軟工', 'hours': 3},
    {'teacher': '丙', 'name':'行動', 'hours': 3},
    {'teacher': '丙', 'name':'網路', 'hours': 3},
    {'teacher': '丁', 'name':'媒體', 'hours': 3},
    {'teacher': '丁', 'name':'工數', 'hours': 3},
    {'teacher': '丁', 'name':'動畫', 'hours': 3},
    {'teacher': '丁', 'name':'電子', 'hours': 4},
    {'teacher': '丁', 'name':'嵌入', 'hours': 3},
    {'teacher': '戊', 'name':'網站', 'hours': 3},
    {'teacher': '戊', 'name':'網頁', 'hours': 3},
    {'teacher': '戊', 'name':'演算', 'hours': 3},
    {'teacher': '戊', 'name':'結構', 'hours': 3},
    {'teacher': '戊', 'name':'智慧', 'hours': 3}
]

teachers = ['甲', '乙', '丙', '丁', '戊']  

rooms = ['A', 'B']  

slots = [
    'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17',
    'A21', 'A22', 'A23', 'A24', 'A25', 'A26', 'A27',
    'A31', 'A32', 'A33', 'A34', 'A35', 'A36', 'A37',
    'A41', 'A42', 'A43', 'A44', 'A45', 'A46', 'A47',
    'A51', 'A52', 'A53', 'A54', 'A55', 'A56', 'A57',
    'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17',
    'B21', 'B22', 'B23', 'B24', 'B25', 'B26', 'B27',
    'B31', 'B32', 'B33', 'B34', 'B35', 'B36', 'B37',
    'B41', 'B42', 'B43', 'B44', 'B45', 'B46', 'B47',
    'B51', 'B52', 'B53', 'B54', 'B55', 'B56', 'B57',
]

### 生成初始时间表
initial_schedule = generate_initial_schedule(courses, slots)

### 使用爬山演算法寻找最优时间表
optimal_schedule = hill_climbing(initial_schedule, lambda x: height(x, teachers), lambda x: get_neighbors(x, slots))


for (teacher, course), time_slots in optimal_schedule.items():
    print(f"Teacher: {teacher}, Course: {course}, Time Slots: {time_slots}")
