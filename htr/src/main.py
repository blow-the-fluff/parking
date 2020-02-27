from flask import Flask, render_template, request
import batch_process


app = Flask(__name__)

@app.route("/htr", methods=['GET'])
def htr():
    if request.method == 'GET':
        form_id = request.args.get('form_id')
        source_folder = '{}'.format(form_id)
        batch_process.process_write_data(source_folder)
        return "Done"

if __name__ == "__main__":
    app.run(debug=True, port=8810)