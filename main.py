import cv2
import numpy as np
import time

CAMERA_INDEX = 0
FRAME_WIDTH = 960
FRAME_HEIGHT = 540
CAPTURE_SECONDS = 3

def capture_background(cap):
    print(f"\nCapturing background for {CAPTURE_SECONDS} seconds...")
    frames = []
    start = time.time()

    while time.time() - start < CAPTURE_SECONDS:
        ok, frame = cap.read()
        if not ok:
            continue

        frame = cv2.flip(frame, 1)
        frames.append(frame)

        remaining = max(0, CAPTURE_SECONDS - (time.time() - start))
        cv2.putText(
            frame,
            f"Background capture: {remaining:.1f}s",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )
        cv2.imshow("Invisible Cloak", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            return None

    if not frames:
        return None

    # Median background is more stable than using only one frame.
    background = np.median(np.array(frames), axis=0).astype(np.uint8)
    return background


def create_red_mask(frame):
    """Detect red cloth using HSV color ranges."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red wraps around the HSV hue range, so two ranges are needed.
    lower_red_1 = np.array([0, 100, 70])
    upper_red_1 = np.array([10, 255, 255])

    lower_red_2 = np.array([170, 100, 70])
    upper_red_2 = np.array([179, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)

    mask = cv2.bitwise_or(mask1, mask2)

    # Clean small holes/noise.
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    return mask


def make_invisible(frame, background):
    mask = create_red_mask(frame)

    # White = cloak, black = everything else.
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # Put the captured background where the red cloth is.
    background_part = cv2.bitwise_and(background, mask_3ch)
    foreground_part = cv2.bitwise_and(frame, cv2.bitwise_not(mask_3ch))

    result = cv2.add(background_part, foreground_part)
    return result, mask


def main():
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("ERROR: Could not open webcam.")
        print("Try changing CAMERA_INDEX in main.py from 0 to 1.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    print("\n========================================")
    print("        INVISIBLE CLOAK - PYTHON")
    print("========================================")
    print("Controls:")
    print("  B = capture/re-capture background")
    print("  M = show/hide detection mask")
    print("  Q = quit")
    print("========================================\n")

    background = capture_background(cap)
    if background is None:
        cap.release()
        cv2.destroyAllWindows()
        return

    show_mask = False

    while True:
        ok, frame = cap.read()
        if not ok:
            print("Could not read webcam frame.")
            break

        frame = cv2.flip(frame, 1)

        result, mask = make_invisible(frame, background)

        # Add a small status panel.
        cv2.rectangle(result, (10, 10), (390, 95), (20, 20, 20), -1)
        cv2.putText(
            result,
            "INVISIBLE CLOAK",
            (25, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 255, 255),
            2,
        )
        cv2.putText(
            result,
            "B: Background | M: Mask | Q: Quit",
            (25, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.48,
            (255, 255, 255),
            1,
        )

        if show_mask:
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combined = np.hstack((result, mask_bgr))
            cv2.imshow("Invisible Cloak + Mask", combined)
        else:
            cv2.imshow("Invisible Cloak", result)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("b"):
            new_background = capture_background(cap)
            if new_background is not None:
                background = new_background
        elif key == ord("m"):
            show_mask = not show_mask

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
