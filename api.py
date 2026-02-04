# api.py
from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# ===================== DATOS =====================
PERSONAJES = {
    "rostro": {"sketch": 25000, "grises": 37000, "color": 55000, "full": 75000},
    "busto": {"sketch": 37000, "grises": 55000, "color": 75000, "full": 110000},
    "medio cuerpo": {"sketch": 55000, "grises": 74000, "color": 110000, "full": 167000},
    "cuerpo completo": {"sketch": 92000, "grises": 130000, "color": 185000, "full": 259000},
    "chibi": {"sketch": 30000, "grises": 44000, "color": 66000, "full": 93000}
}

ESCENARIOS = {
    "simple": {"sketch": 74000, "grises": 111000, "color": 167000, "full": 241000},
    "media": {"sketch": 130000, "grises": 185000, "color": 259000, "full": 370000},
    "alta": {"sketch": 222000, "grises": 296000, "color": 444000, "full": 592000}
}

EXTRAS_RANGE = "Los extras tienen un costo adicional desde 18.500 COP hasta 185.000 COP dependiendo del detalle."

# ===================== FUNCIONES =====================
def consultar_comision(personaje, detalle, escenario=None):
    personaje = personaje.lower()
    detalle = detalle.lower()
    if escenario:
        escenario = escenario.lower()

    # Validar personaje y detalle
    if personaje not in PERSONAJES:
        return f"❌ Personaje '{personaje}' no encontrado."
    if detalle not in PERSONAJES[personaje]:
        return f"❌ Detalle '{detalle}' no válido para '{personaje}'."

    precio_personaje = PERSONAJES[personaje][detalle]

    mensaje = f"✅ Precio del personaje '{personaje}' con detalle '{detalle}': {precio_personaje} COP."

    if escenario:
        if escenario not in ESCENARIOS:
            return f"❌ Escenario '{escenario}' no válido."
        precio_escenario = ESCENARIOS[escenario][detalle]
        mensaje += f"\n🏞️ Precio del escenario '{escenario}' con mismo detalle: {precio_escenario} COP."
    
    mensaje += f"\n💡 {EXTRAS_RANGE}"
    return mensaje

# ===================== RUTA =====================
@app.route("/", methods=["GET", "POST"])
def home():
    respuesta = ""
    if request.method == "POST":
        personaje = request.form["personaje"]
        detalle = request.form["detalle"]
        escenario = request.form.get("escenario")
        respuesta = consultar_comision(personaje, detalle, escenario)
    return render_template_string(html, respuesta=respuesta)

# ===================== ARRANQUE =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

