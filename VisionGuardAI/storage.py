
import lzma
import os
from datetime import datetime

def save_image(frame):
    os.makedirs("records", exist_ok=True)

    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".xz"
    path = os.path.join("records", filename)

    compressed = lzma.compress(frame.tobytes())

    with open(path, "wb") as f:
        f.write(compressed)

    return path
