from nanohubuidl.teleport import TeleportComponent, TeleportElement, TeleportContent
from nanohubuidl.teleport import TeleportStatic, TeleportRepeat, TeleportDynamic
from nanohubuidl.material import MaterialContent

def Loader(Component, *args, **kwargs):
    Component.addStateVariable(
        kwargs.get("loader_status", "loader_status"),
        {"type": "string", "defaultValue": ""},
    )
    Component.addStateVariable(
        kwargs.get("loader_open", "loader_open"),
        {"type": "boolean", "defaultValue": kwargs.get("is_open", True)},
    )

    Loader = TeleportElement(MaterialContent(elementType="Dialog"))
    Loader.content.attrs["open"] = {
        "type": "dynamic",
        "content": {
            "referenceType": "state",
            "id": kwargs.get("open", "loader_open"),
        },
    }
    #Loader.content.attrs["disableBackdropClick"] = True
    Loader.content.attrs["disableEscapeKeyDown"] = True
    Loader.content.attrs["fullWidth"] = True
    Loader.content.attrs["maxWidth"] = "xs"
    loadercnt = TeleportElement(MaterialContent(elementType="DialogContent"))
    loadercnt.content.style = {"textAlign": "center", "overflow": "hidden"}

    LinearProgress = TeleportElement(MaterialContent(elementType="LinearProgress"))
    LinearProgress.content.attrs["color"] = "secondary"

    loadertext = TeleportElement(MaterialContent(elementType="DialogTitle"))
    loadertext.addContent(
        TeleportDynamic(
            content={
                "referenceType": "state",
                "id": kwargs.get("open", "loader_status"),
            }
        )
    )
    loadertext.content.style = {"textAlign": "center"}

    # loadercnt.addContent(loadercir)
    loadercnt.addContent(LinearProgress)
    Loader.addContent(loadercnt)
    Loader.addContent(loadertext)

    return Loader

def Error(Component, *args, **kwargs):
    Component.addStateVariable(
        kwargs.get("error_status", "error_status"),
        {"type": "string", "defaultValue": ""},
    )
    Component.addStateVariable(
        kwargs.get("error_open", "error_open"),
        {"type": "boolean", "defaultValue": False},
    )
    Error = TeleportElement(MaterialContent(elementType="Dialog"))
    Error.content.attrs["open"] = {
        "type": "dynamic",
        "content": {
            "referenceType": "state",
            "id": kwargs.get("error_open", "error_open"),
        },
    }
    Error.content.attrs["fullWidth"] = True
    Error.content.attrs["maxWidth"] = "xs"
    DialogContent = TeleportElement(MaterialContent(elementType="DialogContent"))
    DialogContent.content.style = {"textAlign": "center", "overflow": "hidden"}

    Typography = TeleportElement(MaterialContent(elementType="Typography"))
    Typography.content.attrs["variant"] = "h6"
    TypographyText = TeleportStatic(content=kwargs.get("title", "Error Message"))
    Typography.addContent(TypographyText)

    Icon0 = TeleportElement(MaterialContent(elementType="Icon"))
    Icon0.content.style = {"position": "absolute", "top": "10px", "left": "10px"}
    IconText0 = TeleportStatic(content="error")
    Icon0.addContent(IconText0)

    IconButton = TeleportElement(MaterialContent(elementType="IconButton"))
    IconButton.content.style = {
        "position": "absolute",
        "top": "10px",
        "right": "10px",
    }

    Icon = TeleportElement(MaterialContent(elementType="Icon"))
    IconText = TeleportStatic(content="close")
    Icon.addContent(IconText)
    IconButton.addContent(Icon)
    IconButton.content.events["click"] = [
        {
            "type": "stateChange",
            "modifies": kwargs.get("error_open", "error_open"),
            "newState": False,
        }
    ]

    DialogTitle = TeleportElement(MaterialContent(elementType="DialogTitle"))
    DialogTitle.content.attrs["disableTypography"] = True
    DialogTitle.content.style = {
        "textAlign": "center",
        "backgroundColor": "#d95c5c",
    }
    DialogTitle.addContent(IconButton)
    DialogTitle.addContent(Typography)
    DialogTitle.addContent(Icon0)

    DialogContent.addContent(
        TeleportDynamic(
            content={
                "referenceType": "state",
                "id": kwargs.get("error_status", "error_status"),
            }
        )
    )
    DialogContent.content.style = {"textAlign": "center"}

    Error.addContent(DialogTitle)
    Error.addContent(DialogContent)
    return Error

def AppBar(*args, **kwargs):
    AppBar = TeleportElement(MaterialContent(elementType="AppBar"))
    AppBar.content.attrs["position"] = "static"
    AppBar.content.attrs["color"] = kwargs.get("color", "primary")
    AppBar.content.style = {"width": "inherit"}

    ToolBar = TeleportElement(MaterialContent(elementType="Toolbar"))
    ToolBar.content.attrs["variant"] = kwargs.get("variant", "regular")

    Typography = TeleportElement(MaterialContent(elementType="Typography"))
    Typography.content.attrs["variant"] = "h6"
    Typography.content.style = {"flex": 1, "textAlign": "center"}
    TypographyText = TeleportStatic(content=kwargs.get("title", ""))
    Typography.addContent(TypographyText)
    
    ToolBar.addContent(Typography)
    AppBar.addContent(ToolBar)
    return AppBar


def Results(*args, **kwargs):
    results = kwargs.get("results", {})
    onClick = kwargs.get("onClick", [])
    onLoad = kwargs.get("onLoad", [])
    ToggleButtonGroup = TeleportElement(
        MaterialContent(elementType="ToggleButtonGroup")
    )
    ToggleButtonGroup.content.style = {
        "width": "100%",
        "flexDirection": "column",
        "display": "inline-flex",
    }
    ToggleButtonGroup.content.attrs["orientation"] = "vertical"
    ToggleButtonGroup.content.attrs["exclusive"] = True

    ToggleButtonGroup.content.attrs["value"] = {
        "type": "dynamic",
        "content": {"referenceType": "state", "id": "open_plot"},
    }

    for k, v in results.items():
        v_action = []
        if isinstance(v["action"], dict):
            v_action.append(v["action"])
        elif isinstance(v["action"], list):
            for va in v["action"]:
                v_action.append(va)
        v_action.append(
            {"type": "stateChange", "modifies": "open_plot", "newState": k}
        )
        ToggleButton = TeleportElement(
            MaterialContent(elementType="ToggleButton")
        )
        ToggleButton.content.attrs["value"] = k
        ToggleButton.content.events["click"] = onClick + v_action + onLoad
        Typography = TeleportElement(MaterialContent(elementType="Typography"))
        Typography.addContent(TeleportStatic(content=v["title"]))
        ToggleButton.addContent(Typography)
        ToggleButtonGroup.addContent(ToggleButton)

    return ToggleButtonGroup
