# ═══════════════════════════════════════════════════════════════
# VARIABLE REGISTRY
# ═══════════════════════════════════════════════════════════════
# Predefined variables that can be used in conditions
# This allows autocomplete in the editor when the user
# selects variables in VariableCompare, BoolIsTrue, etc.
# ═══════════════════════════════════════════════════════════════

VARIABLE_REGISTRY = {
    # ─────────────────────────────────────
    # MOVEMENT & PHYSICS
    # ─────────────────────────────────────
    "isGrounded": {
        "type": "bool",
        "description": "Whether the character is on the ground"
    },
    "isJumping": {
        "type": "bool",
        "description": "Whether the character is jumping"
    },
    "isFalling": {
        "type": "bool",
        "description": "Whether the character is falling"
    },
    "isRunning": {
        "type": "bool",
        "description": "Whether the character is running"
    },
    "velocity": {
        "type": "float",
        "description": "Current character velocity"
    },

    # ─────────────────────────────────────
    # TARGET & COMBAT
    # ─────────────────────────────────────
    "distanceToPlayer": {
        "type": "float",
        "description": "Distance to the player"
    },
    "distanceToTarget": {
        "type": "float",
        "description": "Distance to the current target"
    },
    "hasTarget": {
        "type": "bool",
        "description": "Whether a target is assigned"
    },
    "canSeeTarget": {
        "type": "bool",
        "description": "Whether the target is visible (line of sight)"
    },
    "health": {
        "type": "float",
        "description": "Current health"
    },
    "maxHealth": {
        "type": "float",
        "description": "Maximum health"
    },
    "isAlive": {
        "type": "bool",
        "description": "Whether the character is alive"
    },

    # ─────────────────────────────────────
    # COOLDOWNS & STATE
    # ─────────────────────────────────────
    "canAttack": {
        "type": "bool",
        "description": "Whether attack is available (cooldown ready)"
    },
    "attackCooldown": {
        "type": "float",
        "description": "Remaining time on attack cooldown"
    },
    "stateTime": {
        "type": "float",
        "description": "Time spent in the current state"
    },
    "lastSeenTime": {
        "type": "float",
        "description": "Time since the target was last seen"
    },

    # ─────────────────────────────────────
    # STATUS & EFFECTS
    # ─────────────────────────────────────
    "isStunned": {
        "type": "bool",
        "description": "Whether the character is stunned"
    },
    "isAttacking": {
        "type": "bool",
        "description": "Whether an attack is being executed"
    },
    "ammo": {
        "type": "int",
        "description": "Available ammunition"
    },
    "mana": {
        "type": "float",
        "description": "Available mana or energy"
    }
}

# ─────────────────────────────────────
# FLAT LIST FOR AUTOCOMPLETE
# ─────────────────────────────────────

ALL_VARIABLES = list(VARIABLE_REGISTRY.keys())

# ─────────────────────────────────────
# VARIABLE GROUPS (optional)
# ─────────────────────────────────────

VARIABLE_GROUPS = {
    "Movement": ["isGrounded", "isJumping", "isFalling", "isRunning", "velocity"],
    "Combat": ["distanceToPlayer", "distanceToTarget", "hasTarget", "canSeeTarget", "health", "maxHealth", "isAlive"],
    "State": ["canAttack", "attackCooldown", "stateTime", "lastSeenTime"],
    "Status": ["isStunned", "isAttacking", "ammo", "mana"]
}


def get_variable_type(variable_name: str) -> str:
    """
    Gets the type of a variable
    Returns: "bool", "float", "int" or None if it does not exist
    """
    if variable_name in VARIABLE_REGISTRY:
        return VARIABLE_REGISTRY[variable_name]["type"]
    return None


def get_variable_description(variable_name: str) -> str:
    """
    Gets the description of a variable
    """
    if variable_name in VARIABLE_REGISTRY:
        return VARIABLE_REGISTRY[variable_name]["description"]
    return ""


def validate_variable_and_operator(variable_name: str, operator: str) -> tuple[bool, str]:
    """
    Validates that a variable and operator are compatible

    Returns: (is_valid, error_message)
    """
    if variable_name not in VARIABLE_REGISTRY:
        return False, f"Variable '{variable_name}' does not exist"

    var_type = VARIABLE_REGISTRY[variable_name]["type"]

    # Operators for bool
    if var_type == "bool":
        if operator not in ["==", "!="]:
            return False, f"Bool variable only supports ==, != (received: {operator})"

    # Operators for float/int
    if var_type in ["float", "int"]:
        valid_ops = ["==", "!=", ">", ">=", "<", "<="]
        if operator not in valid_ops:
            return False, f"Numeric variable only supports {valid_ops} (received: {operator})"

    return True, ""
