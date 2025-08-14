# Custom Raster Tiles and Coordinate Systems

Instead of just a world map, the cave app also supports custom maps. This allows you to display any image you like, such as a warehouse, to support your needs. In addition, we have a `CustomCoordinateSystem` object in `cave_utils` to allow easy plotting of nodes, paths, or geographic shapes on your map.

## Raster Tiles

Having custom raster tiles allows you to display a custom map such as this in the cave app:

![final warehouse](https://raw.githubusercontent.com/MIT-CAVE/cave_app/refs/heads/main/static/photos/finished_warehouse_example.png)

### Generating Raster Tiles

Map tiles must be generated first. If you do not currently have available tiles for the map, check out [`tile_mapping`](https://github.com/MIT-CAVE/tile_mapping) for a simple way to create the tiles you need.

<details>
<summary>Tutorial with tile_mapping</summary>

`tile_mapping` uses JSON objects to generate tiles. We encourage you to read all the documentation in the `tile_mapping` repository, including the [README](https://github.com/MIT-CAVE/tile_mapping/blob/main/README.md) and [schema](https://github.com/MIT-CAVE/tile_mapping/tree/main/schema) so you are more comfortable on generating more complex tiles. This example will use just one background image and shape to create a map.

1. Create a JSON object with basic information on your custom tiles. This includes the `tileSize` (typically 512 or 256), and the `zoom` limits, which determines at which zoom levels the map should appear. The limits must be in the range [0, 23). `start` is inclusive, `end` is not.

```
{
  "features": {
    "background-images": [],
    "shapes": [],
  },
  "tileSize": 512,
  "zoom": {
    "start": 0,
    "end": 4
  }
}
```
2. Two main features are supported: background images and shapes.
- For images, you are free to either use the image's URL or save it locally. If saving it locally, the image must be saved under `DATA_FOLDER` (defined in `src/main.js` in the `tile_mapping` repository). For each image, a new object must be created, which includes the image's `name`, `url` (only if using URL), and `zoom` limits.
  - Note: `name` must be same as the image file name if it is saved locally
  - [Example using URL](https://github.com/MIT-CAVE/tile_mapping/blob/main/examples/egypt.json)
  - [Example using local save](https://github.com/MIT-CAVE/tile_mapping/blob/main/examples/field.json?short_path=923047c)
- For shapes, it must be in GeoJSON format. You are free to either use the raw URL link to the file or directly use the GeoJSON object itself. For each image, a new object must be created, which includes the shape's `name`, `shape` (URL or raw GeoJSON object), `zoom` limits and `style`. There is also a `longLat` property, which indicates whether or not the GeoJSON object coordinates are using a (long,lat) coordinate system and if conversion is needed. This is important as the generated map uses the Mercator projection.
  - [Example using URL](https://github.com/MIT-CAVE/tile_mapping/blob/main/examples/egypt.json)
  - [Example using raw object](https://github.com/MIT-CAVE/tile_mapping/blob/main/examples/field.json?short_path=923047c)

Read the JSON [schema](https://github.com/MIT-CAVE/tile_mapping/tree/main/schema) on the listed above properties for more detail on what is expected.

Now, the JSON object should look something like this:

```
{
  "features": {
    "background-images": [
      {
        "name": "warehouse",
        "zoom": {
          "start": 0,
          "end": 4
        }
      }
    ],
    "shapes": [
      {
        "name": "Square",
        "shape": "https://website.com/square.geojson",
        "longLat": false,
        "zoom": {
          "start": 0,
          "end": 2
        },
        "style": {
          "type": "fill",
          "outline": {
            "fill": "#0000FF",
            "fill-opacity": "0.8"
          }
        }
      }
    ]
  },
  "tileSize": 512,
  "zoom": {
    "start": 0,
    "end": 4
  }
}
```
Decoding the object, it should generate a map with 4 zoom levels with a tile size of 512. The warehouse background should exist at all 4 levels whilst the square shape, filled blue, will only appear at the top two zoom levels.

3. Execute `src/main.js` in `tile_mapping` with your newly created JSON object. This will generate the tiles and store them in a newly created folder, `tiles/`.
</details>

### Using Raster Tiles

Once the tiles have been created, host them on a third-party website of your choice and ensure the tiles can be requested by a URL in a format similar to this: 
```
https://website.com/{z}/{x}/{y}.png
```

This URL can now be used in your `cave_api` as the source for your raster tiles. Example maps using custom tiles are found in `your_app/cave_api/cave_api/examples/map_custom_tiles`, which contains four different map projections in a 2x2 grid format. This includes three grid maps with different aspect ratios (1:1, 2:1, 1:2) and a simple warehouse map.

Upon running the cave app with your new tiles, you should be able to see your tiles as such:

![base warehouse](https://raw.githubusercontent.com/MIT-CAVE/cave_app/refs/heads/main/static/photos/base_warehouse_example.png)

## CustomCoordinateSystem

In addition to having a custom map background for your project, adding items on top of your map is another useful feature. However, the items' locations must be given in longitude and latitude values, which is difficult to translate onto a flat map. The `CustomCoordinateSystem` object eases the process of adding features at specific points as it allows you to use a Cartesian coordinate system on your map to place objects.

### Example

Say our custom map is a simple grid and we want to place red dots at certain coordinates and connect them with green lines. Instead of manually trying to translate the (x, y, optional z) position of each dot to (longitude, latitude, optional altitude), we can use the `CustomCoordinateSystem` to convert the coordinates for us. Let's say we have a grid like such that is 14x14:

![grid](https://raw.githubusercontent.com/MIT-CAVE/cave_app/refs/heads/main/static/photos/grid.png)

And we want to place dots on these coordinates (with the bottom left corner as (0,0)) and connect them:
- (0, 0)
- (6, 4)
- (9, 12)

First import the object from `cave_utils`:
```
from cave_utils import CustomCoordinateSystem
```

Then create the coordinate system that best works for you. A coordinate system that fits the grid works best for this example.
- Note: There is an optional third dimension you can enter for your coordinate system. If left unspecified, the value is defaulted to 10,000. However, altitude is currently not supported but is planned to be in the future.
```
grid_coordinate_system = CustomCoordinateSystem(14, 14)
```

Finally, convert the (x,y) coordinates based on your coordinate system into (long,lat) coordinates, which can now be used to plot the points. The `CustomCoordinateSystem` object currently supports three conversion methods to fit your needs. The three methods are briefly described below, though we encourage you to also read their docstrings. The object can be accessed in more detail at `cave_utils/cave_utils/custom_coordinates.py`.
- `serialize_coordinates` converts a list of coordinates in your coordinate system to a list of coordinates in (longitude, latitude, optional altitude) format. Requires manual manipulation of output to use in your API.
- `serialize_nodes` converts node coordinates in your coordinate system to a dictionary that can be used directly in your API without additional manual work (for `mapFeatures` with type `node`).
- `serialize_arcs` converts path coordinates in your coordinate system to a dictionary that can be used directly in your API without additional manual work (for `mapFeatures` with type `arc` but not `geoJson`).

The `serialize_nodes` and `serialize_arcs` methods accept `list` type and `dict` type arguments as shown below:
```
list_node_coordinates = [[0, 0], [6, 4], [9, 12]]
dict_node_coordinates = {
  "x": [0, 6, 9],
  "y": [0, 4, 12]
}
node_locations_dict = grid_coordinate_system.serialize_nodes(list_node_coordinates)

list_path_coordinates = [[[0, 0], [6, 4]], [[6, 4], [9, 12]]]
dict_path_coordinates = [
  {
    "x": [0, 6],
    "y": [0, 4]
  },
  {
    "x": [6, 9],
    "y": [4, 12]
  }
]
path_locations_dict = grid_coordinate_system.serialize_arcs(dict_path_coordinates)
```

![final grid](https://raw.githubusercontent.com/MIT-CAVE/cave_app/refs/heads/main/static/photos/grid_example.png)

We can then apply this principle to the warehouse map from earlier to add a path and robot node with ease:
![final warehouse](https://raw.githubusercontent.com/MIT-CAVE/cave_app/refs/heads/main/static/photos/finished_warehouse_example.png)
