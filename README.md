# photo_watermark_tool 使用说明

## 📌 功能说明

本工具可自动识别照片中的 **相机型号、焦距、光圈、快门、ISO、拍摄时间信息**，并**批量为照片添加水印**。

---

## 🛠 使用说明

1. 请各位自行配置好 Python 环境和 IDE；
2. 本程序需安装第三方库：`piexif`；
3. 在程序末尾 `# 批量图片处理` 的三个路径下，分别填入：
   - **待处理的照片文件夹路径**（如：`./example_input`）
   - **相机 LOGO 路径**（`logo` 文件夹中已准备了 sony / nikon / 富士 的 logo，其他品牌请自行下载添加）
   - **输出照片文件夹路径**（如：`./example_output`）

运行程序，即可完成照片批量处理。

---

## 💡 使用效果示例

将以下两张照片作为示例输入：

![示例输入1](./example_input/input1.jpg)
![示例输入2](./example_input/input2.jpg)

---

得到的水印效果如下图所示：

![输出示例1](./example_output/output1.jpg)
![输出示例2](./example_output/output2.jpg)

---

## 📢 后续更新说明

后续作者将更新更多有趣的相机水印，欢迎关注和下载。
