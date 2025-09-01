#!/usr/bin/env python3
"""
ClearVoice API 简单调用示例

读取 input.wav，调用 API，保存为 output.wav
"""

import time
import requests

# 读取音频文件
with open('input.wav', 'rb') as f:
    audio_data = f.read()

# 调用 API
url = "http://0.0.0.0:8000/v1/audio/clearvoice"
print(f"发送请求到: {url}")
print(f"音频数据大小: {len(audio_data)} 字节")

# 记录开始时间
start_time = time.time()

response = requests.post(url, data=audio_data)

# 记录结束时间并计算耗时
end_time = time.time()
request_time = end_time - start_time

print(f"响应状态码: {response.status_code}")
print(f"请求耗时: {request_time:.3f} 秒")

if response.status_code == 200:
    # 直接获取二进制音频数据（新API格式）
    processed_audio = response.content

    # 保存处理后的音频
    with open('output.wav', 'wb') as f:
        f.write(processed_audio)

    print("✅ 处理完成！")
    print(f"输入文件大小: {len(audio_data)} 字节")
    print(f"输出文件大小: {len(processed_audio)} 字节")
else:
    print(f"❌ API调用失败: {response.status_code}")
    print(response.text)
    print(f"请求耗时: {request_time:.3f} 秒")
