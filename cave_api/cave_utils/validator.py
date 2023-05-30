from pamda import pamda
import re
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
    def __init__(self, data, log:LogObject, prepend_path:list=[], require_all_fields:bool=True, log_unknown_fields:bool=True, **kwargs):
        self.data = data
        self.log = LogHelper(log=log, prepend_path=prepend_path)
        self.require_all_fields = require_all_fields
        self.log_unknown_fields = log_unknown_fields
        self.populate_data(**kwargs)
        self.validate()
        try:
            self.additional_validations(**kwargs)
        except Exception as e:
            self.log.add(path=[], error=f"Additional validations failed (likely due to another error)")

    def validate(self):
        if self.require_all_fields:
            for field in self.required_fields:
                if field not in self.data:
                    self.log.add(path=[field], error=f"Missing required field")
        for field, value in self.data.items():
            accepted_values = self.accepted_values.get(field, None)
            if accepted_values is not None and value not in accepted_values:
                self.log.add(path=[field], error=f"Invalid value ({value}): Acceptable values are: {accepted_values}")
                continue
            if self.log_unknown_fields:
                if field not in self.required_fields + self.optional_fields:
                    self.log.add(path=[field], error="Unknown field")
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
            ColorValidator(data=self.data, log=self.log, prepend_path=[], require_all_fields=True, is_color_option=True)
        else:
            for field in ['startGradientColor', 'endGradientColor']:
                ColorValidator(data=self.data.get(field), log=self.log, prepend_path=[field], require_all_fields=True)

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
        validator = kwargs.get('validator')
        assert validator is not None, "Must pass validator to CustomKeyValidator"
        for field, value in self.data.items():
            validator(data=value, log=self.log, prepend_path=[field], require_all_fields=True, **kwargs)

class PropValidator(CoreValidator):
    def populate_data(self):
        validation_type = self.data.get('type')
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
            'value': self.value_types.get(validation_type, None),
            'variant': str,
            'enabled': bool,
            'options': dict,
            'maxValue': (int, float),
            'minValue': (int, float),
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

        self.required_fields = {
            'head': ['name', 'type'],
            'text': ['name', 'type', 'value'],
            'num': ['name', 'type', 'value'],
            'toggle': ['name', 'type', 'value'],
            'button': ['name', 'type', 'value'],
            'selector': ['name', 'type', 'value', 'options'],
            'date': ['name', 'type', 'value'],
        }.get(validation_type, [])

        self.optional_fields = {
            'head': ['help', 'variant'],
            'text': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'minRows', 'maxRows'],
            'num': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'maxValue', 'minValue', 'numberFormat'],
            'toggle': ['help', 'enabled', 'apiCommand', 'apiCommandKeys'],
            'button': ['help', 'enabled', 'apiCommand', 'apiCommandKeys'],
            'selector': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'placeholder'],
            'date': ['help', 'enabled', 'variant', 'apiCommand', 'apiCommandKeys', 'views']
        }.get(validation_type, [])

class PropsValidator(CoreValidator):
    def populate_data(self, **kwargs):
        self.field_types = {i: dict for i in self.data.keys()}
        self.required_fields = list(self.data.keys())
        self.optional_fields = []
        self.accepted_values = {}

    def additional_validations(self, **kwargs):
        for field, value in self.data.items():
            x=PropValidator(data=value, log=self.log, prepend_path=[field], require_all_fields=self.require_all_fields, **kwargs)

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
        if layout_type == 'grid':
            for field, value in self.data.get('data',{}).items():
                LayoutValidator(data=value, log=self.log, prepend_path=['data',field], require_all_fields=True, **kwargs)

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

class ArcsNodesGeosRootValidator(CoreValidator):
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
        CustomKeyValidator(data=self.data.get('types',{}), log=self.log, prepend_path=['types'], require_all_fields=True, validator=ArcsNodesGeosTypesValidator, **kwargs)
        # ArcsNodesGeosDataValidator(data=self.data.get('data',{}), log=self.log, prepend_path=['data'], require_all_fields=True, **kwargs)

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
        CustomKeyValidator(data=self.data.get('colorByOptions',{}), log=self.log, prepend_path=['colorByOptions'], require_all_fields=True, validator=ColorByOptionValidator)
        # Validate Size By Options
        if self.top_level_key in ['nodes', 'arcs']:
            CustomKeyValidator(data=self.data.get('sizeByOptions',{}), log=self.log, prepend_path=['sizeByOptions'], require_all_fields=True, validator=SizeValidator)
        # Validate GeoJson Options
        if self.top_level_key == 'geos':
            GeoJsonValidator(data=self.data.get('geoJson',{}), log=self.log, prepend_path=['geoJson'], require_all_fields=True)
        props = self.data.get('props')
        layout = self.data.get('layout')
        if props is not None:
            PropsValidator(data=props, log=self.log, prepend_path=['props'], require_all_fields=False)
        if layout is not None:
            LayoutValidator(data=layout, log=self.log, prepend_path=['layout'], require_all_fields=True)


class MapTypeObject():
    def __init__(self, type_key:str, type_dict:dict, top_level_key:str, log:LogObject):
        # Basic Data + Validation
        assert top_level_key in ["nodes", "arcs", "geos"], "top_level_key must be one of `nodes`, `arcs`, or `geos`"
        self.type_key = type_key
        self.type_dict = type_dict
        self.top_level_key = top_level_key
        self.log = LogHelper(log=log, prepend_path=[self.top_level_key, 'types', self.type_key])

        # Special attribute for props
        self.props = pamda.pathOr({}, ['props'], self.type_dict)

        # Data
        self.validate_fields()

    def validate_fields(self):
        self.optional_fields = ["name", "props", "layout"]
        self.required_fields = ["colorByOptions", "colorBy"]
        if self.top_level_key in ['geos']:
            self.required_fields += ["geoJson", "icon"]

        if self.top_level_key in ['nodes']:
            self.required_fields += ["sizeByOptions", "sizeBy", "startSize", "endSize", "icon"]

        if self.top_level_key in ["arcs"]:
            self.required_fields += ["sizeByOptions", "sizeBy", "startSize", "endSize", "lineByOptions", "lineBy"]

        self.all_fields = self.required_fields + self.optional_fields

        for field in self.all_fields:
            field_data = pamda.path([field], self.type_dict)
            if field_data is None:
                field_type = 'required' if field in self.required_fields else 'optional'
                log_level = 'error' if field in self.required_fields else 'warning'
                self.log.add(path=[field], error=f"Missing {field_type} field.", level=log_level)
            else:
                self.validate_field_data(field, field_data)

        for key in self.type_dict.keys():
            if key not in self.all_fields:
                self.log.add(path=[key], error=f"Unknown field passed.", level="warning")

    def validate_field_data(self, field, field_data):
        if field in ["colorByOptions", "sizeByOptions", "lineByOptions"]:
            for option_key, option_dict in field_data.items():
                related_prop = pamda.pathOr(None, [option_key], self.props)
                if related_prop is None:
                    self.log.add(path=[field,option_key], error=f"Option key not found in props.", level="error")
                    continue
                related_prop_type = pamda.pathOr(None, ['type'], related_prop)
                if related_prop_type not in ['num', 'toggle', 'selector']:
                    self.log.add(path=[field,option_key], error=f"Associated prop type can not be used in sizeBy lineBy or colorBy", level="error")
                    continue
                if related_prop_type == 'num':
                    # Check for Min and Max
                    # if related_prop.get('min') is None:
                    #     self.log.add(path=[field,option_key,'min'], error=f"Associated prop type is num but min is not defined.", level="warning")
                    # if related_prop.get('min') is None:
                    #     self.log.add(path=[field,option_key,'max'], error=f"Associated prop type is num but max is not defined.", level="warning")
                    
                    # Check for startGradient and endGradient color
                    if field == "colorByOptions":
                        for gradient in ['startGradientColor', 'endGradientColor']:
                            for color in ['dark', 'light']:
                                rgb_string = pamda.pathOr("", [gradient, color], option_dict)
                                # validate that the rgb string is valid 
                                if validate_rgb_string(rgb_string) is False:
                                    self.log.add(path=[field,option_key,'gradients'], error=f"Associated prop type is num but something in your colorByOptions gradients is not properly defined.", level="error")
                elif related_prop_type == 'selector' or related_prop_type == 'toggle':
                    if field == "colorByOptions":
                        # Check that the selector options are valid
                        prop_options = pamda.pathOr({}, ['options'], related_prop).keys()
                        for prop_option_key, prop_option_rgb_string in option_dict.items():
                            if prop_option_key not in prop_options and related_prop_type == 'selector':
                                self.log.add(path=[field,option_key,prop_option_key], error=f"Selector option not found in prop options.", level="error")
                            if validate_rgb_string(prop_option_rgb_string) is False:
                                self.log.add(path=[field,option_key,prop_option_key], error=f"Selector option value is not a valid rgb string.", level="error")
                    else:
                        self.log.add(path=[field,option_key], error=f"`selector` and `toggle` prop types can only be used in colorByOptions.", level="error")
                else:
                    self.log.add(path=[field,option_key], error=f"Unsupported prop type ({related_prop_type}). Only `num` type props can be used for `lineByOptions` or `sizeByOptions`. `colorByOptions` can accept `num`, `selector` and `toggle` types", level="error")     
        elif field in ["geoJson"]:
            for option_key in ['geoJsonLayer', 'geoJsonProp']:
                option_value = field_data.get(option_key)
                if option_value is None:
                    self.log.add(path=[field,option_key], error=f"Missing required field.", level="error")
                elif not isinstance(option_value, str):
                    self.log.add(path=[field,option_key], error=f"This field must be a string", level="error")
        elif field in ["icon","startSize", "endSize", "name", "colorBy", "sizeBy", "lineBy"]:
            if not isinstance(field_data, str):
                self.log.add(path=[field], error=f"This field must be a string", level="error")
            elif field in ['colorBy', 'sizeBy']:
                related_prop = pamda.pathOr(None, [field_data], self.props)
                if related_prop is None:
                    self.log.add(path=[field], error=f"Option key not found in props.", level="error")
            elif field =='lineBy':
                if field_data not in ['dotted', 'dashed', 'solid']:
                    self.log.add(path=[field], error=f"LineBy can only be `dotted`, `dashed` or `solid` but got `{field_data}` instead.", level="error")
        elif field in ["props"]:
            props = PropsValidator(key=field, data=field_data, log=self.log, require_all_fields=False)

        elif field in ["layout"]:
            # TODO
            pass

        else:
            self.log.add(path=[field], error=f"Unknown field passed.", level="warning")

class MapDataObject():
    def __init__(self, data_key:str, data_dict:dict, top_level_key:str, session_data:dict, log:LogObject):
        self.data_key = data_key
        self.data_dict = data_dict
        self.top_level_key = top_level_key

        self.log = LogHelper(log=log, prepend_path=[self.top_level_key, 'data', self.data_key])

        self.default_props = pamda.pathOr({}, [top_level_key,'types', pamda.pathOr(None, ['type'], self.data_dict), 'props'], session_data)
        self.categories = pamda.pathOr({}, ['categories','data'], session_data)

    # def 


class Validator():
    def __init__(self, session_data, version):
        self.session_data = session_data
        # TODO: Figure out how to validate arbitrary versions
        self.version = version
        self.log = LogObject()

        self.check_top_level_keys()
        self.check_map_types()

        self.log.show()

    def check_top_level_keys(self):
        top_level_keys = self.session_data.keys()

        for check_key in [
            "appBar",
            "arcs",
            "categories",
            "dashboards",
            "geos",
            "kpis",
            "kwargs",
            "maps",
            "nodes",
            "panes",
            "settings",
            "stats",
        ]:
            if check_key not in top_level_keys:
                self.log.add(path=['top_level_keys'], error=f"Missing top level key: `{check_key}`", level='warning')

    def check_map_types(self):
        for top_level_key in ["nodes", "arcs", "geos"]:
            ArcsNodesGeosRootValidator(data=pamda.pathOr({}, [top_level_key], self.session_data), log=self.log, prepend_path=[top_level_key], top_level_key=top_level_key)
            # for type_key, type_dict in pamda.pathOr({}, [top_level_key, 'types'], self.session_data).items():
            #     MapTypeObject(type_key=type_key, type_dict=type_dict, top_level_key=top_level_key, log=self.log)

    def check_settings(self):
        pass

    def check_kwargs(self):
        pass

    def check_stats(self):
        pass

    def check_kpis(self):
        pass

    def check_dashboards(self):
        # Uses kpis and stats 
        pass

    def check_geos(self):
        pass

    def check_arcs(self):
        pass
    
    def check_nodes(self):
        pass

    def check_maps(self):
        # Uses geos nodes and arcs
        pass

    