# data/action_registry.py

ACTION_REGISTRY = {
    "Animation": {
        "PlayAnimation": {
            "animationName": "string",
            "speed": "float"
        },
        "CrossFadeAnimation": {
            "animationName": "string",
            "duration": "float"
        },
        "SetAnimatorBool": {
            "parameter": "string",
            "value": "bool"
        },
        "SetAnimatorTrigger": {
            "parameter": "string"
        },
    },

    "Movement": {
        "MoveToPosition": {
            "x": "float",
            "y": "float",
            "z": "float"
        },
        "SetSpeed": {
            "speed": "float"
        },
        "Jump": {
            "force": "float"
        },
        "Teleport": {
            "x": "float",
            "y": "float",
            "z": "float"
        }
    },

    "Combat": {
        "Attack": {
            "damage": "int"
        },
        "TakeDamage": {
            "amount": "int"
        },
        "Heal": {
            "amount": "int"
        }
    },

    "Variables": {
        "SetBool": {
            "variableName": "string",
            "value": "bool"
        },
        "SetInt": {
            "variableName": "string",
            "value": "int"
        },
        "SetFloat": {
            "variableName": "string",
            "value": "float"
        }
    }
}

# Lista plana para autocompletado
ALL_ACTIONS = [
    action
    for category in ACTION_REGISTRY.values()
    for action in category.keys()
]