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
            if isinstance(value, (list,dict,)) and accepted_values is not None:
                check_value = value
                if isinstance(value, dict):
                    check_value = list(value.keys())
                value_diff = pamda.difference(check_value, accepted_values)
                if len(value_diff) > 0:
                    self.log.add(path=[field], error=f"Invalid values ({value_diff}): Acceptable values are: {accepted_values}")
                    continue
            else:
                if accepted_values is not None and value not in accepted_values:
                    self.log.add(path=[field], error=f"Invalid value ({value}): Acceptable values are: {accepted_values}")
                    continue
            if field not in self.required_fields + self.optional_fields:
                self.log.add(path=[field], error=f"Unknown field: Acceptable fields are: {self.required_fields + self.optional_fields}")
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

    def warn(self, error:str, prepend_path:list=[]):
        self.log.add(path=prepend_path, error=error, level='warning')

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

class NumberFormatValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'precision': int,
            'unit': str,
            'unitSpace': bool,
            'currency': bool,
            'trailingZeros': bool,
            'nilValue': str,
            'locale': str,
        }
        self.required_fields = []
        self.optional_fields = list(self.field_types.keys())
        self.accepted_values = {}

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
            'variant': self.allowed_variants.get(validation_type, None),
            'views': ['year', 'day', 'hours', 'minutes'],
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

        if validation_type=='selector':
            self.accepted_values['value']=list(self.data.get('options', {}).keys())

        if kwargs.get('is_context', False):
            self.optional_fields += ['selectableCategories', 'label']
            self.accepted_values.update({
                'selectableCategories': list(kwargs.get('categories_key_values', {}).keys()),
            })
            self.field_types.update({
                'selectableCategories': list,
                'label': str
            })

    def additional_validations(self, **kwargs):
        is_types_prop = kwargs.get('is_types_prop', False)
        validation_type = self.data.get('type')

        if validation_type == 'num':
            number_format = self.data.get('numberFormat')
            if number_format:
                NumberFormatValidator(data=number_format, log=self.log, prepend_path=['numberFormat'])
        
        elif validation_type == 'selector':
            if self.data.get('variant') != 'checkbox' and len(self.data.get('value',[])) > 1:
                self.error("Only one value can be selected for this variant.", prepend_path=['value'])

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

        self.accepted_values = {
            'type': ['grid', 'item'],
        }

        if layout_type == 'grid':
            self.required_fields = ['type', 'numColumns', 'numRows', 'data']
            self.optional_fields = []

        elif layout_type == 'item':
            self.required_fields = ['type', 'itemId']
            self.optional_fields = ['column', 'row']
            self.accepted_values['itemId'] = kwargs.get('acceptable_keys', [])

        else:
            self.required_fields = []
            self.optional_fields = ['type', 'numColumns', 'numRows', 'data', 'itemId', 'column', 'row']


        if isinstance(self.data.get("numColumns", None), str):
            self.accepted_values['numColumns'] = ['auto', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if isinstance(self.data.get("numRows", None), str):
            self.accepted_values['numRows'] = ['auto', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def additional_validations(self, **kwargs):
        layout_type = self.data.get("type", None)
        if layout_type == 'grid':
            for field, value in self.data.get('data',{}).items():
                LayoutValidator(data=value, log=self.log, prepend_path=['data',field], **kwargs)

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
            acceptable_keys = list(props.keys()) if props is not None else []
            LayoutValidator(data=layout, log=self.log, prepend_path=['layout'], acceptable_keys=acceptable_keys)

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
            acceptable_keys = list(props.keys()) if props is not None else []
            LayoutValidator(data=layout, log=self.log, prepend_path=['layout'], acceptable_keys=acceptable_keys, **kwargs)
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

class AppBarValidator(CoreValidator):
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
        data = self.data.get('data',{})
        if 'appBarId' in data:
            # Note: Can pop since this is a deep copy of the data when passed in to the CoreValidator __init__ function
            appBarId = data.pop('appBarId')
            if not isinstance(appBarId, str):
                self.log.error('appBarId must be a string', prepend_path=['data','appBarId'])
            if appBarId not in data:
                self.log.error('appBarId must be a key in the data dictionary', prepend_path=['data','appBarId'])
        CustomKeyValidator(data=data, log=self.log, prepend_path=['data'], validator=AppBarDataValidator, **kwargs)

class AppBarDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'icon': str,
            'type': str,
            'bar': str,
            'order': int,
            'color': dict,
            'apiCommand': str,
            'apiCommandKeys': list,
        }
        self.accepted_values ={
            'type': ['map', 'stats', 'kpi', 'pane', 'button'],
            'bar': ['upper', 'lower'],
        }
        self.required_fields = ['icon', 'type', 'bar']
        self.optional_fields = ['order', 'color', 'apiCommand', 'apiCommandKeys']

    def additional_validations(self, **kwargs):
        color = self.data.get('color')
        if color:
            ColorValidator(data=color, log=self.log, prepend_path=['color'])

class KpisValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'data': dict,
            'layout': dict,
            'allowModification': bool,
            'sendToApi': bool,
            'sendToClient': bool,
        }

        self.accepted_values = {}

        self.required_fields = ['data']

        self.optional_fields = ['allowModification', 'sendToApi', 'sendToClient', 'layout']
        
    def additional_validations(self, **kwargs):
        data = self.data.get('data',{})
        layout = self.data.get('layout')

        CustomKeyValidator(data=data, log=self.log, prepend_path=['data'], validator=KpisDataValidator, **kwargs)

        if layout is not None:
            acceptable_keys = list(data.keys()) if data is not None else []
            LayoutValidator(data=layout, log=self.log, prepend_path=['layout'], acceptable_keys=acceptable_keys)

class KpisDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        validation_type = self.data.get('type', 'num')

        self.allowed_variants = {
            'head': ['column', 'row'],
        }

        self.value_types = {
            'num': (int, float),
            'text': str,
            'head': type(None)
        }

        self.field_types = {
            'type': str,
            'name': str,
            'icon': str,
            'mapKpi': bool,
            'numberFormat': dict,
            'variant': str,
            'value': self.value_types.get(validation_type, type(None)),
        }

        self.accepted_values = {
            'type': ['head', 'num', 'text'],
            'variant': self.allowed_variants.get(validation_type, [])
        }

        self.required_fields = ['name', 'icon']

        self.optional_fields = ['type', 'mapKpi', 'variant', 'value']

        if validation_type != 'head':
            self.required_fields.append('value')

        if validation_type == 'num':
            self.optional_fields.append('numberFormat')

    def additional_validations(self, **kwargs):
        numberFormat = self.data.get('numberFormat')
        if numberFormat:
            NumberFormatValidator(data=numberFormat, log=self.log, prepend_path=['numberFormat'])

class DashboardsValidator(CoreValidator):
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
        data = self.data.get('data',{})
        CustomKeyValidator(data=data, log=self.log, prepend_path=['data'], validator=DashboardDataValidator, **kwargs)

class DashboardDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'dashboardLayout': list,
            'statOptions': list,
            'lockedLayout': bool,
        }

        self.accepted_values = {
            'statOptions': kwargs.get('acceptable_stats', [])
        }

        self.required_fields = ['dashboardLayout']

        self.optional_fields = ['statOptions', 'lockedLayout']

    def additional_validations(self, **kwargs):
        for idx, layout in enumerate(self.data.get('dashboardLayout',[])):
            DashboardLayoutValidator(data=layout, log=self.log, prepend_path=['dashboardLayout', idx], **kwargs)

class DashboardLayoutValidator(CoreValidator):
    def populate_data(self, **kwargs):
        categories = kwargs.get('categories_key_levels', {})

        self.field_types = {
            'type': str,
            'chart': str,
            'grouping': str,
            'kpi': (str, list,),
            'statistic': (str, list,),
            'level': str,
            'category': str,
            'level2': str,
            'category2': str,
            'sessions': list,

        }

        self.accepted_values = {
            'type': ['stats', 'kpis'],
            'statistic': kwargs.get('acceptable_stats', []),
            'kpi': kwargs.get('acceptable_kpis', []),
            'category': list(categories.keys()),
            'category2': list(categories.keys()),
            'level': categories.get(self.data.get('category'), []),
            'level2': categories.get(self.data.get('category2'), []),
        }

        self.required_fields = ['chart', 'grouping']

        self.optional_fields = ['type', 'level', 'category', 'level2', 'category2', 'sessions']

        if self.data.get('type') == 'kpis':
            self.optional_fields.append('kpi')
        else:
            self.optional_fields.append('statistic')

class MapsValidator(CoreValidator):
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
        data = self.data.get('data',{})
        CustomKeyValidator(data=data, log=self.log, prepend_path=['data'], validator=MapDataValidator, **kwargs)

class MapDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'defaultViewport': dict,
            'optionalViewports': dict,
            'legendGroups': dict,
        }

        self.accepted_values = {}

        self.required_fields = ['defaultViewport', 'legendGroups']

        self.optional_fields = ['optionalViewports']

    def additional_validations(self, **kwargs):
        ViewportValidator(data=self.data.get('defaultViewport',{}), log=self.log, prepend_path=['defaultViewport'], **kwargs)
        
        for viewportId, viewport in self.data.get('optionalViewports',{}).items():
            ViewportValidator(data=viewport, log=self.log, prepend_path=['optionalViewports', viewportId], is_optional_viewport=True, **kwargs)

        CustomKeyValidator(data=self.data.get('legendGroups',{}), log=self.log, prepend_path=['legendGroups'], validator=LegendGroupsValidator, **kwargs)

class LegendGroupsValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'name': str,
            'nodes': dict,
            'arcs': dict,
            'geos': dict,
            'order': int,
        }

        self.accepted_values = {}

        self.required_fields = ['name']

        self.optional_fields = ['nodes', 'arcs', 'geos', 'order']

    def additional_validations(self, **kwargs):
        options_dicts = {
            'nodes': kwargs.get('node_prop_options', []),
            'arcs': kwargs.get('arc_prop_options', []),
            'geos': kwargs.get('geo_prop_options', []),
        }

        for option_key, options in options_dicts.items():
            for key, value in self.data.get(option_key,{}).items():
                if key not in options:
                    self.error('Invalid key {}'.format(key))
                    continue
                LegendGroupLayersValidator(data=value, log=self.log, prepend_path=[option_key, key], layer_type=option_key, prop_options=options.get(key, []), **kwargs)

class LegendGroupLayersValidator(CoreValidator):
    def populate_data(self, **kwargs):
        layer_type = kwargs.get('layer_type')
        prop_options = kwargs.get('prop_options', [])
        categories = kwargs.get('categories_key_levels', {})

        self.field_types = {
            'value': bool,
            'sizeBy': str,
            'colorBy': str,
            'allowGrouping': bool,
            'group': bool,
            'groupCalcByColor': str,
            'groupCalcBySize': str,
            'groupScaleWithZoom': bool,
            'groupScale': (int, float,),
            'groupMatchCategory': str,
            'groupMatchCategoryLevel': str,
        }

        self.accepted_values = {
            'sizeBy': prop_options,
            'colorBy': prop_options,
            'groupCalcByColor': ["count", "sum", "mean", "median", "mode", "min", "max"],
            'groupCalcBySize': ["count", "sum", "mean", "median", "mode", "min", "max"],
            'groupMatchCategory': list(categories.keys()),
            'groupMatchCategoryLevel': categories.get(self.data.get('groupMatchCategory'), []),
        }

        self.required_fields = ['value', 'colorBy']

        self.optional_fields = []

        if layer_type == 'nodes':
            self.optional_fields.extend(['allowGrouping', 'group', 'groupCalcByColor', 'groupCalcBySize', 'groupScaleWithZoom', 'groupScale', 'groupMatchCategory', 'groupMatchCategoryLevel'])

        if layer_type  != 'geos':
            self.required_fields.append('sizeBy')

class ViewportValidator(CoreValidator):
    def populate_data(self, **kwargs):
        is_optional_viewport = kwargs.get('is_optional_viewport', False)
        self.field_types = {
            'latitude': (float, int,),
            'longitude': (float, int,),
            'zoom': (float, int,),
            'bearing': (float, int,),
            'pitch': (float, int,),
            'height': (float, int,),
            'altitude': (float, int,),
            'maxZoom': (float, int,),
            'minZoom': (float, int,),
            'icon': str,
            'name': str,
            'order': int,
        }

        self.accepted_values = {}

        self.required_fields = ['latitude', 'longitude', 'zoom']

        self.optional_fields = ['maxZoom', 'minZoom', 'height', 'altitude', 'bearing', 'pitch', 'order']

        if is_optional_viewport:
            self.required_fields += ['icon', 'name']

class PanesValidator(CoreValidator):
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
        CustomKeyValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], validator=PanesDataValidator, **kwargs)

class PanesDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        variant = self.data.get('variant')

        self.field_types = {
            'variant': str,
            'name': str,
            'props': dict,
            'layout': dict,
            'data': dict,
            'teamSyncCommand': str,
            'teamSyncCommandKeys': list,
        }

        self.accepted_values = {
            'variant': ['session', 'appSettings', 'options', 'context', 'filter'],
        }

        self.required_fields = ['name']

        self.optional_fields = ['variant']

        if variant == 'options':
            self.required_fields += ['props']
            self.optional_fields += ['layout', 'teamSyncCommand', 'teamSyncCommandKeys']
        if variant == 'context':
            self.required_fields += ['props']
            self.optional_fields += ['data', 'teamSyncCommand', 'teamSyncCommandKeys']

    def additional_validations(self, **kwargs):
        variant = self.data.get('variant')
        props_data = self.data.get('props',{})
        if variant == 'options':
            CustomKeyValidator(data=props_data, log=self.log, prepend_path=['props'], validator=PropValidator, **kwargs)
            LayoutValidator(data=self.data.get('layout',{}), log=self.log, prepend_path=['layout'], acceptable_keys=list(props_data.keys()), **kwargs)
        #TODO Finish validating context panes
        if variant == 'context': 
            CustomKeyValidator(data=props_data, log=self.log, prepend_path=['props'], validator=PropValidator, is_context=True,  **kwargs)
            CustomKeyValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], validator=PanesContextDataValidator, prop_options=list(props_data.keys()), **kwargs)

class PanesContextDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'prop': str,
            'value': (str, int, float, bool,),
            'applyCategories': dict,
        }

        self.accepted_values = {
            'prop': kwargs.get('prop_options', []),
        }

        self.required_fields = ['prop', 'value', 'applyCategories']

        self.optional_fields = []

    def additional_validations(self, **kwargs):
        PanesContextApplyCategoriesValidator(data=self.data.get('applyCategories',{}), log=self.log, prepend_path=['applyCategories'], **kwargs)

class PanesContextApplyCategoriesValidator(CoreValidator):
    def populate_data(self, **kwargs):
        categories_key_values = kwargs.get('categories_key_values', [])
        self.field_types = {i:list for i in categories_key_values.keys()}

        self.accepted_values = categories_key_values

        self.required_fields = []

        self.optional_fields = list(categories_key_values.keys())

class SettingsValidator(CoreValidator):
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
        SettingsDataValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], **kwargs)

class SettingsDataValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'sync': dict,
            'iconUrl': str,
            'numberFormat': dict,
            'timeLength': int,
            'timeUnits': str,
            'debug': bool,
        }

        self.accepted_values = {}

        self.required_fields = ['iconUrl']

        self.optional_fields = ['sync', 'numberFormat', 'timeLength', 'timeUnits', 'debug']

    def additional_validations(self, **kwargs):
        NumberFormatValidator(data=self.data.get('numberFormat',{}), log=self.log, prepend_path=['numberFormat'], **kwargs)
        CustomKeyValidator(data=self.data.get('sync',{}), log=self.log, prepend_path=['sync'], validator=SettingsDataSyncValidator, **kwargs)

class SettingsDataSyncValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {
            'name': str,
            'showToggle': bool,
            'value': bool,
            'data': dict,
        }

        self.accepted_values = {}

        self.required_fields = ['name', 'showToggle', 'value', 'data']

        self.optional_fields = []

    def additional_validations(self, **kwargs):
        root_data = kwargs.get('root_data',{})
        for key, path in self.data.get('data',{}).items():
            if not pamda.hasPath(path, root_data):
                self.warn(f"Path {path} does not exist.", prepend_path=['data', key])

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
        categories_key_levels = {i:list(pamda.pathOr({}, ['nestedStructure'], j).keys()) for i,j in categories_data.items()}

        # Validate Stats
        StatsValidator(data=self.data.get('stats',{}), log=self.log, prepend_path=['stats'], categories_key_values=categories_key_values)
        ## Get useful stats data for future validations
        acceptable_stats = list(pamda.pathOr({}, ['stats', 'types'], self.data).keys())

        # Validate KPIs
        KpisValidator(data=self.data.get('kpis',{}), log=self.log, prepend_path=['kpis'])
        ## Get useful kpis data for future validations
        acceptable_kpis = list(pamda.pathOr({}, ['kpis', 'data'], self.data).keys())

        # Validate Arcs nodes and Geos
        ArcsNodesGeosValidator(data=self.data.get('arcs',{}), log=self.log, prepend_path=['arcs'], top_level_key='arcs', categories_key_values=categories_key_values)
        ArcsNodesGeosValidator(data=self.data.get('nodes',{}), log=self.log, prepend_path=['nodes'], top_level_key='nodes', categories_key_values=categories_key_values)
        ArcsNodesGeosValidator(data=self.data.get('geos',{}), log=self.log, prepend_path=['geos'], top_level_key='geos', categories_key_values=categories_key_values)
        ## Get useful arcs, nodes, and geos data for future validations
        node_prop_options = {k:list(v.get('props',{}).keys()) for k,v in pamda.pathOr({}, ['nodes', 'types'], self.data).items()}
        arc_prop_options = {k:list(v.get('props',{}).keys()) for k,v in pamda.pathOr({}, ['arcs', 'types'], self.data).items()}
        geo_prop_options = {k:list(v.get('props',{}).keys()) for k,v in pamda.pathOr({}, ['geos', 'types'], self.data).items()}

        # Validate AppBar
        AppBarValidator(data=self.data.get('appBar',{}), log=self.log, prepend_path=['appBar'])

        # Validate Dashboards
        DashboardsValidator(data=self.data.get('dashboards',{}), log=self.log, prepend_path=['dashboards'], categories_key_levels=categories_key_levels, acceptable_stats=acceptable_stats, acceptable_kpis=acceptable_kpis)
        
        # Validate Kwargs
        KwargsValidator(data=self.data.get('kwargs',{}), log=self.log, prepend_path=['kwargs'])
        
        # Validate Maps
        MapsValidator(data=self.data.get('maps',{}), log=self.log, prepend_path=['maps'], categories_key_levels=categories_key_levels, node_prop_options=node_prop_options, arc_prop_options=arc_prop_options, geo_prop_options=geo_prop_options)

        # Validate Panes
        PanesValidator(data=self.data.get('panes',{}), log=self.log, prepend_path=['panes'], categories_key_values=categories_key_values)

        # Validate Settings
        SettingsValidator(data=self.data.get('settings',{}), log=self.log, prepend_path=['settings'], root_data=self.data)

class Validator():
    def __init__(self, session_data, version):
        self.session_data = session_data
        # TODO: Figure out how to validate arbitrary versions
        self.version = version
        self.log = LogObject()

        RootValidator(data=self.session_data, log=self.log, prepend_path=[])

        self.log.show()
