import os  
import sys 
from groq import Groq  

def get_groq_answer(question):
    
    client = Groq(api_key=os.environ.get("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"))

    ### 使用客戶端進行聊天完成請求，回傳訊息的完整性為第一個選擇的訊息內容
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user", ### 設置角色為使用者
                "content": question, ### 設置內容為傳入的問題
            }
        ],
        model="llama3-8b-8192",  
    )

    return chat_completion.choices[0].message.content  ### 回傳第一個選擇的訊息內容

def main():
    if len(sys.argv) < 2:
        print("請輸入問題")  ###如果命令列參數少於 2 個，輸出提示請輸入問題
        return

    question = " ".join(sys.argv[1:]) 
    print("問題：", question)  

    answer = get_groq_answer(question)  
    print("回答：", answer)  

if __name__ == "__main__":
    main() 
