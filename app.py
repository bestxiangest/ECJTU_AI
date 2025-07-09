from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import json
from ecjtu import ECJTU
from datetime import datetime
import requests
import dashscope
from http import HTTPStatus
import threading
import time

app = Flask(__name__)
app.secret_key = 'ecjtu_secret_key_2024'  # 用于session管理

# 启用CORS
CORS(app)

# 阿里云API KEY
AL_API_KEY = 'sk-dcbb7246ac3f402994454b91120b95ab'
dashscope.api_key = AL_API_KEY

# 用于存储每个用户的对话历史和上次交互时间
conversations = {}
last_interaction = {}
conversation_lock = threading.Lock()

# 定义对话超时时间（秒）
CONVERSATION_TIMEOUT = 60

# 全局变量存储当前登录的客户端
current_client = None
current_student_id = None
current_password = None


@app.route('/')
def index():
    """主页面 - 重定向到登录页面"""
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    """登录页面"""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    """处理登录请求"""
    global current_client, current_student_id, current_password
    
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        password = data.get('password')
        
        if not student_id or not password:
            return jsonify({
                "success": False,
                "message": "请填写完整的学号和密码"
            }), 400
        
        # 尝试创建ECJTU客户端并登录
        try:
            client = ECJTU(stud_id=student_id, password=password)
            client.login()
            
            # 登录成功，保存到全局变量和session
            current_client = client
            current_student_id = student_id
            current_password = password
            
            session['student_id'] = student_id
            session['logged_in'] = True
            
            return jsonify({
                "success": True,
                "message": "登录成功",
                "student_id": student_id
            })
            
        except Exception as login_error:
            print(f"登录失败: {login_error}")
            return jsonify({
                "success": False,
                "message": "学号或密码错误，请检查后重试"
            }), 401
            
    except Exception as e:
        print(f"登录处理错误: {e}")
        return jsonify({
            "success": False,
            "message": "服务器错误，请稍后重试"
        }), 500

@app.route('/dashboard')
def dashboard():
    """仪表板页面"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    """退出登录"""
    global current_client, current_student_id, current_password
    
    session.clear()
    current_client = None
    current_student_id = None
    current_password = None
    
    return redirect(url_for('login_page'))

@app.route('/api')
def api_info():
    """API信息页面"""
    return """
    <h1>ECJTU成绩查询与分析系统 API</h1>
    <h2>可用接口：</h2>
    <ul>
        <li><a href="/api/scores">/api/scores</a> - 获取学生成绩数据（JSON格式）</li>
        <li><a href="/api/analyze">/api/analyze</a> - 获取AI成绩分析报告</li>
        <li>/ai - POST接口，用于与AI进行对话交互</li>
    </ul>
    <p><a href="/">返回主页</a></p>
    """


@app.route('/api/scores')
def get_scores_api():
    """获取学生成绩的API接口"""
    global current_client, current_student_id
    
    # 检查登录状态
    if not session.get('logged_in') or not current_client:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    try:
        # 入学时间
        enrollment_time = int(current_student_id[0:4])
        print(f"入学时间: {enrollment_time}")

        # 获取所有成绩
        all_scores = get_all_scores(current_client, enrollment_time)
        
        # 获取学生真实GPA
        try:
            gpa_info = current_client.gpa.today()
            student_gpa = gpa_info.gpa
            print(f"获取到学生GPA: {student_gpa}")
        except Exception as gpa_error:
            print(f"获取GPA失败: {gpa_error}")
            student_gpa = "未获取到"

        # 构建返回的JSON数据
        result = {
            "success": True,
            "message": "成绩获取成功",
            "student_id": current_student_id,
            "enrollment_year": enrollment_time,
            "total_semesters": len(all_scores),
            "GPA": student_gpa,
            "data": all_scores
        }

        return jsonify(result)

    except Exception as e:
        error_result = {
            "success": False,
            "message": f"获取成绩失败: {str(e)}",
            "data": None
        }
        return jsonify(error_result), 500


def get_all_scores(client, start_year):
    """获取从指定年份开始的所有学期成绩，返回按学期分组的JSON格式数据"""
    scores_by_semester = {}
    current_year = datetime.now().year

    # 从入学年份开始遍历所有可能的学期
    for year in range(start_year, current_year + 1):
        for semester in [1, 2]:
            semester_str = f"{year}.{semester}"
            try:
                scores = client.scores.filter(semester=semester_str)
                if scores:  # 如果该学期有成绩
                    # 将Score对象转换为字典格式
                    semester_scores = []
                    for score in scores:
                        score_dict = {
                            "course_name": score.course_name,
                            "course_nature": score.course_nature,
                            "credit": score.credit,
                            "grade": score.grade
                        }
                        semester_scores.append(score_dict)

                    scores_by_semester[semester_str] = {
                        "semester": semester_str,
                        "course_count": len(scores),
                        "courses": semester_scores
                    }
                    print(f"找到 {semester_str} 学期成绩：{len(scores)} 门课程")
            except Exception as e:
                print(f"获取 {semester_str} 学期成绩失败：{e}")

    return scores_by_semester


# 大模型部分

# 提示词
PROMPT = '''
你是一位资深的大学学业导师和数据分析专家。你的任务是分析一名学生从入学至今的完整成绩单（以JSON格式提供），并生成一份全面、积极、富有建设性的学业评估报告。

**核心指令：**

1.  **数据预处理（极其重要）：**
    * 在分析前，你必须将所有非百分制的成绩转换为统一的百分制分数进行计算。转换规则如下：
        * "优秀" = 90分
        * "良好" = 75分
        * "合格" = 60分以上
        * "不合格" = 60分一下
    * 在报告中引用课程名称时，必须**移除**名称前的课程代码和括号，例如，将 "【1506102050】程序设计基础" 清理为 "程序设计基础"。

2.  **分析维度：**
    * **你无需计算GPA：** 每位学生的GPA将与学生的成绩数据一同发送给你。 
    * **识别优势与不足：** 找出学生持续获得高分（90分以上）的学科类别作为优势领域。找出成绩较低（75分以下）或出现明显下滑的科目作为待提升领域。
    * **分析学习趋势：** 比较不同学期之间的核心课程平均分或GPA变化，判断学生的学习状态是上升、稳定还是波动。
    * **提供个性化建议：** 你的建议必须具体、可行，并与学生的学科表现紧密相关。

3.  **输出格式（必须严格遵守）：**
    * 你的回复**必须且只能是**一个格式化良好的JSON对象。
    * 禁止在JSON对象前后添加任何说明性文字、注释或Markdown标记。
    * JSON对象的结构必须严格遵循以下定义：
        ```json
        {
          "studentId": "学生的学号，从输入中获取",
          "reportTitle": "学业成绩综合评估报告",
          "overallAssessment": {
            "summary": "（一段对学生整体表现的、鼓励性的总结文字）",
            "gpa": "（学生的绩点，从输入中获取）",
            "level": "（根据整体表现给出的“优秀/良好/中等/待提高”评级）"
          },
          "performanceAnalysis": {
            "strengths": [
              "（列出1-3项学生的显著优势，字符串数组）"
            ],
            "areasForImprovement": [
              "（列出1-2项学生需要关注和提升的领域，字符串数组）"
            ]
          },
          "learningTrajectory": {
            "trend": "（“上升/稳定/波动/下降”中的一个）",
            "analysis": "（一句话解释这个趋势是如何得出的）"
          },
          "personalizedSuggestions": {
            "academic": [
              "（针对薄弱环节的1-2条具体学习建议，字符串数组）"
            ],
            "developmental": [
              "（结合优势学科的1-2条长远发展建议，字符串数组）"
            ]
          },
          "keyCourseBreakdown": [
            {
              "courseName": "（一门关键课程的名称）",
              "trend": "（该课程系列（如高数I/II）的成绩趋势：“优秀/稳定/波动/下降”）",
              "comment": "（对该课程表现的一句精炼点评）"
            }
          ]
        }
        ```

4.  **语言风格：**
    * 报告的整体基调必须是积极、正面、鼓励为主。
    * 在指出不足时，使用“有待提升”、“可以进一步巩固”等建设性词语，而非“差”、“不及格”等负面词汇。

现在，请根据用户提供的学生成绩JSON数据，开始分析并生成报告。
        '''


def call_qwen(messages):
    """调用通义千问 API"""
    try:
        responses = dashscope.Generation.call(
            api_key=AL_API_KEY,
            # model="qwen2.5-14b-instruct-1m", # 聪明一点
            model="qwen-turbo",  # 速度最快
            messages=messages,
            result_format='message',
            stream=True,  # 设置输出方式为流式输出
            incremental_output=True  # 增量式流式输出
        )
        # 单次输出
        # if response.status_code == HTTPStatus.OK:
        #     return response.output.choices[0]['message']
        # else:
        #     print(
        #         f"通义千问 API 调用失败：Request id: {response.request_id}, Status code: {response.status_code}, error code: {response.code}, error message: {response.message}")
        #     return None

        # 使用流式输出
        full_content = ""
        # print("流式输出内容为：")
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                full_content += response.output.choices[0].message.content
                # print(response.output.choices[0]['message']['content'], end='')
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))
        # print(f"\n完整内容为：{full_content}")
        return full_content


    except Exception as e:
        print(f"调用通义千问 API 发生异常：{e}")
        return None


def handle_ai_response(user_id, qwen_response):
    print(qwen_response)
    return jsonify({"response": qwen_response})


@app.route('/api/analyze', methods=['GET', 'POST'])
def analyze_scores():
    """分析学生成绩的API接口"""
    global current_client, current_student_id
    
    # 检查登录状态
    if not session.get('logged_in') or not current_client:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    try:
        # 检查是否通过POST传递了成绩数据
        if request.method == 'POST' and request.json and 'scores_data' in request.json:
            # 使用传递的成绩数据
            scores_data = request.json['scores_data']
            print("使用前端传递的成绩数据，避免重复调用API")
        else:
            # 获取学生成绩数据（兼容GET请求）
            enrollment_time = int(current_student_id[0:4])
            all_scores = get_all_scores(current_client, enrollment_time)
            
            if not all_scores:
                return jsonify({
                    "success": False,
                    "message": "未找到成绩数据",
                    "data": None
                }), 404
            
            # 获取学生真实GPA
            try:
                gpa_info = current_client.gpa.today()
                student_gpa = gpa_info.gpa
                print(f"获取到学生GPA: {student_gpa}")
            except Exception as gpa_error:
                print(f"获取GPA失败: {gpa_error}")
                student_gpa = "未获取到"
            
            # 构建发送给AI的成绩数据
            scores_data = {
                "student_id": current_student_id,
                "enrollment_year": enrollment_time,
                "total_semesters": len(all_scores),
                "GPA": student_gpa,
                "data": all_scores
            }
        
        # 将成绩数据转换为JSON字符串发送给AI
        scores_json = json.dumps(scores_data, ensure_ascii=False, indent=2)
        
        # 构建AI对话消息
        messages = [
            {'role': 'system', 'content': PROMPT},
            {'role': 'user', 'content': f"请分析以下学生成绩数据：\n{scores_json}"}
        ]
        
        # 调用AI分析
        ai_response = call_qwen(messages)
        
        if ai_response:
            try:
                # 尝试解析AI返回的JSON
                analysis_result = json.loads(ai_response)
                return jsonify({
                    "success": True,
                    "message": "成绩分析完成",
                    "raw_scores": scores_data,
                    "analysis": analysis_result
                })
            except json.JSONDecodeError:
                # 如果AI返回的不是有效JSON，返回原始文本
                return jsonify({
                    "success": True,
                    "message": "成绩分析完成（文本格式）",
                    "raw_scores": scores_data,
                    "analysis_text": ai_response
                })
        else:
            return jsonify({
                "success": False,
                "message": "AI分析失败，请稍后重试",
                "raw_scores": scores_data
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"分析过程中发生错误: {str(e)}",
            "data": None
        }), 500


@app.route('/ai', methods=['POST'])
def chat():
    user_id = request.remote_addr  # 使用客户端 IP 作为用户标识符
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "请求中缺少 'message' 字段"}), 400

    with conversation_lock:
        current_time = time.time()

        # 检查用户是否已存在对话，以及是否超时
        if user_id in conversations:
            if current_time - last_interaction.get(user_id, 0) > CONVERSATION_TIMEOUT:
                # 对话超时，重新开始
                conversations[user_id] = [{
                    'role': 'system',
                    'content': PROMPT
                }]
                print(f"用户 {user_id} 的对话已超时，已重置。")
            last_interaction[user_id] = current_time
        else:
            # 新用户，创建新的对话
            conversations[user_id] = [{
                'role': 'system',
                'content': PROMPT
            }]
            last_interaction[user_id] = current_time
            print(f"为用户 {user_id} 创建新的对话。")

        # 将用户的消息添加到对话历史
        conversations[user_id].append({'role': 'user', 'content': user_message})

        # 调用通义千问 API
        qwen_response = call_qwen(conversations[user_id])

        if qwen_response:
            conversations[user_id].append({'role': 'assistant', 'content': qwen_response})
            print(jsonify({"response": qwen_response}))
            # 将大模型回答传给处理函数
            final = handle_ai_response(user_id, qwen_response)
            return final, 200
        else:
            # 如果调用失败，移除用户刚刚发送的消息，保持对话历史的完整性
            conversations[user_id].pop()
            print(jsonify({"error": "调用通义千问 API 失败，请稍后重试"}), 500)
            return jsonify({"error": "调用通义千问 API 失败，请稍后重试"}), 500


if __name__ == '__main__':
    app.run()
