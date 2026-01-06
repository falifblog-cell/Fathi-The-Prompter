# Logic CSS (Tema & HILANGKAN SEMUA BRANDING)
if tema == "☀️ Mode Cerah (Light)":
    st.markdown("""
        <style>
            /* Tema Putih */
            .stApp { background-color: #ffffff; color: #000000; }
            .stNumberInput input { color: #000000 !important; background-color: #f0f2f6 !important; }
            .stMarkdown, .stText, p, label, .stMetricLabel { color: #000000 !important; }
            div[data-testid="stMetricValue"] { color: #000000 !important; }
            
            /* SOROKKAN MENU & FOOTER BIASA */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* CUBA SOROKKAN BADGE MERAH (HOSTED WITH STREAMLIT) */
            .viewerBadge_container__1QSob {display: none !important;}
            .styles_viewerBadge__1yB5_ {display: none !important;}
        </style>
    """, unsafe_allow_html=True)
else:
    # Dark Mode pun sama
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* CUBA SOROKKAN BADGE MERAH */
            .viewerBadge_container__1QSob {display: none !important;}
            .styles_viewerBadge__1yB5_ {display: none !important;}
        </style>
    """, unsafe_allow_html=True)
