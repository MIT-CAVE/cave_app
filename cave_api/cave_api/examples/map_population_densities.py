import requests

def execute_command(session_data, socket, command="init", **kwargs):
    # `init` is the default command that is run when a session is created
    # It should return an initial state for the app
    if command == "init":
        #Define the API URL and the parameters for the request
        api_url = "https://api.census.gov/data/2021/pep/population"
        params = {
            "get": "DENSITY_2021,NAME",
            "for": "state:*",
            "key": "260e4fe4b5850a56eb7bd98d35140fba57de6dae"
        }
        
        #Make the API request and handle exceptions
        try:
            response = requests.get(api_url, params=params)
            population_data = response.json()
            socket.notify("Notification: `refresh population` has been triggered!")
        except requests.RequestException as e:
            print(f"Error fetching population density data: {e}")

        #Fill geo_json_values array with a list of IDs that match the geoJsonProp in the geoJson file
        geo_json_values = []
        abbreviations = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
        geo_json_values = ['US.' + abb for abb in abbreviations]

        #Fill population_densities array with a list of population densities for each US state in the same order as above
        population_densities = []
        non_states = {"District of Columbia", "Puerto Rico"}
        for [density, name, state_code] in sorted(population_data[1:],key = lambda x:x[2]):
            if name not in non_states:
                population_densities.append(float(density))

        session_data = {
            "settings": {
                # Icon Url is used to load icons from a custom icon library
                # See the available versions provided by the cave team here:
                # https://react-icons.mitcave.com/versions.txt
                # Once you select a version, you can see the available icons in the version
                # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
                "iconUrl": "https://react-icons.mitcave.com/4.10.1"
            },
            "appBar": {
                "data": {
                    # Add a simple button to the app bar to trigger the `init` command
                    # This is useful for resetting the app to its initial state and for refetching population data from the external API
                    "refreshButton": {
                        "icon": "md/MdRefresh",
                        "apiCommand": "init",
                        "type": "button",
                        "bar": "upperLeft",
                    },
                },
            },
            "maps": {
                "data": {
                    "populationMap": {
                        "name": "Population Map",
                        # Specify the default projection for the map
                        # Note: globe can only be used if you have a mapbox token
                        "currentProjection": "mercator",
                        # Specify the default viewport for the map
                        "defaultViewport": {
                            "longitude": -95.71,
                            "latitude": 39,
                            "zoom": 4.4,
                            "pitch": 0,
                            "bearing": 0,
                            "maxZoom": 12,
                            "minZoom": 0,
                        },
                        #Specify the legend groups shown on the map
                        "legendGroups": {
                            #Specify the Population Densities legend group
                            "populationDensities": {
                                "name": "Population Densities",
                                "data": {
                                    "state": {
                                        "value": True,
                                        "colorBy": "populationDensity",
                                        "colorByOptions": {
                                            "populationDensity": {
                                                "startGradientColor": "rgba(255, 0, 0, 255)",
                                                "endGradientColor": "rgba(0, 255, 0, 255)",
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    }
                }
            },
            "mapFeatures": {
                "data": {
                    "state": {
                        "type": "geo",
                        "name": "State",
                        "geoJson": {
                            # geoJsonLayer must be a URL pointing to a raw geojson file
                            # Local file support is not supported
                            # To upload your own geojson file, use a service like GitHub and upload your file there
                            # Then copy the raw URL and paste it in the geoJsonLayer field to use it
                            # See data in https://github.com/MIT-CAVE/cave_app_extras/tree/main/example_data
                            "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                            # geoJsonProp is the property in the geoJson file that contains the id you specify in the data.location.geoJsonValue field
                            "geoJsonProp": "code_hasc",
                        },
                        "props": {
                            "populationDensity": {
                                "name": "Population Density",
                                "type": "num",
                                "enabled": True,
                                "help": "The state's population density in people per square mile",
                                "unit": "People per Square Mile",
                            },
                        },
                        "data": {
                            "location": {
                                # geoJsonValue must be a list of ids that match the geoJsonProp in the geoJson file
                                # The order of the ids must match the order of the values in the data.values fields
                                "geoJsonValue": geo_json_values,
                            },
                            "valueLists": {
                                "populationDensity": population_densities,
                            }
                        }
                    },
                },     
            },
            # Add a map page to the app using the population map specified above
            "pages": {
                "currentPage": "mapPage",
                "data": {
                    "mapPage": {
                        "pageLayout": [
                            {
                                "type": "map",
                                "mapId": "populationMap",
                                "showToolbar": False,
                                "maximized": True,
                            },
                        ],
                    },
                },
            }
        }
        return session_data
