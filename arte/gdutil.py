"""Helpers to write GDevelop 5 events and objects as JSON from Python.

Used by the arte/generar_*.py scripts that edit Legado Radioactivo-Papayork.json.
"""
import uuid


def uid(): return str(uuid.uuid4())
def q(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---------- events ----------
def I(t, *p, inv=False):
    i = {"type": {"value": t}, "parameters": [str(x) for x in p]}
    if inv: i["type"]["inverted"] = True
    return i
def C(t, *p, inv=False): return I(t, *p, inv=inv)
def A(t, *p): return I(t, *p)
def EV(conds=(), acts=(), subs=(), variables=None):
    e = {"type": "BuiltinCommonInstructions::Standard", "conditions": list(conds), "actions": list(acts)}
    if subs: e["events"] = list(subs)
    if variables: e["variables"] = variables
    return e
def FOREACH(obj, conds=(), acts=(), subs=()):
    e = {"type": "BuiltinCommonInstructions::ForEach", "object": obj, "conditions": list(conds), "actions": list(acts)}
    if subs: e["events"] = list(subs)
    return e
def REPEAT(times, conds=(), acts=(), subs=()):
    e = {"type": "BuiltinCommonInstructions::Repeat", "repeatExpression": str(times), "conditions": list(conds), "actions": list(acts)}
    if subs: e["events"] = list(subs)
    return e
def COM(text):
    return {"type": "BuiltinCommonInstructions::Comment",
            "color": {"b": 109, "g": 230, "r": 255, "textB": 0, "textG": 0, "textR": 0}, "comment": text}
def LINK(name): return {"type": "BuiltinCommonInstructions::Link", "include": {"includeConfig": 0}, "target": name}
def ONCE(): return C("BuiltinCommonInstructions::Once")
def var(name, typ, value): return {"name": name, "type": typ, "value": value}
def struct(name, children): return {"name": name, "type": "structure", "children": children}

# variables
def sv(v, val, op="="): return A("SetStringVariable", v, op, val)
def nv(v, val, op="="): return A("SetNumberVariable", v, op, val)
def bv(v, val): return A("SetBooleanVariable", v, val, "")
def isv(v, val, op="="): return C("StringVariable", v, op, val)
def inv_(v, val, op="="): return C("NumberVariable", v, op, val)
def ibv(v, val): return C("BooleanVariable", v, val, "")
def objv_s(o, v, val, op="="): return C("StringObjectVariable", o, v, op, val)
def objv_n(o, v, val, op="="): return C("NumberObjectVariable", o, v, op, val)
def objv_b(o, v, val): return C("BooleanObjectVariable", o, v, val, "")
def set_objv_b(o, v, val): return A("SetBooleanObjectVariable", o, v, val, "")
def set_objv_n(o, v, val, op="="): return A("SetNumberObjectVariable", o, v, op, val)
def set_objv_s(o, v, val, op="="): return A("SetStringObjectVariable", o, v, op, val)

# objects / input / sound
def anim(o, name): return A("SetAnimationName", o, name)
def txt(o, val): return A("TextContainerCapability::TextContainerBehavior::SetValue", o, "Text", "=", val)
def color(o, rgb): return A("TextObject::ChangeColor", o, q(rgb))
def snd(f, vol=60): return A("PlaySound", "", f, "no", str(vol), "1")
def cursor(o, inv=False): return C("IsCursorOnObject", o, "", "", "", inv=inv)
def released(button="Left"): return C("MouseButtonFromTextReleased", "", q(button))
def key_released(k): return C("KeyFromTextReleased", "", q(k))
def show(o): return A("Show", o, "")
def hide(o): return A("Hide", o)
def opacity(o, v): return A("OpacityCapability::OpacityBehavior::SetValue", o, "Opacity", "=", str(v))
def tw_y(o, ident, to, ease, dur, destroy="no"): return A("Tween::TweenBehavior::AddObjectPositionYTween2", o, "Tween", q(ident), to, q(ease), str(dur), destroy)
def tw_op(o, ident, to, ease, dur, destroy="no"): return A("Tween::TweenBehavior::AddObjectOpacityTween2", o, "Tween", q(ident), str(to), q(ease), str(dur), destroy)

# ---------- objects ----------
TWEEN = {"name": "Tween", "type": "Tween::TweenBehavior"}
FONT = "Fuentes/PixelifySans.ttf"

def frame(img, origin=(0, 0), mask=None):
    return {"hasCustomCollisionMask": mask is not None, "image": img, "points": [],
            "originPoint": {"name": "origine", "x": origin[0], "y": origin[1]},
            "centerPoint": {"automatic": True, "name": "centre", "x": 0, "y": 0},
            "customCollisionMask": [mask] if mask else []}
def rect(x0, y0, x1, y1): return [{"x": x0, "y": y0}, {"x": x1, "y": y0}, {"x": x1, "y": y1}, {"x": x0, "y": y1}]
def anim_def(name, frames, loop=False, dt=0.08):
    return {"name": name, "useMultipleDirections": False,
            "directions": [{"looping": loop, "timeBetweenFrames": dt, "sprites": frames}]}
def sprite_obj(name, anims, variables=(), tween=True):
    return {"adaptCollisionMaskAutomatically": False, "assetStoreId": "", "name": name, "persistentUuid": uid(),
            "type": "Sprite", "updateIfNotVisible": False, "variables": list(variables), "effects": [],
            "behaviors": [TWEEN] if tween else [], "animations": anims}
def text_obj(name, text, size=12, rgb=(255, 255, 255), outline=(36, 21, 13), align="left", variables=(), tween=False):
    col = f"{rgb[0]};{rgb[1]};{rgb[2]}"
    return {"assetStoreId": "", "bold": False, "italic": False, "name": name, "persistentUuid": uid(), "smoothed": False,
            "type": "TextObject::Text", "underlined": False, "variables": list(variables), "effects": [],
            "behaviors": [TWEEN] if tween else [],
            "string": text, "font": FONT, "textAlignment": align, "characterSize": size,
            "color": {"r": rgb[0], "g": rgb[1], "b": rgb[2]},
            "content": {"bold": False, "isOutlineEnabled": outline is not None, "isShadowEnabled": False, "italic": False,
                        "outlineColor": f"{outline[0]};{outline[1]};{outline[2]}" if outline else "0;0;0",
                        "outlineThickness": 2, "shadowAngle": 90, "shadowBlurRadius": 2, "shadowColor": "0;0;0",
                        "shadowDistance": 4, "shadowOpacity": 127, "smoothed": False, "underlined": False,
                        "text": text, "font": FONT, "textAlignment": align, "verticalTextAlignment": "top",
                        "characterSize": size, "lineHeight": 0, "color": col}}
def inst(name, x, y, layer="", z=0, w=None, h=None, variables=()):
    return {"angle": 0, "customSize": w is not None, "height": h or 0, "keepRatio": True, "layer": layer, "name": name,
            "persistentUuid": uid(), "width": w or 0, "x": x, "y": y, "zOrder": z,
            "numberProperties": [], "stringProperties": [], "initialVariables": list(variables)}

# ---------- project ----------
def add_resource(d, kind, name, file):
    res = d["resources"]["resources"]
    if any(r["name"] == name for r in res): return
    r = {"file": file, "kind": kind, "metadata": "", "name": name, "userAdded": True}
    if kind == "image": r.update({"metadata": "{\"extension\":\".png\"}", "smoothed": False})
    if kind == "audio": r.update({"preloadAsMusic": False, "preloadAsSound": True, "preloadInCache": False})
    res.append(r)
def set_global_object(d, obj):
    d["objects"] = [o for o in d["objects"] if o["name"] != obj["name"]] + [obj]
    ch = d["objectsFolderStructure"]["children"]
    if not any(c.get("objectName") == obj["name"] for c in ch): ch.append({"objectName": obj["name"]})
def set_global_var(d, v):
    d["variables"] = [x for x in d["variables"] if x["name"] != v["name"]] + [v]
def external_events(d, name, events, layout="Nivel 01"):
    ext = next((e for e in d["externalEvents"] if e["name"] == name), None)
    if ext is None:
        ext = {"associatedLayout": layout, "name": name, "events": []}
        d["externalEvents"].append(ext)
    ext["events"] = events
    return ext
