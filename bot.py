import json

with open("intents.json", encoding="utf-8") as f:
    intents = json.load(f)

# ===================== PRECIOS =====================

PERSONAJES = {
    "rostro": {
        "sketch": 25000,
        "grises": 37000,
        "color": 55000,
        "full": 75000
    },
    "busto": {
        "sketch": 37000,
        "grises": 55000,
        "color": 75000,
        "full": 110000
    },
    "medio cuerpo": {
        "sketch": 55000,
        "grises": 74000,
        "color": 110000,
        "full": 167000
    },
    "cuerpo completo": {
        "sketch": 92000,
        "grises": 130000,
        "color": 185000,
        "full": 259000
    },
    "chibi": {
        "sketch": 30000,
        "grises": 44000,
        "color": 66000,
        "full": 93000
    }
}

ESCENARIOS = {
    "simple": {
        "sketch": 74000,
        "grises": 111000,
        "color": 167000,
        "full": 241000
    },
    "media": {
        "sketch": 130000,
        "grises": 185000,
        "color": 259000,
        "full": 370000
    },
    "alta": {
        "sketch": 222000,
        "grises": 296000,
        "color": 444000,
        "full": 592000
    }
}

EXTRAS_RANGE = "Los extras tienen un costo adicional desde 18.500 COP hasta 185.000 COP dependiendo del detalle."

# ===================== ESTADO =====================

state = {
    "step": "start",
    "category": None,
    "type": None
}

# ===================== UTILIDADES =====================

def detect_goodbye(msg):
    for intent in intents["intents"]:
        if intent["name"] == "goodbye":
            for p in intent["patterns"]:
                if p in msg:
                    return intent["responses"][0]
    return None

def reset_state():
    state["step"] = "start"
    state["category"] = None
    state["type"] = None

# ===================== CORE =====================

def get_response(message: str) -> str:
    message = message.lower()

    # Finalizar conversación
    bye = detect_goodbye(message)
    if bye:
        reset_state()
        return bye

    # Reinicio manual
    if message in ["personaje", "escenario", "concept art"]:
        reset_state()
        state["category"] = message
        state["step"] = "type"

    # ---------- INICIO ----------
    if state["step"] == "start":
        state["step"] = "category"
        return "¿Qué deseas cotizar? (personaje, escenario o concept art)"

    # ---------- CATEGORÍA ----------
    if state["step"] == "category":
        if message in ["personaje", "escenario", "concept art"]:
            state["category"] = message
            state["step"] = "type"

            if message == "personaje":
                return "¿Qué tipo de personaje? (rostro, busto, medio cuerpo, cuerpo completo, chibi)"

            return "¿Qué tipo de escenario? (simple, media, alta)"

        return "Escribe: personaje, escenario o concept art."

    # ---------- TIPO ----------
    if state["step"] == "type":
        if state["category"] == "personaje" and message in PERSONAJES:
            state["type"] = message
            state["step"] = "style"
            return "¿En qué estilo? (sketch, grises, color, full)"

        if state["category"] in ["escenario", "concept art"] and message in ESCENARIOS:
            state["type"] = message
            state["step"] = "style"
            return "¿En qué estilo? (sketch, grises, color, full)"

        return "Opción inválida. Usa las opciones indicadas."

    # ---------- ESTILO ----------
    if state["step"] == "style":
        if message in ["sketch", "grises", "color", "full"]:
            if state["category"] == "personaje":
                price = PERSONAJES[state["type"]][message]
            else:
                price = ESCENARIOS[state["type"]][message]

            state["step"] = "done"
            return f"💰 Precio fijo: {price:,} COP\n{EXTRAS_RANGE}"

        return "Estilo inválido. Usa: sketch, grises, color o full."

    # ---------- FINAL ----------
    if state["step"] == "done":
        if "extra" in message or "fondo" in message or "objeto" in message or "efecto" in message:
            return EXTRAS_RANGE

        return "Si deseas otra cotización escribe: personaje, escenario o concept art."

    return intents["fallback"]

# ===================== CHAT =====================

print("🤖 Bot activo. Escribe 'salir' para terminar.")

while True:
    user_input = input("Tú: ")

    if user_input.lower() == "salir":
        print("Bot: ¡Adiós! 👋")
        break

    print("Bot:", get_response(user_input))