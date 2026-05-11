#include QMK_KEYBOARD_H
#include "keymap_japanese.h"

// Mod-tap: tap = Esc, hold = LCtrl
#define MT_ESC_CTL LCTL_T(KC_ESC)

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

  // ===== Layer 0: Base (QWERTY / JIS) =====
  [0] = LAYOUT_split_3x6_3_ex2(
    KC_TAB,   KC_Q,    KC_W,    KC_E,    KC_R,    KC_T,    MT_ESC_CTL,                  KC_LCTL, KC_Y,    KC_U,    KC_I,    KC_O,    KC_P,     JP_MINS,
    KC_LALT,  KC_A,    KC_S,    KC_D,    KC_F,    KC_G,    JP_KANA,                     JP_EISU, KC_H,    KC_J,    KC_K,    KC_L,    JP_SCLN,  JP_COLN,
    KC_LSFT,  KC_Z,    KC_X,    KC_C,    KC_V,    KC_B,                                          KC_N,    KC_M,    KC_COMM, KC_DOT,  JP_SLSH,  KC_LGUI,
                                         KC_LCTL, MO(1),   KC_BSPC,                     KC_ENT,  MO(2),   KC_SPC
  ),

  // ===== Layer 1: Function / Numbers / Mouse =====
  [1] = LAYOUT_split_3x6_3_ex2(
    KC_TAB,   KC_F1,   KC_F2,   KC_F3,   KC_F4,   KC_F5,   _______,                     _______, JP_SLSH, JP_MINS, JP_COLN, JP_SCLN, JP_YEN,   JP_CIRC,
    KC_LALT,  JP_EXLM, JP_DQUO, JP_HASH, JP_DLR,  JP_PERC, _______,                     KC_INS,  JP_AMPR, JP_QUOT, JP_LPRN, JP_RPRN, KC_0,     JP_CIRC,
    KC_LSFT,  KC_F6,   KC_F7,   KC_F8,   KC_F9,   KC_F10,                                        KC_F11,  KC_F12,  _______, _______, _______,  KC_LGUI,
                                         KC_LCTL, _______, KC_MS_U,                     KC_MS_D, _______, KC_SPC
  ),

  // ===== Layer 2: Symbols / Arrows / IME =====
  [2] = LAYOUT_split_3x6_3_ex2(
    KC_TAB,   JP_EXLM, JP_DQUO, JP_HASH, JP_DLR,  JP_PERC, KC_LCTL,                     KC_LCTL, JP_AMPR, JP_QUOT, JP_LPRN, JP_RPRN, S(KC_0),  KC_BSPC,
    KC_LALT,  _______, _______, _______, _______, _______, KC_LALT,                     KC_LALT, KC_LEFT, KC_UP,   KC_DOWN, KC_RGHT, JP_RBRC,  JP_ZKHK,
    KC_LSFT,  JP_AT,   JP_CIRC,  JP_LBRC, JP_MINS, JP_RBRC,                                       JP_UNDS, JP_EQL,  JP_LCBR, JP_RCBR, KC_LSFT,  JP_ZKHK,
                                         KC_LGUI, _______, KC_SPC,                      KC_ENT,  _______, KC_LGUI
  ),

  // ===== Layer 3: Adjust (Bootloader / Underglow) =====
  [3] = LAYOUT_split_3x6_3_ex2(
    QK_BOOT,  _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______,  _______,
    RGB_TOG,  RGB_HUI, RGB_SAI, RGB_VAI, _______, _______, _______,                     _______, _______, _______, _______, _______, _______,  _______,
    RGB_MOD,  RGB_HUD, RGB_SAD, RGB_VAD, _______, _______,                                       _______, _______, _______, _______, _______,  _______,
                                         KC_LGUI, _______, KC_SPC,                      KC_ENT,  _______, KC_LGUI
  ),

  // ===== Layer 4: (reserved / transparent) =====
  [4] = LAYOUT_split_3x6_3_ex2(
    _______, _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,                                       _______, _______, _______, _______, _______, _______,
                                         _______, _______, _______,                     _______, _______, _______
  ),

  // ===== Layer 5: (reserved / transparent) =====
  [5] = LAYOUT_split_3x6_3_ex2(
    _______, _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______, _______,                     _______, _______, _______, _______, _______, _______, _______,
    _______, _______, _______, _______, _______, _______,                                       _______, _______, _______, _______, _______, _______,
                                         _______, _______, _______,                     _______, _______, _______
  ),
};
