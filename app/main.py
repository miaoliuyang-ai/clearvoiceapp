"""
ClearVoice API - 语音降噪服务

功能特性:
- 基于 ClearVoice 库的音频降噪处理
- 支持多种音频格式 (Int16 PCM, Float32)
- 自动音频格式检测和转换
- 完整的错误处理和日志记录
- RESTful API 接口

使用方法:
1. 启动服务: python -m uvicorn main:app --host 0.0.0.0 --port 8000
2. 发送 POST 请求到 /v1/audio/clearvoice?session_id=your_session_id，body 为音频数据
3. 如果不提供session_id参数，系统会自动生成一个
4. 返回降噪后的音频数据

API 端点:
- GET /health: 健康检查
- POST /v1/audio/clearvoice?session_id=xxx: 音频降噪处理
"""

import numpy as np
import time
import os
import wave
from scipy.io import wavfile
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from utilities.logging_manager import setup_api_logging

# 尝试导入 ClearVoice
try:
    from clearvoice import ClearVoice
    CLEARVOICE_AVAILABLE = True
except ImportError:
    ClearVoice = None
    CLEARVOICE_AVAILABLE = False

# 设置日志

logger = setup_api_logging()

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

# ClearVoice 语音降噪实例
clearvoice_instance = None


def initialize_clearvoice():
    """初始化 ClearVoice 语音降噪并进行预训练"""
    global clearvoice_instance

    if not CLEARVOICE_AVAILABLE:
        logger.warning("ClearVoice 库未正确导入，跳过初始化")
        return False

    if clearvoice_instance is not None:
        logger.info("ClearVoice 已经初始化")
        return True

    try:
        logger.info("初始化 ClearVoice 语音降噪...")
        # 使用 MossFormerGAN_SE_16K 模型进行语音增强，适合16kHz采样率
        clearvoice_instance = ClearVoice(
            task='speech_enhancement',
            model_names=['MossFormerGAN_SE_16K']
        )
        logger.info("ClearVoice 语音降噪初始化成功")

        # 进行预训练：处理sample目录下的input.wav文件
        sample_file_path = os.path.join(os.path.dirname(__file__), 'sample', 'input.wav')
        if os.path.exists(sample_file_path):
            logger.info("开始预训练：处理sample/input.wav文件")
            try:
                # 使用ClearVoice进行预训练处理
                start_time = time.time()
                preprocessed_audio = clearvoice_instance(audio_data, False)
                preprocess_time = time.time() - start_time

                logger.info(f"预训练完成，耗时 {preprocess_time:.3f}秒")
                logger.info("ClearVoice 预训练成功，模型已准备就绪")

            except Exception as e:
                logger.warning(f"预训练失败，但不影响服务运行: {e}")
        else:
            logger.info("未找到sample/input.wav文件，跳过预训练")

        return True
    except Exception as e:
        logger.error(f"ClearVoice 初始化失败: {e}")
        logger.warning("将继续运行，但不使用降噪功能")
        clearvoice_instance = None
        return False


def _denoise_audio(audio: np.ndarray, session_id: str = "api") -> np.ndarray:
    """使用 ClearVoice 进行音频降噪处理"""
    if not clearvoice_instance or audio is None:
        logger.info(f"[{session_id}] 跳过降噪处理：ClearVoice 未初始化或音频为空")
        return audio

    try:
        logger.info(f"[{session_id}] 开始音频降噪处理...")
        start_time = time.time()

        # ClearVoice 期望输入是 numpy 数组或 torch 张量
        # 确保音频数据是正确的格式（float32，范围 -1 到 1）
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)

        # 确保 chunk 范围在 [-1, 1]
        if np.max(np.abs(audio)) > 1.0:
            audio = audio / np.max(np.abs(audio))

        # 重塑为 [1, length] 格式，符合 ClearVoice 的输入要求
        if len(audio.shape) < 2:
            audio = np.reshape(audio, [1, audio.shape[0]])

        # 调用 ClearVoice 进行降噪
        denoised_audio = clearvoice_instance(audio, False)

        denoise_time = time.time() - start_time
        logger.info(f"[{session_id}] 音频降噪完成，耗时 {denoise_time:.3f}秒")
        # 确保输出格式正确
        if isinstance(denoised_audio, np.ndarray):
            if denoised_audio.dtype != np.float32:
                denoised_audio = denoised_audio.astype(np.float32)

            return denoised_audio
        else:
            # 如果返回 torch 张量，转换为 numpy
            try:
                import torch
                if isinstance(denoised_audio, torch.Tensor):
                    processed_audio = denoised_audio.detach().cpu().numpy().astype(np.float32)

                    return processed_audio
                else:
                    logger.warning(f"[{session_id}] ClearVoice 返回了未知类型: {type(denoised_audio)}")
                    return audio
            except ImportError:
                logger.warning(f"[{session_id}] 无法导入 torch，但 ClearVoice 返回了非 numpy 类型")
                return audio

    except Exception as e:
        logger.error(f"[{session_id}] 音频降噪失败: {e}")
        logger.info(f"[{session_id}] 返回原始音频数据")
        return audio


def _preprocess_audio_data(audio_data: bytes, session_id: str = "api") -> np.ndarray:
    """预处理音频数据，将 bytes 转换为 numpy 数组"""
    try:
        # 优先尝试 Int16 PCM（适配前端流式发送）
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            if len(audio_array) > 0:
                audio = audio_array.astype(np.float32) / 32767.0
                logger.info(f"[{session_id}] 按 Int16 PCM 解析，音频长度: {len(audio)} 样本")
                return audio
        except Exception as e:
            logger.warning(f"[{session_id}] Int16 PCM 解析失败: {e}")

        # 其次尝试 float32
        try:
            expected_samples = len(audio_data) // 4  # float32 每个样本 4 字节
            if expected_samples > 0:
                audio_array = np.frombuffer(audio_data, dtype=np.float32)
                if len(audio_array) == expected_samples:
                    logger.info(f"[{session_id}] 按 float32 解析，音频长度: {len(audio_array)} 样本")
                    return audio_array
        except Exception as e:
            logger.info(f"[{session_id}] float32 格式解析失败: {e}")

        # 最后尝试将原始 16 位 PCM 作为 float32 处理（兼容性兜底）
        try:
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            audio = audio_array.astype(np.float32) / 32767.0
            logger.info(f"[{session_id}] PCM 兜底解析为 float32，音频长度: {len(audio)} 样本")
            return audio
        except Exception as e:
            logger.error(f"[{session_id}] 无法解析 PCM 数据: {e}")
            return None

    except Exception as e:
        logger.error(f"[{session_id}] 音频预处理失败: {e}")
        return None


# 健康检查路由
@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"  # 实际项目中应该返回当前时间戳
    }

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化 ClearVoice"""
    initialize_clearvoice()


@app.post("/v1/audio/clearvoice")
async def process_audio(
    request: Request,
    session_id: str = Query(None, description="会话ID，如果不提供将自动生成")
):
    """处理音频数据，使用 ClearVoice 进行降噪处理"""
    # 获取原始二进制数据
    audio_data = await request.body()

    if not audio_data:
        return {
            "audio_data": b"",
            "denoised": False,
            "session_id": session_id
        }

    # 如果没有提供session_id，自动生成一个
    if not session_id:
        session_id = f"api_{int(time.time() * 1000)}"

    logger.info(f"[{session_id}] 开始处理音频数据，大小: {len(audio_data)} 字节")

    try:
        # 步骤 1: 预处理音频数据
        audio_array = _preprocess_audio_data(audio_data, session_id)
        if audio_array is None:
            logger.error(f"[{session_id}] 音频预处理失败")
            return {
                "audio_data": audio_data,  # 返回原始数据
                "denoised": False,
                "session_id": session_id
            }

        # 步骤 2: 执行音频降噪
        denoised_audio = _denoise_audio(audio_array, session_id)

        # 步骤 3: 将处理后的音频转换回 bytes
        if denoised_audio is not None:
            # 确保音频数据是一维的
            if len(denoised_audio.shape) > 1:
                denoised_audio = denoised_audio.flatten()

            # 转换回 int16 格式用于传输
            processed_audio_int16 = (denoised_audio * 32767.0).astype(np.int16)
            processed_audio_bytes = processed_audio_int16.tobytes()

            logger.info(f"[{session_id}] 音频处理完成，原始大小: {len(audio_data)} 字节，处理后大小: {len(processed_audio_bytes)} 字节")

            return {
                "audio_data": processed_audio_bytes,
                "denoised": clearvoice_instance is not None,
                "session_id": session_id
            }
        else:
            logger.warning(f"[{session_id}] 降噪处理失败，返回原始音频数据")
            return {
                "audio_data": audio_data,
                "denoised": False,
                "session_id": session_id
            }

    except Exception as e:
        logger.error(f"[{session_id}] 音频处理异常: {e}")
        return {
            "audio_data": audio_data,  # 返回原始数据
            "denoised": False,
            "session_id": session_id
        }
