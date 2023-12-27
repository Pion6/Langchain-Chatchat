from flask import Flask, request

app = Flask(__name__)


@app.route("/school/sheet/<parm1>/<parm2>", methods=['GET'])
def handle_request(parm1, parm2):
    # 这里是你的接口逻辑，你可以访问参数parm1和parm2

    # 示范返回参数值
    # return "Parameter 1: {}, Parameter 2: {}".format(parm1, parm2)
    return f"用户名为{parm1},时间为{parm2},今天有两节算法设计与分析的课程，今天晚上有两节深度学习技术与实践的课程"


if __name__ == "__main__":
    app.run(host="10.12.54.64", port=5000)