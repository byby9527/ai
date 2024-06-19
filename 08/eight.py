# 參考老師的程式碼:https://github.com/ccc112b/py2cs/blob/master/03-%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7/06-%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92/01-%E5%BC%B7%E5%8C%96%E5%AD%B8%E7%BF%92/01-gym/04-run/cartpole_human_run.py
import gymnasium as gym


env = gym.make("CartPole-v1", render_mode = "human")
observation, info = env.reset(seed = 42)
steps = 0

for _ in range(1000):
    env.render()

   ### 根據觀測值決定動作：當槓桿角度 observation[2] 和角速度 observation[3] 都小於 0 時，執行動作 0；否則執行動作 1
    if observation[2] < 0 and observation[3] < 0:
        action = 0
    elif observation[2] > 0 and observation[3] > 0:
        action = 1

    ###透過執行動作獲得下一步的觀測值 observation、獎勵 reward、終止狀態 terminated、截斷狀態 truncated 和額外資訊 info
    observation, reward, terminated, truncated, info = env.step(action)

    steps += 1  ###步數計數器加一
    print("step", steps)  ###輸出當前步數

    ### 如果遊戲結束或被截斷，則重置環境並重置步數計數器
    if terminated or truncated:
        observation, info = env.reset()
        steps = 0
        print()

env.close()  