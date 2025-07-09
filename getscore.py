import requests
import os

def get_score():
    """
    通过POST请求向UESTC教务系统查询成绩。
    从环境变量中读取 COOKIE, XNM (学年), XQM (学期)。
    """
    # 从环境变量中获取敏感信息和查询参数
    COOKIE = os.environ.get('COOKIE')
    XNM = os.environ.get('XNM')
    XQM = os.environ.get('XQM')
    
    # 检查环境变量是否设置
    if not all([COOKIE, XNM, XQM]):
        print("错误: 请确保设置了 COOKIE, XNM, 和 XQM 环境变量。")
        return None

    # 请求的API地址
    url = "https://eams.uestc.edu.cn/eams/teach/grade/course/person!search.action?semesterId=463&projectType="
    
    # POST请求的表单数据
    data = {
        "xnm": XNM,
        "xqm": XQM,
        "queryModel.showCount": "100",  # 查询数量，设置为100以获取所有成绩
    }
    
    # 根据你提供的最新信息更新请求头
    # 注意：Host, Origin, Referer, User-Agent等都已更新为 eams.uestc.edu.cn 相关信息
    headers = {
        # 核心请求头，指明我们希望接收JSON数据
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Cookie": COOKIE,
        "Host": "eams.uestc.edu.cn",
        "Origin": "https://eams.uestc.edu.cn",
        # Referer更新为查询成绩的页面，这对于防止CSRF很重要
        "Referer": "https://eams.uestc.edu.cn/eams/teach/grade/course/person.action",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        # 更新为移动端User-Agent
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        # 表明这是一个AJAX请求
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
    }
    
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=data, timeout=10)
        # 检查响应状态码
        response.raise_for_status()  # 如果状态码不是 2xx，将引发HTTPError
        
        # 解析返回的JSON数据
        score_data = response.json()
        return score_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None
    except requests.exceptions.JSONDecodeError:
        print("解析JSON失败，收到的响应可能不是有效的JSON格式。")
        print("收到的内容:", response.text)
        return None

# --- 使用示例 ---
# 在运行前，请确保在你的环境中设置了以下变量
# export COOKIE='你的cookie字符串'
# export XNM='2023'  # 替换为你想查询的学年
# export XQM='3'     # 替换为你想查询的学期（3代表第一学期，12代表第二学期）

if __name__ == '__main__':
    scores = get_score()
    if scores:
        print("成功获取到成绩数据:")
        # 这里可以添加处理和展示成绩数据的代码
        # 例如，打印出课程名称和成绩
        if 'items' in scores and scores['items']:
            for item in scores['items']:
                course_name = item.get('courseName')
                grade_score = item.get('gradeScore')
                print(f"课程: {course_name}, 成绩: {grade_score}")
        else:
            print("未找到成绩项目或返回数据格式不符。")
            print("完整响应:", scores)
