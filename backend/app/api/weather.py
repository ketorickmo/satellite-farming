from flask import request, jsonify, current_app
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app import db
from app.models.weather import WeatherData
from app.schemas.weather import weather_schema
from app.services.agromonitoring import AgromonitoringService
from app.services.geometry import get_centroid
from app.utils.helpers import format_exception

class WeatherResource(Resource):
    def get(self):
        """Get weather data for a location"""
        try:
            # Extract latitude and longitude from request
            lat = request.args.get('lat')
            lon = request.args.get('lon')
            
            # Validate coordinates
            if not lat or not lon:
                return {"message": "Latitude and longitude are required"}, 400
                
            try:
                lat = float(lat)
                lon = float(lon)
            except ValueError:
                return {"message": "Invalid coordinates format"}, 400
            
            # Check for existing weather data in the last hour
            now = datetime.utcnow()
            one_hour_ago = datetime(now.year, now.month, now.day, now.hour - 1)
            
            existing_weather = WeatherData.query.filter(
                WeatherData.date >= one_hour_ago
            ).order_by(WeatherData.date.desc()).first()
            
            # If recent data exists, return it
            if existing_weather:
                return weather_schema.dump(existing_weather), 200
            
            # Otherwise, fetch from Agromonitoring API
            agro_service = AgromonitoringService()
            weather_data = agro_service.get_weather(lat, lon)
            
            if not weather_data:
                return {"message": "Failed to retrieve weather data"}, 500
            
            # Extract relevant data
            temperature = weather_data.get('main', {}).get('temp')
            rainfall = weather_data.get('rain', {}).get('1h', 0)
            
            # Create new weather record
            weather_record = WeatherData(
                date=datetime.utcnow(),
                temperature=temperature,
                rainfall=rainfall,
                forecast=weather_data
            )
            
            # Save to database
            db.session.add(weather_record)
            db.session.commit()
            
            return weather_schema.dump(weather_record), 200
            
        except SQLAlchemyError as e:
            db.session.rollback()
            error_msg = format_exception(e)
            current_app.logger.error(f"Database error retrieving weather data: {error_msg}")
            return {"message": "Database error", "error": str(e)}, 500
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error retrieving weather data: {error_msg}")
            return {"message": "Failed to retrieve weather data", "error": str(e)}, 500 