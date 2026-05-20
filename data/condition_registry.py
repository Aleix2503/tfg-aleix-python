CONDITION_REGISTRY = {
    "Variable": {
        "VariableCompare": {
            "variableName": "string",
            "operator": "operator",
            "value": "string"
        },
        "BoolIsTrue": {
            "variableName": "string"
        },
        "BoolIsFalse": {
            "variableName": "string"
        }
    },

    # "Target": {
    #     "HasTarget": {},
    #     "TargetInRange": {
    #         "range": "float"
    #     },
    #     "TargetOutOfRange": {
    #         "range": "float"
    #     },
    #     "CanSeeTarget": {},
    #     "LostSightOfTarget": {
    #         "duration": "float"
    #     }
    # },

    # "Combat": {
    #     "HealthBelow": {
    #         "value": "float"
    #     },
    #     "HealthAbove": {
    #         "value": "float"
    #     },
    #     "CooldownReady": {
    #         "cooldownName": "string"
    #     },
    #     "HasAmmo": {},
    #     "IsDead": {}
    # },

    # "Animation": {
    #     "AnimationFinished": {
    #         "animationName": "string"
    #     },
    #     "AnimationTimeGreater": {
    #         "animationName": "string",
    #         "normalizedTime": "float"
    #     }
    # },

    # "Time": {
    #     "TimerFinished": {
    #         "timerName": "string"
    #     },
    #     "StateTimeGreater": {
    #         "seconds": "float"
    #     }
    # },

    # "Events": {
    #     "EventReceived": {
    #         "eventName": "string"
    #     },
    #     "FlagTriggered": {
    #         "flagName": "string"
    #     }
    # },

    # "Random": {
    #     "RandomChance": {
    #         "probability": "float"
    #     }
    # }
}

ALL_CONDITIONS = [
    condition
    for category in CONDITION_REGISTRY.values()
    for condition in category.keys()
]