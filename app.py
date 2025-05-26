# app.py
import streamlit as st
import cv2
import tempfile
import time
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("3D Pile Modeling Demo")

col1, col2 = st.columns([1, 1])

with col1:
    st.header("Senser Capture")

    video_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov", "mkv"])
    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        cap = cv2.VideoCapture(tfile.name)

        if not cap.isOpened():
            st.error("Cannot open file")
        else:
            fps = cap.get(cv2.CAP_PROP_FPS) or 25
            delay = 1.0 / fps

            frame_slot = st.empty()
            info_slot = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    st.warning("Done")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_slot.image(frame_rgb, channels="RGB", use_column_width=True)

                frame_no = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                h, w = frame.shape[:2]
                info_slot.markdown(f"""
                **FrameNo**: {frame_no}  
                **Resolution**: {w}×{h}  
                **FPS**: {fps:.2f}
                """)
                time.sleep(delay)

            cap.release()

with col2:
    st.header("Pile Modeling")

    verts = {
        "x": [1, -1, -1,  1],
        "y": [1, -1,  1, -1],
        "z": [1,  1, -1, -1],
    }
    faces = {
        "i": [0, 0, 0, 1],
        "j": [1, 2, 3, 2],
        "k": [2, 3, 1, 3],
    }

    mesh = go.Mesh3d(
        x=verts["x"], y=verts["y"], z=verts["z"],
        i=faces["i"], j=faces["j"], k=faces["k"],
        opacity=0.5,
        flatshading=True,
        lighting=dict(ambient=0.5, diffuse=0.8, roughness=0.5, fresnel=0.2),
        lightposition=dict(x=100, y=200, z=0)
    )

    fig = go.Figure(data=[mesh])
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data"
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)
