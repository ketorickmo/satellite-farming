from flask import request, jsonify, current_app
from flask_restful import Resource
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import json

from app import db
from app.models.paddock import Paddock
from app.models.ndvi import NDVIHistory
from app.schemas.ndvi import ndvi_schema, ndvi_list_schema
from app.services.agromonitoring import AgromonitoringService
from app.utils.helpers import format_exception, parse_datetime, get_ndvi_health_status

class NDVIResource(Resource):
    def get(self, paddock_id):
        """Get NDVI data for a specific paddock"""
        try:
            paddock = Paddock.query.get(paddock_id)
            if not paddock:
                return {"message": f"Paddock with ID {paddock_id} not found"}, 404
                
            # Check for date range parameters
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            # Parse dates if provided
            start_date = parse_datetime(start_date) if start_date else None
            end_date = parse_datetime(end_date) if end_date else None
            
            current_app.logger.info(f"Fetching NDVI data for paddock {paddock_id} (Agromonitoring ID: {paddock.agromonitoring_id})")
            current_app.logger.info(f"Date range: {start_date} to {end_date}")
            
            # Initialize Agromonitoring service
            agro_service = AgromonitoringService()
            
            # Get satellite imagery metadata
            images = agro_service.get_satellite_imagery(
                paddock.agromonitoring_id,
                start_date,
                end_date
            )
            
            current_app.logger.info(f"Retrieved {len(images)} satellite images")
            current_app.logger.info(f"Satellite images: {json.dumps(images, indent=2)}")
            
            if not images:
                return {"message": "No satellite imagery available for this paddock"}, 404
            
            # Get the latest image for current NDVI display
            latest_image = next((img for img in images if img.get('image', {}).get('ndvi')), None)
            
            if not latest_image:
                return {"message": "No NDVI data available for this paddock"}, 404
            
            current_app.logger.info(f"Latest image: {json.dumps(latest_image, indent=2)}")
            
            # Get NDVI data for the latest image
            ndvi_url = latest_image['image']['ndvi']
            current_app.logger.info(f"NDVI URL: {ndvi_url}")
            
            ndvi_data = agro_service.get_ndvi_data(paddock.agromonitoring_id, ndvi_url)
            current_app.logger.info(f"NDVI data: {json.dumps(ndvi_data, indent=2)}")
            
            # Get historical NDVI data
            ndvi_history = agro_service.get_ndvi_history(
                paddock.agromonitoring_id,
                start_date,
                end_date
            )
            
            current_app.logger.info(f"Retrieved {len(ndvi_history)} historical NDVI records")
            
            # Prepare the response
            response = {
                'current': {
                    'date': latest_image.get('date'),
                    'statistics': ndvi_data.get('statistics', {}),
                    'tile_url': ndvi_data.get('tile_url'),
                    'image_url': ndvi_data.get('image_url'),
                    'clouds': latest_image.get('clouds'),
                    'coverage': latest_image.get('coverage'),
                    'satellite': latest_image.get('type'),
                    'sun': latest_image.get('sun', {})
                },
                'available_dates': [
                    {
                        'date': img.get('date'),
                        'clouds': img.get('clouds'),
                        'coverage': img.get('coverage'),
                        'satellite': img.get('type'),
                        'urls': img.get('image', {})
                    }
                    for img in images if img.get('image', {}).get('ndvi')
                ],
                'history': ndvi_history
            }
            
            current_app.logger.info(f"Final response: {json.dumps(response, indent=2)}")
            return response, 200
            
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error retrieving NDVI data: {error_msg}")
            return {"message": "Failed to retrieve NDVI data", "error": str(e)}, 500 