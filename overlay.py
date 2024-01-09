import cv2
import numpy as np


def overlay_images(bg_path: str, ov_path: str, output_path: str) -> None:
    try:
        print(f"Overlaying {ov_path} on {bg_path} and saving to {output_path}")

        background = cv2.imread(bg_path)
        overlay = cv2.imread(ov_path)

        # Resize images
        W = 750
        imgScale = W / background.shape[1]
        new_background = cv2.resize(
            background, (int(background.shape[1] * imgScale),
                         int(background.shape[0] * imgScale)))

        W = 700  # Increase this value to make the overlay image bigger
        imgScale = W / overlay.shape[1]
        new_overlay = cv2.resize(overlay, (int(overlay.shape[1] * imgScale), int(overlay.shape[0] * imgScale)))

        # Create white square
        square = np.zeros_like(new_background)
        square.fill(255)

        # Adjust the offset for making the overlay image bigger from the left side
        offset = 0  # You can adjust this value to make it bigger or smaller
        y, x, _ = new_background.shape
        square[int(y - new_overlay.shape[0]) - offset:int(y) - offset,
               :new_overlay.shape[1]] = new_overlay

        # Overlay with specified opacity
        OPACITY = 0.7
        added_image = cv2.addWeighted(new_background, 0.6, square, 0.4, 0)

        # Adjust contrast
        alpha = 1.3
        beta = -75
        adjusted = cv2.convertScaleAbs(added_image, alpha=alpha, beta=beta)

        # Save the result
        cv2.imwrite(output_path, adjusted)

        print(f"Overlayed successfully to {output_path}")

    except Exception as e:
        raise e
