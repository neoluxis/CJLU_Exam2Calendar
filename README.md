# CJLU 考试安排转日历

## 安装

### Arch Linux

对于 Arch Linux 直接安装 AUR 包即可

```bash
paru -S cjlu-exams2calendar
```

### 非 Arch Linux

1. 创建 Python 环境  
    可以使用 Anaconda 或 venv 或者直接使用系统 Python
2. 安装 Python 依赖  
    ```bash
    pip install -r requirements.txt
    ```
3. 安装 Tesseract OCR 软件
    - Arch Linux：
        ```bash 
        paru -S extra/tesseract-data-chi_sim
        ```
    - Windows:  
        1. 从[Tesseract Release](https://github.com/tesseract-ocr/tesseract/releases) 下载安装包并安装，安装时 <font color='red'>要勾选简体中文语言包</font>
        2. ~~下载[简体中文语言包](https://github.com/tesseract-ocr/tessdata/raw/refs/heads/main/chi_sim.traineddata)~~, 
        


## 使用说明

1. 在CJLU 教务处公众号，截图校内考试（可以长截图），保存到电脑本地。
2. 运行 `main.py`  
 使用方法：
 ```bash
 python main.py -i 图片路径 -o 输出路径 -t Tesseract可执行文件路径
 ```
 输出路径如果是 `*.ics` 就表示输出到文件，否则会新建文件夹。
 - 可以添加 `-v` 参数来查看运行情况
3. 使用日历程序打开输出的 `.ics` 文件
