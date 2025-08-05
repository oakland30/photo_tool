from PIL import Image, ImageDraw, ImageFont, ExifTags
import os
import piexif

#读取照片信息
def extract_exif(photo_path):
    image = Image.open(photo_path)
    exif_data_raw = image._getexif()
    exif_data = {}
    if exif_data_raw:
        for tag_id, value in exif_data_raw.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            exif_data[tag] = value

    model = exif_data.get('Model', 'Unknown Camera')
    brand = exif_data.get('Make', 'Unknown Brand')
    datetime = exif_data.get('DateTime', 'Unknown Time')
    exposure = exif_data.get('ExposureTime', '?')
    fnumber = exif_data.get('FNumber', '?')
    iso = exif_data.get('ISOSpeedRatings', '?')
    focal = exif_data.get('FocalLength', '?')

    if isinstance(fnumber, tuple):
        fnumber_val = round(fnumber[0] / fnumber[1], 1)
    else:
        fnumber_val = fnumber

    if isinstance(focal, tuple):
        focal_val = round(focal[0] / focal[1], 1)
    else:
        focal_val = focal

    if isinstance(exposure, tuple):
        exposure = f"{exposure[0]}/{exposure[1]}"

    if focal_val == 0 and fnumber_val == 0:
        focal_str = "50mm  f/1.2"            #如果读取到的焦距和光圈值都为0，取这里的默认值50mm f/1.2，如果你想使用其他值，就把这里的50mm f/1.2替换为你想使用的值，如果想不显示将引号中设置空格即可
        fnumber_str = ""
    else:
        focal_str = f"{focal_val}mm"
        fnumber_str = f"f/{fnumber_val}"

    return {
        'model': model,
        'brand': brand,
        'datetime': datetime,
        'exposure': exposure,
        'fnumber': fnumber_str,
        'iso': f"ISO{iso}",
        'focal': focal_str
    }

#获取照片方向
def get_orientation(photo_path):
    try:
        image = Image.open(photo_path)
        exif_dict = piexif.load(image.info['exif'])
        orientation = exif_dict['0th'].get(piexif.ImageIFD.Orientation, 1)
        return orientation
    except Exception:
        return 1

#垂直照片水印
def add_vertical_watermark(image, info, logo_path, output_path):
    width, height = image.size
    footer_width = int(min(width, height) * 0.15 * 0.75)
    result = Image.new("RGB", (width + footer_width, height), "white")
    result.paste(image, (0, 0))

    en_font_path = "C:/Windows/Fonts/arial.ttf"
    font_size = int(footer_width * 0.28)
    line_spacing = int(font_size * 0.5)
    font = ImageFont.truetype(en_font_path, font_size)
    small_font = ImageFont.truetype(en_font_path, int(font_size * 0.9))

    draw = ImageDraw.Draw(result)

    logo_target_h = int(footer_width * 0.3)
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        ratio = logo_target_h / logo.height
        logo = logo.resize((int(logo.width * ratio), logo_target_h))
        logo = logo.rotate(-90, expand=True)
        logo_x = width + (footer_width - logo.width) // 2
        logo_y = 50
        result.paste(logo, (logo_x, logo_y), logo)

        line_length = int(footer_width * 0.6)
        line_img = Image.new("RGBA", (2, line_length), (0, 0, 0, 255))
        line_img = line_img.rotate(90, expand=True)
        result.paste(line_img, (logo_x - line_length // 4, logo_y + logo.height + int(font_size * 0.5)), line_img)

        model_img = Image.new("RGBA", (font_size * 10, font_size * 2), (255, 255, 255, 0))
        model_draw = ImageDraw.Draw(model_img)
        model_draw.text((0, 0), info['model'], font=font, fill="black")
        model_img = model_img.rotate(-90, expand=True)
        model_y = logo_y + logo.height + int(font_size * 0.5) + int(font_size)
        result.paste(model_img, (logo_x - footer_width//4 , model_y), model_img)

    left_text = info['datetime']
    right_text = f"{info['focal']}  {info['fnumber']}  {info['exposure']}  {info['iso']}"

    left_img = Image.new("RGBA", (font_size * 12, font_size * 2), (255, 255, 255, 0))
    left_draw = ImageDraw.Draw(left_img)
    left_draw.text((0, 0), left_text, font=small_font, fill="gray")
    left_img = left_img.rotate(-90, expand=True)

    right_img = Image.new("RGBA", (font_size * 16, font_size * 2), (255, 255, 255, 0))
    right_draw = ImageDraw.Draw(right_img)
    right_draw.text((0, 0), right_text, font=font, fill="black")
    right_img = right_img.rotate(-90, expand=True)

    margin_bottom = int(height * 0.02)
    result.paste(left_img, (width - int(footer_width * 0.1), height - int(left_img.height * 0.8)), left_img)
    result.paste(right_img, (width + int(footer_width * 0.25), height - int(right_img.height * 0.92)), right_img)

    result.save(output_path)
    print(f"Saved vertical watermarked image to {output_path}")

#水平照片水印
def add_horizontal_watermark(image, info, logo_path, output_path):
    width, height = image.size
    footer_height = int(min(width, height) * 0.15 * 0.75)
    result = Image.new("RGB", (width, height + footer_height), "white")
    result.paste(image, (0, 0))

    en_font_path = "C:/Windows/Fonts/arial.ttf"
    font_size = int(footer_height * 0.28)
    line_spacing = int(font_size * 0.5)
    font = ImageFont.truetype(en_font_path, font_size)
    small_font = ImageFont.truetype(en_font_path, int(font_size * 0.9))

    draw = ImageDraw.Draw(result)
    margin = int(width * 0.02)
    center_y = height + footer_height // 2

    logo_target_h = int(footer_height * 0.4)
    logo_spacing = int(logo_target_h * 0.4)
    text_spacing = int(logo_target_h * 0.6)

    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        ratio = logo_target_h / logo.height
        logo = logo.resize((int(logo.width * ratio), logo_target_h))
        logo_pos = (margin, center_y - logo.height // 2)
        result.paste(logo, logo_pos, logo)

        line_x = logo_pos[0] + logo.width + logo_spacing
        line_y0 = height + int(footer_height * 0.15)
        line_y1 = height + footer_height - int(footer_height * 0.15)
        draw.line([(line_x, line_y0), (line_x, line_y1)], fill="black", width=2)

        model_text = info['model']
        text_pos = (line_x + text_spacing, center_y - font_size // 2)
        draw.text(text_pos, model_text, font=font, fill="black")

    right_text_1 = f"{info['focal']}  {info['fnumber']}  {info['exposure']}  {info['iso']}",
    right_text_2 = info['datetime']

    bbox1 = draw.textbbox((0, 0), right_text_1[0], font=font)
    bbox2 = draw.textbbox((0, 0), right_text_2, font=small_font)
    total_text_height = bbox1[3] - bbox1[1] + bbox2[3] - bbox2[1] + int(line_spacing)
    start_y = height + (footer_height - total_text_height) // 2

    x1 = width - margin - (bbox1[2] - bbox1[0])
    x2 = width - margin - (bbox2[2] - bbox2[0])
    y1 = start_y
    y2 = start_y + (bbox1[3] - bbox1[1]) + int(line_spacing)

    draw.text((x1, y1), right_text_1[0], font=font, fill="black")
    draw.text((x2, y2), right_text_2, font=small_font, fill="gray")

    result.save(output_path)
    print(f"Saved watermarked image to {output_path}")

#单张图片处理主程序函数
def add_watermark(photo_path, logo_path, output_path):
    info = extract_exif(photo_path)
    image = Image.open(photo_path)
    orientation = get_orientation(photo_path)
    #print(f"Orientation: {orientation}")

    is_vertical = orientation in [6, 8] or image.height > image.width
    if is_vertical:
        add_vertical_watermark(image, info, logo_path, output_path)
    else:
        add_horizontal_watermark(image, info, logo_path, output_path)

#批量处理主程序函数
def batch_add_watermark(photo_folder, logo_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(photo_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(photo_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                add_watermark(input_path, logo_path, output_path)
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# 单张图片处理
# photo_path = "E:/DCIM/100MSDCF/DSC00704.JPG"
# logo_path = "D:/Desktop/常用脚本/sony.png"
# output_path = "D:/Desktop/output_with_watermark2.jpg"
# add_watermark(photo_path, logo_path, output_path)

# 批量图片处理
photo_folder = "./example_input"                      # 输入待处理照片文件夹路径
logo_path = "./logo/sony.png"              # 相机logo路径，文件夹中为大家准备了sony/nikon/富士，其他品牌请自行添加logo图片
output_folder = "./example_output"                    # 输出带水印照片文件夹路径
batch_add_watermark(photo_folder, logo_path, output_folder)
