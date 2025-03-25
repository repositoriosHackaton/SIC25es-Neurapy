import nltk
import json
import random
import numpy as np
import re
from nltk.stem import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
import customtkinter as ctk

# ---- FUNCIONES DE UTILIDAD PARA GUARDAR JSON ----
def guardar_json(datos, filename):
    """Creación de función para guardar
    diccionario de conocimiento en formato json"""
    with open(filename, "w") as archivo:
        json.dump(datos, archivo, indent=4)


# ---- DEFINICIÓN DE ENTIDADES DE MEDICAMENTOS ----
# Diccionario de entidades (medicamentos)
medicamentos = {
    "paracetamol": {
        "descripcion": "El Paracetamol es un analgésico y antipirético comúnmente usado para aliviar el dolor leve a moderado y reducir la fiebre. Es efectivo para dolores de cabeza, musculares y de muelas.",
        "uso": "Paracetamol es utilizado para aliviar dolores leves y reducir la fiebre. No se recomienda exceder la dosis diaria de 4 gramos, ya que puede causar daño hepático."
    },
    "mejoral": {
        "descripcion": "Mejoral es un medicamento que combina aspirina y paracetamol, utilizado principalmente para aliviar dolores como dolores de cabeza, musculares o articulares. También ayuda a reducir la fiebre.",
        "uso": "Mejoral es eficaz para aliviar dolores leves y moderados, además de reducir la fiebre. Es una opción común para aliviar dolores como los de cabeza y musculares."
    },
    "alkaseltzer": {
        "descripcion": "Alka-Seltzer es un medicamento efervescente utilizado para aliviar la acidez estomacal, indigestión y malestar estomacal. También es eficaz para reducir el dolor causado por estas molestias.",
        "uso": "Alka-Seltzer se utiliza comúnmente para aliviar problemas digestivos, como la acidez estomacal o la indigestión, proporcionando alivio rápido."
    },
    "tabcin": {
        "descripcion": "Tabcin es un medicamento utilizado para aliviar los síntomas del resfriado, como la congestión nasal, la tos y el malestar general. Contiene un antihistamínico y descongestionante.",
        "uso": "Tabcin es eficaz para tratar los resfriados comunes, ayudando a reducir la congestión nasal y otros síntomas molestos relacionados con resfriados."
    },
    "vickvaporub": {
        "descripcion": "Vick VapoRub es una pomada tópica utilizada para aliviar la congestión nasal, la tos y los dolores musculares. Contiene mentol, alcanfor y aceite de eucalipto.",
        "uso": "Vick VapoRub es muy útil para aliviar la congestión respiratoria y los dolores musculares. Se aplica directamente sobre el pecho o la garganta."
    },
    "intestinomicina": {
        "descripcion": "Intestinomicina es un medicamento utilizado para tratar infecciones intestinales, como la diarrea infecciosa o bacteriana. Actúa eliminando bacterias dañinas en el intestino.",
        "uso": "Intestinomicina es eficaz para el tratamiento de infecciones intestinales y problemas digestivos causados por bacterias, ayudando a restaurar el equilibrio intestinal."
    },
    "panadol": {
        "descripcion": "Panadol es un analgésico utilizado para aliviar dolores leves a moderados, como dolores de cabeza, dolor muscular, dolor de muelas, o fiebre.",
        "uso": "Panadol es eficaz para el alivio rápido de dolores comunes y fiebre, al igual que el paracetamol, pero es una de las marcas más reconocidas."
    },
    "salandrews": {
        "descripcion": "Sal Andrews es un medicamento efervescente utilizado para tratar la acidez estomacal y la indigestión, aliviando la sensación de ardor en el estómago.",
        "uso": "La Sal Andrews ayuda a neutralizar el ácido estomacal, proporcionando alivio rápido para las molestias causadas por la acidez o la indigestión."
    },
    "pildorin": {
        "descripcion": "Pildorín es un anticonceptivo oral utilizado para prevenir embarazos no deseados. Contiene hormonas que controlan el ciclo menstrual y previenen la ovulación.",
        "uso": "Pildorín es una opción de pastillas anticonceptivas que ayuda a regular el ciclo menstrual y evita la fertilización."
    },
    "cafiaspirina": {
        "descripcion": "Cafiaspirina es un medicamento combinado de cafeína y aspirina, utilizado para aliviar dolores de cabeza, migrañas y dolores musculares.",
        "uso": "Cafiaspirina actúa combatiendo el dolor de cabeza y mejorando la circulación sanguínea, gracias a la acción conjunta de la cafeína y la aspirina."
    },
    "atamel": {
        "descripcion": "Atamel es un medicamento que contiene paracetamol, utilizado para aliviar dolores de cabeza, fiebre y dolores musculares.",
        "uso": "Atamel es similar al Paracetamol, con propiedades analgésicas y antipiréticas, efectivo para reducir dolores y fiebre."
    },
    "dramamine": {
        "descripcion": "Dramamine, también conocido como 'El Drama', es un medicamento utilizado para prevenir y tratar los mareos, náuseas y vómitos causados por el movimiento, como en los viajes en automóvil, barco o avión.",
        "uso": "Dramamine es un antihistamínico utilizado para combatir los síntomas del mareo y las náuseas, especialmente en viajes largos o en situaciones de mareo por movimiento."
    },
    "bicarbonato": {
        "descripcion": "El Bicarbonato, conocido también como 'El Bicarbo', es un medicamento utilizado para aliviar la acidez estomacal y la indigestión. Neutraliza el exceso de ácido en el estómago.",
        "uso": "El Bicarbonato se usa comúnmente para reducir la acidez estomacal y aliviar los síntomas de la indigestión. También puede ser útil en algunos problemas de acidez gástrica."
    },
    "dolex": {
        "descripcion": "Dolex es un analgésico utilizado para aliviar dolores de cabeza, dolores musculares y dolores leves a moderados. Contiene paracetamol como principio activo.",
        "uso": "Dolex es comúnmente usado para tratar dolores de cabeza, musculares y otros dolores menores, ofreciendo alivio rápido y efectivo."
    },
    "lemisol": {
        "descripcion": "Lemisol, o 'El Lemi', es un medicamento utilizado como antiséptico para tratar heridas y quemaduras leves. Se aplica tópicamente para prevenir infecciones en la piel.",
        "uso": "Lemisol es un antiséptico eficaz para limpiar y desinfectar heridas, cortaduras y quemaduras menores, ayudando a prevenir infecciones."
    },
    "tachipirin": {
        "descripcion": "Tachipirín es un medicamento utilizado para tratar la fiebre en niños. Contiene paracetamol, lo que ayuda a reducir la fiebre y aliviar dolores leves a moderados.",
        "uso": "Tachipirín es un medicamento especialmente formulado para niños, utilizado para bajar la fiebre y aliviar dolores causados por resfriados o infecciones comunes."
    },
    "alkad": {
        "descripcion": "Alka-D es un medicamento utilizado para aliviar la acidez estomacal y el malestar causado por la indigestión. Actúa neutralizando el exceso de ácido en el estómago.",
        "uso": "Alka-D se usa para tratar problemas digestivos como la acidez y el malestar estomacal, proporcionando alivio rápido y efectivo."
    },
    "enteroguanil": {
        "descripcion": "Enteroguanil, o 'La Guanil', es un medicamento utilizado para tratar la diarrea. Ayuda a reducir la frecuencia y la intensidad de las evacuaciones intestinales.",
        "uso": "Enteroguanil es eficaz en el tratamiento de la diarrea aguda, especialmente en casos causados por infecciones intestinales, restaurando el equilibrio digestivo."
    },
    "dolofin": {
        "descripcion": "Dolofin, o 'El Dolo', es un medicamento utilizado para aliviar dolores leves a moderados, como dolores musculares y de cabeza. Contiene paracetamol como principio activo.",
        "uso": "Dolofin es utilizado para aliviar dolores como los de cabeza, musculares y otras molestias menores, proporcionando un alivio rápido y efectivo."
    },
    "neosaldina": {
        "descripcion": "Neosaldina, o 'La Neo', es un medicamento utilizado para tratar migrañas y dolores de cabeza intensos. Contiene principios activos que ayudan a aliviar el dolor y reducir la inflamación.",
        "uso": "Neosaldina es muy eficaz para aliviar las migrañas y dolores de cabeza severos, proporcionando un alivio rápido y eficaz."
    },
    "amoxil": {
        "descripcion": "Amoxil, o 'La Amoxilina', es un antibiótico utilizado para tratar infecciones bacterianas, como infecciones respiratorias, del tracto urinario y otras infecciones comunes.",
        "uso": "Amoxil es un medicamento antibiótico que combate infecciones bacterianas al interferir con la producción de las paredes celulares de las bacterias, ayudando a eliminarlas."
    }
}


# Diccionario simplificado para este ejemplo (agrega todos los medicamentos de tu lista original)
variantes_medicamentos = {
    "paracetamol": ["paracetamol", "acetaminofén", "acetaminofen", "tylenol"],
    "mejoral": ["mejoral", "mejora", "mejoralito"],
    "alkaseltzer": ["alkaseltzer", "alka seltzer", "alka-seltzer", "alkaceltzer"],
    "tabcin": ["tabcin", "tapcin", "tabsin", "tabsín"],
    "vickvaporub": ["vickvaporub", "vick vaporub", "vick", "vaporub", "vaporrub"],
    "intestinomicina": ["intestinomicina", "intestinomisina", "intestino micina"],
    "panadol": ["panadol", "panadoll"],
    "salandrews": ["salandrews", "sal andrews", "sal de andrews", "sales andrews"],
    "pildorin": ["pildorin", "pildorín", "pildora", "anticonceptivo"],
    "cafiaspirina": ["cafiaspirina", "cafiaspirina", "cafi aspirina", "cafe aspirina"],
    "atamel": ["atamel", "atamet"],
    "dramamine": ["dramamine", "dramamin", "drama", "el drama"],
    "bicarbonato": ["bicarbonato", "bicarbo", "bicarbonato de sodio", "bicarbo soda"],
    "dolex": ["dolex", "doleks", "dolec"],
    "lemisol": ["lemisol", "lemi", "el lemi", "lemi sol"],
    "tachipirin": ["tachipirin", "tachipirín", "tachipirn", "tachi"],
    "alkad": ["alkad", "alka d", "alka-d"],
    "enteroguanil": ["enteroguanil", "guanil", "la guanil", "entero guanil"],
    "dolofin": ["dolofin", "dolofín", "dolo", "el dolo"],
    "neosaldina": ["neosaldina", "neo", "la neo", "neosaldin"],
    "amoxil": ["amoxil", "amoxilina", "amoxicilina", "la amoxilina"]
}

# ---- CARGA DE INTENTS ORIGINALES ----
# Cargar el archivo JSON original
try:
    with open("intents.json") as file:
        intents_originales = json.load(file)
except FileNotFoundError:
    # Si no existe, usamos una estructura básica
    intents_originales = {"intents": []}


# ---- CREACIÓN DE INTENTS MEJORADOS ----
biblioteca_mejorada = {
    "intents": [
        # Mantener los intents de saludos y despedidas del original
        next((i for i in intents_originales["intents"] if i["tag"] == "saludo"), 
            {
                "tag": "saludo",
                "patterns": ["Hola", "¿Cómo estás?", "Buenos días", "¡Hola!", "¡Qué tal!"],
                "responses": [
                    "¡Hola! ¿En qué puedo ayudarte hoy?",
                    "¡Hola! ¿Cómo puedo asistirte con tu consulta sobre medicamentos?",
                ],
            }
        ),
        next((i for i in intents_originales["intents"] if i["tag"] == "despedida"), 
            {
                "tag": "despedida",
                "patterns": [
                    "Adiós",
                    "Hasta luego",
                    "Nos vemos",
                    "Hasta pronto",
                    "Hasta luego, gracias",
                ],
                "responses": [
                    "¡Hasta luego! Que tengas un excelente día.",
                    "¡Adiós! Si necesitas más información, aquí estaré.",
                ],
            }
        ),
        # Intent único para todos los medicamentos
        {
            "tag": "informacion_medicamento",
            "patterns": [
                "¿Qué es el medicamento {}?",
                "¿Para qué sirve el {}?",
                "¿Para qué sirve {}?",
                "Cuéntame sobre {}",
                "¿Qué hace el {}?",
                "¿Qué hace {}?",
                "Información sobre {}",
                "¿Para qué es bueno el {}?",
                "¿Cómo funciona {}?",
                "¿Cuáles son los usos del {}?",
                "¿Cuáles son los beneficios de {}?",
                "¿Qué debo saber sobre {}?",
                "Dime para qué sirve {}",
                "Necesito información de {}"
            ],
            "responses": [
                "Te cuento sobre {medicamento}: {descripcion}",
                "{medicamento} es utilizado para: {uso}"
            ],
            "entities": medicamentos
        },
        # No respuesta (mantener del original o usar uno por defecto)
        next((i for i in intents_originales["intents"] if i["tag"] == "norespuesta"), 
            {
                "tag": "norespuesta",
                "patterns": [
                    "",
                    "no entiendo",
                    "no sé qué decir",
                    "no tengo una respuesta",
                    "no entiendo la pregunta",
                ],
                "responses": [
                    "Lo siento, no pude entender tu pregunta. ¿Podrías reformularla?",
                    "No estoy seguro de cómo responder eso. ¿Podrías ser más específico?",
                    "No reconozco esa solicitud. Si necesitas información sobre medicamentos, por favor, pregúntame de nuevo.",
                ],
            }
        ),
    ]
}

# Opcional: Agregar otros intents del original que no sean de medicamentos
for intent in intents_originales["intents"]:
    if intent["tag"] not in ["saludo", "despedida", "norespuesta"] and not intent["tag"].startswith("informacion_medicamento"):
        biblioteca_mejorada["intents"].append(intent)

# Guardar el nuevo archivo de intents
guardar_json(biblioteca_mejorada, "json/intents_mejorado.json")
guardar_json(medicamentos, "json/entidades_medicamentos.json")
guardar_json(variantes_medicamentos, "json/variantes_medicamentos.json")


# ---- CLASE PROCESADOR DE LENGUAJE ----
class ProcesadorLenguaje:
    def __init__(self, variantes_medicamentos):
        self.variantes_medicamentos = variantes_medicamentos
        # Crear un diccionario inverso para búsqueda rápida
        self.mapa_variantes = {}
        for medicamento, variantes in variantes_medicamentos.items():
            for variante in variantes:
                self.mapa_variantes[variante.lower()] = medicamento
    
    def extraer_entidad_medicamento(self, texto):
        """Extrae la entidad medicamento del texto basado en variantes conocidas"""
        texto_lower = texto.lower()
        
        # Buscar directamente en el mapa de variantes
        for variante, medicamento in self.mapa_variantes.items():
            if variante in texto_lower:
                return medicamento
                
        # Si no se encuentra, buscar patrones más complejos
        palabras = re.findall(r'\b\w+\b', texto_lower)
        for palabra in palabras:
            for variante, medicamento in self.mapa_variantes.items():
                # Comparación aproximada
                if palabra in variante or variante in palabra:
                    return medicamento
        
        return None


# ---- INTEGRACIÓN CON EL MODELO NEURAL ----
# Inicializar procesador de lenguaje
procesador = ProcesadorLenguaje(variantes_medicamentos)

# Inicializar el stemmer y el encoder
stemmer = PorterStemmer()
encoder = LabelEncoder()

# ---- PREPROCESAMIENTO Y GENERACIÓN DE EJEMPLOS PARA ENTRENAMIENTO ----
def generar_ejemplos_entrenamiento():
    """Genera ejemplos de entrenamiento para el modelo incluyendo ejemplos de entidades"""
    patterns = []  # Base de conocimientos por cada intención
    responses = []  # Respuesta de la intención
    tags = []  # Intents
    
    # Agregar intents generales (saludos, despedidas, etc.)
    for intent in biblioteca_mejorada["intents"]:
        if intent["tag"] != "informacion_medicamento":
            for pattern in intent["patterns"]:
                patterns.append(pattern)
                responses.append(intent["responses"])
                tags.append(intent["tag"])
    
    # Agregar ejemplos para el intent de medicamentos con cada entidad
    intent_medicamento = next(i for i in biblioteca_mejorada["intents"] if i["tag"] == "informacion_medicamento")
    for medicamento in medicamentos.keys():
        for pattern_template in intent_medicamento["patterns"]:
            # Crear ejemplos con el medicamento real
            example = pattern_template.format(medicamento)
            patterns.append(example)
            responses.append(intent_medicamento["responses"])
            tags.append("informacion_medicamento")
            
            # Opcional: Agregar variantes para mejorar la capacidad de detección
            for variante in variantes_medicamentos.get(medicamento, [])[:2]:  # Limitamos a 2 variantes por medicamento
                example_variante = pattern_template.format(variante)
                patterns.append(example_variante)
                responses.append(intent_medicamento["responses"])
                tags.append("informacion_medicamento")
    
    return patterns, responses, tags

# Generar los datos de entrenamiento
patterns, responses, tags = generar_ejemplos_entrenamiento()

# ---- TOKENIZACIÓN Y STEMMING ----
def tokenize_and_stem(sentence):
    words = nltk.word_tokenize(sentence)
    words = [stemmer.stem(w.lower()) for w in words if w.isalnum()]
    return words

# Crear el Bag of Words
all_words = []
for pattern in patterns:
    words = tokenize_and_stem(pattern)
    all_words.extend(words)

all_words = sorted(list(set(all_words)))

# Crear el Bag of Words (BoW)
vectorizer = CountVectorizer(vocabulary=all_words)
X_train = vectorizer.transform(patterns).toarray()

# Codificar las etiquetas
y_train = encoder.fit_transform(tags)

# ---- DEFINICIÓN Y ENTRENAMIENTO DEL MODELO ----
# Crear la red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(X_train.shape[1],), activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(len(set(tags)), activation="softmax"))

# Compilar el modelo
model.compile(
    loss="sparse_categorical_crossentropy", 
    optimizer=Adam(), 
    metrics=["accuracy"]
)

# Entrenar el modelo
model.fit(X_train, y_train, epochs=200, batch_size=5, verbose=1)

# ---- FUNCIÓN PARA PREDECIR LA INTENCIÓN ----
def predecir_intencion(texto):
    # Preprocesar el texto de entrada
    text_words = tokenize_and_stem(texto)
    bow = np.zeros(len(all_words))

    for word in text_words:
        if word in all_words:
            bow[all_words.index(word)] = 1

    # Predecir la categoría
    prediction = model.predict(np.array([bow]))[0]
    tag = encoder.inverse_transform([np.argmax(prediction)])
    confidence = np.max(prediction)
    
    return tag[0], confidence

# ---- FUNCIÓN PRINCIPAL DEL CHATBOT ----
def chatbot_response(texto):
    # Paso 1: Predecir la intención básica con el modelo
    intent_tag, confidence = predecir_intencion(texto)
    
    # Paso 2: Si es una consulta sobre medicamento, extraer la entidad
    if intent_tag == "informacion_medicamento":
        medicamento = procesador.extraer_entidad_medicamento(texto)
        
        if medicamento and medicamento in medicamentos:
            # Obtener el intent correspondiente
            intent_medicamento = next(i for i in biblioteca_mejorada["intents"] if i["tag"] == "informacion_medicamento")
            
            # Seleccionar aleatoriamente una plantilla de respuesta
            respuesta_template = random.choice(intent_medicamento["responses"])
            
            # Formatear la respuesta con la información del medicamento
            return respuesta_template.format(
                medicamento=medicamento.capitalize(),
                descripcion=medicamentos[medicamento]["descripcion"],
                uso=medicamentos[medicamento]["uso"]
            )
        else:
            # Si no se identifica el medicamento específico
            return "Me parece que quieres información sobre un medicamento, pero no logro identificar cuál. ¿Podrías ser más específico?"
    
    # Paso 3: Para otras intenciones, buscar en la biblioteca
    for intent in biblioteca_mejorada["intents"]:
        if intent["tag"] == intent_tag:
            return random.choice(intent["responses"])
    
    # Respuesta por defecto si no se encuentra la intención
    return "Lo siento, no entiendo tu consulta. ¿Podrías reformularla?"

# ---- INTERFAZ GRÁFICA CON CUSTOMTKINTER ----
class MediBotApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        ctk.set_appearance_mode("light")  # Modo claro
        ctk.set_default_color_theme("blue")
        
        # Configurar fondo blanco para la ventana principal (root)
        self.root.configure(bg="white")
        self.root.title("MediBot - Asistente de Medicamentos")
        self.root.geometry("500x600")
        self.root.minsize(400, 700)
        
        # Fondo blanco para el frame principal
        self.main_frame = ctk.CTkFrame(self.root, fg_color="white", border_width=0)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.main_frame, text="MediBot", 
                                        font=ctk.CTkFont(size=24, weight="bold"), 
                                        text_color="#0078D7",
                                        fg_color="white")
        self.title_label.pack(pady=(10, 5))
        
        self.subtitle_label = ctk.CTkLabel(self.main_frame, text="Tu asistente virtual de medicamentos", 
                                          font=ctk.CTkFont(size=14), text_color="#333333",
                                          fg_color="white")
        self.subtitle_label.pack(pady=(0, 10))
        
        # Fondo blanco para el frame del chat sin borde
        self.chat_frame = ctk.CTkFrame(self.main_frame, fg_color="white", border_width=0)
        self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Mantener el color específico para el área de chat (preguntas y respuestas)
        self.chat_window = ctk.CTkTextbox(self.chat_frame, width=450, height=400, wrap="word",
                                          fg_color="#f0f0f0", text_color="#0078D7")
        self.chat_window.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.chat_window.insert("end", "MediBot: ¡Hola! Soy tu asistente virtual de medicamentos. Pregúntame lo que necesites.\n\n", "bot")
        self.chat_window.tag_config("bot", foreground="#0078D7")
        self.chat_window.tag_config("user", foreground="#333333")
        
        self.chat_window.configure(state="disabled")  # Solo lectura
        
        # Fondo blanco para el frame de entrada sin borde
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="white", border_width=0)
        self.input_frame.pack(padx=10, pady=(0, 10), fill="x")
        
        # Quitar el borde del campo de entrada de preguntas
        self.entry = ctk.CTkEntry(self.input_frame, width=350, 
                                 placeholder_text="Escribe tu pregunta aquí...",
                                 text_color="#333333", fg_color="#f0f0f0",
                                 border_width=0)  # Quitar el borde
        self.entry.pack(pady=10, padx=10, side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda event: self.send_message())
        
        self.send_button = ctk.CTkButton(self.input_frame, text="Enviar", command=self.send_message,
                                        fg_color="#0078D7", text_color="#ffffff")
        self.send_button.pack(pady=10, padx=10, side="right")
        
        self.footer_label = ctk.CTkLabel(self.main_frame, text="Powered by NeuraPy - Versión 1.0", 
                                       font=ctk.CTkFont(size=10), text_color="#707070",
                                       fg_color="white")
        self.footer_label.pack(pady=5)
        
    def send_message(self):
        user_input = self.entry.get()
        if user_input:
            self.chat_window.configure(state="normal")
            self.chat_window.insert("end", "Tú: " + user_input + "\n", "user")
            
            response = chatbot_response(user_input)
            
            self.chat_window.insert("end", "MediBot: " + response + "\n\n", "bot")
            
            self.chat_window.see("end")
            self.chat_window.configure(state="disabled")
            self.entry.delete(0, "end")

def main():
    root = ctk.CTk()
    app = MediBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()