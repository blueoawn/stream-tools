import obspython as obs
import time
import random

# main.py
# OBS Studio script: briefly shakes every scene item in the active scene
# Drop this file into OBS's "Scripts" (or load it via Tools → Scripts)


# user-configurable
duration = 0.5      # seconds
magnitude = 200.0    # pixels (max translation)
frequency = 30.0    # updates per second (influences visual smoothness)

# internal state
_shaking = False
_start_time = 0.0
_end_time = 0.0
_items = []  # list of dicts: { "item": sceneitem, "orig": (x,y) }
# default key: Numpad 3 (virtual-key code VK_NUMPAD3 = 0x63)

VK_NUMPAD3 = 0x63
_hotkey_id = VK_NUMPAD3

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def _get_scene_items():
    """Return a list of scene items for the current scene."""
    src = obs.obs_frontend_get_current_scene()
    if src is None:
        return []
    scene = obs.obs_scene_from_source(src)
    obs.obs_source_release(src)
    if scene is None:
        return []
    items = obs.obs_scene_enum_items(scene)
    # obs_scene_enum_items returns a list of obs_sceneitem_t*
    return items

def _vec2_from_item(item):
    v = obs.vec2()
    obs.obs_sceneitem_get_pos(item, v)
    return (v.x, v.y)

def _set_item_pos(item, x, y):
    v = obs.vec2()
    v.x = x
    v.y = y
    obs.obs_sceneitem_set_pos(item, v)

def _restore_all():
    global _items
    for entry in _items:
        try:
            item = entry["item"]
            ox, oy = entry["orig"]
            _set_item_pos(item, ox, oy)
            # release scene item reference if API supports it
            try:
                obs.obs_sceneitem_release(item)
            except Exception:
                pass
        except Exception:
            pass
    _items = []

# ---------------------------------------------------------------------
# Shake control
# ---------------------------------------------------------------------
def start_shake():
    global _shaking, _start_time, _end_time, _items
    if _shaking:
        return
    items = _get_scene_items()
    if not items:
        return
    _items = []
    for item in items:
        orig = _vec2_from_item(item)
        _items.append({"item": item, "orig": orig})
    _start_time = time.time()
    _end_time = _start_time + duration
    _shaking = True

def script_update(settings):
    global duration, magnitude, frequency
    duration = obs.obs_data_get_double(settings, "duration")
    magnitude = obs.obs_data_get_double(settings, "magnitude")
    frequency = obs.obs_data_get_double(settings, "frequency")

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_float(props, "duration", "Duration (s)", 0.05, 10.0, 0.05)
    obs.obs_properties_add_float(props, "magnitude", "Magnitude (px)", 0.0, 1000.0, 1.0)
    obs.obs_properties_add_float(props, "frequency", "Frequency (updates/sec)", 1.0, 120.0, 1.0)
    obs.obs_properties_add_button(props, "shake_button", "Shake Now", lambda props, prop: _on_shake_button())
    return props

def _on_shake_button():
    start_shake()
    return True

def script_description():
    return "Briefly shakes every item in the active scene by modifying their transform (position)."

def script_load(settings):
    """Called when the script is loaded. Register hotkey."""
    global _hotkey_id
    _hotkey_id = obs.obs_hotkey_register_frontend(
        "shake_everything.trigger",
        "Shake Everything",
        _hotkey_callback
    )
    hotkey_save_array = obs.obs_data_get_array(settings, "shake_hotkey")
    obs.obs_hotkey_load(_hotkey_id, hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

def script_save(settings):
    """Called when settings are saved. Save hotkey binding."""
    global _hotkey_id
    hotkey_save_array = obs.obs_hotkey_save(_hotkey_id)
    obs.obs_data_set_array(settings, "shake_hotkey", hotkey_save_array)
    obs.obs_data_array_release(hotkey_save_array)

def _hotkey_callback(pressed):
    """Called when the registered hotkey is pressed."""
    if pressed:
        start_shake()

def script_tick(seconds):
    global _shaking, _items
    if not _shaking:
        return
    now = time.time()
    if now >= _end_time:
        # restore originals and stop
        _restore_all()
        _shaking = False
        return
    # compute damping (optional easing out)
    t = (now - _start_time) / max(1e-6, (duration))
    damping = 1.0 - t  # linear decay
    # control update rate: we run every tick but we can scale randomness by seconds if needed
    for entry in _items:
        item = entry["item"]
        ox, oy = entry["orig"]
        # random jitter; could also use noise/sin for different feel
        dx = (random.uniform(-1.0, 1.0) * magnitude * damping)
        dy = (random.uniform(-1.0, 1.0) * magnitude * damping)
        _set_item_pos(item, ox + dx, oy + dy)

def script_unload():
    """Called when the script is unloaded. Clean up resources."""
    global _shaking, _hotkey_id
    # ensure we restore if OBS is closing while shaking
    if _shaking:
        _restore_all()
        _shaking = False
    # unregister hotkey
    if _hotkey_id is not None:
        obs.obs_hotkey_unregister(_hotkey_id)