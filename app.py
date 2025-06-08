from flask import Flask, render_template, request, url_for
import uuid

app = Flask(__name__)
links = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        show_url = request.form['show_url']
        yt_channel = request.form['yt_channel']
        yt_video = request.form['yt_video']
        uid = str(uuid.uuid4())[:8]
        links[uid] = {
            'url': show_url,
            'channel': yt_channel,
            'video': yt_video
        }
        return render_template('result.html', link=url_for('show', link_id=uid, _external=True))
    return render_template('index.html')

@app.route('/index.html')
def redirect_to_root():
    return redirect('/')

@app.route('/unlock', methods=['POST'])
def unlock():
    link_id = request.form.get('link_id')
    if not link_id or link_id not in links:
        return "Invalid unlock request", 400
    
    # Redirect to the original show_url
    return redirect(links[link_id]['url'])
    
@app.route('/show/<link_id>')
def show(link_id):
    data = links.get(link_id)
    if not data:
        return "Invalid Link"
    return render_template('show.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # Render uses PORT from environment, but this is fine for local
