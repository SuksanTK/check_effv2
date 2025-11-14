import streamlit as st
import pandas as pd

st.set_page_config(page_title="Line–Style–Layout Generator", page_icon="📊", layout="wide")

st.title("📊 Line × Style × Layout Generator")
st.write("อัปโหลดไฟล์ Location, Style List และ Layout เพื่อสร้างตาราง Mapping อัตโนมัติ")

# -------------------------------------------------------
# 1. Upload Files
# -------------------------------------------------------
st.header("📂 Upload Files")

loc_file = st.file_uploader("📌 Upload Location file (Lines)", type=["xlsx", "csv"])
style_file = st.file_uploader("📌 Upload style_list file (Style)", type=["xlsx", "csv"])
layout_file = st.file_uploader("📌 Upload layout file (Style, Jobtitle, Machine)", type=["xlsx", "csv"])

# -------------------------------------------------------
# 2. When All Files Are Uploaded → Start Processing
# -------------------------------------------------------
if loc_file and style_file and layout_file:

    def read_file(file):
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        return pd.read_excel(file)

    df_loc = read_file(loc_file)
    df_style = read_file(style_file)
    df_layout = read_file(layout_file)

    st.success("✔ โหลดไฟล์สำเร็จ! กำลังประมวลผล...")

    # Filter layout → เฉพาะ Style ที่อยู่ใน style_list
    df_layout_filtered = df_layout[df_layout["Style"].isin(df_style["Style"])]

    # Cartesian Product: Lines × layout_filtered
    df_loc["key"] = 1
    df_layout_filtered["key"] = 1

    df_output = df_loc.merge(df_layout_filtered, on="key").drop("key", axis=1)

    # Show Output Preview
    st.subheader("📄 ผลลัพธ์ที่สร้าง (Preview)")
    st.dataframe(df_output, use_container_width=True)

    # -------------------------------------------------------
    # 6. Download Result as CSV
    # -------------------------------------------------------
    csv_data = df_output.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 Download CSV File",
        data=csv_data,
        file_name="line_style_layout_output.csv",
        mime="text/csv"
    )

else:
    st.info("⬆ กรุณาอัปโหลดไฟล์ให้ครบทั้ง 3 ไฟล์")
