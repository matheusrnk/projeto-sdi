from flask import Flask, jsonify
from PIL import Image
import os
import datetime

#
# pip install Pillow
#

app = Flask(__name__)

def extract_metadata(image_path):
    with Image.open(image_path) as img:
        metadata = {
            "filename": os.path.basename(image_path),
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "info": {key: str(value) for key, value in img.info.items()},  # Convertendo valores de info para strings
            "peso": os.path.getsize(image_path), # tamanho da imagem com bytes
            "criado em": datetime.datetime.fromtimestamp(os.path.getctime(image_path)).strftime('%Y-%m-%d %H:%M:%S') # Tempo de criação
        }
    return metadata

@app.route('/fotos', methods=['GET'])
def get_metadata():
    #directory = '.'


    # pastas com fotos
    directories = ['.', '..//usuario2']
    metadata_list = []

    for directory in directories:

        if not os.path.exists(directory):
            continue # Ignora se o diretório não existir
    
        if not os.path.isdir(directory):
            continue # Ignora se não for um diretório

        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                image_path = os.path.join(directory, filename)
                metadata = extract_metadata(image_path)
                metadata_list.append(metadata)
    
    if not os.path.exists(directory):
        return jsonify({"error": "O caminho especificado não existe"}), 400

    
    if not os.path.isdir(directory):
        return jsonify({"error": "O caminho especificado não é um diretório"}), 400
    
    return jsonify(metadata_list)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9999, debug=True)

# 
# o endereco do browser eh 127.0.0.1/fotos
#