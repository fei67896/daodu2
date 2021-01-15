import pickle
import os
from flask import Flask, request, json
from flask_cors import CORS

import readvec
from qsresouce import *

Smartguide_hotel_queList = []
Smartguide_hotel_ansList = []
readQSresouce('corpus/smartguide_hotel_2.0.txt', Smartguide_hotel_queList, Smartguide_hotel_ansList)  # 读取物流沙盘语料库

StopWord_list = []
readQSresouce('corpus/stopword.txt', StopWord_list, StopWord_list)
# 停用词读取

with open('newembedding.pickle', 'rb') as handle:
    vectors = pickle.load(handle)
# 用vectors从embedding.pickle中读取全部词向量

#####################酒店沙盘智能导读接口######################
app = Flask(__name__)
CORS(app)


@app.route("/smartguide_hotel_Q")
def smartguide_hotel_Q():
    tmpcontent = request.args.get('content')
    content = tmpcontent.replace('\n', '')
    answer = readvec.getQ(content, vectors, Smartguide_hotel_queList, Smartguide_hotel_ansList)
    ##Log##
    Logfile = open("Log/HistorySmartguide_hotel.txt", "a")
    Logfile.write(content)
    Logfile.write("\n")
    Logfile.write(answer)
    Logfile.write("\n")
    Logfile.close()
    print(content)
    print(answer)
    print("#####################")
    return json.dumps({'as': answer})


@app.route("/smartguide_hotel_A")
def smartguide_hotel_A():
    tmpcontent = request.args.get('content')
    content = tmpcontent.replace('\n', '')
    answer = readvec.getA(content, vectors, Smartguide_hotel_queList, Smartguide_hotel_ansList)
    ##Log##
    Logfile = open("Log/HistorySmartguide_hotel.txt", "a")
    Logfile.write(content)
    Logfile.write("\n")
    Logfile.write(answer)
    Logfile.write("\n")
    Logfile.close()
    print(content)
    print(answer)
    print("#####################")
    return json.dumps({'as': answer})


# if __name__ == '__main__':
#     # app.run()
#     app.run(debug=True)
#    # debug=True,debug模式会产生双倍的内存消耗

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=False)
