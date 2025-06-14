# 📸 HDR Photo Maker

**HDR Photo Maker** is a desktop GUI application for applying enhanced tone mapping and exposure adjustments to your images. It supports multiple tone mapping algorithms like Reinhard, Drago, and Mantiuk.

---

## 🧰 Features

- Adjustable exposure and shadow enhancement
- Multiple tone mapping algorithms:
  - Reinhard
  - Drago
  - Mantiuk
- PNG output with adjustable compression level
- Auto-logging with per-session logs
- Clean, cross-platform interface (Linux/macOS)

---

## 🚀 Setup Instructions (Linux/macOS)

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/yourusername/hdr-photo-maker.git
cd hdr-photo-maker
```

### Step 2: Run the Setup Script

This will:
- Create a Python virtual environment
- Install dependencies (Pillow, OpenCV, NumPy)
- Launch the application

```bash
chmod +x setup_hdr_env.sh
./setup_hdr_env.sh
```

---

## 💡 Notes

- Make sure Python 3 is installed: `python3 --version`
- On **Ubuntu/Debian**:
  ```bash
  sudo apt install python3-tk
  ```

- On **macOS**:
  - Use Python installed via [Homebrew](https://brew.sh/) to ensure full `tkinter` support:
    ```bash
    brew install python-tk
    ```

- If HDR tone mapping is not available:
  ```bash
  pip install opencv-contrib-python
  ```

---

## 🖼 Sample Output

Processed images will be saved to:

```bash
~/HDR_Output/
```

Logs will be stored in:

```bash
~/HDR_Logs/
```

---

## 📂 File Structure

```
hdr-photo-maker/
├── hdr_photo_maker.py       # Main GUI application
├── setup_hdr_env.sh         # Environment setup + launcher script
├── README.md
```

---

## 🧪 Requirements

- Python 3.7+
- `tkinter`
- `pillow`
- `opencv-python`
- `numpy`

---

## 📃 License

MIT License — see `LICENSE` file for details.

---

## 🙋‍♂️ Author

Created by Coolythecoder — Contributions welcome!
