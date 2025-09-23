from PIL import Image
img = Image.open('res/tex_tiket_star5_R.png').convert('RGBA')
# 生成多尺寸 ico（16,32,48,256）
sizes = [(16,16),(32,32),(48,48),(256,256)]
img.save('res/tex_tiket_star5_R.ico', sizes=sizes)