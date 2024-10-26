#!/usr/bin/env python3

import json
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from geopy.geocoders import Nominatim

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/cgi-bin/geolocation.py"):
            # Parse the query string to get location name
            query_components = parse_qs(self.path.split('?')[1])
            location_name = query_components.get('location', [None])[0]

            # Get coordinates
            coordinates = self.get_coordinates(location_name)

            # Send response
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(coordinates).encode('utf-8'))

    def get_coordinates(self, location_name):
        if not location_name:
            return {"error": "Location not provided"}

        geolocator = Nominatim(user_agent="my_geocoder")
        location = geolocator.geocode(location_name)
        if location:
            return {"latitude": location.latitude, "longitude": location.longitude}
        else:
            return {"error": "Location not found"}

    def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()