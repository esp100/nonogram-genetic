from flask import Blueprint, jsonify, request, render_template
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

@main.route("/nonogram/get", methods=["POST"])
@inject
def get_nonogram(nonogram_service: NonogramService = Provide[Container.nonogram_service]):
    nonogram = nonogram_service.get_nonogram(nonogram_service)
    return jsonify(nonogram), 200
