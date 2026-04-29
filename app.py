from flask import Flask, render_template, request, send_file, jsonify
from datetime import datetime, time
import pandas as pd
import io

app = Flask(__name__)

# Simulación de base de datos de contratos (Luego se llena con el Excel)
CONTRATOS = {
    "CONT-001": {"cliente": "Empresa Alfa", "max_mbtu": 5000, "puntos": ["Mamonal", "Cartagena"]},
    "CONT-002": {"cliente": "Empresa Beta", "max_mbtu": 2000, "puntos": ["Aguachica"]}
}

nominaciones_db = [] # Aquí se guardarán temporalmente

def get_status_ventana():
    ahora = datetime.now().time()
    # Para pruebas, puedes comentar estas líneas o ajustarlas
    limite = time(16, 0)
    apertura_reno = time(17, 0)
    
    if ahora <= limite: return "ABIERTA"
    if limite < ahora < apertura_reno: return "BLOQUEADA"
    return "RENOMINACION"

@app.route('/')
def index():
    return render_template('index.html', status=get_status_ventana())

@app.route('/nominar', methods=['POST'])
def nominar():
    data = request.json
    status = get_status_ventana()
    
    # Validación de seguridad de última hora
    if status == "BLOQUEADA":
        return jsonify({"error": "Ventana cerrada por proceso de confirmación"}), 403
    
    # Validación de cantidad MBTU
    contrato = CONTRATOS.get(data['contrato'])
    if float(data['cantidad']) > contrato['max_mbtu']:
        return jsonify({"error": f"Excede el límite del contrato ({contrato['max_mbtu']} MBTU)"}), 400

    data['fecha_registro'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['estado'] = "En Proceso"
    nominaciones_db.append(data)
    
    return jsonify({"message": "Nominación recibida correctamente", "data": data})

@app.route('/exportar')
def exportar():
    df = pd.DataFrame(nominaciones_db)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Nominaciones')
    output.seek(0)
    return send_file(output, attachment_filename="nominaciones_geam.xlsx", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
