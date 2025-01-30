python
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Load public transportation data
transit_data = pd.read_csv('public_transport.csv')  # Example CSV file

# Load sports and entertainment venues data
venues_data = gpd.read_file('venues.geojson')  # Example GeoJSON file

# Convert transit data to GeoDataFrame
transit_data['geometry'] = transit_data.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
transit_gdf = gpd.GeoDataFrame(transit_data, geometry='geometry')

# Spatial join to find nearest transit stop to each venue
venues_with_transit = gpd.sjoin(venues_data, transit_gdf, how='left', op='intersects')

# Example function to suggest transit options
def suggest_transit_options(venue_id):
    venue = venues_with_transit[venues_with_transit['id'] == venue_id]
    stops = transit_gdf[transit_gdf.intersects(venue.geometry.iloc[0])]
    return stops[['stop_id', 'route_name', 'schedule_info']].to_dict('records')

# Example usage
venue_id = 123  # Replace with actual venue ID
transit_options = suggest_transit_options(venue_id)
print(f'Transit options for venue {venue_id}:', transit_options)
