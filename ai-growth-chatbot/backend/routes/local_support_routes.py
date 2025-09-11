from flask import Blueprint, request, jsonify
from services.local_support_service import LocalSupportService
from utils.auth import token_required
import logging

local_support_bp = Blueprint('local_support', __name__)
local_support_service = LocalSupportService()

@local_support_bp.route('/search', methods=['GET'])
@token_required
def search_local_support(current_user):
    """
    Search for local mental health support services
    Query parameters:
    - location: City name or zip code (required)
    - service_type: Type of service (optional, default: 'all')
    """
    try:
        location = request.args.get('location', '').strip()
        service_type = request.args.get('service_type', 'all')

        if not location:
            return jsonify({
                'success': False,
                'error': 'Location parameter is required'
            }), 400

        # Search for local support services
        result = local_support_service.search_mental_health_services(location, service_type)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Search failed'),
                'results': [],
                'total': 0
            }), 500

    except Exception as e:
        logging.error(f"Error in local support search: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'results': [],
            'total': 0
        }), 500

@local_support_bp.route('/service-types', methods=['GET'])
@token_required
def get_service_types(current_user):
    """Get available service types"""
    try:
        service_types = local_support_service.get_service_types()
        return jsonify({
            'success': True,
            'service_types': service_types
        }), 200
    except Exception as e:
        logging.error(f"Error getting service types: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get service types'
        }), 500

@local_support_bp.route('/supported-locations', methods=['GET'])
@token_required
def get_supported_locations(current_user):
    """Get supported locations"""
    try:
        locations = local_support_service.get_supported_locations()
        return jsonify({
            'success': True,
            'locations': locations
        }), 200
    except Exception as e:
        logging.error(f"Error getting supported locations: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get supported locations'
        }), 500
