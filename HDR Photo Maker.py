# Enhanced HDR Photo Maker with Improved Tone Mapping
# Dependencies: tkinter, PIL (Pillow), OpenCV (cv2), numpy, json, pathlib, logging, os, threading, datetime
# To install all dependencies, run:
# pip install pillow opencv-python numpy
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import cv2
import numpy as np
import os
import logging
from pathlib import Path
import json
from datetime import datetime
import threading

# Ensure that the log directory exists
LOG_DIR = Path.home() / "HDR_Logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
log_filename = LOG_DIR / f"hdr_app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def load_config():
    try:
        with open(Path.home() / ".hdr_photo_maker_config.json") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        return {}

class HDRProcessor:
    def __init__(self, temp_dir, output_dir):
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        self.exposure = 1.0
        self.shadow = 1.0
        self.tone_mapping = 'None'
        self.compression_level = 3
    def set_exposure(self, val):
        self.exposure = max(0.1, float(val))
    def set_shadow(self, val):
        self.shadow = max(0.1, float(val))
    def set_tone_mapping(self, mode):
        self.tone_mapping = mode
    def set_compression(self, level):
        self.compression_level = int(level)
    def process_image(self, img_path):
        img = cv2.imread(str(img_path))
        if img is None:
            logging.error(f"Cannot read {img_path}")
            return None
        img = np.clip(img * self.exposure, 0, 255).astype(np.uint8)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = np.clip(l / self.shadow, 0, 255).astype(np.uint8)
        img_processed = cv2.cvtColor(cv2.merge((l, a, b)), cv2.COLOR_LAB2BGR)
        return img_processed
    def apply_tone_mapping(self, img):
        if img is None:
            return None
        try:
            if self.tone_mapping == 'Reinhard':
                tonemap = cv2.createTonemapReinhard(gamma=1.5, intensity=0)
                img = (tonemap.process(img.astype(np.float32) / 255) * 255).astype(np.uint8)
            elif self.tone_mapping == 'Drago':
                tonemap = cv2.createTonemapDrago(gamma=1.0, saturation=1.0, bias=0.85)
                img = (tonemap.process(img.astype(np.float32) / 255) * 255).astype(np.uint8)
            elif self.tone_mapping == 'Mantiuk':
                tonemap = cv2.createTonemapMantiuk(saturation=1.0, scale=0.7)
                img = (tonemap.process(img.astype(np.float32) / 255) * 255).astype(np.uint8)
        except Exception as e:
            logging.error(f"Error applying tone mapping: {e}")
        return img
    def apply_all_and_save(self, img_path, filename):
        img = self.process_image(img_path)
        if img is None:
            return None
        img = self.apply_tone_mapping(img)
        out_path = self.output_dir / filename
        cv2.imwrite(str(out_path), img, [cv2.IMWRITE_PNG_COMPRESSION, self.compression_level])
        return out_path

class HDRApp:
    def __init__(self, root):
        self.root = root
        self.processor = HDRProcessor(Path.home() / "HDR_Temp", Path.home() / "HDR_Output")
        self.setup_ui()
        self.load_settings()
    def setup_ui(self):
        self.root.title("HDR Photo Maker")
        self.root.geometry("1000x800")
        ttk.Button(self.root, text="Load Image", command=self.load_image).pack(pady=10)
        ttk.Button(self.root, text="Save HDR with All Settings", command=self.save_image).pack(pady=10)
        ttk.Label(self.root, text="Exposure").pack()
        self.exposure_slider = ttk.Scale(self.root, from_=0.1, to=3.0, command=self.update_exposure)
        self.exposure_slider.set(1.0)
        self.exposure_slider.pack(pady=10)
        ttk.Label(self.root, text="Shadows").pack()
        self.shadow_slider = ttk.Scale(self.root, from_=0.1, to=3.0, command=self.update_shadow)
        self.shadow_slider.set(1.0)
        self.shadow_slider.pack(pady=10)
        ttk.Label(self.root, text="Tone Mapping").pack()
        self.tone_mapping_var = tk.StringVar(value='None')
        ttk.OptionMenu(self.root, self.tone_mapping_var, 'None', 'Reinhard', 'Drago', 'Mantiuk', command=self.update_tone).pack()
        ttk.Label(self.root, text="Compression Level").pack()
        self.compression_spin = ttk.Spinbox(self.root, from_=-1, to=9, increment=1, command=self.update_compression)
        self.compression_spin.set(3)
        self.compression_spin.pack(pady=10)
        self.log_text = tk.Text(self.root, height=10)
        self.log_text.pack(fill='x', pady=10)
    def load_settings(self):
        config = load_config()
        self.processor.tone_mapping = config.get('tone_mapping', 'None')
        self.processor.compression_level = config.get('compression_level', 3)
    def load_image(self):
        self.loaded_path = filedialog.askopenfilename()
        if self.loaded_path:
            self.log(f"Image loaded: {self.loaded_path}")
    def save_image(self):
        if hasattr(self, 'loaded_path'):
            path = self.processor.apply_all_and_save(self.loaded_path, 'output_hdr_with_all.png')
            if path:
                self.log(f"Saved HDR image with all settings to {path}")
            else:
                self.log("Failed to save HDR image")
        else:
            self.log("No image loaded")
    def update_exposure(self, val):
        self.processor.set_exposure(val)
    def update_shadow(self, val):
        self.processor.set_shadow(val)
    def update_tone(self, val):
        self.processor.set_tone_mapping(val)
    def update_compression(self):
        self.processor.set_compression(self.compression_spin.get())
    def log(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = HDRApp(root)
    root.mainloop()
