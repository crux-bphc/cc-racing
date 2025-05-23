import importlib.util


def load_ai(path):

    spec = importlib.util.spec_from_file_location("ai_module", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, "ai_step"):
        raise ValueError(f"AI module {path} does not have an 'ai_step' function.")
    if not callable(mod.ai_step):
        raise ValueError(f"AI module {path} 'ai_step' is not callable.")

    if not hasattr(mod, "TOP_SPEED"):
        raise ValueError(f"AI module {path} does not define 'TOP_SPEED'.")
    if not hasattr(mod, "ACCELARATION"):
        raise ValueError(f"AI module {path} does not define 'ACCELARATION'.")
    if not hasattr(mod, "TURN_SPEED"):
        raise ValueError(f"AI module {path} does not define 'TURN_SPEED'.")
    if not hasattr(mod, "SENSOR_RANGE"):
        raise ValueError(f"AI module {path} does not define 'SENSOR_RANGE'.")

    params = {
        "top_speed": mod.TOP_SPEED,
        "accel": mod.ACCELARATION,
        "turn": mod.TURN_SPEED,
        "sensor_dist": mod.SENSOR_RANGE,
    }
    return params, mod.ai_step
