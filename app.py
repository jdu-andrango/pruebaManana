from flask import Flask, send_file,jsonify, request
from psycopg2 import connect,extras

app= Flask(__name__)

host='localhost'
port=5432
database='flaskJonathan'
user='postgres'
password='david'

def getConexion():
    conexion= connect(host=host,port=port,database=database,user=user,password=password)
    return conexion


@app.get('/')
def index():
    return send_file('static/index.html')

@app.get('/jonathan/automovil')
def automovil():
    conexion=getConexion()
    curSor=conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM automovil')
    automovil= curSor.fetchall()
    curSor.close()
    conexion.close()
    return jsonify(automovil)

@app.post('/jonathan/automovil')
def enviarAutomovil():
    
    nuevoAutomovil= request.get_json()
    
    marca = nuevoAutomovil['marca']
    modelo = nuevoAutomovil['modelo']
    fecha=nuevoAutomovil['fecha']
    duenos=nuevoAutomovil['duenos']
    costos=nuevoAutomovil['costos']
    choques=nuevoAutomovil['choques']
    
    conexion=getConexion()
    curSor=conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('INSERT INTO automovil (marca, modelo, fecha, duenos, costos, choques) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *',(marca, modelo, fecha, duenos, costos, choques))
    newAutomovil= curSor.fetchone()
    conexion.commit()
    curSor.close()
    conexion.close()
    
    
    return jsonify(newAutomovil)



@app.get('/jonathan/automovil/<id>')
def traerAutomoviles(id):
    
    
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    
    curSor.execute('SELECT * FROM automovil WHERE id = %s ', (id, ))
    traerAutomovil=curSor.fetchone()
    
    
    if traerAutomovil is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    print (traerAutomovil)
    return jsonify(traerAutomovil)
    

@app.delete('/jonathan/automovil/<id>')
def deleteAutomovil(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)

   
    curSor.execute('DELETE FROM automovil WHERE id = %s RETURNING *', (id, ))
    automovilEliminado=curSor.fetchone()
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if automovilEliminado is None:
        return jsonify({'message':'usyuario no encontrado'}),404
    
    return jsonify(automovilEliminado)


@app.put('/jonathan/automovil/<id>')
def updateAutomovil(id):
    conexion = getConexion()
    curSor = conexion.cursor(cursor_factory=extras.RealDictCursor)


    newAutomovil= request.get_json()
   
    marca = newAutomovil['marca']
    modelo= newAutomovil['modelo']
    fecha= newAutomovil['fecha']
    duenos= newAutomovil['duenos']
    costos= newAutomovil['costos']
    choques= newAutomovil['choques']
    
    curSor.execute('UPDATE automovil SET marca= %s, modelo= %s, fecha= %s, duenos= %s,costos= %s,choques= %s WHERE id=%s RETURNING *',(marca, modelo, fecha, duenos, costos, choques,id))
    automovilActualizado=curSor.fetchone()
    
    conexion.commit()
    
    curSor.close()
    conexion.close()
    
    if automovilActualizado is None:
        return jsonify({'message':'automovil no encontrado'}),404
    

    return jsonify(automovilActualizado)


if __name__=='__main__':
    app.run(debug=True)