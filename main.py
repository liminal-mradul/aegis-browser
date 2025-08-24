#!/usr/bin/env python3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QToolBar, QLineEdit
)
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys

HOMEPAGE = "https://online.bonjourr.fr/"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aegis Browser By Mradul Umrao")
        self.resize(1000, 700)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Navigation toolbar
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        back_btn = QAction("←", self)
        back_btn.triggered.connect(self.go_back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction("→", self)
        forward_btn.triggered.connect(self.go_forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        new_tab_btn = QAction("➕", self)
        new_tab_btn.triggered.connect(self.add_tab)
        nav_bar.addAction(new_tab_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Add first tab with Bonjourr homepage
        self.add_tab(HOMEPAGE)

    def add_tab(self, url=None):
        browser = QWebEngineView()
        if not url:
            url = HOMEPAGE
        browser.setUrl(QUrl(url))

        i = self.tabs.addTab(browser, "New Tab")
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_url(self, qurl, browser):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.tabs.currentWidget().setUrl(QUrl(url))

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(HOMEPAGE))

    def go_back(self):
        self.tabs.currentWidget().back()

    def go_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec())
