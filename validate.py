import os
import json
import yaml
import jsonschema
from datetime import datetime
import shutil

# Cargar el esquema JSON
with open('esquema.json', 'r') as schema_file:
    schema = json.load(schema_file)

# Directorios
docs_dir = 'docs' # Directorio donde se encuentran los archivos YAML a validar
ready_dir = 'ready' # Directorio donde se moverán los archivos YAML válidos
result_dir = 'result' # Directorio donde se guardarán los resultados de la validación

# Crear el archivo de log
log_file = 'EXECUTIONLOG.md'
with open(log_file, 'a') as log:
    log.write('# Execution Log\n\n') # Escribir el encabezado del archivo de log

# Función para validar un archivo YAML contra el esquema JSON
def validate_yaml(yaml_file, schema):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file) # Cargar el contenido del archivo YAML
    try:
        jsonschema.validate(instance=data, schema=schema) # Validar el contenido YAML contra el esquema JSON
        return True, None # Retornar True si la validación es exitosa
    except jsonschema.exceptions.ValidationError as err: 
        return False, err # Retornar False y el error si la validación falla

# Procesar cada archivo YAML en el directorio docs
for filename in os.listdir(docs_dir):
    if filename.endswith('.yaml'): # Procesar solo archivos con extensión .yaml
        yaml_path = os.path.join(docs_dir, filename)
        is_valid, error = validate_yaml(yaml_path, schema) # Validar el archivo YAML
        
        # Generar el nombre del archivo de resultados
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S') # Obtener la fecha y hora actual en el formato especificado
        result_filename = filename.replace('.yaml', f'_result_mdlint_{datetime.now().strftime("%Y%m%d%H%M%S")}.txt') # Generar el nombre del archivo de resultados
        result_path = os.path.join(result_dir, result_filename)
        
        # Escribir los resultados de la validación
        with open(result_path, 'w') as result_file:
            if is_valid:
                result_file.write('Validation successful.\n') # Escribir mensaje de éxito si la validación es correcta
            else:
                result_file.write(f'Validation failed:\n{error}\n') # Escribir el error si la validación falla
        
        # Mover el archivo YAML si es válido
        if is_valid:
            shutil.move(yaml_path, os.path.join(ready_dir, filename))
        
        # Registrar la ejecución en el log
        with open(log_file, 'a') as log:
            log.write(f"- **Fecha/Hora**: {timestamp}\n")
            log.write(f"  **Archivo Comprobado**: {filename}\n")
            log.write(f"  **Resultado**: {'Correcto' if is_valid else 'Incorrecto'}\n")
            log.write(f"  **Archivo de Resultados**: {result_filename}\n\n")
