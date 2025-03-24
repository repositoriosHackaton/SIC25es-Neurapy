![397227369-057ac64a-1499-4e0d-966b-eb0b13b44a79](https://github.com/user-attachments/assets/6ac9b822-9183-4980-b021-80cd7c39b429)

# MediBot | Asistente Inteligente de Medicamentos
Este chatbot permite consultar información sobre medicamentos, efectos secundarios y dosis recomendadas.


# 1. Miembros del Equipo
- FRANKLIN ESTEBAN PEREZ FUENTES 
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
2. Interactúa con el chatbot escribiendo preguntas relacionadas con medicamentos.

## Entrenamiento del Modelo
El chatbot utiliza una red neuronal con capas densas para clasificar las intenciones. Para mejorar el desempeño, se pueden ajustar los hiperparámetros como el número de épocas y el tamaño del lote en la función `model.fit()`.

## Contribuciones
Si deseas mejorar este chatbot, puedes:
- Agregar más medicamentos a la base de conocimientos (`intents.json`).
- Mejorar el preprocesamiento del texto.
- Optimizar la arquitectura del modelo de redes neuronales.

## Licencia
Este proyecto está bajo la Licencia MIT.