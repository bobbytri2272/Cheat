import os
import threading
import time
import tkinter as tk
import warnings
from PIL import Image
from google import genai
import keyboard
from pynput import mouse
import pyautogui

warnings.filterwarnings('ignore')

current_status = 'OK'
status_lock = threading.Lock()
running = True


def load_api_key():
  if os.path.exists('config.txt'):
    with open('config.txt', 'r', encoding='utf-8') as f:
      key = f.read().strip()
      if key:
        return key
  return 'TU_KHOA_API_CUA_BAN'


client = genai.Client(api_key=load_api_key())


def overlay_worker():
  global current_status, running

  root = tk.Tk()
  root.overrideredirect(True)
  root.geometry('+5+5')
  root.attributes('-topmost', True)

  TRANSPARENT_COLOR = '#000001'
  root.config(bg=TRANSPARENT_COLOR)
  root.attributes('-transparentcolor', TRANSPARENT_COLOR)

  label = tk.Label(
      root,
      text='OK',
      font=('Arial', 10, 'normal'),
      fg='#000000',
      bg=TRANSPARENT_COLOR,
  )
  label.pack(anchor='w')

  def update_display():
    if not running:
      root.destroy()
      return
    with status_lock:
      label.config(text=current_status)
    root.after(100, update_display)

  root.after(100, update_display)
  root.mainloop()


def set_status(text):
  global current_status
  with status_lock:
    current_status = text.strip()[:5]


def wait_for_long_press():
  global running
  captured_pos = []
  is_holding = [False]
  start_hold_time = [None]

  def on_click(x, y, button, pressed):
    if not running:
      return False
    if button == mouse.Button.left:
      if pressed:
        is_holding[0] = True
        start_hold_time[0] = time.time()
        captured_pos.clear()
        captured_pos.append((x, y))
      else:
        if is_holding[0]:
          elapsed = time.time() - start_hold_time[0]
          if elapsed >= 1.5:
            return False
          else:
            is_holding[0] = False

  with mouse.Listener(on_click=on_click) as listener:
    while listener.is_alive():
      if not running or keyboard.is_pressed('f11'):
        listener.stop()
        return None
      time.sleep(0.1)

  if captured_pos:
    return captured_pos[0]
  return None


def main():
  global running

  threading.Thread(target=overlay_worker, daemon=True).start()

  f11_count = [0]

  def on_f11():
    f11_count[0] += 1
    if f11_count[0] >= 2:
      global running
      running = False

  keyboard.add_hotkey('f11', on_f11)

  set_status('OK')
  time.sleep(1.5)

  while running:
    set_status('?')
    pos_a = wait_for_long_press()
    if not running or not pos_a:
      break

    set_status('+')
    pos_b = wait_for_long_press()
    if not running or not pos_b:
      break

    x1, y1 = pos_a
    x2, y2 = pos_b
    xmin = min(x1, x2)
    ymin = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    if width < 10 or height < 10:
      continue

    set_status('=')

    screenshot = pyautogui.screenshot(region=(xmin, ymin, width, height))

    prompt_trac_nghiem = (
        'Đây là ảnh chụp một câu hỏi trắc nghiệm.'
        ' Hãy phân tích và CHỈ TRẢ VỀ DUY NHẤT một ký tự đáp án đúng nhất (A, B,'
        ' C hoặc D). Tuyệt đối không kèm theo chữ "Đáp án" hay bất kỳ giải'
        ' thích nào khác. KHÔNG CẦN GIẢI THÍCH, CHỈ TRẢ VỀ KÝ TỰ ĐÁP ÁN. Nếu không xác định được đáp án, hãy trả về chữ "NO"'
    )

    try:
      response = client.models.generate_content(
          model='gemini-3.5-flash-lite', contents=[screenshot, prompt_trac_nghiem]
      )
      answer_text = response.text.strip()
    except Exception:
      answer_text = 'Lỗi'

    set_status(answer_text)
    time.sleep(5)


if __name__ == '__main__':
  main()