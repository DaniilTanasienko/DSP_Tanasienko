import cv2
import os

def main():
    print("=== МЕДИА-ПЛЕЕР ===")

    # 1. Выбор файла
    filename = input("Введите имя файла: ").strip()

    if not os.path.exists(filename):
        if os.path.exists(f"../{filename}"):
            filename = f"../{filename}"
            print(f">> Файл найден: {filename}")
        else:
            print(f"Ошибка: Файл '{filename}' не найден!")
            return

    cap = cv2.VideoCapture(filename)
    if not cap.isOpened():
        print("Ошибка открытия видео.")
        return

    # 2. Настройка окна
    new_width = 1280
    ret, test_frame = cap.read()
    if not ret: return
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    h, w = test_frame.shape[:2]
    ratio = new_width / w
    new_height = int(h * ratio)

    # 3. Настройки
    mode = 'normal'
    paused = False

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or fps > 120: fps = 30

    base_delay = int(1000 / fps)
    current_delay = base_delay
    speed_label = "x1.0"

    print("\nВидео загружено:")
    print(" [ПРОБЕЛ] - Пауза / Старт")
    print(" [r] - повтор")
    print(" [1] - Нормальная скорость")
    print(" [2] - Ускорение (x2)")
    print("-" * 20)
    print(" [f/e/b/c] - Фильтры")
    print(" [q] - Выход")


    font = cv2.FONT_HERSHEY_TRIPLEX

    while True:
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Конец видео. Нажмите 'r' для повтора.")
                paused = True
                while paused:
                    key = cv2.waitKey(100) & 0xFF
                    if key == ord('r'):
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        paused = False
                        break
                    elif key == ord('q'):
                        cap.release()
                        cv2.destroyAllWindows()
                        return
                continue

        frame_show = cv2.resize(frame, (new_width, new_height))

        # Фильтры
        if mode == 'blur':
            frame_show = cv2.GaussianBlur(frame_show, (15, 15), 0)
        elif mode == 'contrast':
            frame_show = cv2.convertScaleAbs(frame_show, alpha=1.5, beta=10)
        elif mode == 'bw':
            gray = cv2.cvtColor(frame_show, cv2.COLOR_BGR2GRAY)
            frame_show = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        status = "PAUSED" if paused else "PLAY"

        # Новый формат строки: [ PLAY ]  >> x1.0 <<  { Mode: normal }
        text = f"[{status}]  >> {speed_label} <<  {{ Mode: {mode} }}"
        text_size = cv2.getTextSize(text, font, 0.7, 1)[0]
        text_w = text_size[0]
        x_pos = (new_width - text_w) // 2
        y_pos = new_height - 30
        cv2.putText(frame_show, text, (x_pos, y_pos),
                    font, 0.7, (0, 0, 255), 1, cv2.LINE_AA)

        cv2.imshow('Media Player', frame_show)

        # Управление
        wait_time = 100 if paused else current_delay
        key = cv2.waitKey(wait_time) & 0xFF

        if key == ord('q'):
            break
        elif key == 32:  # Пробел
            paused = not paused
        elif key == ord('r'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            paused = False

        # Скорость
        elif key == ord('1'):
            current_delay = base_delay
            speed_label = "x1.0"
        elif key == ord('2'):
            current_delay = max(1, base_delay // 2)
            speed_label = "x2.0"

        # Фильтры
        elif key == ord('f'):
            mode = 'blur'
        elif key == ord('e'):
            mode = 'contrast'
        elif key == ord('b'):
            mode = 'bw'
        elif key == ord('c'):
            mode = 'normal'

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()
