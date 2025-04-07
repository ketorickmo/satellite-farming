import json
from shapely.geometry import shape, mapping
from pyproj import Geod

def calculate_area(geojson):
    """
    Calculate the area of a GeoJSON polygon in hectares
    
    Args:
        geojson (dict or str): GeoJSON polygon
        
    Returns:
        float: Area in hectares
    """
    if isinstance(geojson, str):
        geojson = json.loads(geojson)
        
    # Create a Shapely geometry from the GeoJSON
    polygon = shape(geojson)
    
    # Use pyproj to calculate the geodesic area
    geod = Geod(ellps="WGS84")
    area_sqm = abs(geod.geometry_area_perimeter(polygon)[0])
    
    # Convert square meters to hectares
    return area_sqm / 10000

def get_centroid(geojson):
    """
    Get the centroid of a GeoJSON polygon
    
    Args:
        geojson (dict or str): GeoJSON polygon
        
    Returns:
        tuple: (longitude, latitude) of the centroid
    """
    if isinstance(geojson, str):
        geojson = json.loads(geojson)
        
    polygon = shape(geojson)
    centroid = polygon.centroid
    
    return (centroid.x, centroid.y)

def simplify_geometry(geojson, tolerance=0.001):
    """
    Simplify a GeoJSON polygon to reduce the number of points
    
    Args:
        geojson (dict or str): GeoJSON polygon
        tolerance (float): Simplification tolerance
        
    Returns:
        dict: Simplified GeoJSON polygon
    """
    if isinstance(geojson, str):
        geojson = json.loads(geojson)
        
    polygon = shape(geojson)
    simplified = polygon.simplify(tolerance, preserve_topology=True)
    
    return mapping(simplified) 