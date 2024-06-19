import random

def generate_initial_schedule(courses, slots):
    schedule = {}
    for course in courses:
        if course['hours'] > 0:
            time_slots = random.sample(slots, course['hours'])
            schedule[(course['teacher'], course['name'])] = time_slots
    return schedule

def get_neighbors(schedule, slots):
    neighbors = []
    for key in schedule.keys():
        for _ in range(3):  
            new_schedule = schedule.copy()
            new_slots = random.sample(slots, len(schedule[key]))
            new_schedule[key] = new_slots
            neighbors.append(new_schedule)
    return neighbors

def height(schedule, teachers):
    conflicts = 0
    teacher_slots = {teacher: set() for teacher in teachers}
    all_slots = set()
    
    for (teacher, _), time_slots in schedule.items():
        for slot in time_slots:
            if slot in teacher_slots[teacher]:
                conflicts += 1
            else:
                teacher_slots[teacher].add(slot)
                
            if slot in all_slots:
                conflicts += 1
            else:
                all_slots.add(slot)
    
    return -conflicts  # We aim to minimize conflicts

def hill_climbing(x, height, neighbor, max_fail=10000):
    fail = 0
    while True:
        nx = random.choice(neighbor(x))
        if height(nx) > height(x):
            x = nx
            fail = 0
        else:
            fail += 1
            if fail > max_fail:
                return x

# 初始课程表
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

# 生成初始时间表
initial_schedule = generate_initial_schedule(courses, slots)

# 使用爬山演算法寻找最优时间表
optimal_schedule = hill_climbing(initial_schedule, lambda x: height(x, teachers), lambda x: get_neighbors(x, slots))

# 打印结果
for (teacher, course), time_slots in optimal_schedule.items():
    print(f"Teacher: {teacher}, Course: {course}, Time Slots: {time_slots}")
