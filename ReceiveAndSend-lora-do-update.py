import sys, getopt
from flask import Flask
from flask import request
from flask import Response
import base64
import pprint
import json
import requests

from Adafruit_IO import Client
aio = Client("username", "my_key")
# username for adafruit login
# my_key = AIO key

app = Flask(__name__)

app.debug = True


@app.route('/lns', methods=['POST'])
def get_from_LNS():

    fromGW = request.get_json(force=True)
    print ("HTTP POST RECEIVED")
    pprint.pprint(fromGW)
    if "data" in fromGW:
        payload = base64.b64decode(fromGW["data"])
        print (payload)
        payload = json.loads(str(payload[2:-1]))
        # send to Adafruit IO feeds
        for kei in payload :
            aio.send_data(key, float(payload[key]))

        github_repo = "https://github.com/ThomasRoeder/Projet_S5"
        github_repo = github_repo.rstrip('/').replace('https://github.com',  'https://api.github.com/repos')
        latest_release = requests.get(github_repo + '/releases/latest')
        version = latest_release.json()['tag_name']
        latest_release.close()

        replyDict = { "message": "ok", "version": version}
        replyStr = json.dumps(replyDict)
        answer = {
          "fPort" : fromGW["fPort"],
          "devEUI": fromGW["devEUI"],
          "data"  : base64.b64encode(bytes(replyStr, 'utf-8')).decode('utf-8')
        }

        print()
        print ("HTTP POST REPLY")
        pprint.pprint(answer)
        resp = Response(response=json.dumps(answer), status=200, mimetype="application/json")
        print (resp)
        return resp

if __name__ == '__main__':
    print (sys.argv)

    defPort=7009
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hp:",["port="])
    except getopt.GetoptError:
        print ("{0} -p <port> -h".format(sys.argv[0]))
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ("{0} -p <port> -h".format(sys.argv[0]))
            sys.exit()
        elif opt in ("-p", "--port"):
            defPort = int(arg)


    app.run(host="0.0.0.0", port=defPort)
