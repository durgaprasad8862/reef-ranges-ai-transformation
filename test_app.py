import os,tempfile,importlib,sys

def setup_module():
 global mod,tmp
 tmp=tempfile.TemporaryDirectory();os.environ['REEF_DB']=tmp.name+'/test.db';os.environ['ADMIN_PASSWORD']='test-only-password';sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','app'));mod=importlib.import_module('main')

def teardown_module():tmp.cleanup()

def test_enquiry_and_escalation():
 c=mod.app.test_client();r=c.post('/api/enquiries',json={'name':'Sample','email':'test@example.invalid','message':'I need a refund'});assert r.status_code==201;assert r.json['status']=='needs_review'

def test_admin_access():
 c=mod.app.test_client();assert c.get('/admin/enquiries').status_code==401;assert c.post('/login',json={'password':'test-only-password'}).status_code==200;assert c.get('/admin/enquiries').status_code==200

def test_capacity():
 c=mod.app.test_client();c.post('/login',json={'password':'test-only-password'})
 for n,guests in enumerate([8,5]):
  e=c.post('/api/enquiries',json={'name':'Demo','email':'demo@example.invalid','message':'Book reef tour'}).json['id']
  r=c.post('/admin/bookings',json={'enquiry_id':e,'tour':'reef','tour_date':'2027-01-15','guests':guests});assert r.status_code==([201,409][n])

def test_faq():
 c=mod.app.test_client();assert c.get('/api/faq?topic=weather').json['human_review'] is False
