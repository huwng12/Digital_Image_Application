import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class ImageProcessor:
     
    def __init__(self, window):     
        self.window = window
        self.window.title("Image Enhancement")
        self.img_path = None
        self.img = None
        self.processed_img = None
        self.previous_processed_img = None  
        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas_original = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas_processed = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas_original.pack(side=tk.LEFT)
        self.canvas_processed.pack(side=tk.RIGHT)
        self.dark_mode = False
        self.create_widgets() 

    def create_widgets(self):
        banner_frame = tk.Frame(self.window, bg="#c5cae9", bd=2, relief=tk.RAISED)
        banner_frame.pack(side=tk.TOP, fill=tk.X)
        
        title_label = tk.Label(banner_frame, text="Edit Photos", font=("Arial", 20), fg="#283593", bg="#c5cae9")
        title_label.pack(side=tk.TOP, padx=10, pady=5)
        
        banner_frame = tk.Frame(self.window, bg="#c5cae9", bd=2, relief=tk.RAISED)
        banner_frame.pack(side=tk.TOP, fill=tk.X)
        
        team_label = tk.Label(banner_frame, text="Team Members:\n20110426 - Võ Minh Hưng\n20110393 - Nguyễn Thanh Sang\n20110397 - Trần Anh Tài", font=("Arial", 14), fg="#283593", bg="#c5cae9")
        team_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        open_button = tk.Button(text="Open Image", command=self.open_image)
        open_button.pack()
        save_button = tk.Button(text="Save Image", command=self.save_image)
        save_button.pack()
        
        apply_button = tk.Button(text="Apply Filter", command=self.apply_filter)
        apply_button.pack()
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.locnhieu_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.locnhieu_tab, text="Lọc Nhiễu")
             
        median_label = tk.Label(self.locnhieu_tab,text="Meadian")
        median_label.pack()
        median_slider = tk.Scale(self.locnhieu_tab,from_=0, to=10, orient=tk.HORIZONTAL, command=self.process_image_median)
        median_slider.pack()
        median_slider.set(0)
        
        min_label = tk.Label(self.locnhieu_tab, text="Lọc Min")
        min_label.pack()
        min_slider = tk.Scale(self.locnhieu_tab, from_=0, to=10, orient=tk.HORIZONTAL, command=self.process_image_min)
        min_slider.pack()
        min_slider.set(0)
        
        max_label = tk.Label(self.locnhieu_tab, text="Lọc Max")
        max_label.pack()
        max_slider = tk.Scale(self.locnhieu_tab, from_=0, to=10, orient=tk.HORIZONTAL, command=self.process_image_max)
        max_slider.pack()
        max_slider.set(0)


        lowpass_label = tk.Label(self.locnhieu_tab, text="Low pass")
        lowpass_label.pack()
        lowpass_slider = tk.Scale(self.locnhieu_tab, from_=0, to=10, orient=tk.HORIZONTAL, command=self.process_image_lowpass)
        lowpass_slider.pack()
        lowpass_slider.set(0)
        
        gaussian_label = tk.Label(self.locnhieu_tab, text="Lọc Gaussian")
        gaussian_label.pack()
        gaussian_slider = tk.Scale(self.locnhieu_tab, from_=0, to=10, orient=tk.HORIZONTAL, command=self.process_image_gaussian)
        gaussian_slider.pack()
        gaussian_slider.set(0)
            
        self.dosang_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dosang_tab, text="Độ sáng")
        
        power_law_label = tk.Label(self.dosang_tab, text="Power Law")
        power_law_label.pack()
        power_law_slider = tk.Scale(self.dosang_tab, from_=0, to=50, orient=tk.HORIZONTAL, command=self.adjust_power_law_transform)
        power_law_slider.pack()
        power_law_slider.set(0)
        
             
        hist_eq_label = tk.Label(self.dosang_tab, text="Histogram")
        hist_eq_label.pack()
        hist_eq_slider = tk.Scale(self.dosang_tab,from_=0, to=1, orient=tk.HORIZONTAL, command=self.adjust_histogram_equalization)
        hist_eq_slider.pack()
        hist_eq_slider.set(0)
        
        log_label = tk.Label(self.dosang_tab, text="Log transform")
        log_label.pack()
        log_slider = tk.Scale(self.dosang_tab, from_=0, to=10, orient=tk.HORIZONTAL, command=self.adjust_log_transform)
        log_slider.pack()
        log_slider.set(0)
        
        brightness_label = tk.Label(self.dosang_tab, text="Điều chỉnh độ sáng (k)")
        brightness_label.pack()
        brightness_slider = tk.Scale(self.dosang_tab, from_=0, to=3, resolution=0.01, orient=tk.HORIZONTAL, command=self.process_image_brightness)
        brightness_slider.pack()
        brightness_slider.set(0)

    def apply_filter(self):
        self.previous_processed_img = np.copy(self.processed_img)

    def open_image(self):
        self.img_path = filedialog.askopenfilename()
        if self.img_path:
            self.img = cv2.imread(self.img_path)
            self.processed_img = np.copy(self.img)
            self.show_image_original()
            self.show_image_processed()
            self.reset_sliders()
    
    def reset_sliders(self):
         self.median_slider.set(0)
         self.log_slider.set(0)
         self.power_law_slider.set(0)
         self.hist_eq_slider.set(0)

    def save_image(self):
        if self.processed_img is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if save_path:
                cv2.imwrite(save_path, self.processed_img)

    def process_image_median(self, value):
        if self.img is not None:
            kernel_size = int(value) // 2 * 2 + 1
            if self.previous_processed_img is not None:  # Sử dụng ảnh đã được chỉnh sửa của filter cũ làm ảnh đầu vào
                img_median = cv2.medianBlur(self.previous_processed_img, kernel_size)
            else:
                img_median = cv2.medianBlur(self.img, kernel_size)
            self.processed_img = img_median
            self.show_image_processed()
            
    def process_image_min(self, value):
        if self.img is not None:
            kernel_size = int(value) // 2 * 2 + 1
            if self.previous_processed_img is not None:  
                img_min = cv2.erode(self.previous_processed_img, np.ones((kernel_size, kernel_size), np.uint8))
            else:
                img_min = cv2.erode(self.img, np.ones((kernel_size, kernel_size), np.uint8))
            self.processed_img = img_min
            self.show_image_processed()

    def process_image_max(self, value):
        if self.img is not None:
            kernel_size = int(value) // 2 * 2 + 1
            if self.previous_processed_img is not None:  
                img_max = cv2.dilate(self.previous_processed_img, np.ones((kernel_size, kernel_size), np.uint8))
            else:
                img_max = cv2.dilate(self.img, np.ones((kernel_size, kernel_size), np.uint8))
            self.processed_img = img_max
            self.show_image_processed()
            
    def process_image_gaussian(self, value):
        if self.img is not None:
            kernel_size = int(value) // 2 * 2 + 1
            img_gaussian = cv2.GaussianBlur(self.img, (kernel_size, kernel_size), 0)
            self.processed_img = img_gaussian
            self.show_image_processed()
        
    def adjust_log_transform(self, value):
        if self.img is not None:
            log_param = float(value) / 100.0
            if self.previous_processed_img is not None:  
                img_log = np.log1p(self.previous_processed_img * log_param)
            else:
                img_log = np.log1p(self.img * log_param)
            img_log = (img_log / np.max(img_log)) * 255
            img_log = np.array(img_log, dtype=np.uint8)
            self.processed_img = img_log
            self.show_image_processed()
            
    def adjust_power_law_transform(self, value):
        if self.img is not None:
            power_param = 1.0 + float(value) / 100.0
            if self.previous_processed_img is not None:  
                img_power_law = np.power(self.previous_processed_img, power_param)
            else:
                img_power_law = np.power(self.img, power_param)
            img_power_law = (img_power_law / np.max(img_power_law)) * 255
            img_power_law = np.array(img_power_law, dtype=np.uint8)
            self.processed_img = img_power_law
            self.show_image_processed()
            
    def adjust_histogram_equalization(self, value):
        if self.img is not None:
            hist_eq_param = int(value) * 255 // 100
            if self.previous_processed_img is not None:  
                img_gray = cv2.cvtColor(self.previous_processed_img, cv2.COLOR_BGR2GRAY)
            else:
                img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            img_hist_eq = cv2.equalizeHist(img_gray)
            img_hist_eq = cv2.cvtColor(img_hist_eq, cv2.COLOR_GRAY2RGB)
            img_hist_eq = np.array(img_hist_eq, dtype=np.uint8)
            img_hist_eq = cv2.addWeighted(self.img, 0.7, img_hist_eq, 0.3, 0)
            self.processed_img = img_hist_eq
            self.show_image_processed()          
   
    def process_image_lowpass(self, value):
        if self.img is not None:
            kernel_size = int(value) // 2 * 2 + 1
            if self.previous_processed_img is not None:  
                img_lowpass = cv2.GaussianBlur(self.previous_processed_img, (kernel_size, kernel_size), 0)
            else:
                img_lowpass = cv2.GaussianBlur(self.img, (kernel_size, kernel_size), 0)
            self.processed_img = img_lowpass
            self.show_image_processed()
            
    def process_image_brightness(self, value):
        if self.img is not None:
            img_brightness = cv2.convertScaleAbs(self.img, alpha=float(value))
            img_blend = cv2.addWeighted(self.img, 0.5, img_brightness, 0.5, 0)
            self.processed_img = img_blend
            self.show_image_processed()

    def show_image_original(self):
        if self.img is not None:
            h, w, _ = self.img.shape
            ratio = min(self.canvas_width / w, self.canvas_height / h)
            new_h, new_w = int(h * ratio), int(w * ratio)
            img_resized = cv2.resize(self.img, (new_w, new_h))
            self.canvas_original.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="white")
            x = (self.canvas_width - new_w) // 2
            y = (self.canvas_height - new_h) // 2
            self.img_original_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)))
            self.canvas_original.create_image(x, y, image=self.img_original_tk, anchor=tk.NW)
            
    def show_image_processed(self):
        if self.processed_img is not None:
            h, w, _ = self.processed_img.shape            
            ratio = min(self.canvas_width / w, self.canvas_height / h)
            new_h, new_w = int(h * ratio), int(w * ratio)
            img_resized = cv2.resize(self.processed_img, (new_w, new_h))                  
            self.canvas_processed.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="white")
            x = (self.canvas_width - new_w) // 2
            y = (self.canvas_height - new_h) // 2
            self.img_processed_tk = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)))
            self.canvas_processed.create_image(x, y, image=self.img_processed_tk, anchor=tk.NW)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessor(root)
    root.mainloop()