
function_json = {
    "name": "update_map",
    "description": "Update map to center on a particular location",
    "parameters": {
        "type": "object",
        "properties": {
            "longitude": {
                "type": "number",
                "description": "Longitude of the location to center the map on"
        },
            "latitude": {
                "type": "number",
                "description": "Latitude of the location to center the map on"
                },
            "zoom": {
                "type": "integer",
                "description": "Zoom level of the map"
                }
            },
        "required": [
            "longitude",
            "latitude",
            "zoom"
            ]
        }
}