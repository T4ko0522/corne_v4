#pragma once

// 8-byte unique ID for Vial. Regenerate per-keyboard if forking:
//   python3 -c "import secrets; print(','.join(f'0x{b:02X}' for b in secrets.token_bytes(8)))"
#define VIAL_KEYBOARD_UID {0x7A, 0x4E, 0xC9, 0x12, 0xB6, 0x35, 0xD0, 0x81}

// Hold matrix [0,0] + [0,1] simultaneously to unlock Vial security menu.
#define VIAL_UNLOCK_COMBO_ROWS {0, 0}
#define VIAL_UNLOCK_COMBO_COLS {0, 1}

#undef DYNAMIC_KEYMAP_LAYER_COUNT
#define DYNAMIC_KEYMAP_LAYER_COUNT 3

#define TAPPING_TERM 180

// Split master/slave detection is handled by the keyboard's info.json
// (handedness pin GP21). Do not redefine SPLIT_USB_DETECT here.
