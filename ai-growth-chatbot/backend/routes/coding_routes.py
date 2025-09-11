from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.coding_model import CodingProject, CodingTemplate, CodeSnippet
from services.code_execution_service import CodeExecutionService
from bson import ObjectId
import json

coding_bp = Blueprint('coding', __name__)

def serialize_mongo_doc(doc):
    """Convert MongoDB document to JSON serializable format"""
    if isinstance(doc, dict):
        return {k: serialize_mongo_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_mongo_doc(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    else:
        return doc

# Project endpoints
@coding_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    user_id = get_jwt_identity()
    projects = CodingProject.get_projects_by_user(user_id)
    return jsonify({'success': True, 'projects': serialize_mongo_doc(projects)})

@coding_bp.route('/projects', methods=['POST'])
@jwt_required()
def create_project():
    user_id = get_jwt_identity()
    data = request.get_json()

    project_data = {
        'user_id': user_id,
        'name': data.get('name'),
        'description': data.get('description'),
        'language': data.get('language'),
        'framework': data.get('framework'),
        'github_link': data.get('github_link'),
        'phase': data.get('phase', 'idea'),  # idea, prototype, development, production
        'status': 'active'
    }

    project = CodingProject.create_project(project_data)
    return jsonify({'success': True, 'project': serialize_mongo_doc(project)})

@coding_bp.route('/projects/<project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    user_id = get_jwt_identity()
    project = CodingProject.find_by_id(project_id)

    if not project:
        return jsonify({'success': False, 'message': 'Project not found'}), 404

    if project.get('user_id') != user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    return jsonify({'success': True, 'project': serialize_mongo_doc(project)})

@coding_bp.route('/projects/<project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    project = CodingProject.find_by_id(project_id)
    if not project:
        return jsonify({'success': False, 'message': 'Project not found'}), 404

    if project.get('user_id') != user_id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    success = CodingProject.update_project(project_id, data)
    if success:
        updated_project = CodingProject.find_by_id(project_id)
        return jsonify({'success': True, 'project': serialize_mongo_doc(updated_project)})
    else:
        return jsonify({'success': False, 'message': 'Failed to update project'}), 500

@coding_bp.route('/projects/<project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    user_id = get_jwt_identity()

    success = CodingProject.delete_project(project_id, user_id)
    if success:
        return jsonify({'success': True, 'message': 'Project deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Project not found or not authorized'}), 404

# Template endpoints
@coding_bp.route('/templates', methods=['GET'])
@jwt_required()
def get_templates():
    user_id = get_jwt_identity()
    templates = CodingTemplate.get_templates_by_user(user_id)
    return jsonify({'success': True, 'templates': templates})

@coding_bp.route('/templates', methods=['POST'])
@jwt_required()
def create_template():
    user_id = get_jwt_identity()
    data = request.get_json()

    template_data = {
        'user_id': user_id,
        'name': data.get('name'),
        'description': data.get('description'),
        'language': data.get('language'),
        'framework': data.get('framework'),
        'code': data.get('code'),
        'category': data.get('category'),
        'difficulty': data.get('difficulty', 'beginner')
    }

    template = CodingTemplate.create_template(template_data)
    return jsonify({'success': True, 'template': template})

@coding_bp.route('/templates/<template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    user_id = get_jwt_identity()

    success = CodingTemplate.delete_template(template_id, user_id)
    if success:
        return jsonify({'success': True, 'message': 'Template deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Template not found or not authorized'}), 404

# Snippet endpoints
@coding_bp.route('/snippets', methods=['GET'])
@jwt_required()
def get_snippets():
    user_id = get_jwt_identity()
    snippets = CodeSnippet.get_snippets_by_user(user_id)
    return jsonify({'success': True, 'snippets': snippets})

@coding_bp.route('/snippets', methods=['POST'])
@jwt_required()
def create_snippet():
    user_id = get_jwt_identity()
    data = request.get_json()

    snippet_data = {
        'user_id': user_id,
        'name': data.get('name'),
        'description': data.get('description'),
        'language': data.get('language'),
        'code': data.get('code'),
        'category': data.get('category'),
        'tags': data.get('tags', [])
    }

    snippet = CodeSnippet.create_snippet(snippet_data)
    return jsonify({'success': True, 'snippet': snippet})

@coding_bp.route('/snippets/<snippet_id>', methods=['DELETE'])
@jwt_required()
def delete_snippet(snippet_id):
    user_id = get_jwt_identity()

    success = CodeSnippet.delete_snippet(snippet_id, user_id)
    if success:
        return jsonify({'success': True, 'message': 'Snippet deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Snippet not found or not authorized'}), 404

# Code execution endpoints
@coding_bp.route('/execute', methods=['POST'])
@jwt_required()
def execute_code():
    """Execute code in the specified programming language"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'code' not in data or 'language' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: code and language'
            }), 400
        
        code = data.get('code', '').strip()
        language = data.get('language', '').strip()
        input_data = data.get('input', '')
        
        # Validate code before execution
        validation_result = CodeExecutionService.validate_code(code, language)
        if not validation_result.get('valid', False):
            return jsonify({
                'success': False,
                'error': validation_result.get('error'),
                'warning': validation_result.get('warning'),
                'supported_languages': validation_result.get('supported_languages')
            }), 400
        
        # Execute code
        result = CodeExecutionService.execute_code(code, language, input_data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@coding_bp.route('/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported programming languages"""
    try:
        languages = CodeExecutionService.get_supported_languages()
        return jsonify({
            'success': True,
            'languages': languages,
            'total': len(languages)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@coding_bp.route('/validate', methods=['POST'])
@jwt_required()
def validate_code():
    """Validate code before execution"""
    try:
        data = request.get_json()
        
        if not data or 'code' not in data or 'language' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: code and language'
            }), 400
        
        code = data.get('code', '').strip()
        language = data.get('language', '').strip()
        
        result = CodeExecutionService.validate_code(code, language)
        
        return jsonify({
            'success': True,
            'validation': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# Enhanced snippet endpoints with execution capability
@coding_bp.route('/snippets/<snippet_id>/execute', methods=['POST'])
@jwt_required()
def execute_snippet(snippet_id):
    """Execute a saved code snippet"""
    try:
        user_id = get_jwt_identity()
        
        # Get snippet from database
        snippet = CodeSnippet.find_by_id(snippet_id)
        if not snippet:
            return jsonify({
                'success': False,
                'error': 'Snippet not found'
            }), 404
        
        # Check authorization
        if snippet.get('user_id') != user_id:
            return jsonify({
                'success': False,
                'error': 'Unauthorized access to snippet'
            }), 403
        
        # Get input data from request
        data = request.get_json() or {}
        input_data = data.get('input', '')
        
        # Execute snippet
        result = CodeExecutionService.execute_code(
            snippet.get('code', ''),
            snippet.get('language', ''),
            input_data
        )
        
        # Add snippet info to result
        result['snippet_info'] = {
            'id': str(snippet.get('_id')),
            'name': snippet.get('name'),
            'language': snippet.get('language')
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500
