from flask import Flask, request, redirect, render_template
import pypyodbc, json, random, string, os

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
# Configuración de la conexión a SQL Server
server = 'sql.bsite.net\MSSQL2016'
database = 'amhapi_urls'
username = 'amhapi_urls'
password = 'amhurls-123'
connstring = 'DRIVER={SQL Server Native Client 11.0};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
@app.route('/<id>')
def red(id):
     # Establecer la conexión a SQL Server
    conn = pypyodbc.connect(connstring)
    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()
    # Ejecutar la consulta SELECT
    cursor.execute("select urlo from urls where urlg = '"+id+"';")
    # Obtener los resultados de la consulta
    rows = cursor.fetchall()
    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()

    if len(rows)>0:
        return redirect(rows[0].urlo)
    else:
        return redirect("/page/notfound")

# Ruta de la página principal
@app.route('/api/url/generate',methods=['POST'])
def genurl():
    data = request.get_json()
    urlj = data["url"]
    # Establecer la conexión a SQL Server
    conn = pypyodbc.connect(connstring)
    # Crear un cursor para ejecutar consultas
    cursor = conn.cursor()
    # Ejecutar la consulta SELECT
    cursor.execute('select count(*) as num from urls')
    # Obtener los resultados de la consulta
    rows = cursor.fetchall()
    id = rows[0].num
    id = int(id);
    id = id+1
    urlgen = generaridurl(id)
    datares = {
        "url": "urlsh.ddns.net/"+urlgen
    }
    # Cerrar el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()
    regurlg(urlj,urlgen)
    # Establecer el encabezado de la respuesta como JSON
    response = app.response_class(
        response=json.dumps(datares),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/page/notfound")
def notfound():
    return render_template('notfound.html')


def generaridurl(id):
    # Crea una lista con letras mayúsculas y minúsculas 
    caracteres = string.ascii_letters
    # Genera una secuencia de 2 caracteres al azar
    secuencia = ''.join(random.choice(caracteres) for _ in range(2))
    return secuencia+str(id)

def regurlg(urlo,urlg):
    try:
        conn = pypyodbc.connect(connstring)
        # Crear un cursor para ejecutar consultas
        cursor = conn.cursor()
        cursor.execute("insert into urls(urlo,urlg) values('"+urlo+"','"+urlg+"');")
         # Confirma la transacción
        conn.commit()
    except pypyodbc.Error as e:
        # Si se produce un error, imprime el mensaje de error
        print(f"Error en la consulta SQL: {str(e)}")

    

if __name__ == '__main__':
     app.run(port=port)