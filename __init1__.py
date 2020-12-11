#THIS IS A WEBSERVER FOR DEMONSTRATING THE TYPES OF RESPONSES WE SEE FROM AN API ENDPOINT
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from database_setup import Base, UTCBTC, Requests, Pages
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from flask import make_response
import random
import json
import string
import requests
from io import BytesIO
from flask import send_file
from openpyxl import Workbook
import getpass
from datetime import datetime
from sqlalchemy import desc
import uuid
app = Flask(__name__)

engine = create_engine('sqlite:///btc.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()






@app.route('/btc')
def bigtvJSON():
    candles = session.query(UTCBTC).all()
    session.close()
    return jsonify(BTC_USD_CANDLES=[r.serialize for r in candles])

#GET REQUEST[1607546940, 18271.68, 18278.38, 18278.38, 18276.12, 19.17194255]

@app.route('/')
@app.route('/admin')
@app.route('/home')
def homefun():
    try:
        last_request = session.query(UTCBTC).order_by(desc('id')).first()
        session.close()
        pdate = last_request.request_date
    except:
        pdate= 'Requests List is Empty'
    return render_template('index.html', pdate=pdate)


@app.route('/api', methods=['POST'])
def getRequestHello():
    db_list = []


    try:
        if request.form['start'] and request.form['stop']:
            print('Data Sent To server')
        else:
            ermessage = "Please Enter A valid start and stop dates, Do not  Use Inspect aginst my the form"
            return render_template('index.html', pdate=pdate, error=ermessage)
        start_date = '%s' % request.form['start']
        stop_date = '%s' % request.form['stop']
        baseurl = 'https://api.pro.coinbase.com/products/BTC-USD/candles'
        req_id = uuid.uuid1()
        #start_date = '2018-07-10T08:00:00'
        #stop_date = '2018-07-15T12:00:00'
        r =requests.get('https://api.pro.coinbase.com/products/BTC-USD/candles', params={'start':start_date,'stop':stop_date})
        full_url = baseurl + '?start='  + start_date + '&stop=' + stop_date
        r_status = r.status_code
        response_json = r.json()
        r.close()
        # datetime object containing current date and time
        now = datetime.now()
        print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("request made at :", dt_string)
        #return str(response_json[0])
        for alist in response_json:
            len_list = len(alist)
            if len_list == 6:
                change = ((alist[2] - alist[1]) / alist[1]) * 100
                p_time = int(alist[0])
                p_low = int(alist[1])
                p_high = int(alist[2])
                p_open = int(alist[3])
                p_close = int(alist[4])
                p_volume = int(alist[5])
                newItem = UTCBTC(url=full_url, start=start_date, stop=stop_date,status=r_status, time=p_time, low=p_low, high=p_high,
                open=p_open, close=p_close, volume=p_volume,change=change,request_date=dt_string)
                session.add(newItem)
                message = 'candels with Change: %s Added Successfuly' % newItem.change
                session.commit()
                session.close()
                print(message)
                notification_message = "Successfully Got All UTC-BTC Candles"
                flash(message)
                return redirect(url_for('homefun'))
            else:
                continue
                #print(error)
                #return len(alist)  + str(alist)
            # test the data

        #return str(r.content)
    except Exception as e:
        now = datetime.now()
        print("now =", now)
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        return str(e)
        ermessage = "Could Not Send Your Request Please try Again After 2 Minutes, thank you."
        return render_template('index.html', pdate=dt_string, error=ermessage)
    return False


@app.route('/candels_csv', methods = ['GET'])
def return_csv():
    candles = session.query(UTCBTC).all()
    excel_indexer = 1
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = "Prev Price"
    sheet['B1'] = "Last Price"
    sheet['C1'] = "time"
    sheet['D1'] = "Open"
    sheet['F1'] = "Close"
    sheet['G1'] = "volume"
    sheet['H1'] = "change"
    for i in candles:
        excel_indexer += 1
        indexing_a = "A" + str(excel_indexer)
        indexing_b = "B" + str(excel_indexer)
        indexing_c = "C" + str(excel_indexer)
        indexing_d = "D" + str(excel_indexer)
        indexing_f = "F" + str(excel_indexer)
        indexing_g = "G" + str(excel_indexer)
        indexing_h = "H" + str(excel_indexer)
        sheet[indexing_a] = i.low
        sheet[indexing_b] = i.high
        sheet[indexing_c] = i.time
        sheet[indexing_d] = i.open
        sheet[indexing_f] = i.close
        sheet[indexing_g] = i.volume
        sheet[indexing_h] = i.change
    workbook.save(filename="hello_world1.xlsx")
    return 'create /GET enpoint which would return historical data by date range.<br> \
     This /GET endpoint should support both json and csv response <br> <a href="localhost:5000/static/hello_world.xlsx">Download Link</a>'
#POST REQUEST
@app.route('/', methods = ['GET'])
def home():
	return "This IS BTC API"

#POST REQUEST
@app.route('/createHello', methods = ['POST'])
def postRequestHello():
	return "I see you sent a POST message :-)"
#UPDATE REQUEST
@app.route('/updateHello', methods = ['PUT'])
def updateRequestHello():
	return "Sending Hello on an PUT request!"

#UPDATE REQUEST
@app.route('/patchhello', methods = ['PATCH'])
def patchRequestHello():
	return "Sending Hello on an PUT request!"


#DELETE REQUEST
@app.route('/deleteHello', methods = ['DELETE'])
def deleteRequestHello():
	return "Deleting your hard drive.....haha just kidding! I received a DELETE request!"

if __name__ == '__main__':
    app.secret_key = 'S&Djry636qyye21777346%%^&&&#^$^^y___'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
