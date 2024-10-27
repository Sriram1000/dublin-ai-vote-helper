from flask import Flask, request, jsonify
import ollama
import flask_cors as cors

app = Flask(__name__)
cors.CORS(app)

with open('aivoter.modelfile', 'r', encoding='utf-8') as f:
    model_file = f.read()

model_name = 'aivoterhelperfinal'
print(model_file)

@app.route("/setup", methods=['GET'])
def setup():
    try:
        print(model_file)
        response = ollama.create(model=model_name, modelfile=model_file)
        return jsonify({'message': 'Model loaded', 'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '').strip()

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        response = ollama.generate(model=model_name, prompt=prompt)
        output = response.get('response', '').strip()
        if not output:
            return jsonify({'error': 'No response from the model'}), 500

        return jsonify({'response': output}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
