from pamda import pamda
import re, copy
from pprint import pp

class LogObject():
    def __init__(self, errors:dict=dict(), warnings:dict=dict()):
        self.errors = errors
        self.warnings = warnings

    def add(self, path, error, level='error'):
        assert level in ['error', 'warning'], "level must be one of `error` or `warning`"
        data = self.warnings if level == 'warning' else self.errors
        path = path + [level]
        pamda.assocPath(path=path, value=pamda.pathOr([], path, data) + [error], data=data)

    def show_errors(self):
        if self.errors != {}:
            pp("Errors:")
            pp(self.errors)

    def show_warnings(self):
        if self.warnings != {}:
            pp("Warnings:")
            pp(self.warnings)

    def show(self):
        self.show_errors()
        self.show_warnings()

class LogHelper():
    def __init__(self, log:LogObject, prepend_path:list):
        self.log = log
        self.prepend_path = prepend_path

    def add(self, path, error, level='error'):
        self.log.add(path=self.prepend_path+path, error=error, level=level)

    def show(self):
        self.log.show()

class CoreValidator:
    def __init__(self, data, log:LogObject, prepend_path:list=[], **kwargs):
        self.data = copy.deepcopy(data)
        self.log = LogHelper(log=log, prepend_path=prepend_path)
        self.populate_data(**kwargs)
        self.validate()
        # try:
        #     self.additional_validations(**kwargs)
        # except Exception as e:
        #     self.log.add(path=[], error=f"Additional validations failed (likely due to another error)")
        self.additional_validations(**kwargs)

    def validate(self):
        for field in self.required_fields:
            if field not in self.data:
                self.log.add(path=[field], error=f"Missing required field")
        for field, value in self.data.items():
            accepted_values = self.accepted_values.get(field, None)
            if accepted_values is not None and value not in accepted_values:
                self.log.add(path=[field], error=f"Invalid value ({value}): Acceptable values are: {accepted_values}")
                continue
            if field not in self.required_fields + self.optional_fields:
                self.log.add(path=[field], error=f"Unknown field")
                continue
            acceptable_types = self.field_types.get(field, type(None))
            if not isinstance(value, acceptable_types):
                self.log.add(path=[field], error=f"Invalid type ({type(value)}): Acceptable types are: {acceptable_types}")

    def additional_validations(self, **kwargs):
        pass

    def is_rgb_string_valid(self, rgb_string:str):
        try:
            if 'rgb(' != rgb_string[:4]:
                return False
            if ')' != rgb_string[-1]:
                return False
            rgb_list = rgb_string[4:-1].replace(' ','').split(',')
            for rgb in rgb_list:
                if not rgb.isdigit():
                    return False
                if int(rgb) < 0 or int(rgb) > 255:
                    return False
        except:
            return False
        return True

    def validate_rgb_string(self, rgb_string:str, prepend_path:list=[]):
        if not self.is_rgb_string_valid(rgb_string):
            self.log.add(path=prepend_path, error=f"Invalid rgb string: {rgb_string}")

    def is_url_valid(self, url:str):
        # Use Django regex for URL validation
        # See https://stackoverflow.com/a/7160778/12014156
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        is_valid = re.match(regex, url) is not None
        return re.match(regex, url) is not None

    def validate_url(self, url:str, prepend_path:list=[]):
        if not self.is_url_valid(url):
            self.log.add(path=prepend_path, error=f"Invalid URL: {url}")

    def error(self, error:str, prepend_path:list=[]):
        self.log.add(path=prepend_path, error=error)

    def validate_subset(self, subset:list, valid_values:list, prepend_path:list=[]):
        invalid_values = pamda.difference(subset, valid_values)
        if len(invalid_values) > 0:
            self.log.add(path=prepend_path, error=f'Invalid subset values: {invalid_values}')

class NumericDictValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {i:(int,float) for i in self.data.keys()}
        self.required_fields = list(self.data.keys())
        self.optional_fields = []
        self.accepted_values = {}

class ColorValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.expected_color_fields = list(self.data.keys()) if kwargs.get('is_color_option', False) else ['dark', 'light']
        self.field_types = {i:str for i in self.expected_color_fields}
        self.required_fields = self.expected_color_fields
        self.optional_fields = []
        self.accepted_values = {}

    def additional_validations(self, **kwargs):
        for field in self.expected_color_fields:
            self.validate_rgb_string(self.data.get(field,''), prepend_path=[field])

class ColorByOptionValidator(CoreValidator):
    def is_categorical(self):
        expected_keys = ['min', 'max', 'startGradientColor', 'endGradientColor']
        return len(pamda.intersection(expected_keys, list(self.data.keys())))==0

    def populate_data(self, **kwargs):
        if self.is_categorical():
            self.field_types = {i: str for i in self.data.keys()}
            self.required_fields = list(self.data.keys())
            self.optional_fields = []
        else:
            self.field_types = {
                'min': (float, int),
                'max': (float, int),
                'startGradientColor': dict,
                'endGradientColor': dict,
            }
            self.required_fields = ['startGradientColor', 'endGradientColor']
            self.optional_fields = ['min', 'max']
        self.accepted_values = {}

    def additional_validations(self, **kwargs):
        if self.is_categorical():
            ColorValidator(data=self.data, log=self.log, prepend_path=[], is_color_option=True)
        else:
            for field in ['startGradientColor', 'endGradientColor']:
                ColorValidator(data=self.data.get(field), log=self.log, prepend_path=[field])

class SizeValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'min': (float, int),
            'max': (float, int),
        }
        self.required_fields = []
        self.optional_fields = ['min', 'max']
        self.accepted_values = {}

class CustomKeyValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {i:dict for i in self.data.keys()}
        self.required_fields = list(self.data.keys())
        self.optional_fields = []
        self.accepted_values = {}


    def additional_validations(self, **kwargs):
        assert 'validator' in kwargs, "Must pass validator to CustomKeyValidator"
        validator = kwargs.pop('validator')
        for field, value in self.data.items():
            validator(data=value, log=self.log, prepend_path=[field], **kwargs)

class PropValidator(CoreValidator):
    def populate_data(self, **kwargs):
        is_types_prop = kwargs.get('is_types_prop', False)
        validation_type = self.data.get('type')
        variant = self.data.get('variant')

        self.value_types = {
            'num': (int, float),
            'toggle': bool,
            'button': str,
            'text': str,
            'selector': list,
            'date': str,
        }

        self.field_types = {
            'name': str,
            'help': str,
            'type': str,
            'placeholder': str,
            'apiCommand': str,
            'views': str,
            'apiCommandKeys': list,
            'value': self.value_types.get(validation_type, type(None)),
            'variant': str,
            'enabled': bool,
            'options': dict,
            'maxValue': (int, float),
            'minValue': (int, float),
            'maxRows': int,
            'minRows': int,
            'numberFormat': dict,
        }

        self.allowed_variants = {
            'head': ['column', 'row'],
            'text': ['textarea'],
            'num': ['slider'],
            'selector': ['dropdown', 'checkbox', 'radio', 'combobox'],
            'date': ['date', 'time', 'datetime'],
        }

        self.accepted_values = {
            'type': ["head", "num", "toggle", "button", "text", "selector", "date"],
            'views': ['year','day','hours','minutes'],
            'variant': self.allowed_variants.get(validation_type, None),
        }

        # Note this may be modified in the semi_required_fields section below
        self.required_fields = ['type'] 

        # Note this may be modified in the semi_required_fields section below
        self.optional_fields = {
            'head': ['help', 'variant'],
            'text': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'minRows', 'maxRows'],
            'num': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'maxValue', 'minValue', 'numberFormat'],
            'toggle': ['help', 'enabled', 'apiCommand', 'apiCommandKeys'],
            'button': ['help', 'enabled', 'apiCommand', 'apiCommandKeys'],
            'selector': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'placeholder'],
            'date': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'views']
        }.get(validation_type, list(self.field_types.keys()))

        # Custom code to handle semi-required fields 
        # If the prop is a types prop, then these fields are optional
        # Otherwise, they are required
        semi_required_fields = {
            'head': ['name'],
            'text': ['name','value'],
            'num': ['name','value'],
            'toggle': ['name','value'],
            'button': ['name','value'],
            'selector': ['name','value', 'options'],
            'date': ['name','value'],
        }.get(validation_type, [])

        if is_types_prop:
            self.optional_fields += semi_required_fields
        else:
            self.required_fields += semi_required_fields

        # Custom code to handle slider variant required fields
        if validation_type=='num' and variant == 'slider':
            self.required_fields += ['maxValue', 'minValue']

    def additional_validations(self, **kwargs):
        pass
        # validation_type = self.data.get('type')
        # TODO
        # if self.data.get('type') == 'num':
        #     if self.data.get('numberFormat'):
        #         CustomKeyValidator(data=self.data.get('numberFormat'), log=self.log, prepend_path=['numberFormat'])
        # if validation_type == 'selector':
        #     Ensure that the values are in the options
        #     Ensure that the correct number of options are selected

class LayoutValidator(CoreValidator):
    def populate_data(self, **kwargs):
        layout_type = self.data.get("type", None)

        self.field_types = {
            'type': str,
            'numColumns': (str, int),
            'numRows': (str, int),
            'data': dict,
            'itemId': str,
            'column': int,
            'row': int,
        }

        if layout_type == 'grid':
            self.required_fields = ['type', 'numColumns', 'numRows', 'data']
            self.optional_fields = []

        elif layout_type == 'item':
            self.required_fields = ['type', 'itemId']
            self.optional_fields = ['column', 'row']

        else:
            self.required_fields = []
            self.optional_fields = ['type', 'numColumns', 'numRows', 'data', 'itemId', 'column', 'row']

        self.accepted_values = {
            'type': ['grid', 'item'],
        }

        if isinstance(self.data.get("numColumns", None), str):
            self.accepted_values['numColumns'] = ['auto', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if isinstance(self.data.get("numRows", None), str):
            self.accepted_values['numRows'] = ['auto', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def additional_validations(self, **kwargs):
        layout_type = self.data.get("type", None)
        prop_keys = kwargs.get('prop_keys', None)
        if layout_type == 'grid':
            for field, value in self.data.get('data',{}).items():
                LayoutValidator(data=value, log=self.log, prepend_path=['data',field], **kwargs)
        else:
            itemId = self.data.get('itemId', None)
            if itemId not in prop_keys:
                self.error(f"`{itemId}` not found in props", prepend_path=['itemId'])

class GeoJsonValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'geoJsonLayer': str,
            'geoJsonProp': str,
        }
        self.required_fields = ['geoJsonLayer', 'geoJsonProp']
        self.optional_fields = []
        self.accepted_values = {}

    def additional_validations(self, **kwargs):
        self.validate_url(self.data.get('geoJsonLayer', None), prepend_path=['geoJsonLayer'])

class ArcsNodesGeosValidator(CoreValidator):
    def populate_data(self, **kwargs):
        top_level_key = kwargs.get("top_level_key", None)
        assert top_level_key in ["nodes", "arcs", "geos"], "top_level_key must be one of `nodes`, `arcs`, or `geos`"
        
        self.field_types = {
            'types': dict,
            'data': dict,
            'allowModification': bool,
            'sendToApi': bool,
            'sendToClient': bool,
        }

        self.accepted_values = {}

        self.required_fields = ['data']

        self.optional_fields = ['types', 'allowModification', 'sendToApi', 'sendToClient']
        
    def additional_validations(self, **kwargs):
        types_data = self.data.get('types',{})
        CustomKeyValidator(data=types_data, log=self.log, prepend_path=['types'], validator=ArcsNodesGeosTypesValidator, **kwargs)
        CustomKeyValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], validator=ArcsNodesGeosDataValidator, types_data=types_data, **kwargs)

class ArcsNodesGeosTypesValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.top_level_key = kwargs.get("top_level_key", None)

        self.field_types = {
            'name': str,
            'colorByOptions': dict,
            'sizeByOptions': dict,
            'lineBy': str,
            'startSize': str,
            'endSize': str,
            'props': dict,
            'layout': dict,
            'icon': str,
            'height': (float, int),
            'geoJson': dict,
        }

        self.required_fields = {
            'nodes': ['name', 'colorByOptions', 'sizeByOptions', 'startSize', 'endSize', 'icon'],
            'arcs': ['name', 'colorByOptions', 'sizeByOptions', 'startSize', 'endSize', 'lineBy'],
            'geos': ['name', 'colorByOptions', 'geoJson', 'icon'],
        }.get(self.top_level_key, [])

        self.optional_fields = {
            'nodes': ['props', 'layout'],
            'arcs': ['props', 'layout', 'height'],
            'geos': ['props', 'layout'],
        }.get(self.top_level_key, [])

        self.accepted_values = {
            'lineBy': ['dotted', 'dashed', 'solid', '3d'],
        }
    
    def additional_validations(self, **kwargs):
        # Validate Color By Options
        CustomKeyValidator(data=self.data.get('colorByOptions',{}), log=self.log, prepend_path=['colorByOptions'], validator=ColorByOptionValidator)
        # Validate Size By Options
        if self.top_level_key in ['nodes', 'arcs']:
            CustomKeyValidator(data=self.data.get('sizeByOptions',{}), log=self.log, prepend_path=['sizeByOptions'], validator=SizeValidator)
        # Validate GeoJson Options
        if self.top_level_key == 'geos':
            GeoJsonValidator(data=self.data.get('geoJson',{}), log=self.log, prepend_path=['geoJson'])
        props = self.data.get('props')
        layout = self.data.get('layout')
        if props is not None:
            CustomKeyValidator(data=props, log=self.log, prepend_path=['props'], validator=PropValidator, is_types_prop=True)
        if layout is not None:
            prop_keys = list(props.keys()) if props is not None else []
            LayoutValidator(data=layout, log=self.log, prepend_path=['layout'], prop_keys=prop_keys)

class ArcsNodesGeosDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        # Additional Setup Steps (Modify Data)
        self.types_data = kwargs.get("types_data", {})
        self.top_level_key = kwargs.get("top_level_key", None)
        if 'props' in self.data:
            self.data['props'] = pamda.mergeDeep(
                pamda.pathOr({}, [self.data.get('type'), 'props'], self.types_data), 
                self.data.get('props', {})
            )
        
        self.field_types = {
            'name': str,
            'type': str,
            'geoJsonValue': str,
            'latitude': (float, int),
            'longitude': (float, int),
            'altitude': (float, int),
            'startLatitude': (float, int),
            'startLongitude': (float, int),
            'startAltitude': (float, int),
            'startClick': int,
            'endLatitude': (float, int),
            'endLongitude': (float, int),
            'endAltitude': (float, int),
            'endClick': int,
            'category': dict,
            # Overlapping fields
            'props': dict,
            'layout': dict,
        }

        self.required_fields = {
            'nodes': ['props', 'type', 'latitude', 'longitude'],
            'arcs': ['props', 'type', 'startLatitude', 'startLongitude', 'endLatitude', 'endLongitude'],
            'geos': ['props', 'type', 'geoJsonValue'],
        }.get(self.top_level_key, [])

        self.optional_fields = {
            'nodes': ['name', 'layout', 'startClick', 'endClick', 'category', 'altitude'],
            'arcs': ['name', 'layout', 'startClick', 'endClick', 'category', 'startAltitude', 'endAltitude'],
            'geos': ['name', 'layout', 'startClick', 'endClick', 'category'],
        }.get(self.top_level_key, [])

        self.accepted_values = {
            'type': list(self.types_data.keys()),
        }

    def additional_validations(self, **kwargs):
        props = self.data.get('props')
        layout = self.data.get('layout')
        category = self.data.get('category')
        if props is not None:
            CustomKeyValidator(data=props, log=self.log, prepend_path=['props'], validator=PropValidator, **kwargs)
        if layout is not None:
            prop_keys = list(props.keys()) if props is not None else []
            LayoutValidator(data=layout, log=self.log, prepend_path=['layout'], prop_keys=prop_keys, **kwargs)
        if category is not None:
            CategoryValidator(data=category, log=self.log, prepend_path=['category'], **kwargs)

class CategoriesValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'data': dict,
            'allowModification': bool,
            'sendToApi': bool,
            'sendToClient': bool,
        }

        self.accepted_values = {}

        self.required_fields = ['data']

        self.optional_fields = ['allowModification', 'sendToApi', 'sendToClient']
        
    def additional_validations(self, **kwargs):
        CustomKeyValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], validator=CategoriesDataValidator, **kwargs)

class CategoriesDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'name': str,
            'data': dict,
            'nestedStructure': dict,
            'layoutDirection': str,
            'grouping': str,
            'order': int
        }

        self.accepted_values = {
            'layoutDirection': ['horizontal', 'vertical'],
        }

        self.required_fields = ['name', 'data', 'nestedStructure']

        self.optional_fields = ['layoutDirection', 'grouping', 'order']

    def additional_validations(self, **kwargs):
        nested_structure = self.data.get('nestedStructure')
        data = self.data.get('data')
        nested_structure_keys = list(nested_structure.keys()) if nested_structure is not None else []
        if nested_structure is not None:
            CustomKeyValidator(data=nested_structure, log=self.log, prepend_path=['nestedStructure'], validator=NestedStructureValidator, **kwargs)
        if data is not None:
            CustomKeyValidator(data=data, log=self.log, prepend_path=['data'], validator=CategoryDataValidator, nested_structure_keys=nested_structure_keys, **kwargs)

class CategoryDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        nested_structure_keys = kwargs.get('nested_structure_keys', [])
        self.field_types = {i:str for i in nested_structure_keys}
        self.required_fields = nested_structure_keys
        self.optional_fields = []
        self.accepted_values = {}

class NestedStructureValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'name': str,
            'order': int,
            'ordering': list
        }
        self.required_fields = ['name']
        self.optional_fields = ['order', 'ordering']
        self.accepted_values = {}

class CategoryValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.categories_key_values = kwargs.get('categories_key_values', {})
        self.categories_keys = list(self.categories_key_values.keys())

        self.field_types = {i:list for i in self.categories_keys}
        self.required_fields = []
        self.optional_fields = self.categories_keys
        self.accepted_values = {}

    
    def additional_validations(self, **kwargs):
        for category_id, subcategory_list in self.data.items():
            self.validate_subset(
                subset=subcategory_list, 
                valid_values=self.categories_key_values.get(category_id, []),
                prepend_path=[category_id]
            )

class StatsValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'types': dict,
            'data': dict,
            'allowModification': bool,
            'sendToApi': bool,
            'sendToClient': bool,
        }

        self.accepted_values = {}

        self.required_fields = ['types', 'data']

        self.optional_fields = ['allowModification', 'sendToApi', 'sendToClient']
        
    def additional_validations(self, **kwargs):
        CustomKeyValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], validator=StatsDataValidator, **kwargs)
        CustomKeyValidator(data=self.data.get('types',{}), log=self.log, prepend_path=['types'], validator=StatsTypesValidator, **kwargs)

class StatsTypesValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'name': str,
            'calculation': str,
            'numberFormat': dict,
            'groupByOptions': list,
            'order': int
        }

        self.accepted_values = {}

        self.required_fields = ['name', 'calculation']

        self.optional_fields = ['numberFormat', 'groupByOptions', 'order']

    def additional_validations(self, **kwargs):
        self.validate_subset(
            subset=self.data.get('groupByOptions',[]),
            valid_values=list(kwargs.get('categories_key_values', {}).keys()),
            prepend_path=['groupByOptions']
        )

class StatsDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'category': dict,
            'values': dict,
        }

        self.accepted_values = {}

        self.required_fields = ['category', 'values']

        self.optional_fields = []

    def additional_validations(self, **kwargs):
        CategoryValidator(data=self.data.get('category',{}), log=self.log, prepend_path=['category'], **kwargs)
        NumericDictValidator(data=self.data.get('values',{}), log=self.log, prepend_path=['values'], **kwargs)

class KwargsValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'wipeExisting': bool,
        }

        self.accepted_values = {}

        self.required_fields = []

        self.optional_fields = ['wipeExisting']

class RootValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'appBar': dict,
            'arcs': dict,
            'categories': dict,
            'dashboards': dict,
            'geos': dict,
            'kpis': dict,
            'kwargs': dict,
            'maps': dict,
            'nodes': dict,
            'panes': dict,
            'settings': dict,
            'stats': dict,
        }
        self.required_fields = [
            'appBar',
            'arcs',
            'categories',
            'dashboards',
            'geos',
            'kpis',
            'kwargs',
            'maps',
            'nodes',
            'panes',
            'settings',
            'stats',
        ]
        self.optional_fields = []
        self.accepted_values = {}

    def additional_validations(self, **kwargs):

        # Validate Categories
        ## Note this happens first to give useful feedback as categories are used in other validations
        CategoriesValidator(data=self.data.get('categories',{}), log=self.log, prepend_path=['categories'])
        ## Get useful categories data for future validations
        categories_data = pamda.pathOr({},['categories', 'data'], self.data)
        categories_key_values = {i:list(pamda.pathOr({}, ['data'], j).keys()) for i,j in categories_data.items()}


        # Validate Arcs nodes and Geos
        ArcsNodesGeosValidator(data=self.data.get('arcs',{}), log=self.log, prepend_path=['arcs'], top_level_key='arcs', categories_key_values=categories_key_values)
        ArcsNodesGeosValidator(data=self.data.get('nodes',{}), log=self.log, prepend_path=['nodes'], top_level_key='nodes', categories_key_values=categories_key_values)
        ArcsNodesGeosValidator(data=self.data.get('geos',{}), log=self.log, prepend_path=['geos'], top_level_key='geos', categories_key_values=categories_key_values)

        # Validate AppBar
        # Validate Dashboards
        # Validate KPIs
        # Validate Kwargs
        KwargsValidator(data=self.data.get('kwargs',{}), log=self.log, prepend_path=['kwargs'])
        # Validate Maps
        # Validate Panes
        # Validate Settings
        # Validate Stats
        StatsValidator(data=self.data.get('stats',{}), log=self.log, prepend_path=['stats'], categories_key_values=categories_key_values)
        
class Validator():
    def __init__(self, session_data, version):
        self.session_data = session_data
        # TODO: Figure out how to validate arbitrary versions
        self.version = version
        self.log = LogObject()

        RootValidator(data=self.session_data, log=self.log, prepend_path=[])

        self.log.show()
