import streamlit as st

def load_particles():
    st.markdown("""
    <style>
    #particles-js {position: fixed; width: 100%; height: 100%; z-index:-1; top:0; left:0;}
    body {background:#121212; color:#e3f2fd; font-family:'Segoe UI', sans-serif;}
    .result-box {background: rgba(255,255,255,0.08);backdrop-filter:blur(6px);border-radius:12px;padding:15px;margin-top:10px;}
    .abusive:hover {background-color: rgba(255,82,82,0.2); cursor:pointer;}
    </style>
    <div id="particles-js"></div>
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script>
    particlesJS("particles-js", {
      "particles": {"number":{"value":70},"color":{"value":"#00e5ff"},"shape":{"type":"circle"},
      "opacity":{"value":0.5},"size":{"value":3},"line_linked":{"enable":true,"distance":150,"color":"#00e5ff","opacity":0.4,"width":1},
      "move":{"enable":true,"speed":2}}});
    </script>
    """, unsafe_allow_html=True)
