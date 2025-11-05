from flask import Flask, request, make_response

app = Flask(__name__)

EXPECTED_UA = "E4syCTF-Client/1.0"

try:
        with open("flag.txt", "r") as f:
                FLAG = f.read().strip()
except FileNotFoundError:
        FLAG = "File Not Found! Contact to admin."

@app.route('/')
def index():
        user_agent = request.headers.get('User-Agent')

        if user_agent == EXPECTED_UA:
                response_text = f"\nWelcome, authorized client!\nFlag: {FLAG}\n"
                response = make_response(response_text, 200)
                response.mimetype = "text/plain"
                return response

        else:
                response_text = "Access Denied: This service is only for authorized clients.\n"
                response_text += f"Your User-Agent: {user_agent}\n"
                response = make_response(response_text, 200)
                response.mimetype = "text/plain"

                response.headers['X-Client-Name'] = 'E4syCTF-Client'
                response.headers['X-Client-Version'] = '1.0'
                return response

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)