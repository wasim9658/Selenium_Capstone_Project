"""Screenshot helper. Every screenshot is saved to reports/screenshots and its path is
also recorded so the HTML report can embed it."""
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCREENSHOT_DIR = ROOT / "reports" / "screenshots"


def _safe(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", text).strip("_")


def take_screenshot(driver, test_name: str, step: str) -> Path:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    path = SCREENSHOT_DIR / f"{_safe(test_name)}__{_safe(step)}__{stamp}.png"
    driver.save_screenshot(str(path))
    return path
