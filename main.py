import os, sqlite3, secrets, json
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string, session
from werkzeug.security import check_password_hash, generate_password_hash

app=Flask(__name__)
app.secret_key=os.environ.get('SESSION_SECRET', secrets.token_hex(32))
DB=os.environ.get('REEF_DB','reef_ranges.db')
TOURS={'reef':'Great Barrier Reef Discovery','ranges':'Rainforest & Ranges Explorer'}
CAPACITY={'reef':12,'ranges':8}
FAQ={'pickup':'Pickup details are confirmed by staff after booking. Please check your confirmation.', 'bring':'Bring sun protection, water, comfortable shoes, and a reusable water bottle.', 'weather':'Weather-related cancellations and refunds require staff confirmation. We never guarantee a departure in unsafe conditions.'}

def conn():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c

def init_db():
 with conn() as c:
  c.execute('CREATE TABLE IF NOT EXISTS enquiries(id INTEGER PRIMARY KEY, name TEXT, email TEXT, message TEXT, category TEXT, status TEXT, created_at TEXT)')
  c.execute('CREATE TABLE IF NOT EXISTS bookings(id INTEGER PRIMARY KEY, enquiry_id INTEGER, tour TEXT, tour_date TEXT, guests INTEGER, status TEXT, created_at TEXT)')
  c.execute('CREATE UNIQUE INDEX IF NOT EXISTS uq_booking_enquiry ON bookings(enquiry_id)')

def classify(message):
 t=message.lower()
 if any(w in t for w in ['refund','cancel','allergy','medical','wheelchair','emergency','complaint']):return 'human_review'
 if any(w in t for w in ['book','reserve','availability','seat']):return 'booking'
 if any(w in t for w in ['pickup','bring','weather']):return 'faq'
 return 'human_review'

@app.before_request
def protect():
 if request.path.startswith('/admin') and not session.get('admin'):
  return jsonify(error='Sign in required'),401

@app.get('/')
def home():
 return render_template_string('''<!doctype html><html lang="en"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Reef & Ranges Tours</title><style>body{font:16px system-ui;background:#f0f7f8;color:#14343a;margin:0}header{background:#075f68;color:white;padding:35px max(5%,calc((100% - 900px)/2))}main{max-width:900px;margin:30px auto;padding:0 20px}.panel{background:white;border-radius:14px;padding:25px;margin-bottom:18px;box-shadow:0 4px 18px #173a4015}input,textarea,select,button{display:block;width:100%;box-sizing:border-box;padding:12px;margin:8px 0 16px;border:1px solid #abc;border-radius:8px;font:inherit}button{background:#007f83;color:white;border:0;cursor:pointer}small{color:#53666a}</style><header><h1>Reef & Ranges Tours</h1><p>Explore Cairns, the reef and the rainforest • Fictional demonstration</p></header><main><div class="panel"><h2>Ask about a tour</h2><p>Our team reviews all enquiries. This demonstration does not send emails or accept payments.</p><form id="f"><label>Name<input name="name" required maxlength="80"></label><label>Email<input type="email" name="email" required maxlength="120"></label><label>Question<textarea name="message" required maxlength="2000"></textarea></label><button>Send enquiry</button></form><p id="result" role="status"></p></div><div class="panel"><h2>Quick answers</h2><p><b>What should I bring?</b> Sun protection, water and comfortable shoes.</p><p><b>Pickup and weather?</b> Staff confirm pickup details and any weather-related changes.</p></div><small>All business information is illustrative. Never enter real customer information.</small></main><script>document.getElementById('f').onsubmit=async e=>{e.preventDefault();let d=Object.fromEntries(new FormData(e.target));let r=await fetch('/api/enquiries',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});let j=await r.json();document.getElementById('result').textContent=r.ok?'Enquiry #'+j.id+' received. Status: '+j.status:(j.error||'Unable to submit');if(r.ok)e.target.reset()}</script></html>''')

@app.post('/api/enquiries')
def enquiry():
 d=request.get_json(silent=True) or {};name=str(d.get('name','')).strip();email=str(d.get('email','')).strip();msg=str(d.get('message','')).strip()
 if not name or len(name)>80 or not email or len(email)>120 or '@' not in email or not msg or len(msg)>2000:return jsonify(error='Valid name, email and message required'),400
 category=classify(msg);status='needs_review' if category=='human_review' else 'new'
 with conn() as c:
  cur=c.execute('INSERT INTO enquiries(name,email,message,category,status,created_at) VALUES(?,?,?,?,?,?)',(name,email,msg,category,status,datetime.now(timezone.utc).isoformat()));i=cur.lastrowid
 return jsonify(id=i,category=category,status=status),201

@app.post('/login')
def login():
 d=request.get_json(silent=True) or {};password=os.environ.get('ADMIN_PASSWORD')
 if not password or not secrets.compare_digest(str(d.get('password','')),password):return jsonify(error='Invalid login or admin not configured'),401
 session['admin']=True;return jsonify(ok=True)

@app.post('/logout')
def logout():session.clear();return jsonify(ok=True)

@app.get('/admin/enquiries')
def list_enquiries():
 with conn() as c:return jsonify([dict(x) for x in c.execute('SELECT * FROM enquiries ORDER BY id DESC')])

@app.post('/admin/bookings')
def book():
 d=request.get_json(silent=True) or {}
 try:enquiry_id=int(d.get('enquiry_id'));guests=int(d.get('guests'));tour=d.get('tour');date=d.get('tour_date');datetime.strptime(date,'%Y-%m-%d')
 except (ValueError,TypeError):return jsonify(error='Invalid booking fields'),400
 if tour not in TOURS or guests<1 or guests>CAPACITY[tour]:return jsonify(error='Invalid tour or party size'),400
 with conn() as c:
  c.execute('BEGIN IMMEDIATE')
  if not c.execute('SELECT id FROM enquiries WHERE id=?',(enquiry_id,)).fetchone():return jsonify(error='Enquiry not found'),404
  used=c.execute("SELECT COALESCE(SUM(guests),0) FROM bookings WHERE tour=? AND tour_date=? AND status='confirmed'",(tour,date)).fetchone()[0]
  if used+guests>CAPACITY[tour]:return jsonify(error='Not enough seats; request staff review'),409
  try:
   cur=c.execute('INSERT INTO bookings(enquiry_id,tour,tour_date,guests,status,created_at) VALUES(?,?,?,?,?,?)',(enquiry_id,tour,date,guests,'confirmed',datetime.now(timezone.utc).isoformat()))
  except sqlite3.IntegrityError:return jsonify(error='This enquiry already has a booking'),409
  return jsonify(id=cur.lastrowid,status='confirmed'),201

@app.get('/admin/report')
def report():
 with conn() as c:
  return jsonify(enquiries=c.execute('SELECT COUNT(*) FROM enquiries').fetchone()[0],pending_review=c.execute("SELECT COUNT(*) FROM enquiries WHERE status='needs_review'").fetchone()[0],confirmed_bookings=c.execute("SELECT COUNT(*) FROM bookings WHERE status='confirmed'").fetchone()[0])

@app.get('/api/faq')
def faq():
 topic=request.args.get('topic','').lower();return jsonify(answer=FAQ.get(topic,'A team member will review your question.'),human_review=topic not in FAQ)

init_db()
if __name__=='__main__':app.run(host='127.0.0.1',port=5000,debug=False)
