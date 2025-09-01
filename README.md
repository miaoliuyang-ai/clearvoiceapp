# ClearVoice API

ClearVoice 是一个基于 FastAPI 开发的现代化 HTTP 后端服务。

## 功能特性

- 🚀 基于 FastAPI 框架，性能优异
- 📖 自动生成交互式 API 文档
- 🔄 支持热重载，便于开发
- 🛡️ 内置 CORS 支持
- 📝 类型提示和数据验证
- 🧪 易于测试

## 项目结构

```
clearvoice/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI 应用主文件
├── main.py              # 应用启动入口
├── run.py               # 便捷启动脚本
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

### 方法一：使用启动脚本（推荐）

```bash
python run.py
```

### 方法二：直接运行

```bash
python main.py
```

服务启动后，你可以访问：

- **API 服务**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **交互式文档**: http://localhost:8000/redoc

## API 接口

### 基础接口

- `GET /` - 欢迎信息
- `GET /health` - 健康检查
- `GET /api/v1/items/{item_id}` - 获取项目信息
- `POST /api/v1/items` - 创建新项目

## 开发说明

### 添加新路由

在 `app/main.py` 中添加新的路由：

```python
@app.get("/api/v1/new-endpoint")
async def new_endpoint():
    return {"message": "新的接口"}
```

### 运行测试

```bash
# 安装测试依赖（可选）
pip install pytest httpx

# 运行测试
pytest
```

## 部署说明

### 生产环境部署

```bash
# 使用 uvicorn 启动生产服务器
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 或者使用 gunicorn
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## 许可证

MIT License
