# -*- coding: utf-8 -*-

def obtener_narrativa(id_escenario):
    """Librería Maestra de Fontanería Sentinel Alpha - v3.4 (PRO)"""
    
    narrativas = {
        # --- ESCENARIOS DE CONVEXIDAD NEGATIVA (MAGENTA / SHORT GAMMA) ---
        "M_REV_A4": {
            "r": "A++++", "t": "REVERSIÓN SHORT CONVEXITY (SUELO)", "col": "#ff00ff", "i": "💎",
            "f": "Mecánica de Fredy: Put Wall tocado + Skew Empinado.",
            "c": "Vanna Rally inminente: El Dealer está corto de gamma y la caída de volatilidad le obliga a COMPRAR SPX agresivamente.",
            "p": "90%", "tr": "Largo Contratendencia"
        },
        "M_AIR_A3": {
            "r": "A+++", "t": "CASCADA SHORT CONVEXITY", "col": "#ff00ff", "i": "🌪️",
            "f": "Air Pocket bajo Zero Gamma sin muros de soporte.",
            "c": "Aceleración por pánico: El Dealer vende para cubrir delta en un vacío de liquidez. Peligro de caída libre.",
            "p": "75%", "tr": "Corto en Momentum"
        },
        "M_MAGNET_P": {
            "r": "A++", "t": "PINNING: IMÁN DE FREDY", "col": "#ff00ff", "i": "🧲",
            "f": "Vértice de IV Mínima (Classic). Zona de succión operativa.",
            "c": "El precio queda pegado por el equilibrio de costes de cobertura. El Dealer no necesita moverse. Rango estrecho.",
            "p": "N/A", "tr": "Neutral / Recogida beneficios"
        },
        "M_FRIC_B": {
            "r": "B", "t": "FRICCIÓN EN EL SUELO", "col": "#ff00ff", "i": "🧱",
            "f": "Cyan Spike detectado en Short Convexity.",
            "c": "Absorción: Hay ventas masivas pero el Dealer las está comprando todas. El precio no bajará de aquí por ahora.",
            "p": "60%", "tr": "Preparar Reversión"
        },

        # --- ESCENARIOS DE CONVEXIDAD POSITIVA (CIAN / LONG GAMMA) ---
        "C_FOMO_S": {
            "r": "A+++", "t": "LONG CONVEXITY RALLY (TECHO)", "col": "#00f2ff", "i": "🚀",
            "f": "Skew Plano/Invertido sobre Zero Gamma.",
            "c": "FOMO Squeeze: No hay coberturas que frenen el precio. El Dealer acompaña el movimiento sin fricción.",
            "p": "85%", "tr": "Largo en Ruptura"
        },
        "C_AIR_A2": {
            "r": "A+", "t": "MOMENTUM CIAN (AIR POCKET)", "col": "#00f2ff", "i": "📈",
            "f": "Sobre Zero Gamma con vacío hasta la siguiente Call Wall.",
            "c": "Entorno de calma institucional. El Charm (paso del tiempo) ayuda a que el precio suba solo.",
            "p": "70%", "tr": "Scalping Alcista"
        },
        "C_WALL_B": {
            "r": "B", "t": "ABSORCIÓN LONG CONVEXITY", "col": "#00f2ff", "i": "🧱",
            "f": "Toque de Call Wall con Skew Normal.",
            "c": "El Dealer vende calls para cubrirse, frenando el avance. Muro de cemento técnico.",
            "p": "N/A", "tr": "Toma de beneficios"
        },

        # --- ESCENARIOS DE TRANSICIÓN Y CAOS ---
        "Z_FLIP_C": {
            "r": "C", "t": "GAMMA FLIP (ZONA DE CAOS)", "col": "#ffffff", "i": "⚠️",
            "f": "Cruzando el Zero Gamma de Classic.",
            "c": "Punto de inflexión: La volatilidad cambia de bando. El mercado no sabe si comprar o vender. No operar.",
            "p": "0%", "tr": "FUERA DEL MERCADO"
        },
        "Z_DIV_H": {
            "r": "C", "t": "DIVERGENCIA TRIPLE CORONA", "col": "#ffffff", "i": "📵",
            "f": "Imanes de SPX y NDX desalineados.",
            "c": "El mercado tecnológico y el general van por caminos distintos. Riesgo alto de trampa institucional.",
            "p": "0%", "tr": "FUERA DEL MERCADO"
        }
    }
    return narrativas.get(id_escenario, narrativas["Z_FLIP_C"])
