from openai import OpenAI
def Deepseek_API(message):
    '''
    封装Deepseek-API接口，并支持将流式内容写入文件
    :param base_url: API链接地址
    :param api_key: API秘钥
    :param model: 模型选择
    :param stream: 是否为流式输出
    :param role: 角色
    :param content: 语句
    :param output_file: 输出文件路径（如果为 None，则不写入文件）
    :return:
    '''
    # 构造 client
    client = OpenAI(
        base_url="https://api.deepseek.com",
        api_key="sk-8a16a27c607a4b87b569387714d4442f",
    )

    # 发送请求
    chat_completion = client.chat.completions.create(
        model="deepseek-chat",
        messages=message,
        stream=False,
    )
    result = chat_completion.choices[0].message.content
    
    return result
