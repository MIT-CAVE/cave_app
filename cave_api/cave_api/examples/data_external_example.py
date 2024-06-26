import requests

def execute_command(session_data, socket, command="init", **kwargs):
    # `init` is the default command that is run when a session is created
    # It should return an initial state for the app
    if command == "init":
        # Make a request to the US Census Bureau API to get the population density data for each US state
        # Define the API URL and the parameters for this request
        api_url = "https://api.census.gov/data/2021/pep/population"
        params = {
            "get": "DENSITY_2021,NAME",
            "for": "state:*",
            "key": "260e4fe4b5850a56eb7bd98d35140fba57de6dae"
        }
        
        # Make the API request with an exception handler
        try:
            response = requests.get(api_url, params=params)
            # The response from the API is a list of lists with the format:
            # [['DENSITY_2021', 'NAME', 'state'], ['58.1171593930', 'Oklahoma', '40'],...]
            population_data_raw = response.json()
            # Convert the list of lists to a dictionary with the state name as the key 
            # and the population density as the value:
            # {'Oklahoma': '58.1171593930',...}
            population_data = {i[1]: i[0] for i in population_data_raw[1:]}
            # Notify the user that the population data was successfully fetched
            socket.notify("Fetched population data!", title="Success", theme="success")
            socket.notify("This product uses the Census Bureau Data API but is not endorsed or certified by the Census Bureau.", title="Disclaimer", theme="info")
        except requests.RequestException as e:
            # If an exception is raised, notify the user that the population data was not fetched
            socket.notify("Unable to fetch population data.", title="Error", theme="error")
            population_data = {}
        
        # Define a dictionary of state codes to state names
        state_code_map = {
            'US.AL': "Alabama",
            'US.AK': "Alaska",
            'US.AZ': "Arizona",
            'US.AR': "Arkansas",
            'US.CA': "California",
            'US.CO': "Colorado",
            'US.CT': "Connecticut",
            'US.DE': "Delaware",
            'US.FL': "Florida",
            'US.GA': "Georgia",
            'US.HI': "Hawaii",
            'US.ID': "Idaho",
            'US.IL': "Illinois",
            'US.IN': "Indiana",
            'US.IA': "Iowa",
            'US.KS': "Kansas",
            'US.KY': "Kentucky",
            'US.LA': "Louisiana",
            'US.ME': "Maine",
            'US.MD': "Maryland",
            'US.MA': "Massachusetts",
            'US.MI': "Michigan",
            'US.MN': "Minnesota",
            'US.MS': "Mississippi",
            'US.MO': "Missouri",
            'US.MT': "Montana",
            'US.NE': "Nebraska",
            'US.NV': "Nevada",
            'US.NH': "New Hampshire",
            'US.NJ': "New Jersey",
            'US.NM': "New Mexico",
            'US.NY': "New York",
            'US.NC': "North Carolina",
            'US.ND': "North Dakota",
            'US.OH': "Ohio",
            'US.OK': "Oklahoma",
            'US.OR': "Oregon",
            'US.PA': "Pennsylvania",
            'US.RI': "Rhode Island",
            'US.SC': "South Carolina",
            'US.SD': "South Dakota",
            'US.TN': "Tennessee",
            'US.TX': "Texas",
            'US.UT': "Utah",
            'US.VT': "Vermont",
            'US.VA': "Virginia",
            'US.WA': "Washington",
            'US.WV': "West Virginia",
            'US.WI': "Wisconsin",
            'US.WY': "Wyoming"
        }
        
        # Create an ordered list of state geojson ids
        geo_json_values = [k for k in state_code_map.keys()]
        # Create an ordered list of population densities
        population_densities = [round(float(population_data.get(v,0)), 2) for v in state_code_map.values()]

        session_data = {
            "settings": {
                # Icon Url is used to load icons from a custom icon library
                # See the available versions provided by the cave team here:
                # https://react-icons.mitcave.com/versions.txt
                # Once you select a version, you can see the available icons in the version
                # EG: https://react-icons.mitcave.com/5.0.1/icon_list.txt
                "iconUrl": "https://react-icons.mitcave.com/5.0.1"
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
