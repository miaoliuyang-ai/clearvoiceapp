# ClearVoice API 使用指南

## 概述

ClearVoice API 提供音频数据处理服务。本文档介绍 `/api/v1/audio` 接口的使用方法。

## API 端点

### POST /api/v1/audio

处理上传的音频数据并直接返回。

#### 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| `audio_data` | file | 是 | 音频文件（支持WAV、MP3、AAC等格式） |

#### 请求格式

- **Content-Type**: `multipart/form-data`
- **Method**: `POST`

#### 请求示例

```bash
# 使用curl上传文件
curl -X POST "http://localhost:8000/api/v1/audio" \
     -F "audio_data=@audio_file.wav"
```

#### Python示例

```python
import requests

# 上传音频文件
def upload_audio(file_path):
    with open(file_path, 'rb') as f:
        files = {'audio_data': f}
        response = requests.post('http://localhost:8000/api/v1/audio', files=files)
        return response.json()

# 使用示例
result = upload_audio('path/to/audio.wav')
print(result)
```

#### 响应格式

```json
{
    "audio_data": "<base64_encoded_audio_data>",
    "content_type": "audio/wav"
}
```

#### 响应字段说明

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `audio_data` | bytes | 处理后的音频数据（二进制） |
| `content_type` | string | 音频文件的MIME类型 |

#### 状态码

- `200`: 成功处理
- `400`: 请求参数错误
- `500`: 服务器内部错误

## 快速开始

### 1. 启动服务器

```bash
cd clearvoice
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 测试API

```bash
# 健康检查
curl http://localhost:8000/health

# 上传音频文件
curl -X POST "http://localhost:8000/api/v1/audio" \
     -F "audio_data=@samples/test.wav"
```

### 3. 查看API文档

访问以下地址查看自动生成的API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 支持的音频格式

- WAV
- MP3
- AAC
- M4A
- 其他常见音频格式

## 错误处理

API会返回适当的HTTP状态码和错误信息：

```json
{
    "detail": "Error description"
}
```

## 性能考虑

- 文件大小限制：取决于服务器配置
- 处理时间：取决于音频文件大小和服务器性能
- 并发请求：支持多个并发上传

## 示例文件

项目中提供了以下示例文件：

- `api_example.py`: Python客户端使用示例
- `curl_examples.sh`: cURL命令使用示例
- `API_USAGE.md`: 本文档

## 与 server_main.py 集成

该API设计用于与 `HuaweiAICall/server_main.py` 中的音频处理逻辑集成，可以：

1. 接收 `server_main.py` 发送的音频数据
2. 进行必要的处理（当前版本直接返回）
3. 将处理结果返回给调用方

## 注意事项

1. 确保上传的文件是有效的音频格式
2. 检查文件大小是否在服务器允许的范围内
3. 处理网络超时和连接错误
4. 在生产环境中配置适当的安全措施
