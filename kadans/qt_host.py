"""Kadans WASDEV — fallback browser: the Chromium inside PySide6 (QtWebEngine), in its own process.

    python -m kadans.qt_host <url> <tabs> <width> <height> <devtools port>

Opens <tabs> hidden views on the composition and serves the DevTools protocol on 127.0.0.1:<port>; prints READY.
Only used when no Edge / Chrome is installed. Its own off-the-record profile: nothing is shared with any browser.
"""
import os
import sys


def main():
    url, n, w, h, port = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    os.environ["QTWEBENGINE_REMOTE_DEBUGGING"] = f"127.0.0.1:{port}"
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS", "--disable-background-timer-throttling "
                          "--disable-renderer-backgrounding --disable-backgrounding-occluded-windows")
    from PySide6.QtCore import Qt, QTimer, QUrl
    from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
    from PySide6.QtWebEngineWidgets import QWebEngineView
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    profile = QWebEngineProfile()                       # off the record
    views, loaded = [], [0]

    def ok(_):
        loaded[0] += 1
        if loaded[0] == n:
            print("READY", flush=True)
    for _ in range(n):
        v = QWebEngineView()
        v.setPage(QWebEnginePage(profile, v))
        v.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        v.setFixedSize(min(w, 1600), min(h, 1600))
        v.move(-w - 500, -h - 500)
        v.loadFinished.connect(ok)
        v.load(QUrl(url))
        v.show()
        views.append(v)
    watchdog = QTimer(interval=2000)                    # parent gone (render finished / killed): quit
    watchdog.timeout.connect(lambda: sys.stdin.closed and app.quit())
    watchdog.start()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
