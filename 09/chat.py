import os
import sys
from groq import Groq

def get_groq_answer(question):
    client = Groq(api_key=os.environ.get("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"))

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

def main():
    if len(sys.argv) < 2:
        print("請輸入問題")
        return

    question = " ".join(sys.argv[1:])
    print("問題：", question)

    answer = get_groq_answer(question)
    print("回答：", answer)

if __name__ == "__main__":
    main()
