from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)


# 企业微信 测试 webhook
WECHAT_WEBHOOK_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cd0e17a9-ecfe-4a2d-942e-4bcf873cb76c'

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/alert', methods=['POST'])
def alert():
    # 获取阿里云云监控的告警消息
    alert_data = request.json
    logger.info(f"Received alert: {alert_data}")


    # 处理告警消息并发送到企业微信
    send_to_wechat(alert_data)

    return jsonify({"status": "success"}), 200


def send_to_wechat(alert_data):
    # 构建企业微信消息
    wechat_message = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"**告警信息**\n\n**告警名称:** {alert_data['alertName']}\n**告警级别:** {alert_data['severity']}\n**告警详情:** {alert_data['alertDescription']}"
        }
    }

    # 发送消息到企业微信
    response = requests.post(WECHAT_WEBHOOK_URL, json=wechat_message)
    if response.status_code != 200:
        print(f"Failed to send message to WeChat: {response.text}")
