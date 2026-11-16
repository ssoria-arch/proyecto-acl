import io
import os
import json
import base64
import html
from datetime import datetime, date
from pathlib import Path
import streamlit as st
from PIL import Image

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    import qrcode
except ImportError:
    qrcode = None

try:
    from conexion import conectar as conectar_local
except ImportError:
    conectar_local = None

# =====================================================
# 1. CONFIGURACIÓN GENERAL Y CARGA DE LOGOTIPO NATIVO
# =====================================================

st.set_page_config(
    page_title="ACL | Sistema de Gestión y Trazabilidad",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent

def cargar_logo():
    for nombre in ["logo_acl.png", "a_logo_acl.png", "logo_acl.jpg"]:
        ruta = BASE_DIR / nombre
        if ruta.exists():
            try:
                with Image.open(ruta) as img:
                    img.load()
                    return img.convert("RGBA")
            except Exception:
                continue
    return None

logo_img = cargar_logo()

if logo_img is not None and hasattr(st, "logo"):
    try:
        st.logo(logo_img, icon_image=logo_img)
    except Exception:
        pass

# =====================================================
# 2. ESTILOS CSS CON LEGIBILIDAD Y ALTO CONTRASTE REFORZADOS
# =====================================================

st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&display=swap');

/* Fondo general de la aplicación */
html, body, .stApp {
    background-color: #F2F3F5 !important;
    color: #1F2328 !important;
    font-family: 'Public Sans', 'Segoe UI', Arial, sans-serif !important;
}

/* Texto base para párrafos y etiquetas generales */
.stApp p, .stApp label, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
[data-testid="stMarkdownContainer"] p,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: #1F2328 !important;
}

/* ----------------------------------------------------- */
/* 1. CORRECCIÓN PARA BOTONES (TEXTO BLANCO BRILLANTE)   */
/* ----------------------------------------------------- */
button,
.stButton > button,
[data-testid="stForm"] .stButton > button,
button[kind="primary"],
button[kind="secondary"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background-color: #963A27 !important;
    border: 1px solid #7A2E1F !important;
    border-radius: 8px !important;
    padding: 10px 18px !important;
}

button *,
.stButton > button *,
[data-testid="stForm"] .stButton > button *,
button[kind="primary"] *,
button[kind="secondary"] *,
[data-testid="stBaseButton-secondary"] *,
[data-testid="stBaseButton-primary"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

button:hover, .stButton > button:hover {
    background-color: #7A2E1F !important;
}

/* ----------------------------------------------------- */
/* 2. CORRECCIÓN PARA TODAS LAS ALERTAS (SUCCESS/WARN/ERR)*/
/* ----------------------------------------------------- */
[data-testid="stAlert"],
[data-testid="stAlertContainer"],
div[role="alert"],
[data-baseweb="notification"] {
    background-color: #FFFFFF !important;
    border: 1px solid #B0B5BD !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06) !important;
}

[data-testid="stAlert"] > div,
[data-testid="stAlertContainer"] > div,
div[role="alert"] > div,
[data-baseweb="notification"] > div {
    background-color: transparent !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]),
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) {
    background-color: #E6F4EA !important;
    border: 1px solid #1A5C3C !important;
    border-left: 6px solid #1A5C3C !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]),
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) {
    background-color: #FEF7E0 !important;
    border: 1px solid #C69000 !important;
    border-left: 6px solid #D99B00 !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentError"]),
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) {
    background-color: #FCE8E6 !important;
    border: 1px solid #963A27 !important;
    border-left: 6px solid #963A27 !important;
}

[data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]),
[data-testid="stAlertContainer"]:has([data-testid="stAlertContentInfo"]) {
    background-color: #E8F0FE !important;
    border: 1px solid #1D4ED8 !important;
    border-left: 6px solid #1D4ED8 !important;
}

[data-testid="stAlert"] *,
[data-testid="stAlertContainer"] *,
div[role="alert"] *,
[data-baseweb="notification"] * {
    color: #1F2328 !important;
    -webkit-text-fill-color: #1F2328 !important;
    font-weight: 600 !important;
}

/* ----------------------------------------------------- */
/* 3. CAJAS DE ENTRADA DE TEXTO, SELECTS Y EXPANDERS     */
/* ----------------------------------------------------- */
input[type="text"], textarea, .stTextInput input, .stTextArea textarea,
div[data-baseweb="input"] input, div[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    color: #1F2328 !important;
    border: 1px solid #B0B5BD !important;
    border-radius: 6px !important;
}

input::placeholder, textarea::placeholder, .stTextInput input::placeholder {
    color: #565C66 !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #565C66 !important;
}

div[data-baseweb="select"] *, div[data-baseweb="popover"] *, div[data-baseweb="menu"] *, ul[role="listbox"] * {
    background-color: #FFFFFF !important;
    color: #1F2328 !important;
}

[data-testid="stExpander"],
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary {
    background-color: #FFFFFF !important;
    color: #1F2328 !important;
    border-radius: 8px !important;
}

/* ----------------------------------------------------- */
/* 4. BARRA LATERAL (SIDEBAR)                            */
/* ----------------------------------------------------- */
[data-testid="stSidebar"] {
    background-color: #2B2D31 !important;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stButton > button {
    background-color: rgba(255, 255, 255, 0.12) !important;
    border: none !important;
    border-left: 4px solid #E8702F !important;
    border-radius: 6px !important;
    padding: 10px 14px !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 600 !important;
}

.user-badge {
    background: rgba(255,255,255,0.1); border-radius: 10px;
    padding: 12px 16px; margin-bottom: 15px; border-left: 4px solid #E8702F;
}
.user-badge span { display: block; color: #DDE0E5 !important; font-size: 0.8rem; }
.user-badge b { color: #FFFFFF !important; font-size: 1.05rem; }

.side-etq { color: #B4B2AD !important; font-size: 0.82rem; font-weight: 600; margin: 18px 0 6px 4px; text-transform: uppercase; }

.tarjeta { background: #FFFFFF; border: 1px solid #DDE0E5; border-radius: 12px; padding: 20px; margin-bottom: 20px; color: #1F2328; }
.kpi-card { background: #FFFFFF; border-radius: 10px; border: 1px solid #DDE0E5; border-left: 5px solid #963A27; padding: 14px 18px; }
.kpi-title { color: #565C66 !important; font-size: 0.85rem; font-weight: 600; }
.kpi-val { color: #1F2328 !important; font-size: 1.8rem; font-weight: 800; margin-top: 4px; }

.badge-sem { display: inline-block; padding: 4px 12px; border-radius: 999px; font-size: 0.85rem; font-weight: 700; text-align: center; }
.sem-aprobado { background: #DAEEE2; color: #1A5C3C !important; }
.sem-pendiente { background: #FAEFCF; color: #6B4F08 !important; }
.sem-rechazado { background: #F6DCD8; color: #8A1D13 !important; }
.sem-revision { background: #FCE8D9; color: #93410F !important; }

.cert-box { background: #FFFFFF; border: 1px solid #C9CDD4; border-left: 5px solid #1A5C3C; border-radius: 10px; padding: 16px; margin-top: 10px; color: #1F2328; }
.esp-badge { background: #EAF2FE; color: #1D4ED8; font-weight: 700; padding: 3px 10px; border-radius: 6px; font-size: 0.82rem; display: inline-block; }
</style>
''', unsafe_allow_html=True)

# =====================================================
# 3. PERSISTENCIA EN MEMORIA Y BASE DE DATOS EN LA NUBE
# =====================================================

def init_session_state():
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None
    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "dashboard"
    if "filtro_area" not in st.session_state:
        st.session_state["filtro_area"] = "Todas"

    if "db_mock" not in st.session_state:
        st.session_state["db_mock"] = {
            "usuarios": [
                {"id_usuario": 1, "rut": "11.111.111-1", "email": "at@acl.cl", "nombre": "Carlos Asistente", "rol": "AT"},
                {"id_usuario": 2, "rut": "22.222.222-2", "email": "finanzas@acl.cl", "nombre": "María Finanzas", "rol": "Finanzas"},
                {"id_usuario": 3, "rut": "33.333.333-3", "email": "prevencion@acl.cl", "nombre": "Juan Prevención", "rol": "Prevencion"},
                {"id_usuario": 4, "rut": "44.444.444-4", "email": "calidad@acl.cl", "nombre": "Andrea Calidad", "rol": "Calidad"},
            ],
            "subcontratistas": [
                {"id_subcontratista": 1, "nombre": "Constructora Norte SpA", "rut": "76.123.456-7", "contacto": "contacto@norte.cl"},
                {"id_subcontratista": 2, "nombre": "Servicios Mineros Sur Ltda", "rut": "77.234.567-8", "contacto": "contacto@sur.cl"},
            ],
            "hojas": [
                {
                    "id_hoja_ruta": 1, "codigo": "HR-001", "fecha_recepcion": "2026-11-01",
                    "proyecto": "Proyecto Mina Norte", "especialidad": "Montaje Estructural / Altura",
                    "estado_actual": "En revisión", "id_subcontratista": 1, "subcontratista": "Constructora Norte SpA"
                },
                {
                    "id_hoja_ruta": 2, "codigo": "HR-002", "fecha_recepcion": "2026-11-03",
                    "proyecto": "Proyecto Planta Sur", "especialidad": "Obras Civiles / Hormigones",
                    "estado_actual": "Pendiente", "id_subcontratista": 2, "subcontratista": "Servicios Mineros Sur Ltda"
                },
            ],
            "validaciones": [
                {
                    "id_validacion": 1, "id_hoja_ruta": 1, "area": "Prevencion",
                    "estado_validacion": "Aprobado",
                    "tarea": "Revisión de Exámenes de Altura Física, Líneas de Vida y Cotizaciones F30-1.",
                    "comentario": "Documentación laboral y exámenes de altura al 100%.",
                    "id_usuario_validador": 3, "validador_nombre": "Juan Prevención", "fecha_actualizacion": "2026-11-02 10:30"
                },
                {
                    "id_validacion": 2, "id_hoja_ruta": 1, "area": "Calidad",
                    "estado_validacion": "Pendiente (Con Observaciones)",
                    "tarea": "Auditoría de Certificados de Calibración de Torquímetro y Pernos.",
                    "comentario": "Falta adjuntar el certificado de torque de pernos estructurales.",
                    "id_usuario_validador": 4, "validador_nombre": "Andrea Calidad", "fecha_actualizacion": "2026-11-02 11:15"
                },
                {
                    "id_validacion": 3, "id_hoja_ruta": 1, "area": "Finanzas",
                    "estado_validacion": "Pendiente",
                    "tarea": "Verificación de Facturas y Cuadre Presupuestario.",
                    "comentario": "En espera de la subsanación de Calidad.",
                    "id_usuario_validador": 2, "validador_nombre": "María Finanzas", "fecha_actualizacion": "2026-11-02 09:00"
                },
                {
                    "id_validacion": 4, "id_hoja_ruta": 2, "area": "Prevencion",
                    "estado_validacion": "Pendiente (Con Observaciones)",
                    "tarea": "Inspección de Matriz MIPER y EPP de Hormigonado.",
                    "comentario": "Se requiere actualizar la matriz MIPER.",
                    "id_usuario_validador": 3, "validador_nombre": "Juan Prevención", "fecha_actualizacion": "2026-11-03 14:00"
                },
                {
                    "id_validacion": 5, "id_hoja_ruta": 2, "area": "Calidad",
                    "estado_validacion": "Pendiente",
                    "tarea": "Revisión de Ensayes de Probetas de Hormigón H30.",
                    "comentario": "Carpetas técnicas recibidas en evaluación.",
                    "id_usuario_validador": 4, "validador_nombre": "Andrea Calidad", "fecha_actualizacion": "2026-11-03 14:00"
                },
                {
                    "id_validacion": 6, "id_hoja_ruta": 2, "area": "Finanzas",
                    "estado_validacion": "Pendiente",
                    "tarea": "Auditoría de Facturas y Antecedentes Comerciales.",
                    "comentario": "Pendiente respaldos de facturación.",
                    "id_usuario_validador": 2, "validador_nombre": "María Finanzas", "fecha_actualizacion": "2026-11-03 14:00"
                },
            ],
            "firmas": [
                {"id_firma": 1, "id_hoja_ruta": 1, "id_validacion": 1, "token_hash": "CERT-PREVENCION-HR-001", "fecha_firma": "2026-11-02 10:30:00"}
            ],
            "seguimientos": [],
            "pagos": []
        }

init_session_state()

def limpiar_db_url(raw_url):
    if not raw_url:
        return None
    url = str(raw_url).strip()
    if url.startswith("psql "):
        url = url[5:].strip()
    url = url.strip("'\"")
    if "&channel_binding=require" in url:
        url = url.replace("&channel_binding=require", "")
    return url

def conectar():
    db_url = None
    try:
        if "DATABASE_URL" in st.secrets:
            db_url = st.secrets["DATABASE_URL"]
    except Exception:
        pass

    if not db_url:
        db_url = os.environ.get("DATABASE_URL")

    db_url = limpiar_db_url(db_url)

    if db_url and psycopg2 is not None:
        try:
            return psycopg2.connect(db_url)
        except Exception as e:
            st.session_state["ultimo_error_bd"] = f"Error de conexión a Neon: {e}"
            return None

    if conectar_local is not None:
        return conectar_local()

    return None

def db_consultar(sql, params=None):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            cols = [desc[0] for desc in cursor.description]
            res = [dict(zip(cols, row)) for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            st.session_state["ultimo_error_bd"] = None
            return res
        except Exception as e:
            st.session_state["ultimo_error_bd"] = f"Error SQL al consultar: {e}"
            conn.close()
    return None

def db_ejecutar(sql, params=None):
    conn = conectar()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params or ())
            conn.commit()
            cursor.close()
            conn.close()
            st.session_state["ultimo_error_bd"] = None
            return True
        except Exception as e:
            st.session_state["ultimo_error_bd"] = f"Error SQL al guardar: {e}"
            conn.rollback()
            conn.close()
    return False

def generar_qr_base64(contenido):
    if qrcode is not None:
        qr = qrcode.QRCode(version=1, box_size=5, border=2)
        qr.add_data(contenido)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#963A27", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    else:
        return base64.b64encode(contenido.encode('utf-8')).decode('utf-8')

def badge_html(estado):
    estado_str = str(estado)
    if "Aprobado" in estado_str or "Aprobada" in estado_str:
        return f'<span class="badge-sem sem-aprobado">🟢 {html.escape(estado_str)}</span>'
    elif "Pendiente" in estado_str:
        return f'<span class="badge-sem sem-pendiente">🟡 {html.escape(estado_str)}</span>'
    elif "Rechazado" in estado_str or "Rechazada" in estado_str:
        return f'<span class="badge-sem sem-rechazado">🔴 {html.escape(estado_str)}</span>'
    else:
        return f'<span class="badge-sem sem-revision">🟠 {html.escape(estado_str)}</span>'

# =====================================================
# 4. PÁGINAS DE LA APLICACIÓN
# =====================================================

def login_page():
    if logo_img is not None:
        col_l1, col_l2, col_l3 = st.columns([1.5, 1, 1.5])
        with col_l2:
            st.image(logo_img, use_container_width=True)

    st.markdown('''
    <div style="text-align:center; padding: 10px 0 20px 0;">
        <h1 style="color:#963A27; font-size:2.2rem; font-weight:800;">ACL | Plataforma de Gestión y Control</h1>
        <p style="color:#565C66; font-size:1.05rem;">Autenticación por RUT y Correo Electrónico — Control de Acceso por Roles</p>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.subheader("🔑 Iniciar Sesión")
            rut_in = st.text_input("RUT del Usuario", placeholder="Ej: 11.111.111-1")
            email_in = st.text_input("Correo Electrónico", placeholder="Ej: at@acl.cl")

            if st.button("Ingresar a la Plataforma", use_container_width=True, key="login_btn"):
                sql = "SELECT * FROM usuario WHERE rut = %s AND email = %s AND activo = TRUE;"
                u_bd = db_consultar(sql, (rut_in.strip(), email_in.strip().lower()))

                if u_bd and isinstance(u_bd[0], dict):
                    st.session_state["usuario"] = u_bd[0]
                    st.session_state["pagina"] = "dashboard" if u_bd[0]["rol"] == "AT" else "mis_validaciones"
                    st.rerun()
                else:
                    mock_users = st.session_state["db_mock"]["usuarios"]
                    matched = [u for u in mock_users if u["rut"] == rut_in.strip() and u["email"] == email_in.strip().lower()]
                    if matched:
                        st.session_state["usuario"] = matched[0]
                        st.session_state["pagina"] = "dashboard" if matched[0]["rol"] == "AT" else "mis_validaciones"
                        st.rerun()
                    else:
                        st.error("Credenciales no encontradas. Puedes seleccionar un perfil rápido de prueba abajo.")

            st.divider()
            st.markdown("### 👤 Acceso Directo por Perfil (Modo Demo):")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👨‍💼 Carlos (Asistente Técnico)", use_container_width=True, key="btn_at"):
                    st.session_state["usuario"] = st.session_state["db_mock"]["usuarios"][0]
                    st.session_state["pagina"] = "dashboard"
                    st.rerun()
                if st.button("👷 Juan (Prevención de Riesgos)", use_container_width=True, key="btn_prev"):
                    st.session_state["usuario"] = st.session_state["db_mock"]["usuarios"][2]
                    st.session_state["pagina"] = "mis_validaciones"
                    st.rerun()
            with col_b:
                if st.button("💼 María (Finanzas)", use_container_width=True, key="btn_fin"):
                    st.session_state["usuario"] = st.session_state["db_mock"]["usuarios"][1]
                    st.session_state["pagina"] = "mis_validaciones"
                    st.rerun()
                if st.button("🔍 Andrea (Calidad / QA)", use_container_width=True, key="btn_cal"):
                    st.session_state["usuario"] = st.session_state["db_mock"]["usuarios"][3]
                    st.session_state["pagina"] = "mis_validaciones"
                    st.rerun()

def pagina_dashboard(user):
    c_head1, c_head2 = st.columns([4, 1])
    with c_head1:
        st.markdown('''
        <div style="margin-bottom:20px;">
            <h1 style="color:#1F2328; font-size:1.8rem; font-weight:800; margin:0;">Panel Global 360° — Asistente Técnico (AT)</h1>
            <p style="color:#565C66; font-size:1rem; margin-top:4px;">Control integral exclusivo del AT: supervisión de áreas, firmas y habilitación de pagos.</p>
        </div>
        ''', unsafe_allow_html=True)
    with c_head2:
        if st.button("🚪 Cerrar Sesión", use_container_width=True, key="btn_back_dash"):
            st.session_state["usuario"] = None
            st.session_state["pagina"] = "dashboard"
            st.rerun()

    hojas = db_consultar("SELECT h.*, s.nombre as subcontratista FROM hoja_ruta h JOIN subcontratista s ON h.id_subcontratista = s.id_subcontratista ORDER BY h.id_hoja_ruta DESC;")
    if hojas is None:
        if st.session_state.get("ultimo_error_bd"):
            st.error(st.session_state["ultimo_error_bd"])
        hojas = st.session_state["db_mock"]["hojas"]

    validaciones = db_consultar("SELECT * FROM validacion_area;")
    if validaciones is None:
        validaciones = st.session_state["db_mock"]["validaciones"]

    firmas = db_consultar("SELECT * FROM firma_qr;")
    if firmas is None:
        firmas = st.session_state["db_mock"]["firmas"]

    with st.container(border=True):
        f_col1, f_col2 = st.columns([3, 1])
        with f_col1:
            filtro_sel = st.selectbox(
                "🔍 Filtrar Matriz Global por Área:",
                ["Todas", "Prevencion", "Calidad", "Finanzas"],
                index=["Todas", "Prevencion", "Calidad", "Finanzas"].index(st.session_state["filtro_area"])
            )
            st.session_state["filtro_area"] = filtro_sel
        with f_col2:
            st.write("")
            if st.button("↩️ Resetear Filtro", use_container_width=True, key="reset_filt"):
                st.session_state["filtro_area"] = "Todas"
                st.rerun()

    tot_hojas = len(hojas)
    completas = 0
    con_obs = 0

    for h in hojas:
        val_h = [v for v in validaciones if v["id_hoja_ruta"] == h["id_hoja_ruta"]]
        aprobadas_h = sum(1 for v in val_h if v["estado_validacion"] == "Aprobado")
        if aprobadas_h == 3:
            completas += 1
        if any("Observaciones" in v["estado_validacion"] for v in val_h):
            con_obs += 1

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">TOTAL HOJAS DE RUTA</div><div class="kpi-val">{tot_hojas}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">CON 100% VALIDACIÓN</div><div class="kpi-val" style="color:#1A5C3C;">{completas}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">CON OBSERVACIONES</div><div class="kpi-val" style="color:#93410F;">{con_obs}</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="kpi-card"><div class="kpi-title">FIRMAS DIGITALES EMITIDAS</div><div class="kpi-val" style="color:#963A27;">{len(firmas)}</div></div>', unsafe_allow_html=True)

    st.markdown("<h3 style='margin-top:25px; color:#1F2328;'>Matriz Global de Seguimiento 360°</h3>", unsafe_allow_html=True)

    rows_html = []
    for h in hojas:
        val_h = {v["area"]: v for v in validaciones if v["id_hoja_ruta"] == h["id_hoja_ruta"]}
        st_prev = val_h.get("Prevencion", {}).get("estado_validacion", "Pendiente")
        st_cal = val_h.get("Calidad", {}).get("estado_validacion", "Pendiente")
        st_fin = val_h.get("Finanzas", {}).get("estado_validacion", "Pendiente")

        v_prev = badge_html(st_prev) if st.session_state["filtro_area"] in ["Todas", "Prevencion"] else "—"
        v_cal = badge_html(st_cal) if st.session_state["filtro_area"] in ["Todas", "Calidad"] else "—"
        v_fin = badge_html(st_fin) if st.session_state["filtro_area"] in ["Todas", "Finanzas"] else "—"
        esp_texto = h.get("especialidad") or "Obras Civiles / Hormigones"
        esp_tag = f'<span class="esp-badge">{html.escape(esp_texto)}</span>'

        row_str = f'<tr style="border-bottom:1px solid #DDE0E5; background:#FFFFFF;"><td style="padding:12px; font-weight:700; color:#1F2328;">{html.escape(h["codigo"])}</td><td style="padding:12px; color:#1F2328;">{html.escape(h["proyecto"])}</td><td style="padding:12px;">{esp_tag}</td><td style="padding:12px; color:#1F2328;">{html.escape(h["subcontratista"])}</td><td style="padding:12px;">{badge_html(h["estado_actual"])}</td><td style="padding:12px;">{v_prev}</td><td style="padding:12px;">{v_cal}</td><td style="padding:12px;">{v_fin}</td></tr>'
        rows_html.append(row_str)

    table_header = '<table style="width:100%; border-collapse:collapse; background:#FFFFFF; border-radius:10px; overflow:hidden; border:1px solid #DDE0E5; font-size:0.95rem; margin-top:10px;"><thead><tr style="background:#2B2D31; color:#FFFFFF; text-align:left;"><th style="padding:12px; color:#FFFFFF;">Hoja de Ruta</th><th style="padding:12px; color:#FFFFFF;">Proyecto</th><th style="padding:12px; color:#FFFFFF;">Especialidad</th><th style="padding:12px; color:#FFFFFF;">Subcontratista</th><th style="padding:12px; color:#FFFFFF;">Estado General</th><th style="padding:12px; color:#FFFFFF;">Prevención</th><th style="padding:12px; color:#FFFFFF;">Calidad</th><th style="padding:12px; color:#FFFFFF;">Finanzas</th></tr></thead><tbody>'
    table_footer = '</tbody></table>'
    st.markdown(table_header + "".join(rows_html) + table_footer, unsafe_allow_html=True)

def pagina_mis_validaciones(user):
    rol_area = user.get("rol", "General")
    
    c_head1, c_head2 = st.columns([4, 1])
    with c_head1:
        st.markdown(f'''
        <div style="margin-bottom:20px;">
            <h1 style="color:#1F2328; font-size:1.8rem; font-weight:800; margin:0;">Módulo de Trabajo Exclusivo — Área de {rol_area}</h1>
            <p style="color:#565C66; font-size:1rem; margin-top:4px;">Acceso restringido: Visualizas y gestionas únicamente los requisitos correspondientes a {rol_area}.</p>
        </div>
        ''', unsafe_allow_html=True)
    with c_head2:
        if st.button("🚪 Cerrar Sesión", use_container_width=True, key="btn_back_val"):
            st.session_state["usuario"] = None
            st.session_state["pagina"] = "dashboard"
            st.rerun()

    hojas = db_consultar("SELECT h.*, s.nombre as subcontratista FROM hoja_ruta h JOIN subcontratista s ON h.id_subcontratista = s.id_subcontratista ORDER BY h.id_hoja_ruta DESC;")
    if hojas is None:
        if st.session_state.get("ultimo_error_bd"):
            st.error(st.session_state["ultimo_error_bd"])
        hojas = st.session_state["db_mock"]["hojas"]

    validaciones_todas = db_consultar("SELECT * FROM validacion_area WHERE area = %s;", (rol_area,))
    if validaciones_todas is None:
        validaciones_todas = [v for v in st.session_state["db_mock"]["validaciones"] if v["area"] == rol_area]

    if not hojas:
        st.warning("No hay Hojas de Ruta asignadas para auditar.")
        return

    opciones = {f"{h['codigo']} — {h['proyecto']} ({h['subcontratista']})": h for h in hojas}
    
    col_sel, col_back = st.columns([3, 1])
    with col_sel:
        sel_nombre = st.selectbox("Selecciona la Hoja de Ruta a auditar:", list(opciones.keys()))
    with col_back:
        st.write("")
        if st.button("↩️ Resetear Selección", use_container_width=True, key="reset_sel"):
            st.rerun()

    hoja_sel = opciones[sel_nombre]
    esp_actual = hoja_sel.get("especialidad") or "Obras Civiles / Hormigones"

    val_actual = next((v for v in validaciones_todas if v["id_hoja_ruta"] == hoja_sel["id_hoja_ruta"]), None)
    estado_act = val_actual["estado_validacion"] if val_actual else "Pendiente"
    comentario_act = val_actual["comentario"] if val_actual else ""

    st.markdown("<div class='tarjeta'>", unsafe_allow_html=True)
    st.subheader(f"📋 Formulario de Evaluación Exclusiva — Área de {rol_area}")
    st.write(f"**Proyecto:** {hoja_sel['proyecto']} | **Subcontratista:** {hoja_sel['subcontratista']}")
    st.markdown(f"**Especialidad Asignada por AT:** <span class='esp-badge'>{html.escape(esp_actual)}</span>", unsafe_allow_html=True)
    st.write(f"**Estado actual en tu área:** {badge_html(estado_act)}", unsafe_allow_html=True)

    st.markdown(f"#### 🔍 Puntos de Control Obligatorios ({rol_area}):")
    
    if rol_area == "Prevencion":
        st.checkbox("Certificado F30-1 y cotizaciones previsionales al día.")
        if "Altura" in esp_actual:
            st.checkbox("Exámenes de altura física (psicosensométrico al día).")
            st.checkbox("Certificación de arneses y líneas de vida.")
        elif "Eléctricas" in esp_actual:
            st.checkbox("Procedimiento LOTO de bloqueo y etiquetado.")
            st.checkbox("EPP dieléctrico certificado.")
        else:
            st.checkbox("Registro de inducción de seguridad y EPP básico.")
            st.checkbox("Matriz MIPER aprobada para la faena.")

    elif rol_area == "Calidad":
        st.checkbox("Protocolos de inspección en terreno firmados.")
        if "Altura" in esp_actual or "Estructural" in esp_actual:
            st.checkbox("Certificados de torque de pernos y calibración de torquímetro.")
            st.checkbox("Informe de ensayos NDT de soldaduras.")
        elif "Eléctricas" in esp_actual:
            st.checkbox("Licencia SEC de los instaladores técnicos.")
            st.checkbox("Pruebas de puesta a tierra y aislamiento.")
        else:
            st.checkbox("Ensayes de laboratorio (resistencia probetas H30).")
            st.checkbox("Planos As-Built y carpeta técnica conforme.")

    elif rol_area == "Finanzas":
        st.checkbox("Recepción de Facturas autorizadas en SII.")
        st.checkbox("Cuadre presupuestario del avance físico de la obra.")
        st.checkbox("Cálculo y retención del fondo de garantía (5% al 10%).")

    nuevo_estado = st.selectbox("Resultado de la Evaluación:", [
        "Pendiente (Con Observaciones)",
        "Aprobado",
        "Rechazado"
    ], index=1 if "Aprobado" in estado_act else 0)

    nuevo_comentario = st.text_area(
        "Observaciones o Requisitos para Subsanar (puedes actualizar cuantas veces sea necesario):",
        value=comentario_act,
        placeholder="Escribe las observaciones o requisitos pendientes...",
        height=100
    )

    col_btn, col_blank = st.columns([1, 1])
    with col_btn:
        if st.button("💾 Guardar y Emitir / Actualizar Firma QR", use_container_width=True, key="btn_save_val"):
            if not nuevo_comentario.strip():
                st.warning("Ingresa un comentario u observación antes de guardar.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                raw_token = f"HDR:{hoja_sel['codigo']}|AREA:{rol_area}|USER:{user.get('rut')}|TS:{timestamp}"
                qr_b64 = generar_qr_base64(raw_token)
                tarea_desc = f"Auditoría exclusiva de {rol_area} completada para especialidad {esp_actual}."
                token_corto = f"CERT-{rol_area.upper()}-{hoja_sel['codigo']}"

                if val_actual:
                    db_ejecutar("UPDATE validacion_area SET estado_validacion = %s, tarea = %s, comentario = %s, fecha_actualizacion = CURRENT_TIMESTAMP, id_usuario_validador = %s WHERE id_validacion = %s;", (nuevo_estado, tarea_desc, nuevo_comentario.strip(), user.get('id_usuario'), val_actual['id_validacion']))
                    val_actual["estado_validacion"] = nuevo_estado
                    val_actual["comentario"] = nuevo_comentario.strip()
                    val_actual["tarea"] = tarea_desc
                    id_val_ref = val_actual['id_validacion']
                else:
                    db_ejecutar("INSERT INTO validacion_area (id_hoja_ruta, area, estado_validacion, tarea, comentario, id_usuario_validador) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id_hoja_ruta, area) DO UPDATE SET estado_validacion = EXCLUDED.estado_validacion, comentario = EXCLUDED.comentario, fecha_actualizacion = CURRENT_TIMESTAMP;", (hoja_sel['id_hoja_ruta'], rol_area, nuevo_estado, tarea_desc, nuevo_comentario.strip(), user.get('id_usuario')))
                    creada_v = db_consultar("SELECT id_validacion FROM validacion_area WHERE id_hoja_ruta = %s AND area = %s ORDER BY id_validacion DESC LIMIT 1;", (hoja_sel['id_hoja_ruta'], rol_area))
                    id_val_ref = creada_v[0]["id_validacion"] if creada_v else None

                if nuevo_estado == "Aprobado" and id_val_ref is not None:
                    db_ejecutar(
                        """
                        INSERT INTO firma_qr (id_hoja_ruta, id_validacion, token_hash, codigo_qr_base64)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (token_hash) DO UPDATE
                        SET codigo_qr_base64 = EXCLUDED.codigo_qr_base64,
                            fecha_firma = CURRENT_TIMESTAMP;
                        """,
                        (hoja_sel['id_hoja_ruta'], id_val_ref, token_corto, qr_b64)
                    )

                st.session_state["db_mock"]["firmas"].append({
                    "id_firma": len(st.session_state["db_mock"]["firmas"]) + 1,
                    "id_hoja_ruta": hoja_sel['id_hoja_ruta'],
                    "token_hash": token_corto,
                    "codigo_qr_base64": qr_b64,
                    "fecha_firma": timestamp
                })

                db_ejecutar("INSERT INTO seguimiento (estado_registrado, comentario, id_hoja_ruta, id_usuario) VALUES (%s, %s, %s, %s);", (f"{nuevo_estado} ({rol_area})", nuevo_comentario.strip(), hoja_sel["id_hoja_ruta"], user.get("id_usuario")))

                if st.session_state.get("ultimo_error_bd"):
                    st.error(st.session_state["ultimo_error_bd"])
                else:
                    st.success(f"¡Evaluación registrada por {rol_area}! Se generó la Firma QR de validación.")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if "Aprobado" in estado_act:
        st.markdown("<div class='cert-box'>", unsafe_allow_html=True)
        col_q1, col_q2 = st.columns([1, 3])
        with col_q1:
            raw_token = f"HDR:{hoja_sel['codigo']}|AREA:{rol_area}|USER:{user.get('rut')}"
            qr_img_b64 = generar_qr_base64(raw_token)
            st.image(f"data:image/png;base64,{qr_img_b64}", width=140)
        with col_q2:
            st.markdown(f"### 🛡️ Certificado Digital de Validación — {rol_area}")
            st.write(f"**Validador:** {user.get('nombre')} ({user.get('email')})")
            st.write(f"**Especialidad:** {esp_actual}")
            st.caption("Firma Digital QR adjunta a la Hoja de Ruta.")
        st.markdown("</div>", unsafe_allow_html=True)

def pagina_cursar_ep(user):
    st.markdown('''
    <div style="margin-bottom:20px;">
        <h1 style="color:#1F2328; font-size:1.8rem; font-weight:800; margin:0;">Aprobación Final y Cursado de Estado de Pago (EP)</h1>
        <p style="color:#565C66; font-size:1rem; margin-top:4px;">Gestión reservada al Asistente Técnico (AT) tras recopilar el 100% de las firmas.</p>
    </div>
    ''', unsafe_allow_html=True)

    hojas = db_consultar("SELECT h.*, s.nombre as subcontratista FROM hoja_ruta h JOIN subcontratista s ON h.id_subcontratista = s.id_subcontratista ORDER BY h.id_hoja_ruta DESC;")
    if hojas is None:
        hojas = st.session_state["db_mock"]["hojas"]

    validaciones = db_consultar("SELECT * FROM validacion_area;")
    if validaciones is None:
        validaciones = st.session_state["db_mock"]["validaciones"]

    for h in hojas:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            val_h = [v for v in validaciones if v["id_hoja_ruta"] == h["id_hoja_ruta"]]
            aprobadas = [v for v in val_h if v["estado_validacion"] == "Aprobado"]
            es_lista = (len(aprobadas) >= 3) or (h["estado_actual"] == "Lista para EP")
            esp_texto = h.get("especialidad") or "Obras Civiles / Hormigones"

            with col1:
                st.markdown(f"### {h['codigo']} — {h['proyecto']}")
                st.write(f"**Subcontratista:** {h['subcontratista']} | **Especialidad:** {esp_texto}")
                st.write(f"**Estado General:** {badge_html(h['estado_actual'])}", unsafe_allow_html=True)
                st.write(f"Validaciones y Firmas Recopiladas: **{len(aprobadas)} / 3 áreas**")

            with col2:
                if es_lista:
                    st.success("✅ Habilitada para EP")
                    if st.button(f"Cursar EP para {h['codigo']}", key=f"btn_ep_{h['id_hoja_ruta']}"):
                        cod_ep = f"EP-00{h['id_hoja_ruta']}"
                        db_ejecutar("INSERT INTO estado_pago (codigo, fecha_emision, estado_tramitacion, monto, id_hoja_ruta) VALUES (%s, CURRENT_DATE, %s, %s, %s) ON CONFLICT (codigo) DO UPDATE SET estado_tramitacion = EXCLUDED.estado_tramitacion, fecha_emision = CURRENT_DATE;", (cod_ep, "Aprobado", 2500000.00, h['id_hoja_ruta']))
                        db_ejecutar("UPDATE hoja_ruta SET estado_actual = 'Lista para EP' WHERE id_hoja_ruta = %s;", (h['id_hoja_ruta'],))
                        db_ejecutar("INSERT INTO seguimiento (estado_registrado, comentario, id_hoja_ruta, id_usuario) VALUES (%s, %s, %s, %s);", ("Lista para EP", f"Estado de Pago {cod_ep} cursado tras completar el 100% de las validaciones.", h["id_hoja_ruta"], user.get("id_usuario")))
                        st.session_state["db_mock"]["pagos"].append({
                            "id_estado_pago": len(st.session_state["db_mock"]["pagos"]) + 1,
                            "codigo": cod_ep,
                            "hoja_ruta": h["codigo"],
                            "fecha_emision": str(date.today()),
                            "estado_tramitacion": "Aprobado",
                            "monto": 2500000.00,
                            "id_hoja_ruta": h["id_hoja_ruta"]
                        })
                        st.balloons()
                        st.success(f"¡Estado de Pago {cod_ep} generado por $2.500.000 para el Subcontratista!")
                else:
                    st.warning("⏳ Falta Recopilar Firmas")
                    st.caption("Se requiere la validación completa de Prevención, Calidad y Finanzas.")

def pagina_hojas(user):
    st.markdown("<h1 style='color:#1F2328;'>Listado General de Hojas de Ruta</h1>", unsafe_allow_html=True)
    hojas = db_consultar("SELECT h.*, s.nombre as subcontratista FROM hoja_ruta h JOIN subcontratista s ON h.id_subcontratista = s.id_subcontratista ORDER BY h.id_hoja_ruta DESC;")
    if hojas is None:
        hojas = st.session_state["db_mock"]["hojas"]

    st.dataframe(hojas, use_container_width=True)

def pagina_nueva_hoja(user):
    st.markdown("<h1 style='color:#1F2328;'>Registrar Nueva Hoja de Ruta — Asistente Técnico (AT)</h1>", unsafe_allow_html=True)

    subcontratistas = db_consultar("SELECT * FROM subcontratista;")
    if subcontratistas is None:
        if st.session_state.get("ultimo_error_bd"):
            st.error(st.session_state["ultimo_error_bd"])
        subcontratistas = st.session_state["db_mock"]["subcontratistas"]

    hojas_actuales = db_consultar("SELECT id_hoja_ruta FROM hoja_ruta;")
    cant_hojas = len(hojas_actuales) if hojas_actuales is not None else len(st.session_state["db_mock"]["hojas"])

    with st.expander("➕ ¿Empresa no registrada? Presiona aquí para agregar un nuevo Subcontratista"):
        with st.form("form_nuevo_sub"):
            sub_nom = st.text_input("Nombre o Razón Social del Subcontratista", placeholder="Ej: Constructora El Roble SpA")
            sub_rut = st.text_input("RUT de la Empresa", placeholder="Ej: 78.901.234-5")
            sub_cnt = st.text_input("Correo Electrónico o Teléfono de Contacto", placeholder="Ej: contacto@elroble.cl")
            btn_sub = st.form_submit_button("💾 Guardar Nuevo Subcontratista")
            
            if btn_sub:
                if not sub_nom.strip() or not sub_rut.strip():
                    st.error("Ingresa al menos el Nombre y RUT del subcontratista.")
                else:
                    nuevo_id = len(subcontratistas) + 1
                    nuevo_item = {
                        "id_subcontratista": nuevo_id,
                        "nombre": sub_nom.strip(),
                        "rut": sub_rut.strip(),
                        "contacto": sub_cnt.strip()
                    }
                    ok_sub = db_ejecutar("INSERT INTO subcontratista (nombre, rut, contacto) VALUES (%s, %s, %s) ON CONFLICT (rut) DO NOTHING;", (sub_nom.strip(), sub_rut.strip(), sub_cnt.strip()))
                    st.session_state["db_mock"]["subcontratistas"].append(nuevo_item)
                    if not ok_sub and st.session_state.get("ultimo_error_bd"):
                        st.error(st.session_state["ultimo_error_bd"])
                    else:
                        st.success(f"¡Empresa '{sub_nom.strip()}' registrada! Ya puedes seleccionarla en el formulario.")
                        st.rerun()

    st.markdown("---")

    with st.form("form_nueva_hr"):
        cod = st.text_input("Código de la Hoja de Ruta", value=f"HR-00{cant_hojas + 1}")
        proy = st.text_input("Nombre del Proyecto", placeholder="Ej: Proyecto Planta Sur")
        
        especialidad_sel = st.selectbox(
            "🏗️ Especialidad / Tipo de Obra del Subcontrato:",
            [
                "Obras Civiles / Hormigones",
                "Montaje Estructural / Altura",
                "Instalaciones Eléctricas / SEC",
                "Movimiento de Tierras / Excavación",
                "Terminaciones / Servicios Generales"
            ]
        )

        sub_sel = st.selectbox("Subcontratista Encargado", subcontratistas, format_func=lambda x: f"{x['nombre']} ({x.get('rut', 'Sin RUT')})")
        submitted = st.form_submit_button("Registrar Hoja de Ruta")

        if submitted:
            if not proy.strip():
                st.error("Ingresa el nombre del proyecto.")
            elif not sub_sel:
                st.error("Selecciona un subcontratista.")
            else:
                insertado_bd = db_ejecutar(
                    "INSERT INTO hoja_ruta (codigo, proyecto, especialidad, id_subcontratista) VALUES (%s, %s, %s, %s);",
                    (cod.strip(), proy.strip(), especialidad_sel, sub_sel["id_subcontratista"])
                )

                new_id = cant_hojas + 1
                if insertado_bd:
                    creada = db_consultar("SELECT id_hoja_ruta FROM hoja_ruta WHERE codigo = %s ORDER BY id_hoja_ruta DESC LIMIT 1;", (cod.strip(),))
                    if creada:
                        new_id = creada[0]["id_hoja_ruta"]

                new_h = {
                    "id_hoja_ruta": new_id,
                    "codigo": cod.strip(),
                    "fecha_recepcion": str(date.today()),
                    "proyecto": proy.strip(),
                    "especialidad": especialidad_sel,
                    "estado_actual": "En revisión",
                    "id_subcontratista": sub_sel["id_subcontratista"],
                    "subcontratista": sub_sel["nombre"]
                }
                st.session_state["db_mock"]["hojas"].append(new_h)
                db_ejecutar("INSERT INTO seguimiento (estado_registrado, comentario, id_hoja_ruta, id_usuario) VALUES (%s, %s, %s, %s);", ("En revisión", f"Apertura de Hoja de Ruta {cod.strip()} ({especialidad_sel}).", new_id, user.get("id_usuario")))
                
                for area in ["Prevencion", "Calidad", "Finanzas"]:
                    tarea_ini = f"Auditoría técnica de {area} para la especialidad {especialidad_sel}."
                    db_ejecutar(
                        "INSERT INTO validacion_area (id_hoja_ruta, area, estado_validacion, tarea, comentario) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id_hoja_ruta, area) DO NOTHING;",
                        (new_id, area, "Pendiente", tarea_ini, "Revisión asignada automáticamente.")
                    )
                    st.session_state["db_mock"]["validaciones"].append({
                        "id_validacion": len(st.session_state["db_mock"]["validaciones"]) + 1,
                        "id_hoja_ruta": new_id,
                        "area": area,
                        "estado_validacion": "Pendiente",
                        "tarea": tarea_ini,
                        "comentario": "Revisión asignada automáticamente.",
                        "id_usuario_validador": None,
                        "fecha_actualizacion": str(datetime.now())
                    })

                if not insertado_bd and st.session_state.get("ultimo_error_bd"):
                    st.error(st.session_state["ultimo_error_bd"])
                else:
                    st.success(f"Hoja de Ruta {cod} registrada correctamente con especialidad '{especialidad_sel}' y puesta a disposición de las áreas.")

# =====================================================
# 5. CONTROL DE FLUJO Y SEGURIDAD ESTRICTA POR ROL
# =====================================================

user = st.session_state.get("usuario")

if not isinstance(user, dict):
    st.session_state["usuario"] = None
    login_page()
else:
    if user.get("rol") != "AT" and st.session_state["pagina"] != "mis_validaciones":
        st.session_state["pagina"] = "mis_validaciones"

    with st.sidebar:
        rol_act = user.get("rol", "Usuario")
        nom_act = user.get("nombre", "Usuario")
        em_act = user.get("email", "")

        st.markdown(f'''
        <div class="user-badge">
            <span>Sesión Activa ({html.escape(str(rol_act))})</span>
            <b>{html.escape(str(nom_act))}</b><br>
            <small style="color:#DDE0E5;">{html.escape(str(em_act))}</small>
        </div>
        ''', unsafe_allow_html=True)

        st.divider()

        if user.get("rol") == "AT":
            st.markdown('<div class="side-etq">Gestión Global (AT)</div>', unsafe_allow_html=True)
            if st.button("📊 Visión Global 360°", key="nav_dash"):
                st.session_state["pagina"] = "dashboard"
                st.rerun()
            if st.button("📋 Hojas de Ruta", key="nav_hojas"):
                st.session_state["pagina"] = "hojas"
                st.rerun()
            if st.button("➕ Nueva Hoja de Ruta", key="nav_new"):
                st.session_state["pagina"] = "nueva_hoja"
                st.rerun()
            if st.button("💰 Cursar a Estado de Pago", key="nav_ep"):
                st.session_state["pagina"] = "cursar_ep"
                st.rerun()
        else:
            st.markdown('<div class="side-etq">Módulo Exclusivo: ' + html.escape(str(user.get("rol"))) + '</div>', unsafe_allow_html=True)
            if st.button("✍️ Mis Validaciones y Firmas", key="nav_val"):
                st.session_state["pagina"] = "mis_validaciones"
                st.rerun()

        st.markdown('<div class="side-etq">Control de Sesión</div>', unsafe_allow_html=True)
        if st.button("🚪 Cerrar Sesión", key="btn_logout"):
            st.session_state["usuario"] = None
            st.session_state["pagina"] = "dashboard"
            st.rerun()

    paginas = {
        "dashboard": pagina_dashboard,
        "mis_validaciones": pagina_mis_validaciones,
        "cursar_ep": pagina_cursar_ep,
        "hojas": pagina_hojas,
        "nueva_hoja": pagina_nueva_hoja,
    }

    if st.session_state["pagina"] in paginas:
        paginas[st.session_state["pagina"]](user)
