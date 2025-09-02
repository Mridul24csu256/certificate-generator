import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io
import zipfile

st.set_page_config(page_title="Certificate Generator", layout="wide")

st.title("🎓 Certificate Generator")

# Upload files
template_file = st.file_uploader("📌 Upload Certificate Template (PNG/JPG)", type=["png", "jpg", "jpeg"])
excel_file = st.file_uploader("📌 Upload Excel File (with columns: Name, RollNo, Dept)", type=["xlsx"])
font_file = st.file_uploader("📌 Upload Font File (TTF)", type=["ttf"])

# Input positions for text
name_coords = st.text_input("Enter Name Position (x,y)", "600,450")
roll_coords = st.text_input("Enter Roll No Position (x,y)", "600,520")
dept_coords = st.text_input("Enter Dept Position (x,y)", "600,590")

# Font settings
font_size = st.slider("Font Size", 20, 100, 40)
font_color = st.color_picker("Font Color", "#000000")

if template_file and excel_file:
    # Load template
    template = Image.open(template_file).convert("RGB")

    # Load Excel
    df = pd.read_excel(excel_file)

    # Load font
    if font_file:
        font = ImageFont.truetype(font_file, font_size)
    else:
        font = ImageFont.load_default()

    # Preview first certificate
    if st.button("👀 Preview First Certificate"):
        img = template.copy()
        draw = ImageDraw.Draw(img)

        x, y = map(int, name_coords.split(","))
        draw.text((x, y), df.iloc[0]["Name"], fill=font_color, font=font)

        x, y = map(int, roll_coords.split(","))
        draw.text((x, y), str(df.iloc[0]["RollNo"]), fill=font_color, font=font)

        x, y = map(int, dept_coords.split(","))
        draw.text((x, y), df.iloc[0]["Dept"], fill=font_color, font=font)

        st.image(img, caption="Preview")

    # Generate all certificates
    if st.button("🚀 Generate All Certificates"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for idx, row in df.iterrows():
                img = template.copy()
                draw = ImageDraw.Draw(img)

                # Draw name
                x, y = map(int, name_coords.split(","))
                draw.text((x, y), row["Name"], fill=font_color, font=font)

                # Draw roll no
                x, y = map(int, roll_coords.split(","))
                draw.text((x, y), str(row["RollNo"]), fill=font_color, font=font)

                # Draw department
                x, y = map(int, dept_coords.split(","))
                draw.text((x, y), row["Dept"], fill=font_color, font=font)

                # Save as JPG inside ZIP
                file_name = f"{row['Name']}.jpg"
                img_bytes = io.BytesIO()
                img.save(img_bytes, format="JPEG")
                zipf.writestr(file_name, img_bytes.getvalue())

        zip_buffer.seek(0)
        st.download_button(
            label="⬇️ Download All Certificates (ZIP)",
            data=zip_buffer,
            file_name="certificates.zip",
            mime="application/zip"
        )
