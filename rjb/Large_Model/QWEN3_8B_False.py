# 千问3-8B 无微整API接口 ===>原生版
# API调用接口主函数

import requests
import json
def QWEN3_8B_False_API(stream=False, max_tokens=512, enable_thinking=True, thinking_budget=4096, 
                   min_p=0.05, temperature=0.7, top_p=0.7, top_k=50, frequency_penalty=0.5, n=1, stop=[],
                   API_key=None, role="user", content="hello,Who are you?"):
    '''
    默认参数配置------->defult：
        stream: 是否流式输出，默认为False
        max_tokens: 最大输出长度，默认为512
        enable_thinking: 是否启用思考，默认为True
        thinking_budget: 思考预算，默认为4096
        min_p: 最小输出概率，默认为0.05
        temperature: 温度，默认为0.7
        top_p: 采样温度，默认为0.7
        top_k: 采样温度，默认为50
        frequency_penalty: 频率惩罚，默认为0.5
        n: 生成数量，默认为1
        stop: 停止标志，默认为[]

        API_key: API密钥，默认为None
        role: 角色，默认为"user"
        content: 输入内容，默认为"hello,Who are you?"
    return: 返回请求结果
    '''

    url = "https://api.siliconflow.cn/v1/chat/completions"

    payload = {
        "model": "Qwen/Qwen3-8B",
        "stream": stream,
        "max_tokens": max_tokens,
        "enable_thinking": enable_thinking,
        "thinking_budget": thinking_budget,
        "min_p": min_p,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "frequency_penalty": frequency_penalty,
        "n": n,
        "stop": stop
    }

    headers = {
        "Authorization": API_key,
        "Content-Type": "application/json"
    }

    payload["messages"] = [
        {
            "role": role,
            "content": content
        }
    ]

    response = requests.request("POST", url, json=payload, headers=headers)
    # 返回所有请求
    return response

if __name__ == "__main__":

    question = input("请输入问题：")

    qwen = QWEN3_8B_False_API(API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                          content=question)
    
    #======>切片《========
    # 将 JSON 字符串解析为字典
    data = json.loads(qwen.txt)

    # 提取 content 部分
    content = data['choices'][0]['message']['content']

    content = content.replace('\n', '')

    # 打印 content
    print(content)

