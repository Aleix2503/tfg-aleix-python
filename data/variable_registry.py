# ═══════════════════════════════════════════════════════════════
# VARIABLE REGISTRY
# ═══════════════════════════════════════════════════════════════
# Variables predefinidas que pueden usarse en condiciones
# Esto permite autocompletado en el editor cuando el usuario
# selecciona variables en VariableCompare, BoolIsTrue, etc.
# ═══════════════════════════════════════════════════════════════

VARIABLE_REGISTRY = {
    # ─────────────────────────────────────
    # MOVEMENT & PHYSICS
    # ─────────────────────────────────────
    "isGrounded": {
        "type": "bool",
        "description": "Si el personaje está en el suelo"
    },
    "isJumping": {
        "type": "bool",
        "description": "Si el personaje está saltando"
    },
    "isFalling": {
        "type": "bool",
        "description": "Si el personaje está cayendo"
    },
    "isRunning": {
        "type": "bool",
        "description": "Si el personaje está corriendo"
    },
    "velocity": {
        "type": "float",
        "description": "Velocidad actual del personaje"
    },

    # ─────────────────────────────────────
    # TARGET & COMBAT
    # ─────────────────────────────────────
    "distanceToPlayer": {
        "type": "float",
        "description": "Distancia al jugador"
    },
    "distanceToTarget": {
        "type": "float",
        "description": "Distancia al objetivo actual"
    },
    "hasTarget": {
        "type": "bool",
        "description": "Si tiene un objetivo asignado"
    },
    "canSeeTarget": {
        "type": "bool",
        "description": "Si puede ver al objetivo (line of sight)"
    },
    "health": {
        "type": "float",
        "description": "Salud actual"
    },
    "maxHealth": {
        "type": "float",
        "description": "Salud máxima"
    },
    "isAlive": {
        "type": "bool",
        "description": "Si el personaje está vivo"
    },

    # ─────────────────────────────────────
    # COOLDOWNS & STATE
    # ─────────────────────────────────────
    "canAttack": {
        "type": "bool",
        "description": "Si el ataque está disponible (cooldown listo)"
    },
    "attackCooldown": {
        "type": "float",
        "description": "Tiempo restante del cooldown de ataque"
    },
    "stateTime": {
        "type": "float",
        "description": "Tiempo que lleva en el estado actual"
    },
    "lastSeenTime": {
        "type": "float",
        "description": "Hace cuánto tiempo vio al objetivo por última vez"
    },

    # ─────────────────────────────────────
    # STATUS & EFFECTS
    # ─────────────────────────────────────
    "isStunned": {
        "type": "bool",
        "description": "Si el personaje está aturdido"
    },
    "isAttacking": {
        "type": "bool",
        "description": "Si está ejecutando un ataque"
    },
    "ammo": {
        "type": "int",
        "description": "Munición disponible"
    },
    "mana": {
        "type": "float",
        "description": "Maná o energía disponible"
    }
}

# ─────────────────────────────────────
# LISTA PLANA PARA AUTOCOMPLETADO
# ─────────────────────────────────────

ALL_VARIABLES = list(VARIABLE_REGISTRY.keys())

# ─────────────────────────────────────
# GRUPOS DE VARIABLES (opcional)
# ─────────────────────────────────────

VARIABLE_GROUPS = {
    "Movement": ["isGrounded", "isJumping", "isFalling", "isRunning", "velocity"],
    "Combat": ["distanceToPlayer", "distanceToTarget", "hasTarget", "canSeeTarget", "health", "maxHealth", "isAlive"],
    "State": ["canAttack", "attackCooldown", "stateTime", "lastSeenTime"],
    "Status": ["isStunned", "isAttacking", "ammo", "mana"]
}


def get_variable_type(variable_name: str) -> str:
    """
    Obtiene el tipo de una variable
    Returns: "bool", "float", "int" o None si no existe
    """
    if variable_name in VARIABLE_REGISTRY:
        return VARIABLE_REGISTRY[variable_name]["type"]
    return None


def get_variable_description(variable_name: str) -> str:
    """
    Obtiene la descripción de una variable
    """
    if variable_name in VARIABLE_REGISTRY:
        return VARIABLE_REGISTRY[variable_name]["description"]
    return ""


def validate_variable_and_operator(variable_name: str, operator: str) -> tuple[bool, str]:
    """
    Valida que una variable y operador sean compatibles

    Returns: (is_valid, error_message)
    """
    if variable_name not in VARIABLE_REGISTRY:
        return False, f"Variable '{variable_name}' no existe"

    var_type = VARIABLE_REGISTRY[variable_name]["type"]

    # Operadores para bool
    if var_type == "bool":
        if operator not in ["==", "!="]:
            return False, f"Variable bool solo soporta ==, != (recibido: {operator})"

    # Operadores para float/int
    if var_type in ["float", "int"]:
        valid_ops = ["==", "!=", ">", ">=", "<", "<="]
        if operator not in valid_ops:
            return False, f"Variable numérica solo soporta {valid_ops} (recibido: {operator})"

    return True, ""
