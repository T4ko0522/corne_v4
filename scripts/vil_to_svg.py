#!/usr/bin/env python3
"""Render a Vial .vil file as an SVG keymap diagram.

Reads the physical key layout from keymap/vial.json and renders every layer
of corne.vil into one SVG file. No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path

KEY_SIZE = 54
KEY_GAP = 4
PAD = 24
LAYER_GAP = 40
TITLE_HEIGHT = 26


KEY_LABELS: dict[str, str] = {
    "KC_TRNS": "▽",
    "_______": "▽",
    "KC_NO": "",
    "XXXXXXX": "",
    "KC_LSHIFT": "Sft",
    "KC_RSHIFT": "Sft",
    "KC_LCTRL": "Ctrl",
    "KC_RCTRL": "Ctrl",
    "KC_LALT": "Alt",
    "KC_RALT": "Alt",
    "KC_LGUI": "GUI",
    "KC_RGUI": "GUI",
    "KC_TAB": "Tab",
    "KC_ENTER": "Ent",
    "KC_BSPACE": "BSpc",
    "KC_SPACE": "Spc",
    "KC_ESCAPE": "Esc",
    "KC_DELETE": "Del",
    "KC_KANA": "かな",
    "KC_EISU": "英数",
    "KC_CAPSLOCK": "Caps",
    "KC_INSERT": "Ins",
    "KC_LEFT": "←",
    "KC_RIGHT": "→",
    "KC_UP": "↑",
    "KC_DOWN": "↓",
    "KC_MINUS": "-",
    "KC_QUOTE": "'",
    "KC_LBRACKET": "[",
    "KC_RBRACKET": "]",
    "KC_EQUAL": "=",
    "KC_SCOLON": ";",
    "KC_COMMA": ",",
    "KC_DOT": ".",
    "KC_SLASH": "/",
    "KC_GRAVE": "`",
    "KC_BSLASH": "\\",
    "KC_JYEN": "¥",
    "KC_NONUS_HASH": "#",
    "KC_RO": "\\_",
    "KC_BTN1": "Click",
    "KC_BTN2": "RClk",
    "KC_BTN3": "MClk",
    "KC_WH_U": "Wh↑",
    "KC_WH_D": "Wh↓",
    "KC_WH_L": "Wh←",
    "KC_WH_R": "Wh→",
    "KC_MS_U": "Ms↑",
    "KC_MS_D": "Ms↓",
    "KC_MS_L": "Ms←",
    "KC_MS_R": "Ms→",
    "QK_BOOT": "BOOT",
    "RGB_TOG": "RGB",
    "RGB_MOD": "Mode+",
    "RGB_RMOD": "Mode-",
    "RGB_HUI": "Hue+",
    "RGB_HUD": "Hue-",
    "RGB_SAI": "Sat+",
    "RGB_SAD": "Sat-",
    "RGB_VAI": "Brt+",
    "RGB_VAD": "Brt-",
    "KC_MUTE": "Mute",
    "KC_VOLU": "Vol↑",
    "KC_VOLD": "Vol↓",
    "KC_MPLY": "▶/⏸",
    "KC_MNXT": "Next",
    "KC_MPRV": "Prev",
}


def label_for(keycode) -> str:
    """Map a Vial keycode string to a short human-readable label."""
    if keycode == -1 or keycode is None:
        return ""
    keycode = str(keycode)
    if keycode in KEY_LABELS:
        return KEY_LABELS[keycode]

    m = re.match(r"^KC_([A-Z0-9])$", keycode)
    if m:
        return m.group(1)

    m = re.match(r"^KC_F(\d+)$", keycode)
    if m:
        return f"F{m.group(1)}"

    m = re.match(r"^KC_(\d+)$", keycode)
    if m:
        return m.group(1)

    m = re.match(r"^LT(\d+)\((.+)\)$", keycode)
    if m:
        return f"L{m.group(1)}/{label_for(m.group(2)) or '?'}"
    m = re.match(r"^LT\((\d+)\s*,\s*(.+)\)$", keycode)
    if m:
        return f"L{m.group(1)}/{label_for(m.group(2)) or '?'}"

    m = re.match(r"^MO\((\d+)\)$", keycode)
    if m:
        return f"MO{m.group(1)}"
    m = re.match(r"^TO\((\d+)\)$", keycode)
    if m:
        return f"TO{m.group(1)}"
    m = re.match(r"^TG\((\d+)\)$", keycode)
    if m:
        return f"TG{m.group(1)}"
    m = re.match(r"^OSL\((\d+)\)$", keycode)
    if m:
        return f"OSL{m.group(1)}"

    m = re.match(r"^LSFT\((.+)\)$", keycode)
    if m:
        return f"⇧{label_for(m.group(1)) or '?'}"
    m = re.match(r"^LCTL\((.+)\)$", keycode)
    if m:
        return f"⌃{label_for(m.group(1)) or '?'}"
    m = re.match(r"^LALT\((.+)\)$", keycode)
    if m:
        return f"⌥{label_for(m.group(1)) or '?'}"
    m = re.match(r"^LGUI\((.+)\)$", keycode)
    if m:
        return f"◆{label_for(m.group(1)) or '?'}"

    m = re.match(r"^LSFT_T\((.+)\)$", keycode)
    if m:
        return f"Sft/{label_for(m.group(1)) or '?'}"
    m = re.match(r"^LCTL_T\((.+)\)$", keycode)
    if m:
        return f"Ctl/{label_for(m.group(1)) or '?'}"
    m = re.match(r"^LALT_T\((.+)\)$", keycode)
    if m:
        return f"Alt/{label_for(m.group(1)) or '?'}"
    m = re.match(r"^LGUI_T\((.+)\)$", keycode)
    if m:
        return f"GUI/{label_for(m.group(1)) or '?'}"

    if keycode.startswith("KC_"):
        return keycode[3:]
    return keycode


def parse_vial_layout(
    vial_json: dict,
) -> tuple[
    dict[tuple[int, int], tuple[float, float, float, float]],
    list[tuple[int, int, float, float, float, float]],
]:
    """Return (matrix_positions, encoder_positions) from vial.json layouts.keymap.

    Encoder positions use Vial's special label format
    ``"<idx>,<direction>\\n\\n\\n\\n\\n\\n\\n\\n\\ne"`` where direction is 0=CCW, 1=CW.
    """
    keymap_layout = vial_json["layouts"]["keymap"]
    positions: dict[tuple[int, int], tuple[float, float, float, float]] = {}
    encoder_positions: list[tuple[int, int, float, float, float, float]] = []

    y = 0.0
    for row_def in keymap_layout:
        x = 0.0
        h = 1.0
        w = 1.0
        for item in row_def:
            if isinstance(item, dict):
                if "x" in item:
                    x += item["x"]
                if "y" in item:
                    y += item["y"]
                if "h" in item:
                    h = item["h"]
                if "w" in item:
                    w = item["w"]
            elif isinstance(item, str):
                if "\n" in item:
                    head = item.split("\n", 1)[0]
                    try:
                        enc_idx, direction = (int(p) for p in head.split(","))
                        encoder_positions.append((enc_idx, direction, x, y, w, h))
                    except ValueError:
                        pass
                else:
                    try:
                        row_idx, col_idx = (int(p) for p in item.split(","))
                        positions[(row_idx, col_idx)] = (x, y, w, h)
                    except ValueError:
                        pass
                x += w
                w = 1.0
                h = 1.0
        y += 1.0
    return positions, encoder_positions


def render_key(x_units: float, y_units: float, w: float, h: float,
               label: str, ox: float, oy: float) -> str:
    x = ox + x_units * (KEY_SIZE + KEY_GAP)
    y = oy + y_units * (KEY_SIZE + KEY_GAP)
    kw = w * KEY_SIZE + (w - 1) * KEY_GAP
    kh = h * KEY_SIZE + (h - 1) * KEY_GAP

    fill = "#f5f5f7"
    stroke = "#777"
    text_color = "#222"

    if label in ("▽", ""):
        fill = "#fafafa"
        text_color = "#bbb"
    elif label.startswith("L") and "/" in label:
        fill = "#e8f0fe"
        stroke = "#4a78c0"
    elif label.startswith("MO") or label.startswith("TO") or label.startswith("TG"):
        fill = "#e8f0fe"
        stroke = "#4a78c0"
    elif label in ("BOOT",) or label.startswith("RGB") or label.startswith("Mode") or label.startswith("Hue") or label.startswith("Sat") or label.startswith("Brt"):
        fill = "#fef0e8"
        stroke = "#c07a4a"

    out = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{kw:.1f}" height="{kh:.1f}" '
        f'rx="6" ry="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
    ]

    if label:
        font_size = 11 if len(label) <= 5 else 9
        out.append(
            f'<text x="{x + kw/2:.1f}" y="{y + kh/2 + 4:.1f}" '
            f'font-size="{font_size}" font-family="ui-sans-serif, system-ui, sans-serif" '
            f'fill="{text_color}" text-anchor="middle">{escape(label)}</text>'
        )
    return "".join(out)


def render_encoder_key(x_units: float, y_units: float, w: float, h: float,
                       label: str, direction: int, ox: float, oy: float) -> str:
    x = ox + x_units * (KEY_SIZE + KEY_GAP)
    y = oy + y_units * (KEY_SIZE + KEY_GAP)
    cx = x + (w * KEY_SIZE + (w - 1) * KEY_GAP) / 2
    cy = y + (h * KEY_SIZE + (h - 1) * KEY_GAP) / 2
    r = KEY_SIZE / 2 - 2
    arrow = "↺" if direction == 0 else "↻"
    return (
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" '
        f'fill="#eef5ff" stroke="#4a78c0" stroke-width="1.2"/>'
        f'<text x="{cx:.1f}" y="{cy - 6:.1f}" font-size="14" '
        f'font-family="ui-sans-serif, system-ui, sans-serif" '
        f'fill="#4a78c0" text-anchor="middle">{arrow}</text>'
        f'<text x="{cx:.1f}" y="{cy + 12:.1f}" font-size="10" '
        f'font-family="ui-sans-serif, system-ui, sans-serif" '
        f'fill="#222" text-anchor="middle">{escape(label)}</text>'
    )


def render_layer(positions: dict[tuple[int, int], tuple[float, float, float, float]],
                 encoder_positions: list[tuple[int, int, float, float, float, float]],
                 layer: list[list], encoder_pairs: list[list[str]] | None,
                 layer_num: int, ox: float, oy: float) -> tuple[str, float, float]:
    """Render one layer block. Returns (svg, width, height) in pixels."""
    parts = [
        f'<text x="{ox:.1f}" y="{oy + 16:.1f}" font-size="15" font-weight="600" '
        f'font-family="ui-sans-serif, system-ui, sans-serif" fill="#111">Layer {layer_num}</text>'
    ]

    inner_ox = ox
    inner_oy = oy + TITLE_HEIGHT

    max_x_units = 0.0
    max_y_units = 0.0

    for (row, col), (xu, yu, w, h) in positions.items():
        if row >= len(layer) or col >= len(layer[row]):
            continue
        kc = layer[row][col]
        if kc == -1:
            continue
        label = label_for(kc)
        parts.append(render_key(xu, yu, w, h, label, inner_ox, inner_oy))
        max_x_units = max(max_x_units, xu + w)
        max_y_units = max(max_y_units, yu + h)

    for (enc_idx, direction, xu, yu, w, h) in encoder_positions:
        kc = None
        if encoder_pairs and enc_idx < len(encoder_pairs):
            pair = encoder_pairs[enc_idx]
            if pair and direction < len(pair):
                kc = pair[direction]
        label = label_for(kc) if kc is not None else ""
        parts.append(render_encoder_key(xu, yu, w, h, label, direction, inner_ox, inner_oy))
        max_x_units = max(max_x_units, xu + w)
        max_y_units = max(max_y_units, yu + h)

    width = max_x_units * (KEY_SIZE + KEY_GAP)
    height = max_y_units * (KEY_SIZE + KEY_GAP) + TITLE_HEIGHT

    return "".join(parts), width, height


def build_svg(vial_path: Path, vial_json_path: Path) -> str:
    vil = json.loads(vial_path.read_text(encoding="utf-8"))
    vial_json = json.loads(vial_json_path.read_text(encoding="utf-8"))
    positions, encoder_positions = parse_vial_layout(vial_json)

    layers = vil["layout"]
    encoder_layout = vil.get("encoder_layout", [])
    name = vial_json.get("name", "Keymap")

    body_parts: list[str] = []
    current_y = PAD

    layer_widths: list[float] = []

    for i, layer in enumerate(layers):
        enc = encoder_layout[i] if i < len(encoder_layout) else None
        svg, w, h = render_layer(positions, encoder_positions, layer, enc, i, PAD, current_y)
        body_parts.append(svg)
        layer_widths.append(w)
        current_y += h + LAYER_GAP

    width = max(layer_widths) + PAD * 2 if layer_widths else 600
    height = current_y + PAD

    header = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}">'
        f'<rect width="100%" height="100%" fill="#ffffff"/>'
        f'<text x="{PAD}" y="{PAD + 4}" font-size="18" font-weight="700" '
        f'font-family="ui-sans-serif, system-ui, sans-serif" fill="#111">{escape(name)} keymap</text>'
    )

    body = "".join(body_parts)
    return header + body + "</svg>"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("vil", type=Path, help="Path to .vil file")
    parser.add_argument(
        "--vial-json",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "keymap" / "vial.json",
        help="Path to vial.json (default: ../keymap/vial.json relative to this script)",
    )
    parser.add_argument("-o", "--out", type=Path, help="Output SVG path (default: stdout)")
    args = parser.parse_args()

    svg = build_svg(args.vil, args.vial_json)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(svg, encoding="utf-8")
    else:
        sys.stdout.write(svg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
