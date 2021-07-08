#Naming a file "app" will mean we don't have to (set FLASK_bp = name) when restarting command prompt
from flask import render_template, request, redirect, url_for, flash, abort, session, jsonify, Blueprint
import json, os.path
from werkzeug.utils import secure_filename

#Blueprint code directed towards __init__.py
bp = Blueprint('urlshort',__name__)

@bp.route('/') #Single slash means the base/home url
def home(): #127 and localhost are synonmous
    return render_template('home.html', codes=session.keys())

@bp.route('/your-url', methods=['GET', 'POST']) #Name of route and method can be different
def your_url():
    if request.method == 'POST':
        urls = {}
        #If statement to open json file if it exists
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)
        #If statement to avoid duplicate shortened names
        if request.form['code'] in urls.keys():
            #flash to show warning message
            flash('That short name has already been taken. Please select another name.')
            return redirect(url_for('urlshort.home'))
        #If/else statment to update urls dict in json file with url or file key
        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('/Users/mitri/Desktop/url-shortener/urlshort/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        #Creating JSON file to save shortened url and original url
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            #session stores user's shortened url as a cookie
            session[request.form['code']] = True
        #request.form for POST and request.args for GET
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('urlshort.home')) #home is a method

#Variable route to have shortened url redirect to original url
@bp.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))

    return abort(404)

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

#JSON API for the cookies(shortened urls user created)
@bp.route('/api')
def session_api():
    #jsonify takes any list or dictionary and converts it to JSON code
    return jsonify(list(session.keys()))
    

    

