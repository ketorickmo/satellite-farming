import requests
import json
from datetime import datetime
from flask import current_app
from app.utils.helpers import format_exception

class AgromonitoringService:
    """Service to interact with the Agromonitoring API"""
    
    def __init__(self):
        self.api_key = current_app.config['AGROMONITORING_API_KEY']
        self.base_url = current_app.config['AGROMONITORING_API_URL']
    
    def create_polygon(self, name, geojson):
        """
        Register a polygon with the Agromonitoring API
        
        Args:
            name (str): Name of the polygon
            geojson (dict): GeoJSON representing the polygon
            
        Returns:
            dict: Response from the Agromonitoring API containing the polygon ID
        """
        try:
            url = f"{self.base_url}/polygons?appid={self.api_key}"
            
            # Convert GeoJSON to the format expected by Agromonitoring API
            if isinstance(geojson, str):
                geojson = json.loads(geojson)
            
            # If the input is already a Feature, use it as is
            if isinstance(geojson, dict) and geojson.get('type') == 'Feature':
                formatted_geojson = geojson
            else:
                # Otherwise, wrap the geometry in a Feature object
                formatted_geojson = {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": geojson.get('coordinates', []) if isinstance(geojson, dict) else geojson
                    }
                }
            
            payload = {
                "name": name,
                "geo_json": formatted_geojson
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error creating polygon in Agromonitoring API: {error_msg}")
            raise
    
    def delete_polygon(self, polygon_id):
        """
        Delete a polygon from the Agromonitoring API
        
        Args:
            polygon_id (str): The ID of the polygon to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = f"{self.base_url}/polygons/{polygon_id}?appid={self.api_key}"
            response = requests.delete(url)
            response.raise_for_status()
            return True
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error deleting polygon from Agromonitoring API: {error_msg}")
            return False
    
    def get_satellite_imagery(self, polygon_id, start_date=None, end_date=None):
        """
        Get satellite imagery data for a polygon with all available products
        
        Args:
            polygon_id (str): ID of the polygon in Agromonitoring
            start_date (datetime, optional): Start date for image search
            end_date (datetime, optional): End date for image search
            
        Returns:
            list: List of available satellite images
        """
        try:
            from datetime import timedelta
            
            # If no dates provided, use the last 30 days
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
                
            # Convert to timestamps (seconds since epoch)
            start_ts = int(start_date.timestamp())
            end_ts = int(end_date.timestamp())
            
            url = f"{self.base_url}/image/search?appid={self.api_key}&polyid={polygon_id}&start={start_ts}&end={end_ts}"
            response = requests.get(url)
            response.raise_for_status()
            
            # Process and enhance the response
            images = response.json()
            for image in images:
                # Add formatted date
                if 'dt' in image:
                    image['date'] = datetime.fromtimestamp(image['dt']).isoformat()
                # Add coverage percentage if available
                if 'dc' in image:
                    image['coverage'] = image['dc']
                # Add cloud coverage if available
                if 'cl' in image:
                    image['clouds'] = image['cl']
                    
            return images
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error getting satellite imagery from Agromonitoring API: {error_msg}")
            return []
    
    def get_ndvi_data(self, polygon_id, ndvi_url):
        """
        Get NDVI statistics for a polygon using a specific satellite image
        
        Args:
            polygon_id (str): ID of the polygon in Agromonitoring
            ndvi_url (str): Full NDVI URL from the image search response
            
        Returns:
            dict: NDVI statistics for the polygon
        """
        try:
            # Extract the preset code and image ID from the NDVI URL
            parts = ndvi_url.split('/')
            if len(parts) >= 2:
                preset_code = parts[-2]  # e.g., "020598ba200"
                image_id = parts[-1].split('?')[0]
                
                # Get statistics
                stats_url = f"{self.base_url}/stats/1.0/{preset_code}/{image_id}?appid={self.api_key}"
                current_app.logger.info(f"Requesting NDVI stats from URL: {stats_url}")
                
                stats_response = requests.get(stats_url)
                current_app.logger.info(f"Response status code: {stats_response.status_code}")
                current_app.logger.info(f"Response headers: {stats_response.headers}")
                current_app.logger.info(f"Response content: {stats_response.text}")
                
                stats_response.raise_for_status()
                stats = stats_response.json()
                
                # Get tile URL for map display
                tile_url = f"{self.base_url}/tile/1.0/{{z}}/{{x}}/{{y}}/{preset_code}/{image_id}?appid={self.api_key}"
                
                # Combine statistics and URLs
                return {
                    'statistics': stats,
                    'tile_url': tile_url,
                    'image_url': ndvi_url,
                    'preset_code': preset_code,
                    'image_id': image_id
                }
            else:
                raise ValueError("Invalid NDVI URL format")
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error getting NDVI data from Agromonitoring API: {error_msg}")
            return {}
    
    def get_ndvi_image_url(self, image_id):
        """
        Get the URL for an NDVI image
        
        Args:
            image_id (str): ID of the satellite image
            
        Returns:
            str: URL to the NDVI image
        """
        return f"{self.base_url}/image/ndvi/{image_id}?appid={self.api_key}"
    
    def get_ndvi_history(self, polygon_id, start_date=None, end_date=None):
        """
        Get historical NDVI data for a polygon
        
        Args:
            polygon_id (str): ID of the polygon in Agromonitoring
            start_date (datetime, optional): Start date for historical data
            end_date (datetime, optional): End date for historical data
            
        Returns:
            list: List of historical NDVI data
        """
        try:
            from datetime import timedelta
            
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
                
            start_ts = int(start_date.timestamp())
            end_ts = int(end_date.timestamp())
            
            url = f"{self.base_url}/ndvi/history?polyid={polygon_id}&start={start_ts}&end={end_ts}&appid={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            
            history = response.json()
            # Format dates and ensure consistent structure
            formatted_history = []
            for entry in history:
                if 'dt' in entry and 'data' in entry:
                    formatted_history.append({
                        'date': datetime.fromtimestamp(entry['dt']).isoformat(),
                        'ndvi': entry['data'].get('mean', 0),
                        'min': entry['data'].get('min', 0),
                        'max': entry['data'].get('max', 0),
                        'median': entry['data'].get('median', 0),
                        'std': entry['data'].get('std', 0)
                    })
            return formatted_history
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error getting NDVI history from Agromonitoring API: {error_msg}")
            return []
    
    def get_weather(self, lat, lon):
        """
        Get current weather data for a location
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            
        Returns:
            dict: Weather data
        """
        try:
            url = f"{self.base_url}/weather?lat={lat}&lon={lon}&appid={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            error_msg = format_exception(e)
            current_app.logger.error(f"Error getting weather data from Agromonitoring API: {error_msg}")
            return {} 