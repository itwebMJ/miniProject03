from flask import Blueprint, render_template, request, Response
import matplotlib.pyplot as plt
import os, cv2
import opencv.models.cam_server as cam

bp = Blueprint('test', __name__, url_prefix='/test')  #url 생성기

camera = cv2.VideoCapture(0)

def gen_frames():

    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            frame2 = cam.detect(frame)
            if frame2 is not None:
                frame = frame2
            ret, buffer = cv2.imencode('.jpg', frame)#jpg로 인코딩
            frame = buffer.tobytes()#이미지를 바이트로 변환
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/graph')
def graph():
    img_path = 'static/graph/my_plot.png'

    x = [1, 2, 3, 4]
    y = [3, 8, 5, 6]
    fig, _ = plt.subplots() #그래프 그릴 플랏 생성
    plt.plot(x, y) #그래프 그림
    fig.savefig(img_path) #그래프 이미지 파일로 저장
    img_path = '/' + img_path
    return render_template('test/test.html', img_path=img_path)

@bp.route('/upload')
def upload_form():
    return render_template('test/form.html')

@bp.route('/upload', methods=['POST'])
def upload():
    upload_path = 'static/img/'
    f = request.files['file']
    fname = upload_path+f.filename
    f.save(fname)
    fname = '/' + fname
    return render_template('test/test.html', img_path=fname)

@bp.route('/upload2', methods=['POST'])
def upload2():
    upload_path = 'static/img/'
    f = request.files['file']
    fname = upload_path+f.filename
    f.save(fname)
    title = request.form['title']
    print(title)

    return '업로드 완료'

@bp.route('/list')
def list():
    path = 'static/img/'
    files = os.listdir(path)
    print(files)
    return render_template('test/list.html', files=files)




@bp.route('/video_feed')#video_stream.html페이지 <img>의 src 요청
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/stream')    #클라이언트가 비디오 페이지 요청
def index():
    """Video streaming home page."""
    return render_template('video_stream.html')