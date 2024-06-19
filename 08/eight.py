import gym
env = gym.make("CartPole-v1", render_mode="human")  # 若改用這個，會畫圖
# env = gym.make("CartPole-v1", render_mode="rgb_array")
observation, info = env.reset(seed=42)

# 定義策略函式
def balance_policy(observation):
    # 取得竿子的角度
    angle = observation[2]
    # 如果竿子向左傾斜，就向左推，否則向右推
    action = 0 if angle < 0 else 1
    return action

total_steps = 0  # 紀錄總共的步數
while True:
    env.render()
    action = balance_policy(observation)  # 使用我們的策略
    observation, reward, terminated, truncated, info = env.step(action)
    total_steps += 1  # 紀錄總步數
    if terminated or truncated:  # 如果遊戲結束或被截斷
        observation, info = env.reset()
        print('Episode ended after {} steps'.format(total_steps))
        total_steps = 0  # 重置步數計數
env.close()
