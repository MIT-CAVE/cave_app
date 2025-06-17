from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster as Socket
from pathlib import Path


def load_help_content(name: str) -> str:
    """Load help content from markdown files."""
    content_dir = Path(__file__).parent / "content"
    file_path = content_dir / "help" / f"{name}.md"
    try:
        content = file_path.read_text()
        return content
    except FileNotFoundError:
        return f"Help content '{name}' not found"


def execute_command(
    session_data: dict,
    socket: Socket,
    command: str = "init",
    **kwargs,
) -> dict:
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {"data": ["examplePane"]},
            "data": {
                # Add a pane to the app bar
                # This will add a button to the app bar that opens a pane
                # Panes are used to display additional options / data to the user
                # See the panes top level key below for more details
                "examplePane": {
                    "icon": "im/ImCogs",
                    "type": "pane",
                    "variant": "wall",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "examplePane", "pin": True}},
            "data": {
                # Create an options pane with all of the available props
                "examplePane": {
                    "name": "Example Miscellaneous Use Cases",
                    # Use various examples of each prop and variant available in the api
                    "props": {
                        "numericHeader": {
                            "name": "Numeric Props",
                            "type": "head",
                            "help": "Configure numerical inputs with fields, sliders, and incremental controls for precise data entry",
                        },
                        "numericInputExample": {
                            "name": "Truck Load Capacity",
                            "subtitle": "This example uses the `num`'s `field` variant",
                            "type": "num",
                            "maxValue": 1000,
                            "minValue": 0,
                            "notation": "standard",
                            "precision": 2,
                            "unit": "kg",
                            "fullWidth": True,
                            "help": "Enter the maximum cargo weight capacity for this delivery vehicle",
                        },
                        "numericSliderExample": {
                            "name": "Battery Level",
                            "subtitle": "This example uses the `num`'s `slider` variant",
                            "type": "num",
                            "variant": "slider",
                            "maxValue": 100,
                            "minValue": 0,
                            "unit": "%",
                            "precision": 0,
                            "color": "#66bb6a",
                            "propStyle": {
                                "& .MuiSlider-track": {
                                    "background": "linear-gradient(90deg, #f44336 0%, #ffa726 30%, #66bb6a 60%)"
                                },
                            },
                            "help": "Current electric vehicle battery charge level",
                        },
                        "incrementalSliderExample": {
                            "name": "Delivery Speed",
                            "subtitle": "This example uses the `num`'s `incslider` variant",
                            "type": "num",
                            "variant": "incslider",
                            "valueOptions": [1, 2, 3, 5, 7],  # Days to delivery
                            "unit": "days",
                            "marks": {
                                "1": {"label": "Next Day", "color": "#f44336"},
                                "2": {"label": "Express", "color": "#ffa726"},
                                "3": {"label": "Standard", "color": "#66bb6a"},
                                "5": {"label": "Economy", "color": "#42a5f5"},
                                "7": {"label": "Super Saver", "color": "#9575cd"},
                            },
                            "propStyle": {
                                ".MuiSlider-root": {"width": "500px"},
                                ".MuiSlider-markLabel": {"fontWeight": "500"},
                            },
                            "help": "Select estimated delivery time (faster delivery = higher cost)",
                        },
                        "textHeader": {
                            "name": "Text Props",
                            "type": "head",
                            "help": "Text input components for single-line entries and multi-line content with various formatting options",
                        },
                        "textInputExample": {
                            "name": "Project Name",
                            "subtitle": "This example uses the `text`'s `single` variant",
                            "type": "text",
                            "fullWidth": False,
                            "placeholder": "Enter a unique project identifier",
                            "help": "Create a unique identifier for tracking your project across systems and documentation",
                        },
                        "textAreaInputExample": {
                            "name": "Project Description",
                            "subtitle": "This example uses the `text`'s `textarea` variant",
                            "type": "text",
                            "variant": "textarea",
                            "readOnly": True,
                            "rows": 6,
                            "fullWidth": True,
                            "help": "Describe your project's goals, scope, and key features.",
                        },
                        "toggleHeader": {
                            "name": "Toggle Props",
                            "type": "head",
                            "help": "Interactive switches, buttons, and checkboxes for binary or state-based selections",
                        },
                        "toggleSwitchExample": {
                            "name": "Theme Selection",
                            "subtitle": "This example uses the `toggle`'s `switch` variant",
                            "type": "toggle",
                            "variant": "switch",
                            "label": "Light mode",
                            "icon": "md/MdOutlineLightMode",
                            "color": "#fdd835",
                            "activeLabel": "Dark mode",
                            "activeIcon": "md/MdOutlineDarkMode",
                            "activeColor": "#212121",
                            "help": "Switch between light and dark color schemes to optimize visibility in different lighting conditions",
                        },
                        "toggleButtonExample": {
                            "name": "Simulation Control",
                            "subtitle": "This example uses the `toggle`'s `switch` variant",
                            "type": "toggle",
                            "variant": "button",
                            "icon": "md/MdOutlinePlayCircle",
                            "size": 48,
                            "color": "#4caf50",
                            "label": "Start Simulation",
                            "fullWidth": True,
                            "activeIcon": "md/MdOutlinePauseCircle",
                            "activeColor": "#f57c00",
                            "activeLabel": "Pause Simulation",
                            "propStyle": {
                                "padding": "8px 24px",
                                "borderRadius": "8px",
                                "boxShadow": "0 2px 4px rgb(0 0 0 /.2)",
                                "transition": "all 0.3s ease",
                            },
                            "help": "Control the delivery route simulation playback",
                        },
                        "toggleCheckboxExample": {
                            "name": "Package Status",
                            "subtitle": "This example uses the `toggle`'s `checkbox` variant",
                            "type": "toggle",
                            "variant": "checkbox",
                            "icon": "lu/LuPackage",
                            "color": "#bd9a7a",
                            "size": 128,
                            "label": "Package sealed",
                            "activeIcon": "lu/LuPackageOpen",
                            "activeLabel": "Package opened",
                            "labelPlacement": "bottom",
                            "placement": "center",
                            "help": "Track package integrity status throughout the delivery chain for quality assurance",
                        },
                        "buttonHeader": {
                            "name": "Button Props",
                            "type": "head",
                            "help": "Action triggers with different visual styles.",
                        },
                        "filledButtonExample": {
                            "name": "Save Changes",
                            "subtitle": "This example uses the `button`'s `filled` variant",
                            "type": "button",
                            "icon": "hi/HiSave",
                            "color": "#66bb6a",
                            "apiCommand": "saveChanges",
                            "fullWidth": True,
                            "placement": "center",
                            "help": "Persist current changes to ensure data consistency across sessions",
                        },
                        "outlinedButtonExample": {
                            "name": "Delete Project",
                            "subtitle": "This example uses the `button`'s `outlined` variant",
                            "type": "button",
                            "variant": "outlined",
                            "color": "#f44336",
                            "startIcon": "hi/HiTrash",
                            "endIcon": "hi/HiExclamationCircle",
                            "placement": "bottomRight",
                            "apiCommand": "deleteProject",
                            "help": "Permanently remove project data and associated resources from the system",
                        },
                        "textButtonExample": {
                            "name": "Archive Project",
                            "subtitle": "This example uses the `button`'s `text` variant",
                            "type": "button",
                            "variant": "text",
                            "color": "#ffa726",
                            "startIcon": "hi/HiArchive",
                            "apiCommand": "archiveProject",
                            "placement": "bottomLeft",
                            "help": "Move inactive projects to long-term storage while maintaining accessibility",
                        },
                        "iconButtonExample": {
                            "name": "Visit MIT CAVE Lab's GitHub Page",
                            "subtitle": "This example uses the `button`'s `icon` variant",
                            "type": "button",
                            "size": "32px",
                            "variant": "icon",
                            "icon": "fa/FaGithub",
                            "placement": "topCenter",
                            # "container": "minimal",  # Unstyled container that will keep the prop in its layout position
                            "url": "https://github.com/MIT-CAVE",
                        },
                        "mediaHeader": {
                            "name": "Media Props",
                            "type": "head",
                            "help": "Interactive media elements showcasing MIT CAVE Lab",
                        },
                        "pictureExample": {
                            "name": "MIT CAVE Lab Visualization",
                            "subtitle": "This example uses the `media`'s `picture` variant",
                            "type": "media",
                            "variant": "picture",
                            "fullWidth": True,
                            "placement": "center",
                            "help": "Interactive 3D visualization of supply chain networks at MIT CAVE Lab",
                        },
                        "videoExample": {
                            "name": "MIT CAVE Lab Introduction",
                            "subtitle": "This example uses the `media`'s `video` variant",
                            "type": "media",
                            "variant": "video",
                            "fullWidth": True,
                            "scaleMode": "fitContainer",
                            "help": "Watch an overview of MIT CAVE Lab's mission and research initiatives",
                        },
                        "selectorHeader": {
                            "name": "Selection Props",
                            "type": "head",
                            "help": "Some help for Selection Props",
                        },
                        "dropdownItemExample": {
                            "name": "Choose Your Programming Language",
                            "subtitle": "This example uses the `selector`'s `dropdown` variant",
                            "type": "selector",
                            "variant": "dropdown",
                            "options": {
                                "python": {
                                    "name": "Python",
                                    "icon": "si/SiPython",
                                    "color": "#3776ab",
                                },
                                "rust": {
                                    "name": "Rust",
                                    "icon": "si/SiRust",
                                    "color": "#000",
                                },
                                "typescript": {
                                    "name": "TypeScript",
                                    "icon": "si/SiTypescript",
                                    "color": "#3178c6",
                                },
                                "go": {
                                    "name": "Go",
                                    "icon": "si/SiGo",
                                    "color": "#00add8",
                                },
                            },
                            "fullWidth": False,
                            "help": "Select the primary programming language for your development stack",
                        },
                        "checkboxItemExample": {
                            "name": "Message Actions",
                            "subtitle": "This example uses the `selector`'s `hcheckbox` variant",
                            "type": "selector",
                            "variant": "hcheckbox",
                            "options": {
                                "read": {
                                    "icon": "go/GoRead",
                                    "name": "Mark as unread",
                                    "activeName": "Mark as read",
                                    "activeIcon": "go/GoUnread",
                                },
                                "flag": {
                                    "icon": "tb/TbFlag3",
                                    "name": "Flag this message",
                                    "activeIcon": "tb/TbFlag3Filled",
                                    "activeName": "Unflag this message",
                                    "activeColor": "#f44336",
                                },
                                "pin": {
                                    "icon": "tb/TbPin",
                                    "name": "Pin this message",
                                    "activeIcon": "tb/TbPinFilled",
                                    "activeColor": "#90caf9",
                                    "activeName": "Unpin this message",
                                },
                            },
                            "fullWidth": True,
                            "propStyle": {"justifyContent": "space-evenly"},
                            "help": "Manage message visibility and importance in your inbox workflow",
                            "helperText": "Toggle multiple actions to highlight this message in your inbox.",
                            "propStyle": {
                                "& .MuiFormHelperText-root": {
                                    "fontSize": "14px",
                                    "marginTop": "12px",
                                    "textAlign": "center",
                                }
                            },
                        },
                        "radioItemExample": {
                            "name": "Which sorting algorithm runs in O(1) space complexity?",
                            "subtitle": "This example uses the `selector`'s `radio` variant",
                            "type": "selector",
                            "variant": "radio",
                            "size": "24px",
                            "color": "#90caf9",
                            "activeSize": "32px",
                            "options": {
                                "merge": {
                                    "name": "Merge Sort",
                                    "icon": "md/MdMerge",
                                    "activeColor": "#f44336",
                                    "activeIcon": "bi/BiSolidError",
                                    "helperText": "Incorrect! Merge Sort uses O(n) extra space.",
                                },
                                "quick": {
                                    "name": "Quick Sort",
                                    "icon": "md/MdFlashOn",
                                    "activeColor": "#66bb6a",
                                    "activeIcon": "bi/BiSolidCheckCircle",
                                    "helperText": "Correct! Quick Sort uses O(1) auxiliary space.",
                                },
                                "heap": {
                                    "name": "Heap Sort",
                                    "icon": "md/MdOutlineLayers",
                                    "activeColor": "#ffa726",
                                    "activeIcon": "bs/BsFillQuestionCircleFill",
                                    "helperText": "Not quite! Though Heap Sort is in-place, Quick Sort is the standard answer.",
                                },
                                "bubble": {
                                    "name": "Bubble Sort",
                                    "icon": "md/MdOutlineBubbleChart",
                                    "activeColor": "#ce93d8",
                                    "activeIcon": "bi/BiSolidXCircle",
                                    "helperText": "Wrong! Bubble Sort may be simple, but that's not the answer.",
                                },
                            },
                            "propStyle": {
                                "& .MuiFormHelperText-root": {
                                    "fontSize": "16px",
                                    "maxWidth": "400px",
                                }
                            },
                            "help": load_help_content("sorting_space_complexity"),
                            "helperText": "Choose the algorithm that performs in-place sorting without extra memory allocation.",
                        },
                        "hradioItemExample": {
                            "name": "Choose your AI assistant voice",
                            "subtitle": "This example uses the `selector`'s `hradio` variant",
                            "type": "selector",
                            "variant": "hradio",
                            "icon": "fc/FcManager",
                            "size": "24px",
                            "activeIcon": "fc/FcAssistant",
                            "activeSize": "48px",
                            "options": {
                                "alice": {
                                    "name": "Alice",
                                    "icon": "fc/FcBusinesswoman",
                                    "activeName": "Alice is ready!",
                                    "activeIcon": "fc/FcOnlineSupport",
                                },
                                "bob": {
                                    "name": "Bob",
                                    "activeName": "Bob is ready!",
                                },
                                "chad": {
                                    "icon": "fc/FcBusinessman",
                                    "name": "Chad (Coming soon)",
                                    "enabled": False,
                                },
                            },
                            "help": "Configure the voice synthesis preferences for AI assistant interactions",
                        },
                        "hstepperItemExample": {
                            "name": "Project Workflow Tracking",
                            "subtitle": "This example uses the `selector`'s `hstepper` variant",
                            "type": "selector",
                            "variant": "hstepper",
                            "color": "#bdbdbd",
                            "size": "20px",
                            "activeColor": "#66bb6a",
                            "activeSize": "32px",
                            "options": {
                                "requirements": {
                                    "name": "Requirements",
                                    "icon": "hi/HiClipboardCheck",
                                    "help": "Define project requirements and scope",
                                },
                                "design": {
                                    "name": "Design",
                                    "icon": "hi/HiTemplate",
                                    "help": "Create system architecture and design",
                                },
                                "development": {
                                    "name": "Development",
                                    "icon": "hi/HiCode",
                                    "help": "Implement core functionality",
                                },
                                "testing": {
                                    "name": "Testing",
                                    "icon": "hi/HiBeaker",
                                    "help": "Run tests and quality assurance",
                                },
                                "deployment": {
                                    "name": "Deployment",
                                    "icon": "hi/HiCloud",
                                    "help": "Deploy to production environment",
                                },
                            },
                            "help": "Track and manage project progression through key development phases",
                        },
                        "vstepperItemExample": {
                            "name": "Code Review Process",
                            "subtitle": "This example uses the `selector`'s `vstepper` variant",
                            "type": "selector",
                            "variant": "vstepper",
                            "color": "#bdbdbd",
                            "size": "20px",
                            "activeColor": "#ce93d8",
                            "activeSize": "40px",
                            "options": {
                                "submit": {
                                    "name": "Submit PR",
                                    "icon": "hi/HiUpload",
                                    "help": "Create and submit pull request",
                                },
                                "review": {
                                    "name": "Peer Review",
                                    "icon": "hi/HiUsers",
                                    "help": "Get feedback from team members",
                                },
                                "revise": {
                                    "name": "Revisions",
                                    "icon": "hi/HiPencil",
                                    "help": "Address review comments",
                                },
                                "approve": {
                                    "name": "Approval",
                                    "icon": "hi/HiCheck",
                                    "help": "Obtain final approval",
                                },
                            },
                            "help": "Guide code changes through a structured review and approval workflow",
                        },
                        "comboBoxItemExample": {
                            "name": "Select Project Environment",
                            "subtitle": "This example uses the `selector`'s `combobox` variant",
                            "type": "selector",
                            "variant": "combobox",
                            "placeholder": "Choose environment",
                            "options": {
                                "dev": {
                                    "name": "Development",
                                    "icon": "hi/HiTerminal",
                                    "color": "#3498db",
                                },
                                "staging": {
                                    "name": "Staging",
                                    "icon": "hi/HiBeaker",
                                    "color": "#f1c40f",
                                },
                                "prod": {
                                    "name": "Production",
                                    "icon": "hi/HiGlobeAlt",
                                    "color": "#2ecc71",
                                },
                            },
                            "help": "Set the deployment target for your application with appropriate security levels",
                        },
                        "comboBoxMultiExample": {
                            "name": "Select Project Features",
                            "subtitle": "This example uses the `selector`'s `comboboxMulti` variant",
                            "type": "selector",
                            "variant": "comboboxMulti",
                            "placeholder": "Choose features to enable",
                            "options": {
                                "auth": {
                                    "name": "Authentication",
                                    "icon": "hi/HiLockClosed",
                                    "color": "#9b59b6",
                                },
                                "api": {
                                    "name": "REST API",
                                    "icon": "hi/HiServer",
                                    "color": "#3498db",
                                },
                                "analytics": {
                                    "name": "Analytics",
                                    "icon": "hi/HiChartBar",
                                    "color": "#2ecc71",
                                },
                                "notifications": {
                                    "name": "Notifications",
                                    "icon": "hi/HiBell",
                                    "color": "#e74c3c",
                                },
                            },
                            "help": "Enable or disable core platform capabilities based on project requirements",
                        },
                        "nestedItemExample": {
                            "name": "Project Files",
                            "subtitle": "Example for the `selector`'s `nested` variant.",
                            "type": "selector",
                            "variant": "nested",
                            "options": {
                                "src_models": {
                                    "name": "model.py",
                                    "path": ["src", "models"],
                                    "icon": "si/SiPython",
                                },
                                "src_views": {
                                    "name": "views.py",
                                    "path": ["src", "views"],
                                    "icon": "si/SiPython",
                                },
                                "src_utils": {
                                    "name": "utils.py",
                                    "path": ["src", "utils"],
                                    "icon": "si/SiPython",
                                },
                                "test_unit": {
                                    "name": "test_units.py",
                                    "path": ["tests", "unit"],
                                    "icon": "hi/HiBeaker",
                                },
                                "test_integration": {
                                    "name": "test_integration.py",
                                    "path": ["tests", "integration"],
                                    "icon": "hi/HiBeaker",
                                },
                                "docs_api": {
                                    "name": "API.md",
                                    "path": ["docs", "api"],
                                    "icon": "si/SiMarkdown",
                                },
                                "docs_setup": {
                                    "name": "Setup.md",
                                    "path": ["docs", "setup"],
                                    "icon": "si/SiMarkdown",
                                },
                                "config_dev": {
                                    "name": "dev.yaml",
                                    "path": ["config", "environments"],
                                    "icon": "si/SiYaml",
                                },
                                "config_prod": {
                                    "name": "prod.yaml",
                                    "path": ["config", "environments"],
                                    "icon": "si/SiYaml",
                                },
                            },
                            "help": "Navigate and manage project files across different functional categories",
                        },
                        "dateTimeHeader": {
                            "name": "Date and Time Props",
                            "type": "head",
                            "help": "Some help for Date and Time Props",
                        },
                        "dateItemExample": {
                            "name": "Moon Landing Date",
                            "subtitle": "Example for the `date`'s `date` variant.",
                            "type": "date",
                            "variant": "date",
                            "help": "Record significant milestones in space exploration history",
                        },
                        "timeItemExample": {
                            "name": "Lunar Landing Time",
                            "subtitle": "Example for the `date`'s `time` variant.",
                            "type": "date",
                            "variant": "time",
                            "views": ["hours", "minutes", "seconds"],
                            "help": "Document precise timing of mission-critical events",
                        },
                        "dateTimeItemExample": {
                            "name": "First Steps on Moon",
                            "subtitle": "Example for the `date`'s `datetime` variant.",
                            "type": "date",
                            "variant": "datetime",
                            "help": "Track exact timestamps of historic achievements for archival purposes",
                        },
                        "coordinateHeader": {
                            "name": "Coordinate Props",
                            "type": "head",
                            "help": "Some help for Coordinate Props",
                        },
                        "latLngInputExample": {
                            "name": "MIT CAVE Lab Location",
                            "subtitle": "Example for the `coordinate`'s `latLngInput` variant.",
                            "type": "coordinate",
                            "variant": "latLngInput",
                            "precision": 6,
                            "help": "Enter the coordinates of MIT's Center for Transportation & Logistics",
                        },
                        "latLngMapExample": {
                            "name": "Select Meeting Point",
                            "subtitle": "Example for the `coordinate`'s `latLngMap` variant.",
                            "type": "coordinate",
                            "variant": "latLngMap",
                            # "defaultZoom": 16,
                            # "minZoom": 14,
                            # "maxZoom": 19,
                            "help": "Click on the map to select a meeting point on MIT's campus",
                        },
                        "latLngPathExample": {
                            "name": "Campus Tour Route",
                            "subtitle": "Example for the `coordinate`'s `latLngPath` variant.",
                            "type": "coordinate",
                            "variant": "latLngPath",
                            # "defaultZoom": 15,
                            # "pathColor": "#a31f34",  # MIT's primary red
                            # "pathWeight": 3,
                            "help": "A walking tour path from Killian Court to MIT CAVE Lab",
                        },
                    },
                    "values": {
                        "numericInputExample": 750.50,
                        "numericSliderExample": 75,
                        "incrementalSliderExample": 3,
                        "toggleSwitchExample": True,
                        "toggleButtonExample": False,
                        "toggleCheckboxExample": False,
                        "filledButtonExample": "Save",
                        "outlinedButtonExample": "Delete",
                        "textButtonExample": "Archive",
                        "pictureExample": "https://ctl.mit.edu/sites/ctl.mit.edu/files/inline-images/MIT_CTL_CAVE_Lab_2.png",
                        "videoExample": "https://www.youtube.com/embed/6q5R1TDmKnU",
                        "textInputExample": "cave-routing-2025",
                        "textAreaInputExample": "This project aims to optimize last-mile delivery routes using machine learning algorithms. Key features include real-time traffic integration, dynamic route adjustment, and driver mobile app integration. Target completion: Q3 2025.",
                        "dropdownItemExample": ["python"],
                        "checkboxItemExample": ["flag", "pin"],
                        "radioItemExample": ["alice"],
                        "hstepperItemExample": ["requirements"],
                        "vstepperItemExample": ["submit"],
                        "hradioItemExample": ["option_c"],
                        "comboBoxItemExample": ["dev"],
                        "comboBoxMultiExample": ["auth", "api"],
                        "nestedItemExample": [
                            "src_models",
                            "src_views",
                            "test_unit",
                            "docs_api",
                            "config_dev",
                        ],
                        "dateItemExample": "1969-07-20",
                        "timeItemExample": "20:17:40",
                        "dateTimeItemExample": "1969-07-20T20:17:40",
                        "latLngInputExample": [
                            [-71.082524, 42.361145]
                        ],  # MIT CTL Building (E40)
                        "latLngMapExample": [[-71.093773, 42.359244]],  # Killian Court
                        "latLngPathExample": [
                            [-71.093773, 42.359244],  # Start: Killian Court
                            [-71.091627, 42.359925],  # Via: Massachusetts Avenue
                            [-71.088537, 42.360639],  # Via: Vassar Street
                            [-71.082524, 42.361145],  # End: MIT CTL Building
                        ],
                    },
                    "layout": {
                        "type": "grid",
                        "numColumns": 5,
                        "numRows": "auto",
                        "data": {
                            "col1Row1": {
                                "type": "item",
                                "column": 1,
                                "row": 1,
                                "itemId": "numericHeader",
                            },
                            "col1Row2": {
                                "type": "item",
                                "column": 1,
                                "row": 2,
                                "itemId": "numericInputExample",
                            },
                            "col1Row3": {
                                "type": "item",
                                "column": 1,
                                "row": 3,
                                "itemId": "numericSliderExample",
                            },
                            "col1Row4": {
                                "type": "item",
                                "column": 1,
                                "row": 4,
                                "itemId": "incrementalSliderExample",
                            },
                            "col2Row1": {
                                "type": "item",
                                "column": 2,
                                "row": 1,
                                "itemId": "textHeader",
                            },
                            "col2Row2": {
                                "type": "item",
                                "column": 2,
                                "row": 2,
                                "itemId": "textInputExample",
                            },
                            "col2Row3": {
                                "type": "item",
                                "column": 2,
                                "row": 3,
                                "itemId": "textAreaInputExample",
                            },
                            "col3Row1": {
                                "type": "item",
                                "column": 3,
                                "row": 1,
                                "itemId": "toggleHeader",
                            },
                            "col3Row2": {
                                "type": "item",
                                "column": 3,
                                "row": 2,
                                "itemId": "toggleSwitchExample",
                            },
                            "col3Row3": {
                                "type": "item",
                                "column": 3,
                                "row": 3,
                                "itemId": "toggleButtonExample",
                            },
                            "col3Row4": {
                                "type": "item",
                                "column": 3,
                                "row": 4,
                                "itemId": "toggleCheckboxExample",
                            },
                            "col4Row1": {
                                "type": "item",
                                "column": 4,
                                "row": 1,
                                "itemId": "buttonHeader",
                            },
                            "col4Row2": {
                                "type": "item",
                                "column": 4,
                                "row": 2,
                                "itemId": "filledButtonExample",
                            },
                            "col4Row3": {
                                "type": "item",
                                "column": 4,
                                "row": 3,
                                "itemId": "outlinedButtonExample",
                            },
                            "col4Row4": {
                                "type": "item",
                                "column": 4,
                                "row": 4,
                                "itemId": "textButtonExample",
                            },
                            "col4Row5": {
                                "type": "item",
                                "column": 4,
                                "row": 5,
                                "itemId": "iconButtonExample",
                            },
                            "col5Row1": {
                                "type": "item",
                                "column": 5,
                                "row": 1,
                                "itemId": "mediaHeader",
                            },
                            "col5Row2": {
                                "type": "item",
                                "column": 5,
                                "row": 2,
                                "itemId": "pictureExample",
                            },
                            "col5Row3": {
                                "type": "item",
                                "column": 5,
                                "row": 3,
                                "itemId": "videoExample",
                            },
                            "col6Row1": {
                                "type": "item",
                                "column": 6,
                                "row": 1,
                                "itemId": "selectorHeader",
                            },
                            "col6Row2": {
                                "type": "item",
                                "column": 6,
                                "row": 2,
                                "itemId": "dropdownItemExample",
                            },
                            "col6Row3": {
                                "type": "item",
                                "column": 6,
                                "row": 3,
                                "itemId": "checkboxItemExample",
                            },
                            "col6Row4": {
                                "type": "item",
                                "column": 6,
                                "row": 4,
                                "itemId": "radioItemExample",
                            },
                            "col6Row5": {
                                "type": "item",
                                "column": 6,
                                "row": 5,
                                "itemId": "hradioItemExample",
                            },
                            "col6Row6": {
                                "type": "item",
                                "column": 6,
                                "row": 6,
                                "itemId": "comboBoxItemExample",
                            },
                            "col6Row7": {
                                "type": "item",
                                "column": 6,
                                "row": 7,
                                "itemId": "comboBoxMultiExample",
                            },
                            "col6Row8": {
                                "type": "item",
                                "column": 6,
                                "row": 8,
                                "itemId": "hstepperItemExample",
                            },
                            "col6Row9": {
                                "type": "item",
                                "column": 6,
                                "row": 9,
                                "itemId": "vstepperItemExample",
                            },
                            "col6Row10": {
                                "type": "item",
                                "column": 6,
                                "row": 10,
                                "itemId": "nestedItemExample",
                            },
                            "col7Row1": {
                                "type": "item",
                                "column": 7,
                                "row": 1,
                                "itemId": "dateTimeHeader",
                            },
                            "col7Row2": {
                                "type": "item",
                                "column": 7,
                                "row": 2,
                                "itemId": "dateItemExample",
                            },
                            "col7Row3": {
                                "type": "item",
                                "column": 7,
                                "row": 3,
                                "itemId": "timeItemExample",
                            },
                            "col7Row4": {
                                "type": "item",
                                "column": 7,
                                "row": 4,
                                "itemId": "dateTimeItemExample",
                            },
                            "col8Row1": {
                                "type": "item",
                                "column": 8,
                                "row": 1,
                                "itemId": "coordinateHeader",
                            },
                            "col8Row2": {
                                "type": "item",
                                "column": 8,
                                "row": 2,
                                "itemId": "latLngInputExample",
                            },
                            "col8Row3": {
                                "type": "item",
                                "column": 8,
                                "row": 3,
                                "itemId": "latLngMapExample",
                            },
                            "col8Row4": {
                                "type": "item",
                                "column": 8,
                                "row": 4,
                                "itemId": "latLngPathExample",
                            },
                        },
                    },
                },
            },
        },
    }
