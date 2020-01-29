from flask import Flask, g, make_response, Response, request, session
from datetime import datetime, date, timedelta
from flask import render_template, Markup
app = Flask(__name__)
app.debug = True
# app.jinja_env.trim_blocks = True

app.config.update(
    SECRET_KEY= "AERGLIM13",
    SESSION_COOKIE_NAME="pyweb_flask_session",
    PERMANENT_SESSION_LIFETIME=timedelta(31)
)
class Nav:
    def __init__(self, title, url="", children=[]):
        self.title = title
        self.url = url
        self.children = children
@app.route("/main")
def main():
    return render_template("main.html", main_title="WOW_MAIN")
@app.route("/tmpl3")
def tmpl3():
    py=Nav("파이썬","https://naver.com")
    java=Nav("자바","https://naver.com")
    t_prg=Nav("프로그래밍 언어","https://naver.com",[py,java])

    jinja=Nav("jinja","https://naver.com")
    gc=Nav("hhhh,dddd""","https://naver.com")   
    flask=Nav("플라스크","https://naver.com",[jinja,gc])
    
    spr=Nav("스프링","https://naver.com")
    ndjs=Nav("노드JS","https://naver.com")
    t_webf=Nav("프로그래밍 언어","https://naver.com",[flask,spr,ndjs])
    
    my=Nav("나의일상","https://naver.com")
    issue=Nav("이슈 게시판","https://naver.com")
    t_other=Nav("기타","https://naver.com",[my,issue])

    return render_template("index.html" , navs=[t_prg,t_webf,t_other])

@app.route("/tmpl")
def tmpl():
    lst = [("김건모", "만남"), ("노사연", "만남")]
    return render_template("index.html", title = Markup("<strong>title<strong>"), lst=lst)

@app.route('/setsess')
def setsess():
    session['Token'] = '123x'
    return "Session 이 설정되었습니다."
@app.route("/getsess")
def getsess():
    return session.get('Token')

@app.route("/delsess")
def delsess():
    if session.get("Token"):
        del session['Token']
    return "Session 이 삭제되었습니다."

@app.route('/wc')
def wc():
    key = request.args.get("key")
    val = request.args.get("val")
    res = Response("set Cookie")
    res.set_cookie(key, val)
    return make_response(res)

@app.route("/rc")
def rc():
    key = request.args.get('key')
    val = request.cookies.get(key)
    return val

@app.route("/reqenv")
def reqenv():
    return ('REQUEST_METHOD : %(REQUEST_METHOD) s <br>'
            'PATH_INFO : %(PATH_INFO) s <br>') % request.environ

def ymd(fmt):
    def trans(date_str):   
        return datetime.strptime(date_str, fmt)
    return trans

@app.route("/dt")
def dt():
    datestr = request.values.get("data", date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식" + str(datestr)

@app.route("/rp")
def rp():
    # q = request.args.get("q")
    q = request.args.getlist('q')
    return 'q= %s' % str(q)

@app.route("/")
def helloworld():
    return "Hello world"

@app.route("/test")
def test():
    return "Hello World" + getattr(g, 'str', '111')
    
@app.before_request
def before_request():
    print("Before_request!!")
    g.str="한글"

@app.route("/response")
def response_test():
    custom_res = Response("custom Response", 200, {"test":'ttt'})
    return make_response(custom_res)

@app.route("/test_wsgi")
def wsgi_test():
    def application(environ, start_response):
        body = 'the request method was %s' % environ['REQUEST_METHOD']
        headers = [('Content-Type', 'text/plain'),
                    ('Content-Length', str(len(body)))]
        start_response('200', headers)
        return [body]
    return make_response(application)