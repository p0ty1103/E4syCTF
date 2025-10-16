from flask import Flask, request, make_response, render_template_string
import cowsay, io, sys, html

app = Flask(__name__)

try:
    with open("flag.txt", "r") as f:
        FLAG = f.read().strip()
except FileNotFoundError:
    FLAG = "E4syCTF{File_Not_Found!Contact_To_Admin.}"

ALLOWED_CMD = {
    "cat flag.txt"
}

@app.route('/', methods=['GET'])
def index():
    name_payload = request.args.get('name', 'Guest')
    cmd_payload = request.args.get('cmd')

    if cmd_payload:
        cmd_payload = cmd_payload.strip()
        if cmd_payload not in ALLOWED_CMD:
            msg = cowsay.get_output_string('dragon', 'Only allowed commands!')
            return make_response(f"<pre>{html.escape(msg)}</pre>", 200, {"Content-Type":"text/html; charset=utf-8"})

    try:
        rendered_payload = render_template_string(name_payload)
    except Exception as e:
        rendered_payload = f"Template Error: {e}"

    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    try:
        cowsay.cow(rendered_payload)
    except Exception as e:
        print(f"cowsay error: {e}")
    sys.stdout = old_stdout
    cow_speech = redirected_output.getvalue()

    return f"<pre>{html.escape(cow_speech)}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
