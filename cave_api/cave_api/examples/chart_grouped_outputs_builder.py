"""
This is a more complex example that demonstrates how to use the GroupsBuilder to create grouped outputs for a chart page.

It takes advantage of functions in the pamda library to project and pivot the data to be used in the grouped outputs.

It also demonstrates how to use the GroupsBuilder to create a group hierarchy for the grouped outputs.

This file is equivalent in output to the cave_api/cave_api/examples/chart_global_outputs.py file, but it uses the GroupsBuilder to create the grouped outputs.
"""

from cave_utils.builders.groups import GroupsBuilder
from pamda import pamda

def execute_command(session_data, socket, command="init", **kwargs):

    # Specify some example data to use for the grouped outputs
    example_data = [
        {'country': 'USA', 'state': 'Michigan', 'color': 'Red', 'size': 'Medium', 'product': 'Apple', 'sales': 95, 'demand': 100},
        {'country': 'USA', 'state': 'Massachusetts', 'color': 'Red', 'size': 'Medium', 'product': 'Apple', 'sales': 100, 'demand': 108},
        {'country': 'Canada', 'state': 'Ontario', 'color': 'Red', 'size': 'Medium', 'product': 'Apple', 'sales': 100, 'demand': 115},
        {'country': 'Canada', 'state': 'Quebec', 'color': 'Red', 'size': 'Medium', 'product': 'Apple', 'sales': 98, 'demand': 110},
        {'country': 'USA', 'state': 'Michigan', 'color': 'Purple', 'size': 'Small', 'product': 'Grape', 'sales': 60, 'demand': 70},
        {'country': 'USA', 'state': 'Massachusetts', 'color': 'Purple', 'size': 'Small', 'product': 'Grape', 'sales': 65, 'demand': 78},
        {'country': 'Canada', 'state': 'Ontario', 'color': 'Purple', 'size': 'Small', 'product': 'Grape', 'sales': 67, 'demand': 67},
        {'country': 'Canada', 'state': 'Quebec', 'color': 'Purple', 'size': 'Small', 'product': 'Grape', 'sales': 75, 'demand': 89},
        {'country': 'USA', 'state': 'Michigan', 'color': 'Red', 'size': 'Small', 'product': 'Strawberry', 'sales': 80, 'demand': 95},
        {'country': 'USA', 'state': 'Massachusetts', 'color': 'Red', 'size': 'Small', 'product': 'Strawberry', 'sales': 90, 'demand': 100},
        {'country': 'Canada', 'state': 'Ontario', 'color': 'Red', 'size': 'Small', 'product': 'Strawberry', 'sales': 99, 'demand': 100},
        {'country': 'Canada', 'state': 'Quebec', 'color': 'Red', 'size': 'Small', 'product': 'Strawberry', 'sales': 98, 'demand': 98},
    ]

    # Use the pamda project statement to pull out the data for the location and product groups
    # Project is analogous to a SQL SELECT statement only keeping the specified columns
    location_group_data = pamda.project(['country', 'state'], example_data)
    product_group_data = pamda.project(['color', 'size', 'product'], example_data)

    # Create a locations group builder
    location_group_builder = GroupsBuilder(
        group_name="Locations",
        group_data=location_group_data,
        group_parents={"state": "country"},
        group_names={
            "country": "Countries",
            "state": "States",
        },
    )

    # Create a products group builder
    product_group_builder = GroupsBuilder(
        group_name="Products",
        group_data=product_group_data,
        group_parents={},
        group_names={
            "color": "Colors",
            "size": "Sizes",
            "product": "Products",
        },
    )
    
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/4.10.1"
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {"data": ["refreshButton", "chartPage"]},
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                },
                # Add an app bar button to launch a chart dashboard
                "chartPage": {
                    "icon": "md/MdBarChart",
                    "type": "page",
                    "bar": "upperLeft",
                },
            },
        },
        # Add a chart page to the app using the example map specified above
        "pages": {
            "currentPage": "chartPage",
            "data": {
                "chartPage": {
                    "pageLayout": [
                        {
                            "type": "groupedOutput",
                            "variant": "bar",
                            "groupingId": ["product", "location"],
                            "groupingLevel": ["color", "state"],
                            "statAggregation": "sum",
                            "groupedOutputDataId": "salesData",
                            "statId": "sales",
                        }
                    ],
                },
            },
        },
        "groupedOutputs": {
            "order": {
                "groupings": ["location", "product"],
            },
            # Serialize the location and product group builders to be used in the grouped outputs
            "groupings": {
                "location": location_group_builder.serialize(),
                "product": product_group_builder.serialize(),
            },
            "data": {
                # Specify a data set to be used for the grouped outputs
                "salesData": {
                    "order": {
                        "stats": [
                            "demand",
                            "sales",
                            "pctDemandMet",
                        ],
                    },
                    # Specify the stats to be used in the grouped outputs
                    "stats": {
                        "demand": {
                            "name": "Demand",
                            "calculation": "demand",
                            "unit": "units",
                        },
                        "sales": {
                            "name": "Sales",
                            "calculation": "sales",
                            "unit": "units",
                        },
                        "pctDemandMet": {
                            "name": "Percent of Demand Met",
                            "calculation": 'sales / groupSum("demand")',
                            "precision": 2,
                            "trailingZeros": True,
                            "unit": "%",
                            "unitPlacement": "after",
                        },
                    },
                    # Select the appropriate columns and pivot them to be used in the grouped outputs
                    "valueLists": pamda.pivot(pamda.project(['sales', 'demand'], example_data)),
                    # Get the relevant group ids given each item in the base data
                    "groupLists": {
                        "location": [location_group_builder.get_id(i) for i in location_group_data],
                        "product": [product_group_builder.get_id(i) for i in product_group_data],
                    },
                },
            },
        },
    }
