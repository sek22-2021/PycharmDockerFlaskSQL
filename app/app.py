from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oscarData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Oscar Data'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:Index>', methods=['GET'])
def record_view(Index):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale WHERE id=%s', Index)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:Index>', methods=['GET'])
def form_edit_get(Index):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale WHERE id=%s', Index)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:Index>', methods=['POST'])
def form_update_post(Index):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Index'), request.form.get('Year'), request.form.get('Age'), request.form.get('Name'),
                 request.form.get('Movie'), Index)
    sql_update_query = """UPDATE oscarAgeMale t SET t.Index = %s, t.Year = %s, t.Age = %s, t.Name = %s, t.Movie = 
    %s WHERE t.'Index' = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar Award Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Index'), request.form.get('Year'), request.form.get('Age'),
                 request.form.get('Name'), request.form.get('Movie'))
    sql_insert_query = """INSERT INTO oscarAgeMale (Index,Year,Age,Name,Movie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:Index>', methods=['POST'])
def form_delete_post(Index):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscarAgeMale WHERE Index = %s """
    cursor.execute(sql_delete_query, Index)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscar', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:Index>', methods=['GET'])
def api_retrieve(Index) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscarAgeMale WHERE Index=%s', Index)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:Index>', methods=['PUT'])
def api_edit(Index) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/oscar/<int:Index>', methods=['DELETE'])
def api_delete(Index) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)