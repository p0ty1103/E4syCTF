from flask import Flask, jsonify, send_from_directory

app = Flask(__name__)

try:
        with open("flag.txt", "r") as f:
                FLAG = f.read().strip()
except FileNotFoundError:
        FLAG = "E4syCTF{File_Not_Found!Contact_To_Admin!}"

@app.route('/')
def serve_index():
        return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
        return send_from_directory('static', path)

### --- API EndPoind --- ###

@app.route('/api/get_info')
def get_info():
        return jsonify({"error": "Permission Denied."})

@app.route('/api/get_admin_info')
def get_admin_info():
        return jsonify({"flag": FLAG})

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)