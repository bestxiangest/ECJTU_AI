# ECJTU 库使用文档

## 简介

ECJTU 是一个用于华东交通大学教务系统的 Python SDK，提供了便捷的 API 来获取课程表、成绩、绩点、选修课程等信息。

## 安装

打开终端命令行，输入以下命令：

```bash
pip install ecjtu
```

## 快速开始

### 基本使用

```python
from ecjtu import ECJTU

# 创建客户端实例
client = ECJTU(stud_id="你的学号", password="你的密码")

# 登录
client.login()
```

### 环境变量配置（可选）

你也可以通过环境变量来配置学号和密码：

```bash
export ECJTU_STUDENT_ID="你的学号"
export ECJTU_PASSWORD="你的密码"
```

然后直接创建客户端：

```python
from ecjtu import ECJTU

client = ECJTU()  # 自动从环境变量读取
```

## 功能模块

### 1. 课程表查询

#### 获取今日课表

```python
from typing import List
from ecjtu import ECJTU, ScheduledCourse

client = ECJTU(stud_id="你的学号", password="你的密码")

# 获取今日课表
courses: List[ScheduledCourse] = client.scheduled_courses.today()
print(courses)
```

**输出示例：**

```python
[ScheduledCourse(class_span='1,2', course='材料力学(B)', course_name='材料力学(B)(20232-1)', week_span='1-15', course_type='必修课', teacher='程俊峰', week_day=5, class_room='31-504', pk_type='上课'), ScheduledCourse(class_span='3,4', course='Java程序设计(B)', course_name='Java程序设计(B)(20232-2)', week_span='1-16', course_type='限选课', teacher='王珏', week_day=5, class_room='31-311D', pk_type='上课'), ScheduledCourse(class_span='5,6', course='数据库系统原理', course_name='数据库系统原理(20232-2)', week_span='1-16', course_type='必修课', teacher='魏永丰', week_day=5, class_room='31-505', pk_type='上课')]
```

#### 获取指定日期课表

```python
from datetime import date

# 获取指定日期的课表
specific_date = "2023-10-15"
courses = client.scheduled_courses.filter(date=specific_date)
print(courses)
```

#### 获取本周课表

```python
# 获取本周课表（返回7天的课表列表）
week_courses = client.scheduled_courses.this_week()

# week_courses 是一个包含7个列表的列表，每个子列表代表一天的课程
for day_index, day_courses in enumerate(week_courses):
    print(f"第{day_index + 1}天的课程：")
    for course in day_courses:
        print(f"  {course.course} - {course.teacher} - {course.class_room}")
```



### 绩点查询

```python
from ecjtu import GPA

# 获取当前绩点
gpa: GPA = client.gpa.today()
print(f"学生姓名: {gpa.student_name}")
print(f"绩点: {gpa.gpa}")
print(f"状态: {gpa.status}")
```

**输出示例：**

```
学生姓名: 张三
绩点: 3.85
状态: 正常
```

### 3. 成绩查询

#### 获取上学期成绩

```python
from typing import List
from ecjtu import Score

# 获取上学期成绩（当前学期成绩需要等学期结束后才能查看）
scores: List[Score] = client.scores.today()

for score in scores:
    print(f"课程: {score.course_name}")
    print(f"学期: {score.semester}")
    print(f"课程性质: {score.course_nature}")
    print(f"学分: {score.credit}")
    print(f"成绩: {score.grade}")
    print("-" * 30)
```

#### 获取指定学期成绩

```python
# 获取指定学期的成绩
semester_scores = client.scores.filter(semester="2023.1")
print(semester_scores)
```

### 4. 选修课程查询

#### 获取当前学期选修课程

```python
from typing import List
from ecjtu import ElectiveCourse

# 获取当前学期的选修课程
elective_courses: List[ElectiveCourse] = client.elective_courses.today()

for course in elective_courses:
    print(f"课程名称: {course.class_name}")
    print(f"学期: {course.semester}")
    print(f"课程类型: {course.class_type}")
    print(f"考核方式: {course.class_assessment_method}")
    print(f"上课信息: {course.class_info}")
    print(f"学分: {course.credit}")
    print(f"教师: {course.teacher}")
    print("-" * 30)
```

#### 获取指定学期选修课程

```python
# 获取指定学期的选修课程
semester_electives = client.elective_courses.filter(semester="2023.2")
print(semester_electives)
```

## 异步支持

ECJTU 库同时支持异步操作，使用 `AsyncECJTU` 客户端：

```python
import asyncio
from ecjtu import AsyncECJTU

async def main():
    # 创建异步客户端
    client = AsyncECJTU(stud_id="你的学号", password="你的密码")
    
    # 登录
    await client.login()
    
    # 获取今日课表
    courses = await client.scheduled_courses.today()
    print(courses)
    
    # 获取绩点
    gpa = await client.gpa.today()
    print(gpa)
    
    # 获取成绩
    scores = await client.scores.today()
    print(scores)
    
    # 获取选修课程
    electives = await client.elective_courses.today()
    print(electives)

# 运行异步函数
asyncio.run(main())
```

## 数据模型

### ScheduledCourse（课程表）

- `class_span`: 上课时间（如 "1,2" 表示第1-2节课）
- `course`: 课程名称
- `course_name`: 详细课程名称
- `week_span`: 周数（如 "1-15" 表示第1-15周）
- `course_type`: 课程类型（必修课/限选课等）
- `teacher`: 教师姓名
- `week_day`: 星期几（1-7）
- `class_room`: 教室
- `pk_type`: 课程类型（上课/考试等）

### GPA（绩点）

- `student_name`: 学生姓名
- `gpa`: 绩点值
- `status`: 状态

### Score（成绩）

- `semester`: 课程学期（如 "2023.1"）
- `course_name`: 课程名称
- `course_nature`: 课程性质（必修/选修等）
- `credit`: 学分
- `grade`: 成绩

### ElectiveCourse（选修课程）

- `semester`: 学期
- `class_name`: 教学班名称
- `class_type`: 课程类型
- `class_assessment_method`: 考核方式
- `class_info`: 上课信息
- `class_number`: 课程编号
- `credit`: 学分
- `teacher`: 教师

## 错误处理

```python
try:
    client = ECJTU(stud_id="你的学号", password="你的密码")
    client.login()
    courses = client.scheduled_courses.today()
except ValueError as e:
    print(f"登录失败: {e}")
except Exception as e:
    print(f"发生错误: {e}")
```

## 注意事项

1. **账号安全**：请妥善保管你的学号和密码，建议使用环境变量配置。
2. **网络连接**：确保网络连接正常，能够访问华东交通大学教务系统。
3. **成绩查询**：当前学期的成绩需要等学期结束后才能查看，`scores.today()` 返回的是上学期的成绩。
4. **频率限制**：请合理使用 API，避免频繁请求对服务器造成压力。

## 完整示例

```python
from ecjtu import ECJTU

def main():
    # 创建客户端并登录
    client = ECJTU(stud_id="你的学号", password="你的密码")
    
    try:
        client.login()
        print("登录成功！")
        
        # 获取今日课表
        print("\n=== 今日课表 ===")
        courses = client.scheduled_courses.today()
        if courses:
            for course in courses:
                print(f"{course.class_span}节 {course.course} - {course.teacher} - {course.class_room}")
        else:
            print("今天没有课程")
        
        # 获取绩点
        print("\n=== 绩点信息 ===")
        gpa = client.gpa.today()
        print(f"姓名: {gpa.student_name}, 绩点: {gpa.gpa}")
        
        # 获取成绩
        print("\n=== 上学期成绩 ===")
        scores = client.scores.today()
        for score in scores[:5]:  # 只显示前5门课程
            print(f"{score.course_name}: {score.grade} ({score.credit}学分)")
            
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    main()
```

## 更多信息

如果你在使用过程中遇到问题，请检查：

1. 学号和密码是否正确
2. 网络连接是否正常
3. 华东交通大学教务系统是否可以正常访问

祝你使用愉快！