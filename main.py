from kvsqlite.sync import Client
from flask import Flask, render_template, request, jsonify
import random, string
import time
db = Client('site.sqlite', 'niggers')
app = Flask(__name__)
@app.route('/')
def h():
  return render_template('index.html')
@app.route('/add', methods=['POST'])
def home():
  if request.method == 'POST':
    data = request.get_json()
    if not data.get('content'):
      return jsonify({'error': True, 'message': 'no "content" field found.'})
    content = data['content']
    if not content:
      return jsonify({'error':True, 'message':'"content" is empty.'})
    t = time.time()
    code = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(9))
    db.set(f'content_{code}', {"content": content, 'time': int(t), 'code': code})
    return jsonify({"content": content, 'time': int(t), 'code': code, 'error': False})
  else:
    return jsonify({'error':True, 'message': 'method not allowed.'})
@app.route('/raw/<id>')
def getPostAsRaw(id: str):
  x = db.get(f'content_{id}')
  if not x:
    return jsonify({'error': True, 'message': 'not found.'})
  return x['content']
app.run(host='0.0.0.0')