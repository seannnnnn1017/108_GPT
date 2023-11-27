import openai
from dotenv import dotenv_values
import time

with open("多元表現綜整心得.txt", "r", encoding = "utf-8") as file:
    AI_quesntions = [line.strip() for line in file.readlines()]
    file.close()

def generate_text(department="人工智慧系",support="多元表現綜整心得"):
    config = dotenv_values("C:/Users/user/Desktop/env.txt")
    openai.api_key = config["API_KEY"]

    messages = [{"role": "system", "content": "zh-Tw 你要幫準備申請大學的高中生撰寫學習歷程 字數大約1000字"}]

    for i in range(len(AI_quesntions)):
        ans = input(f"\n{AI_quesntions[i]}\nAns{i+1}: ") #iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii
        if ans:
            messages.append({"role": "assistant", "content": AI_quesntions[i]},)
            messages.append({"role": "user", "content": ans})
        elif ans == "0":
            return None

    narration = f'''
        目標學系: {department}
        =====================================
        根據以上問答及提供的學系，幫我完成{support}
    '''
    messages.append({"role": "user", "content": narration})


    print("===========================================================================================")
    start_time = time.time()
    response = openai.ChatCompletion.create(
        model = "gpt-4-1106-preview",
        messages = messages,
        max_tokens = 1000,
    )
    end_time = time.time() 
    print(f"程式執行時間: {end_time - start_time} 秒")
    
    return response['choices'][0]['message']['content']


print(generate_text())
