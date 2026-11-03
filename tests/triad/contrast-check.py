#!/usr/bin/env python3
"""Recalcula la razón de contraste WCAG 2.x de los pares declarados en ALT-TRIAD-001-ui.md.
Uso: python tests/triad/contrast-check.py   (sin dependencias, solo lectura)"""
def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def ratio(a, b):
    hi, lo = sorted([lum(a), lum(b)], reverse=True); return round((hi + .05) / (lo + .05), 2)
# (primer plano, fondo, declarado ORIGINAL en ui.md @ e1d774f, mínimo AA). ui.md ya fue corregido con los valores "real";
# el revisor debe comprobar que los números vigentes de ui.md coinciden con la columna real de esta salida.
PAIRS = [("#132E1B","#F8FAF6",13.8,4.5),("#132E1B","#FFFFFF",14.7,4.5),("#2D5438","#F8FAF6",6.8,4.5),
 ("#2D5438","#FFFFFF",7.3,4.5),("#1E5E3A","#F8FAF6",4.8,3.0),("#FFFFFF","#1E5E3A",5.7,4.5),
 ("#144428","#FFFFFF",7.6,4.5),("#0E5E35","#F8FAF6",4.8,3.0),("#0E5E35","#FFFFFF",5.7,3.0),
 ("#B00020","#FFFFFF",5.9,4.5),("#132E1B","#E3EFE4",11.2,4.5)]
bad = 0
for fg, bg, dec, mn in PAIRS:
    real = ratio(fg, bg); ok = real >= mn; bad += not ok
    print(f"{fg} / {bg}  declarado={dec}  real={real}  min={mn}  {'PASS' if ok else 'FAIL'}"
          f"{'  (declarado inexacto)' if abs(real-dec) > 0.3 else ''}")
raise SystemExit(1 if bad else 0)
