from flask import Flask, render_template
import routes.test_route as rt
import opencv.models.cam_server as cam

app = Flask(__name__, template_folder="templates")

#생성한 블루프린트 등록
app.register_blueprint(rt.bp)

@app.route('/')
def home() :
    return render_template("/index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()#flask 서버 실행