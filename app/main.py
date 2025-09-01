from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用实例
app = FastAPI(
    title="ClearVoice API",
    description="ClearVoice后端API服务",
    version="1.0.0",
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 健康检查路由
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"  # 实际项目中应该返回当前时间戳
    }

@app.post("/v1/audio/clearvocie")
async def process_audio(request: Request):
    """处理音频数据，直接返回音频数据"""
    # 获取原始二进制数据
    audio_data = await request.body()

    # 不做任何处理，直接返回音频数据
    return {
        "audio_data": audio_data
    }
