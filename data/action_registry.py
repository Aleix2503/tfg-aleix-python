# data/action_registry.py

ACTION_REGISTRY = {

    # ─────────────────────────────────────
    # ANIMATION
    # ─────────────────────────────────────

    "Animation": {

        "PlayAnimation": {
            "animationName": "string",
            "speed": "float",
            "loop": "bool"
        },

        "CrossFadeAnimation": {
            "animationName": "string",
            "duration": "float"
        },

        "StopAnimation": {},

        "PauseAnimation": {},

        "ResumeAnimation": {},

        "SetAnimatorBool": {
            "parameter": "string",
            "value": "bool"
        },

        "SetAnimatorTrigger": {
            "parameter": "string"
        },

        "ResetAnimatorTrigger": {
            "parameter": "string"
        },

        "SetAnimatorFloat": {
            "parameter": "string",
            "value": "float"
        },

        "SetAnimatorInt": {
            "parameter": "string",
            "value": "int"
        },

        "SetAnimationLayerWeight": {
            "layer": "int",
            "weight": "float"
        }
    },

    # ─────────────────────────────────────
    # MOVEMENT
    # ─────────────────────────────────────

    "Movement": {

        "MoveToPosition": {
            "x": "float",
            "y": "float",
            "z": "float",
            "speed": "float"
        },

        "MoveToTarget": {
            "targetName": "string",
            "speed": "float"
        },

        "MoveForward": {
            "speed": "float"
        },

        "MoveBackward": {
            "speed": "float"
        },

        "Strafe": {
            "direction": "string",
            "speed": "float"
        },

        "RotateToTarget": {
            "rotationSpeed": "float"
        },

        "RotateToPosition": {
            "x": "float",
            "y": "float",
            "z": "float",
            "rotationSpeed": "float"
        },

        "LookAtTarget": {
            "targetName": "string"
        },

        "SetSpeed": {
            "speed": "float"
        },

        "StopMovement": {},

        "Jump": {
            "force": "float"
        },

        "Dash": {
            "force": "float",
            "duration": "float"
        },

        "AddForce": {
            "x": "float",
            "y": "float",
            "z": "float"
        },

        "Teleport": {
            "x": "float",
            "y": "float",
            "z": "float"
        },

        "EnableGravity": {},

        "DisableGravity": {}
    },

    # ─────────────────────────────────────
    # AI / DECISION
    # ─────────────────────────────────────

    "AI": {

        "SetTarget": {
            "targetName": "string"
        },

        "ClearTarget": {},

        "ChaseTarget": {
            "speed": "float",
            "stoppingDistance": "float"
        },

        "StopChasing": {},

        "FleeFromTarget": {
            "distance": "float",
            "speed": "float"
        },

        "Patrol": {
            "speed": "float"
        },

        "SetPatrolPoint": {
            "pointIndex": "int"
        },

        "NextPatrolPoint": {},

        "Wait": {
            "duration": "float"
        },

        "SearchLastKnownPosition": {
            "duration": "float"
        },

        "SetAggro": {
            "value": "bool"
        },

        "SetAlert": {
            "value": "bool"
        },

        "SetState": {
            "stateName": "string"
        }
    },

    # ─────────────────────────────────────
    # COMBAT
    # ─────────────────────────────────────

    "Combat": {

        "Attack": {
            "damage": "int",
            "range": "float"
        },

        "MeleeAttack": {
            "damage": "int",
            "radius": "float"
        },

        "RangedAttack": {
            "projectile": "string",
            "speed": "float",
            "damage": "int"
        },

        "EnableHitbox": {
            "hitboxName": "string"
        },

        "DisableHitbox": {
            "hitboxName": "string"
        },

        "TakeDamage": {
            "amount": "int"
        },

        "Heal": {
            "amount": "int"
        },

        "Die": {},

        "Revive": {
            "health": "int"
        },

        "ApplyKnockback": {
            "force": "float"
        },

        "SpawnProjectile": {
            "prefabName": "string",
            "speed": "float",
            "damage": "int"
        },

        "ReloadWeapon": {},

        "EquipWeapon": {
            "weaponName": "string"
        },

        "UnequipWeapon": {}
    },

    # ─────────────────────────────────────
    # AUDIO
    # ─────────────────────────────────────

    "Audio": {

        "PlaySound": {
            "clipName": "string",
            "volume": "float"
        },

        "PlayOneShot": {
            "clipName": "string",
            "volume": "float"
        },

        "StopSound": {
            "clipName": "string"
        },

        "PauseSound": {
            "clipName": "string"
        },

        "ResumeSound": {
            "clipName": "string"
        },

        "SetVolume": {
            "volume": "float"
        },

        "MuteAudio": {},

        "UnmuteAudio": {}
    },

    # ─────────────────────────────────────
    # VFX
    # ─────────────────────────────────────

    "VFX": {

        "SpawnVFX": {
            "vfxName": "string"
        },

        "DestroyVFX": {
            "vfxName": "string"
        },

        "PlayParticleSystem": {
            "systemName": "string"
        },

        "StopParticleSystem": {
            "systemName": "string"
        },

        "ShakeCamera": {
            "intensity": "float",
            "duration": "float"
        },

        "FlashScreen": {
            "duration": "float"
        },

        "ChangeColor": {
            "r": "float",
            "g": "float",
            "b": "float"
        },

        "EnableTrail": {},

        "DisableTrail": {}
    },

    # ─────────────────────────────────────
    # VARIABLES
    # ─────────────────────────────────────

    "Variables": {

        "SetBool": {
            "variableName": "string",
            "value": "bool"
        },

        "ToggleBool": {
            "variableName": "string"
        },

        "SetInt": {
            "variableName": "string",
            "value": "int"
        },

        "IncrementInt": {
            "variableName": "string",
            "amount": "int"
        },

        "DecrementInt": {
            "variableName": "string",
            "amount": "int"
        },

        "SetFloat": {
            "variableName": "string",
            "value": "float"
        },

        "AddFloat": {
            "variableName": "string",
            "amount": "float"
        },

        "SubtractFloat": {
            "variableName": "string",
            "amount": "float"
        },

        "SetString": {
            "variableName": "string",
            "value": "string"
        },

        "ClearVariable": {
            "variableName": "string"
        }
    },

    # ─────────────────────────────────────
    # GAMEOBJECT / COMPONENT
    # ─────────────────────────────────────

    "GameObject": {

        "SetActive": {
            "value": "bool"
        },

        "DestroyObject": {
            "delay": "float"
        },

        "InstantiatePrefab": {
            "prefabName": "string"
        },

        "EnableComponent": {
            "componentName": "string"
        },

        "DisableComponent": {
            "componentName": "string"
        },

        "SetTag": {
            "tag": "string"
        },

        "SetLayer": {
            "layer": "int"
        }
    },

    # ─────────────────────────────────────
    # UI
    # ─────────────────────────────────────

    "UI": {

        "ShowUI": {
            "uiName": "string"
        },

        "HideUI": {
            "uiName": "string"
        },

        "SetUIText": {
            "uiElement": "string",
            "text": "string"
        },

        "SetUIProgress": {
            "uiElement": "string",
            "value": "float"
        }
    },

    # ─────────────────────────────────────
    # EVENTS
    # ─────────────────────────────────────

    "Events": {

        "SendEvent": {
            "eventName": "string"
        },

        "BroadcastEvent": {
            "eventName": "string"
        },

        "InvokeMethod": {
            "methodName": "string"
        }
    }
}

# ─────────────────────────────────────
# LISTA PLANA PARA AUTOCOMPLETADO
# ─────────────────────────────────────

ALL_ACTIONS = [
    action
    for category in ACTION_REGISTRY.values()
    for action in category.keys()
]