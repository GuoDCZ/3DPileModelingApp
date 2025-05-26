import streamlit as st
import cv2
import tempfile
import time

st.title("📽️ 实时视频帧信息显示")

# 上传视频文件
video_file = st.file_uploader("上传一个视频文件", type=["mp4", "mov", "avi", "mkv"])

if video_file is not None:
    # 将上传的文件保存为临时文件
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())

    # 打开视频文件
    cap = cv2.VideoCapture(tfile.name)

    if not cap.isOpened():
        st.error("无法打开视频文件。")
    else:
        st.success("视频加载成功，开始播放并解析帧信息...")
        
        # 获取视频的 FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        delay = 1.0 / fps if fps > 0 else 0.04

        # 创建视频帧展示区域和信息展示区域
        frame_location = st.empty()
        info_location = st.empty()

        frame_num = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("视频播放完毕或读取错误。")
                break

            # 转换 BGR 为 RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 显示帧
            frame_location.image(frame_rgb, channels="RGB")

            # 显示帧信息
            info_location.markdown(f"""
            **帧号**: {int(cap.get(cv2.CAP_PROP_POS_FRAMES))}  
            **尺寸**: {frame.shape[1]}x{frame.shape[0]}  
            **FPS**: {fps:.2f}
            """)

            time.sleep(delay)

        cap.release()
        st.success("播放结束。")
