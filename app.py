from flask import Flask, render_template, request, redirect, url_for
import uuid
from supabase import create_client, Client

# Supabase config
SUPABASE_URL = "https://ikxxvgflnpfyncnaqfxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlreHh2Z2ZsbnBmeW5jbmFxZnh4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDYxOTE3NTMsImV4cCI6MjA2MTc2Nzc1M30.YiF46ggItUYuKLfdD_6oOxq2xGX7ac6yqqtEGeM_dg8"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        show_url = request.form['show_url']
        yt_channel = request.form['yt_channel']
        yt_video = request.form['yt_video']
        uid = str(uuid.uuid4())[:8]
        
        # Save to Supabase
        supabase.table('links').insert({
            "id": uid,
            "url": show_url,
            "channel": yt_channel,
            "video": yt_video
        }).execute()

        return render_template('result.html', link=url_for('show', link_id=uid, _external=True))
    
    return render_template('index.html')

@app.route('/index.html')
def redirect_to_root():
    return redirect('/')

@app.route('/unlock', methods=['POST'])
def unlock():
    link_id = request.form.get('link_id')
    
    if not link_id:
        return "Invalid unlock request", 400

    # Fetch the link data from Supabase
    result = supabase.table('links').select("*").eq("id", link_id).execute()
    data = result.data[0] if result.data else None

    if not data:
        return "Invalid Link", 404

    # Redirect to the saved URL
    return redirect(data['url'])

@app.route('/show/<link_id>')
def show(link_id):
    result = supabase.table('links').select("*").eq("id", link_id).execute()
    data = result.data[0] if result.data else None

    if not data:
        return "Invalid Link", 404

    return render_template('show.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
