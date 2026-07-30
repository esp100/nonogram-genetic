from flask import Blueprint, jsonify, request, render_template, send_file
from project.adapters.assembly import Container
from project.domain.nonogram_service import NonogramService
from dependency_injector.wiring import inject, Provide

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/nonogram', methods=['POST'])
@inject
def create_nonogram(nonogram_service: NonogramService = Provide[Container.nonogram_service]):
    data = request.get_json()
    rows = data.get('rows')
    cols = data.get('cols')
    grid = data.get('grid', None)

    row_hints, col_hints = None, None 
    #TODO: Implement logic to calculate hints based on the provided grid 

    nonogram = nonogram_service.create_nonogram(rows, cols, row_hints, col_hints, grid)
    return jsonify(nonogram.get_nonogram()), 201

@main.route('/nonogram/solve', methods=['POST'])
@inject
def solve_nonogram(nonogram_service: NonogramService = Provide[Container.nonogram_service]):
    data = request.get_json()
    rows = data.get('rows')
    cols = data.get('cols')
    row_hints = data.get('row_hints', [])
    col_hints = data.get('col_hints', [])
    grid = data.get('grid', None)

    nonogram = nonogram_service.create_nonogram(rows, cols, row_hints, col_hints, grid)
    solved_nonogram = nonogram_service.solve_nonogram(nonogram)
    return jsonify(solved_nonogram.get_nonogram()), 200

@main.route("/nonogram/load", methods=["POST"])
@inject
def load_nonogram(nonogram_service: NonogramService = Provide[Container.nonogram_service]):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        grid = nonogram_service.csv_adapter.read_stream(file.stream)
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        #TODO: Implement logic to calculate hints based on the provided grid 
        nonogram = nonogram_service.create_nonogram(rows, cols, grid=grid)
        return jsonify({
                "grid": nonogram.get_nonogram().get('grid'),
                "row_hints": nonogram.get_nonogram().get('row_hints'),
                "col_hints": nonogram.get_nonogram().get('col_hints'),
            }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/nonogram/save", methods=["POST"])
@inject
def save_nonogram(nonogram_service: NonogramService = Provide[Container.nonogram_service]):
    data = request.get_json()

    if not data or 'grid' not in data:
        return jsonify({"error": "Invalid request data"}), 400

    try:
        grid = data['grid']
        filename = data.get('filename', 'nonogram.csv')
        
        csv_buffer = nonogram_service.generate_file(grid)

        return send_file(
            csv_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    