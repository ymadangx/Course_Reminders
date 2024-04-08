import datetime
import time
import schedule
import requests
import json

appID = ""
appSecret = ""
openId = ""
weather_template_id = ""
timetable_template_id = ""

timetable = {
    1: ["课程：智能物联网 地点：3219 时间：8-00", "课程：微信移动应用开发 地点：3113 时间：10-00",
        "课程：计算机网络安全管理 地点：1513 时间：14-00", "课程：UNI-app开发技术 地点：1315 时间：16-00"],
    2: ["课程：大数据分析与应用 地点：1319 时间：8-00", None, None, "课程：中国近代史纲要 地点：3314 时间：16-00"],
    3: [None, None, "课程：软件工程 地点：1319 时间：14-00", None],
    4: [None, None, "课程：计算机网络安全管理 地点：1513 时间：14-00", None],
    5: [None, "课程：大数据分析与应用 地点：1319 时间：10-00", None, None],
}


def get_access_token():
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(
        appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    access_token = response.get('access_token')
    return access_token


def send_notification(message):
    access_token = get_access_token()
    body = {
        "touser": openId,
        "template_id": timetable_template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "message": {
                "value": message
            },
        }
    }
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    requests.post(url, json.dumps(body))


def course_reminder():
    today = datetime.datetime.today().weekday()
    current_time = datetime.datetime.now().time()
    courses = timetable.get(today, [])
    for course in courses:
        if course is not None:
            start_time_str = course.split("时间：")[1]
            start_time = datetime.datetime.strptime(start_time_str, "%H-%M").time()
            if current_time >= start_time - datetime.timedelta(minutes=30) and current_time <= start_time:
                send_notification(f"课程提醒：{course}")


if __name__ == '__main__':
    schedule.every().monday.at("07:30").do(course_reminder)
    schedule.every().monday.at("09:30").do(course_reminder)
    schedule.every().monday.at("13:30").do(course_reminder)
    schedule.every().monday.at("15:30").do(course_reminder)

    while True:
        schedule.run_pending()
        time.sleep(1800)
