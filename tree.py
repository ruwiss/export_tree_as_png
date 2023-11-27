from PIL import Image, ImageDraw, ImageFont
import sys
import os


class TreeToPng:
    def __init__(self, root_dir, image_file):
        self.root_dir = root_dir
        self.image_file = image_file
        self.x = 20
        self.y = 20
        self.indent = 18
        self.draw = None
        self.font = ImageFont.load_default()
        self.files_count = 0
        self.max_indent = 0

    def draw_text(self, text, x=None, is_file=False):
        x_value = x if x else self.x
        white_color = (255, 255, 255)
        orange_color = (255, 204, 153)
        self.draw.text((x_value, self.y), text, font=self.font, fill=white_color if is_file else orange_color)
        self.y += self.indent

    def export_tree_recursive(self):
        # Şu anki dizini çiz
        self.draw_text(os.path.basename(self.root_dir))

        # Dosyaları ve alt dizinleri çiz
        # for f in os.walk(self.root_dir):

        for f in os.listdir(self.root_dir):
            self.check_dir_and_files(f)

    def check_dir_and_files(self, f, sub_path=''):
        path = os.path.join(self.root_dir, f)
        if sub_path:
            path = sub_path

        path_indent = len(path.replace(self.root_dir, '').split('\\'))
        indent_x = path_indent * self.indent

        if os.path.isdir(path):
            self.draw_text(f, x=indent_x)
            for fsub in os.listdir(path):
                fpath = os.path.join(path, fsub)
                self.check_dir_and_files(fsub, sub_path=fpath)
        elif os.path.isfile(path):
            self.draw_text(f, x=indent_x, is_file=True)

    def export_tree(self):
        # dosyaların sayısını hesapla (resim boyutlandırma için)
        self.get_files_length()

        image_height = self.files_count * self.indent + 50
        image_width = self.max_indent + 50

        # Yeni bir görüntü ve çizim nesnesi oluştur
        img = Image.new('RGB', (image_width, image_height), color=(25, 25, 25))
        self.draw = ImageDraw.Draw(img)

        # Dizin ağacını tarama ve ağacı görüntü üzerine çizme
        self.export_tree_recursive()

        # Görüntüyü kaydet
        img.save(self.image_file, "PNG")

    def get_files_length(self):
        for root, dirs, files in os.walk(self.root_dir):
            # yüksekliği hesaplamak için dosya ve klasör sayısını al
            self.files_count += len(files) + len(dirs)
            
            # girintiyi hesapla
            path_indent = len(root.replace(self.root_dir, '').split('\\'))

            # Dosya ve klasörlerden en uzun isimli olanı bul
            file_lengths = [len(f) for f in files]
            dir_lengths = [len(d) for d in dirs]
            length = max(max(file_lengths, default=0), max(dir_lengths, default=0))
            
            # Maksimum genişliği elde et
            indent_x = path_indent * self.indent + length * 6
            if self.max_indent < indent_x:
                self.max_indent = indent_x


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Kullanım: python test.py <dosya_yolu>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"{file_path} adlı dosya bulunamadı.")
        sys.exit(1)

    tree_to_png = TreeToPng(file_path, "tree.png")
    tree_to_png.export_tree()
