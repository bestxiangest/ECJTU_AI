# ECJTU成绩查询与分析系统 - 部署指南

## 生产环境部署

### 1. 环境准备

#### 系统要求
- Python 3.8+
- 内存: 至少 512MB
- 磁盘: 至少 1GB 可用空间
- 网络: 需要访问外网（调用AI API）

#### 安装依赖
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置文件

#### 生产环境 .env 配置
```env
# 阿里云通义千问API密钥（必须配置）
AL_API_KEY=your_actual_api_key_here

# Flask应用配置
SECRET_KEY=your_very_secure_secret_key_here
FLASK_ENV=production

# 对话超时时间（秒）
CONVERSATION_TIMEOUT=300

# 日志级别
LOG_LEVEL=WARNING
```

### 3. 使用 Gunicorn 部署

#### 安装 Gunicorn
```bash
pip install gunicorn
```

#### 创建 Gunicorn 配置文件 (gunicorn.conf.py)
```python
# Gunicorn 配置
bind = "0.0.0.0:5000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# 进程管理
pidfile = "gunicorn.pid"
daemon = False
```

#### 启动命令
```bash
# 创建日志目录
mkdir -p logs

# 启动应用
gunicorn -c gunicorn.conf.py app:app
```

### 4. 使用 Nginx 反向代理

#### Nginx 配置示例
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # 静态文件
    location /static {
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # 应用代理
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }
    
    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
```

### 5. 使用 Docker 部署

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建日志目录
RUN mkdir -p logs

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  ecjtu-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./logs:/app/logs
      - ./.env:/app/.env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - ecjtu-app
    restart: unless-stopped
```

### 6. 监控和日志

#### 日志轮转配置 (logrotate)
```
/path/to/your/app/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload gunicorn
    endscript
}
```

#### 系统服务配置 (systemd)
```ini
[Unit]
Description=ECJTU Score Analysis System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
ExecStart=/path/to/your/app/venv/bin/gunicorn -c gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 7. 安全建议

1. **API密钥安全**
   - 使用环境变量存储敏感信息
   - 定期轮换API密钥
   - 限制API密钥权限

2. **网络安全**
   - 使用HTTPS（SSL/TLS）
   - 配置防火墙规则
   - 限制访问IP（如果需要）

3. **应用安全**
   - 定期更新依赖包
   - 配置适当的CORS策略
   - 实施请求频率限制

### 8. 性能优化

1. **缓存策略**
   - 静态文件缓存
   - API响应缓存（Redis）
   - 数据库查询缓存

2. **负载均衡**
   - 多个Gunicorn worker
   - Nginx负载均衡
   - 数据库连接池

### 9. 备份和恢复

1. **数据备份**
   - 定期备份配置文件
   - 备份用户数据（如果有）
   - 备份日志文件

2. **恢复流程**
   - 文档化恢复步骤
   - 测试恢复流程
   - 准备应急方案

### 10. 监控指标

- 应用响应时间
- API调用成功率
- 系统资源使用率
- 错误日志监控
- 用户活跃度

通过访问 `/health` 端点可以获取系统健康状态，通过 `/api/system/info` 可以获取系统信息。