# ECJTU 成绩查询与分析系统

一个基于 Flask 和 AI 技术的华东交通大学学生成绩查询与智能分析系统。

## 📋 项目简介

ECJTU 成绩查询与分析系统是一个现代化的 Web 应用，为华东交通大学学生提供便捷的成绩查询和智能分析服务。系统集成了阿里云通义千问大模型，能够对学生成绩进行深度分析，提供个性化的学习建议和趋势预测。

## ✨ 主要功能

### 🔐 用户认证
- 安全的学号密码登录系统
- Session 管理和状态保持
- 自动登录状态检查

### 📊 成绩查询
- 获取所有学期的详细成绩信息
- 实时 GPA 查询
- 按学期分类展示课程成绩
- 支持课程性质、学分、成绩等详细信息

### 🤖 AI 智能分析
- **总体评估**：基于 GPA 的学术表现评级
- **学习优势**：识别学生的强项学科和能力
- **改进建议**：针对薄弱环节提供具体建议
- **学习趋势**：分析成绩变化趋势和发展方向
- **个性化建议**：提供学术和发展方面的定制化建议

### 📈 数据可视化
- **学期趋势图**：展示各学期平均成绩变化
- **学科分布图**：雷达图显示不同课程性质的成绩分布
- **统计概览**：总课程数、总学分、当前 GPA、学期数等关键指标

### 💻 现代化界面
- 响应式设计，支持桌面和移动设备
- 美观的渐变背景和卡片式布局
- 实时加载状态和错误提示
- 直观的数据展示和交互体验

### 🔧 系统监控
- **健康检查**：实时系统状态监控接口
- **系统信息**：CPU、内存、磁盘使用率监控
- **性能指标**：应用运行时间和资源消耗统计
- **日志系统**：结构化日志记录和错误追踪

### ⚙️ 配置管理
- **环境变量**：统一的配置文件管理
- **配置类**：集中化的应用配置
- **开发/生产环境**：灵活的环境切换
- **安全性**：敏感信息环境变量化

## 🛠️ 技术栈

### 后端技术
- **Flask**: Python Web 框架
- **ECJTU**: 华东交通大学教务系统 SDK
- **DashScope**: 阿里云通义千问 API
- **Session**: 用户状态管理
- **psutil**: 系统监控和性能指标
- **python-dotenv**: 环境变量管理
- **logging**: 结构化日志系统

### 前端技术
- **HTML5/CSS3**: 现代化页面结构和样式
- **JavaScript (ES6+)**: 动态交互逻辑
- **Chart.js**: 数据可视化图表库
- **Fetch API**: 原生 HTTP 请求接口

### 数据处理
- **JSON**: 数据交换格式
- **RESTful API**: 标准化接口设计

### 系统架构
- **配置管理**: 统一的配置类和环境变量
- **装饰器模式**: 登录验证和错误处理
- **日志系统**: 结构化日志记录和监控
- **健康检查**: 系统状态监控接口
- **前端优化**: 使用原生 Fetch API 替代第三方库，提升兼容性和性能

## 📦 安装配置

### 环境要求
- Python 3.7+
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/bestxiangest/ECJTU_AI.git
cd ECJTU_AI
```

2. **创建虚拟环境**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **环境配置**

创建 `.env` 文件并配置必要的环境变量：
```bash
# 阿里云通义千问API密钥
AL_API_KEY=your-dashscope-api-key

# Flask应用配置
SECRET_KEY=your-secret-key-here
FLASK_ENV=development

# 系统配置
CONVERSATION_TIMEOUT=1800
LOG_LEVEL=INFO
```

**重要提示**：
- 请将 `your-dashscope-api-key` 替换为您的阿里云API密钥
- 生产环境请使用强密码作为 `SECRET_KEY`
- 生产环境请将 `FLASK_ENV` 设置为 `production`

5. **运行应用**
```bash
python app.py
```

应用将在 `http://127.0.0.1:5000` 启动。

## 🚀 使用说明

### 登录系统
1. 访问 `http://127.0.0.1:5000`
2. 输入华东交通大学学号和密码
3. 点击"登录系统"按钮

### 查看成绩分析
1. 登录成功后自动跳转到仪表板
2. 系统自动获取成绩数据并进行 AI 分析
3. 查看统计概览、图表可视化和 AI 分析报告
4. 可按学期切换查看详细成绩

### 退出登录
点击右上角的"退出登录"按钮即可安全退出系统。

## 📡 API 文档

### 认证接口

#### POST /login
用户登录接口

**请求参数：**
```json
{
  "student_id": "学号",
  "password": "密码"
}
```

**响应示例：**
```json
{
  "success": true,
  "message": "登录成功",
  "student_id": "202012345"
}
```

#### POST /logout
用户退出登录接口

**响应示例：**
```json
{
  "success": true,
  "message": "退出成功"
}
```

### 系统监控接口

#### GET /health
系统健康检查接口

**响应示例：**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "uptime": "2 days, 5 hours, 30 minutes"
}
```

#### GET /api/system/info
系统信息监控接口（需要登录）

**响应示例：**
```json
{
  "success": true,
  "system_info": {
    "cpu_percent": 25.5,
    "memory_percent": 68.2,
    "disk_percent": 45.8,
    "uptime": "2 days, 5 hours, 30 minutes",
    "python_version": "3.9.7",
    "flask_version": "2.3.3"
  }
}
```

### 成绩接口

#### GET /api/scores
获取学生成绩数据

**响应示例：**
```json
{
  "success": true,
  "message": "成绩获取成功",
  "student_id": "202012345",
  "enrollment_year": 2020,
  "total_semesters": 4,
  "GPA": 3.83,
  "data": {
    "2023.1": {
      "course_count": 12,
      "courses": [
        {
          "course_name": "高等数学",
          "course_nature": "必修",
          "credit": 4,
          "grade": "85"
        }
      ]
    }
  }
}
```

#### GET/POST /api/analyze
获取 AI 成绩分析报告

**POST 请求参数（可选）：**
```json
{
  "scores_data": {
    // 成绩数据对象
  }
}
```

**响应示例：**
```json
{
  "success": true,
  "message": "分析完成",
  "analysis": {
    "overallAssessment": {
      "gpa": "3.83",
      "level": "优秀",
      "summary": "学术表现优异..."
    },
    "performanceAnalysis": {
      "strengths": ["数学基础扎实", "理论课程表现优异"],
      "areasForImprovement": ["实践课程有待加强"]
    },
    "learningTrajectory": {
      "trend": "稳步上升",
      "analysis": "成绩呈现稳定上升趋势..."
    },
    "personalizedSuggestions": {
      "academic": ["建议加强实践能力"],
      "developmental": ["可考虑参与科研项目"]
    }
  }
}
```

## 🏗️ 项目结构

```
ECJTU_AI/
├── app.py                 # 主应用文件
├── requirements.txt       # 项目依赖文件
├── .env                   # 环境变量配置文件
├── deploy.md             # 生产环境部署指南
├── templates/             # HTML 模板目录
│   ├── login.html        # 登录页面
│   ├── dashboard.html    # 仪表板页面
│   └── index.html        # 原始主页（已弃用）
├── static/               # 静态资源目录
├── .venv/                # 虚拟环境
├── .gitignore            # Git 忽略文件
├── ECJTU API使用文档.md   # ECJTU SDK 文档
├── 获取学生所有成绩的返回值实例.md  # 数据格式示例
└── README.md             # 项目说明文档
```

## 🔧 核心功能实现

### 配置管理系统
```python
class Config:
    """应用配置类"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    AL_API_KEY = os.getenv('AL_API_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    CONVERSATION_TIMEOUT = int(os.getenv('CONVERSATION_TIMEOUT', 1800))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
```

### 装饰器模式
```python
def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function

def handle_errors(f):
    """统一错误处理装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"接口 {f.__name__} 发生错误: {str(e)}")
            return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    return decorated_function
```

### 成绩数据获取
```python
def get_all_scores(client, start_year):
    """获取从指定年份开始的所有学期成绩"""
    scores_by_semester = {}
    current_year = datetime.now().year
    
    for year in range(start_year, current_year + 1):
        for semester in [1, 2]:
            semester_str = f"{year}.{semester}"
            try:
                scores = client.scores.filter(semester=semester_str)
                if scores:
                    # 处理成绩数据...
                    logger.info(f"找到 {semester_str} 学期成绩：{len(scores)} 门课程")
            except Exception as e:
                logger.error(f"获取 {semester_str} 学期成绩失败：{e}")
```

### AI 分析集成
```python
@login_required
@handle_errors
def analyze_scores():
    """AI 成绩分析接口"""
    # 构建 AI 对话消息
    messages = [
        {'role': 'system', 'content': PROMPT},
        {'role': 'user', 'content': f"请分析以下学生成绩数据：\n{scores_json}"}
    ]
    
    # 调用通义千问 API
    response = call_qwen(messages, app.config['AL_API_KEY'])
    logger.info(f"AI分析完成，学生ID: {session.get('student_id')}")
```

### 系统监控
```python
@app.route('/health')
def health_check():
    """健康检查接口"""
    uptime = datetime.now() - app_start_time
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'uptime': str(uptime)
    })

@app.route('/api/system/info')
@login_required
@handle_errors
def system_info():
    """系统信息接口"""
    import psutil
    return jsonify({
        'success': True,
        'system_info': {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent
        }
    })
```

### 性能优化
- **数据缓存**：前端缓存成绩数据，避免重复 API 调用
- **异步加载**：分步加载成绩数据和 AI 分析
- **错误处理**：完善的异常处理和用户提示
- **状态管理**：实时更新加载状态和分析进度
- **装饰器优化**：统一的登录验证和错误处理逻辑
- **日志系统**：结构化日志记录，便于问题追踪和性能分析

## 🔒 安全特性

- **Session 管理**：安全的用户状态保持
- **登录验证**：装饰器模式的统一登录验证
- **环境变量**：敏感信息通过环境变量管理
- **配置分离**：开发和生产环境配置分离
- **错误处理**：统一错误处理，避免敏感信息泄露
- **API 安全**：所有敏感接口都需要登录验证
- **日志安全**：不记录敏感用户信息

## 🎯 使用场景

- **学生自查**：快速查看个人成绩和学术表现
- **学习规划**：基于 AI 分析制定学习计划
- **趋势分析**：了解学习进步情况和发展方向
- **决策支持**：为选课、专业方向选择提供数据支持

## 🚧 注意事项

1. **账号安全**：请妥善保管学号和密码，系统不会存储用户密码
2. **环境配置**：请确保正确配置 `.env` 文件中的所有必要环境变量
3. **API 密钥**：请妥善保管阿里云API密钥，不要将其提交到版本控制系统
4. **网络连接**：确保能够正常访问华东交通大学教务系统和阿里云API
5. **API 限制**：请合理使用 AI 分析功能，避免频繁请求
6. **数据准确性**：成绩数据来源于教务系统，请以官方数据为准
7. **生产部署**：生产环境请参考 `deploy.md` 文档进行部署
8. **日志管理**：定期清理日志文件，避免磁盘空间不足

## 🔄 更新日志

### v2.0.0 (最新) - 架构优化版本
- ✅ **配置管理重构**：引入统一的配置类和环境变量管理
- ✅ **装饰器模式**：实现登录验证和错误处理装饰器
- ✅ **日志系统完善**：结构化日志记录和错误追踪
- ✅ **系统监控功能**：新增健康检查和系统信息接口
- ✅ **依赖管理优化**：完善 requirements.txt 和项目结构
- ✅ **部署文档**：新增生产环境部署指南 deploy.md
- ✅ **API密钥问题修复**：解决配置获取方式不一致的问题
- ✅ **性能优化**：改进错误处理和接口响应速度
- ✅ **安全性增强**：敏感信息环境变量化和配置分离

### v1.2.0
- ✅ 优化数据加载性能，避免重复 API 调用
- ✅ 修复学号显示问题
- ✅ 改进 AI 分析状态更新机制
- ✅ 增强错误处理和用户体验

### v1.1.0
- ✅ 集成真实 GPA 获取功能
- ✅ 优化前端界面设计
- ✅ 添加图表可视化功能

### v1.0.0
- ✅ 基础成绩查询功能
- ✅ AI 智能分析集成
- ✅ 用户登录系统
- ✅ 现代化 Web 界面

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

## 📄 许可证

本项目仅供学习和研究使用，请遵守华东交通大学相关规定。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 GitHub Issue
- 发送邮件至[项目维护者](zzningg@qq.com)

---

**⚠️ 免责声明**：本系统仅为学习交流目的开发，不承担因使用本系统而产生的任何责任。请用户合理使用，遵守相关法律法规和学校规定。
