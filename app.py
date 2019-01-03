from flask import Flask
from flask import render_template,request
from flask_cors import *
import sys,os
sys.path.append(os.getcwd())
from gevent import monkey
from gevent.pywsgi import WSGIServer
from hbjsrw import hbjsrwcx
from cxy import cxycx
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def hbjswm():
    return render_template("hbjsrw.html")

@app.route('/3/',methods=["POST"])
def hblongs():
    cph = request.form.get("cph")
    b = hbjsrwcx.hbjsrw1(cph=cph)
    return b

@app.route('/cxy/')
def cxy():
    return render_template("cxy.html")

@app.route('/2/',methods=["POST"])
def cxylongs():
    cph = request.form.get("cph")
    sbm = request.form.get("sbm")
    b = cxycx.cxy(cph=cph, sbm=sbm)
    return b

@app.route('/0/',methods=["POST"])
def apilongs():


    channel_id= request.form.get('channel_id')
    channel_ip= request.form.get('channel_ip')
    channel_memery_total= request.form.get('channel_memery_total')
    channel_memery_used= request.form.get('channel_memery_used')
    channel_disk_total= request.form.get('channel_disk_total')
    channel_disk_used= request.form.get('channel_disk_used')
    channel_province= request.form.get('channel_province')
    channel_bandwidth_total = request.form.get('channel_bandwidth_total')
    channel_bandwidth_used = request.form.get('channel_bandwidth_used')
    a = {
        "channel_province":channel_province,"channel_id":channel_id,"channel_ip":channel_ip,"channel_memery_total":channel_memery_total,
         "channel_memery_used":channel_memery_used,"channel_disk_total":channel_disk_total,"channel_disk_used":channel_disk_used,
         "channel_bandwidth_total":channel_bandwidth_total,"channel_bandwidth_used":channel_bandwidth_used
    }
    return json.dumps(a)

if __name__ == '__main__':
    # app.run(debug=False,host='0.0.0.0', port=8080)
    http_server = WSGIServer(('0.0.0.0', 8080), app)
    http_server.serve_forever()
