from flask import Blueprint, jsonify, request
from app.models.multiagent import orchestrator

# Create blueprint
api_bp = Blueprint('api', __name__)

@api_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing query parameter',
                'status': 400
            }), 400

        query = data['query']
        
        if 'model' in data:
            try:
                orchestrator.assignModel(data['model'])
            except KeyError:
                return jsonify({
                    'error': 'Invalid model selection',
                    'status': 400
                }), 400

        response = orchestrator.process_query(query)
        return jsonify({
            'status': 200,
            'query': query,
            'response': response
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 500
        }), 500

@api_bp.route('/models', methods=['GET'])
def get_available_models():
    return jsonify({
        'status': 200,
        'models': list(orchestrator.modelMap.keys())
    })

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'status': 200,
        'stats': orchestrator.get_inference_stats()
    })