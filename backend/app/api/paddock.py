from flask import request, jsonify, current_app
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
import uuid

from app import db
from app.models.paddock import Paddock
from app.schemas.paddock import paddock_schema, paddocks_schema
from app.services.agromonitoring import AgromonitoringService
from app.services.geometry import calculate_area
from app.utils.helpers import format_exception

class PaddockListResource(Resource):
    def get(self):
        """Get all paddocks"""
        try:
            paddocks = Paddock.query.all()
            return paddocks_schema.dump(paddocks), 200
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error fetching paddocks: {error_msg}")
            return {"message": "Failed to fetch paddocks", "error": str(e)}, 500
    
    def post(self):
        """Create a new paddock"""
        try:
            # Validate request data
            json_data = request.get_json()
            if not json_data:
                return {"message": "No input data provided"}, 400
                
            # Validate with schema
            data = paddock_schema.load(json_data)
            
            # Create paddock in database
            paddock = Paddock(
                name=data["name"],
                geometry=data["geometry"]
            )
            
            # Register polygon with Agromonitoring API
            agro_service = AgromonitoringService()
            try:
                agro_response = agro_service.create_polygon(paddock.name, paddock.geometry)
                paddock.agromonitoring_id = agro_response.get('id')
            except Exception as e:
                error_msg = format_exception(e)
                current_app.logger.error(f"Error registering polygon with Agromonitoring API: {error_msg}")
                # Still continue with creating the paddock in the database
            
            # Save to database
            db.session.add(paddock)
            db.session.commit()
            
            return paddock_schema.dump(paddock), 201
        except ValidationError as e:
            return {"message": "Validation error", "errors": e.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = format_exception(e)
            current_app.logger.error(f"Database error creating paddock: {error_msg}")
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error creating paddock: {error_msg}")
            return {"message": "Failed to create paddock", "error": str(e)}, 500

class PaddockResource(Resource):
    def get(self, paddock_id):
        """Get a specific paddock by ID"""
        try:
            paddock = Paddock.query.get(paddock_id)
            if not paddock:
                return {"message": f"Paddock with ID {paddock_id} not found"}, 404
                
            return paddock_schema.dump(paddock), 200
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error fetching paddock {paddock_id}: {error_msg}")
            return {"message": "Failed to fetch paddock", "error": str(e)}, 500
    
    def put(self, paddock_id):
        """Update a paddock"""
        try:
            # Validate request data
            json_data = request.get_json()
            if not json_data:
                return {"message": "No input data provided"}, 400
                
            # Find the paddock
            paddock = Paddock.query.get(paddock_id)
            if not paddock:
                return {"message": f"Paddock with ID {paddock_id} not found"}, 404
            
            # Validate with schema
            data = paddock_schema.load(json_data)
            
            # Update paddock attributes
            paddock.name = data["name"]
            
            # If geometry changed, update Agromonitoring API
            geometry_changed = False
            if data.get("geometry") and paddock.geometry != json_data.get("geometry"):
                paddock.geometry = data["geometry"]
                paddock.area = calculate_area(paddock.geometry)
                geometry_changed = True
            
            # Update polygon in Agromonitoring API if needed
            if geometry_changed and paddock.agromonitoring_id:
                agro_service = AgromonitoringService()
                try:
                    # Delete old polygon and create new one
                    agro_service.delete_polygon(paddock.agromonitoring_id)
                    agro_response = agro_service.create_polygon(paddock.name, paddock.geometry)
                    paddock.agromonitoring_id = agro_response.get('id')
                except Exception as e:
                    error_msg = format_exception(e)
                    current_app.logger.error(f"Error updating polygon in Agromonitoring API: {error_msg}")
            
            # Save to database
            db.session.commit()
            
            return paddock_schema.dump(paddock), 200
        except ValidationError as e:
            return {"message": "Validation error", "errors": e.messages}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = format_exception(e)
            current_app.logger.error(f"Database error updating paddock: {error_msg}")
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error updating paddock: {error_msg}")
            return {"message": "Failed to update paddock", "error": str(e)}, 500
    
    def delete(self, paddock_id):
        """Delete a paddock"""
        try:
            paddock = Paddock.query.get(paddock_id)
            if not paddock:
                return {"message": f"Paddock with ID {paddock_id} not found"}, 404
            
            # Delete from Agromonitoring API first
            if paddock.agromonitoring_id:
                agro_service = AgromonitoringService()
                try:
                    agro_service.delete_polygon(paddock.agromonitoring_id)
                except Exception as e:
                    error_msg = format_exception(e)
                    current_app.logger.error(f"Error deleting polygon from Agromonitoring API: {error_msg}")
            
            # Delete from database
            db.session.delete(paddock)
            db.session.commit()
            
            return {"message": "Paddock deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = format_exception(e)
            current_app.logger.error(f"Database error deleting paddock: {error_msg}")
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error deleting paddock: {error_msg}")
            return {"message": "Failed to delete paddock", "error": str(e)}, 500 