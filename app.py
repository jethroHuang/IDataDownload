from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import idata

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    db = request.args.get('db', 'SCDB')  # SCDB 为综合数据库
    keyword = request.args.get('keyword', '')
    start = request.args.get('start', '0')
    result = idata.search(keyword, db, start)
    if result['status'] == 0:
        return '接口出错: ' + result['message']
    items = result['data']['items']
    total = result['data']['total_count']
    start = result['data']['start']
    args = dict(request.args)
    for i in args:
        args[i] = args[i][0]
    args['start'] = start
    return render_template('list.html', items=items, total=total, args=args)


@app.route('/detail')
def detail():
    filename = request.args.get('filename')
    dbcode = request.args.get('dbcode')
    if not (filename or dbcode):
        return '缺失必要参数：filename, dbcode'
    res = idata.get_detail(filename, dbcode)
    if res['status'] == 0:
        return '接口出错: ' + res['message']
    detaill = res['data']  # type:dict

    # 拼接作者列表
    detaill['author'] = ','.join([i['name'] for i in detaill.get('author') or []])
    # 拼接单位列表
    detaill['orgniz'] = ','.join([i['name'] for i in detaill.get('orgniz') or []])
    # 拼接导师列表
    detaill['tutor'] = ','.join([i['name'] for i in detaill.get('tutor') or []])
    # 拼接关键字列表
    detaill['kws'] = ','.join(detaill['kws'] or [])

    return render_template('detail.html', detail=detaill)


@app.route('/download_url')
def download():
    filename = request.args.get('filename')
    filename_en = request.args.get('filename_en')
    title = request.args.get('title')
    tablename = request.args.get('tablename')

    res = idata.get_durl(filename, filename_en, title, tablename)
    if res['status'] == 0:
        return '接口出错: ' + res['message']
    if res['data']['durl']:
        return redirect(res['data']['durl'])
    else:
        return redirect(res['data']['url'])

if __name__ == '__main__':
    app.run()
