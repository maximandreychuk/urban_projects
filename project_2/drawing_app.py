import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw
import logging


logging.basicConfig(filename='drawing_app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DrawingApp:
    """
    Класс, представляющий приложение для рисования.

    Атрибуты:
        root (tk.Tk): Корневой объект приложения Tkinter.
        image (Image.Image): Объект изображения PIL, используемый для рисования.
        draw (ImageDraw.Draw): Объект для рисования на изображении.
        canvas (tk.Canvas): Полотно для отображения изображения.
        last_x (int): Координата x последней точки рисования.
        last_y (int): Координата y последней точки рисования.
        pen_color (str): Цвет пера.
        brush_size (int): Размер кисти.
        brush_size_variable (tk.StringVar): Переменная для хранения выбранного размера кисти.
        brush_size_menu (tk.OptionMenu): Выпадающее меню для выбора размера кисти.
    """
    def __init__(self, root):
        """
        Инициализирует приложение для рисования.

        Args:
            root (tk.Tk): Корневой объект приложения Tkinter.
        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 5

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        logging.info("Приложение для рисования запущено.")

    def setup_ui(self):
        """
        Создает элементы управления для приложения.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10]
        self.brush_size_variable = tk.StringVar(control_frame)
        self.brush_size_variable.set(str(sorted(sizes)[0]))
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_variable, *sizes,
                                             command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.RIGHT)

    def paint(self, event):
        """
        Рисует линию на холсте и изображении.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y
        logging.debug(f"Рисование линии: ({self.last_x}, {self.last_y}) -> ({event.x}, {event.y})")

    def reset(self, event):
        """
        Сбрасывает координаты последней точки рисования.
        """
        self.last_x, self.last_y = None, None
        logging.debug("Сброс координат рисования.")

    def clear_canvas(self):
        """
        Очищает холст и изображение.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)
        logging.info("Холст очищен.")

    def choose_color(self):
        """
        Открывает диалоговое окно выбора цвета.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        logging.info(f"Выбран цвет: {self.pen_color}.")

    def save_image(self):
        """
        Сохраняет изображение в файл PNG.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")
            logging.info(f"Изображение сохранено в {file_path}.")

    def update_brush_size(self, value):
        """
        Обновляет размер кисти.
        """
        self.brush_size = int(value)
        logging.info(f"Размер кисти обновлен: {self.brush_size}.")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()