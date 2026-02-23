ACTION_CATEGORIES = {
    "Animation": [
        "PlayAnimation",
        "CrossFadeAnimation",
        "StopAnimation",
        "SetAnimatorBool",
        "SetAnimatorTrigger",
        "SetAnimatorFloat",
        "SetAnimatorInt",
        "ResetAnimatorTrigger",
    ],
    "Movement": [
        "MoveToPosition",
        "MoveForward",
        "MoveBackward",
        "RotateToTarget",
        "Jump",
        "Dash",
        "StopMovement",
    ],
    "Combat": [
        "Attack",
        "EnableHitbox",
        "DisableHitbox",
        "TakeDamage",
        "Heal",
        "SpawnProjectile",
    ],
    "Audio": [
        "PlaySound",
        "StopSound",
        "PlayOneShot",
        "SetVolume",
    ],
    "Variables": [
        "SetBool",
        "SetInt",
        "SetFloat",
        "IncrementInt",
        "ToggleBool",
    ],
    "VFX": [
        "SpawnVFX",
        "DestroyVFX",
        "ChangeColor",
        "ShakeCamera",
    ],
}


ALL_ACTIONS = [
    action
    for category in ACTION_CATEGORIES.values()
    for action in category
]