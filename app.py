from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from datetime import datetime, timedelta
import io

app = Flask(__name__)

# Lista en memoria para guardar nominaciones (se reinicia si el server se apaga en Render Free)
nominaciones = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    data = request.json
    contrato = data.get('contrato')
    cantidad = data.get('cantidad')
    fecha_nominacion = data.get('fecha') # Nueva fecha elegida por el usuario
    
    # --- Lógica de tiempo corregida ---
    # Usamos una hora de cierre amplia (11 PM) para evitar bloqueos por zona horaria en pruebas
    ahora = datetime.now()
    hora_limite = 23 # 11:00 PM
    
    if ahora.hour >= hora_limite and fecha_nominacion == ahora.strftime('%Y-%m-%d'):
        return jsonify({
            "status": "error", 
            "message": f"Ventana cerrada. Las nominaciones para hoy cierran a las {hora_limite}:00"
        })

    # Guardar la nominación
    nueva_nom = {
        "Fecha de Aplicación": fecha_nominacion,
        "Contrato": contrato,
        "Cantidad (MBTU)": cantidad,
        "Fecha de Registro": ahora.strftime("%Y-%m-%d %H:%M:%S")
    }
    nominaciones.append(nueva_nom)
    
    return jsonify({"status": "success", "message": "Nominación registrada exitosamente"})

@app.route('/descargar')
def descargar():
    if not nominaciones:
        return "No hay datos para descargar", 400
    
    df = pd.DataFrame(nominaciones)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Nominaciones')
    output.seek(0)
    
    return send_file(
        output,
        download_name=f"Reporte_GEAM_{datetime.now().strftime('%Y%m%d')}.xlsx",
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
