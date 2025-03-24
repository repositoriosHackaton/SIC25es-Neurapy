![397227369-057ac64a-1499-4e0d-966b-eb0b13b44a79](https://github.com/user-attachments/assets/6ac9b822-9183-4980-b021-80cd7c39b429)

# MediBot | Asistente Inteligente de Medicamentos

# 1. Miembros del Equipo
- Franklin Esteban Perez Fuentes (LÍder)
- Bryan Antonio Martinez Torres
- Jael Esmeralda Flores Fuentes

# 2. Descripción del Proyecto


# Chatbot de Información sobre Consulta de Medicamentos 💊

## 📌 Descripción
Este chatbot permite consultar información sobre medicamentos, efectos secundarios y dosis recomendadas. Además, ofrece información sobre interacciones entre medicamentos y precauciones al usarlos.

El chatbot contiene información sobre los medicamentos más populares utilizados en **El Salvador**, **Guatemala** y **Venezuela**.

La innovación principal es que los usuarios pueden preguntar sobre un medicamento utilizando su nombre coloquial en cada país.

La problemática que aborda esta idea es que muchas personas no conocen el nombre técnico de los medicamentos, pero sí su nombre común o popular en su comunidad. Esta solución permite que puedan obtener información útil sobre los medicamentos utilizando el lenguaje que les es familiar.

### Características:
- Responde preguntas sobre interacciones entre medicamentos.
- Ofrece información sobre efectos adversos y precauciones.
- Permite que los usuarios consulten los medicamentos utilizando su nombre coloquial o popular en su país.

### Ejemplo de uso:
**El Salvador:**
- Usuario: ¿Para qué sirve el Tabcin?
- Respuesta del bot: "Tabcin es un medicamento utilizado para aliviar los síntomas del resfriado, como la congestión nasal, la tos y el malestar general. Contiene un antihistamínico y un descongestionante."

### 🧑‍💻 Tecnologías Utilizadas:
- **Python 3**: Lenguaje de programación principal.
- **TensorFlow/Keras**: Red neuronal para el procesamiento de lenguaje natural y la predicción de respuestas.
- **NLTK**: Para el procesamiento del lenguaje y stemming.
- **Scikit-learn**: Para el procesamiento de etiquetas y características de texto.
- **CustomTkinter**: Para la interfaz gráfica moderna del chatbot.

## 🛠 Requisitos

### Requisitos para ejecutar el proyecto:

1. **Python 3.x** (Recomendado Python 3.7 o superior)
2. **Instalar dependencias**: Usar el archivo `requirements.txt` para instalar las librerías necesarias.

## 📥 Instalación:

1. Clona este repositorio:
   ```sh
   git clone https://github.com/tu-usuario/chatbot-medicamentos.git
   cd chatbot-medicamentos
   ```
2. Instala las dependencias necesarias:
   ```sh
   pip install -r requirements.txt
   ```

## Uso
1. Ejecuta el script principal para entrenar el modelo y habilitar el chatbot:
   ```sh
   python chatbot.py
   ```

# 3. ¿Cómo Funciona el Bot?✅

# 1. Preparación de Datos:
Definición de Medicamentos: Se crea un diccionario (medicamentos) que almacena información detallada sobre cada medicamento (descripción, uso).
Variantes de Medicamentos: Se crea un diccionario (variantes_medicamentos) que contiene las distintas formas en que los usuarios podrían referirse a cada medicamento (sinónimos, errores de ortografía).
Intents Mejorados: Se carga un archivo JSON (intents.json) que define las intenciones del usuario (saludos, preguntas sobre medicamentos, etc.) y se mejora, para que pueda tomar las variantes de los medicamentos.
Procesamiento de Lenguaje: Se define una clase (ProcesadorLenguaje) que utiliza las variantes de medicamentos para extraer la entidad del medicamento del texto del usuario.

# 2. Modelo de Procesamiento del Lenguaje Natural (PLN):
Generación de Ejemplos de Entrenamiento: Se generan ejemplos de entrenamiento para el modelo de PLN, incluyendo preguntas sobre medicamentos con diferentes variantes.
Tokenización y Stemming: Se procesa el texto de entrada (tokenización y stemming) para convertirlo en una representación numérica que el modelo pueda entender.
Creación del Modelo: Se crea un modelo de red neuronal con Keras para clasificar las intenciones del usuario.
Entrenamiento del Modelo: Se entrena el modelo con los datos de entrenamiento preparados.
Predicción de Intención: Se define una función (predecir_intencion) que utiliza el modelo entrenado para predecir la intención del usuario a partir de su texto.

# 3. Lógica del Chatbot:
Función chatbot_response: Esta es la función principal del chatbot. Toma el texto del usuario como entrada y realiza los siguientes pasos:
Predice la intención del usuario utilizando el modelo de PLN.
Si la intención es una pregunta sobre un medicamento, extrae la entidad del medicamento utilizando la clase ProcesadorLenguaje.
Busca la información del medicamento en el diccionario medicamentos y genera una respuesta adecuada.
Si la intención no es sobre un medicamento, busca una respuesta predefinida en el archivo intents.json.
Si no se encuentra ninguna respuesta adecuada, devuelve un mensaje de error.

# 4. Interfaz Gráfica (GUI)(En Desarrollo):
CustomTkinter: Se utiliza la biblioteca CustomTkinter para crear una interfaz gráfica para el chatbot.
Elementos de la GUI: La GUI incluye un área de chat para mostrar la conversación, un campo de entrada para que el usuario escriba sus preguntas y un botón de envío.
Función send_message: Esta función se llama cuando el usuario envía un mensaje. Toma el texto del usuario, lo envía a la función chatbot_response para obtener una respuesta y muestra la conversación en el área de chat.


## Contribuciones
Si deseas mejorar este chatbot, puedes:
- Agregar más medicamentos a la base de conocimientos (`intents.json`).
- Mejorar el preprocesamiento del texto.
- Optimizar la arquitectura del modelo de redes neuronales.

## Licencia
Este proyecto está bajo la Licencia MIT.