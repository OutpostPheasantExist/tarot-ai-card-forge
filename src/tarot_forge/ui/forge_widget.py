"""ForgeWidget — the one screen. Question in, cards out."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from tarot_forge.config.settings import ForgeSettings
from tarot_forge.handlers.reading_handler import ReadingHandler


class ForgeWidget(QWidget):
    def __init__(self, handler: ReadingHandler, settings: ForgeSettings) -> None:
        super().__init__()
        self._handler = handler
        self._settings = settings
        self.setWindowTitle("tarot-ai-card-forge")
        self.resize(960, 640)
        self._build()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.addWidget(QLabel("Ask the deck a question:"))

        self._question = QLineEdit()
        self._question.setPlaceholderText("What should I know about the next release?")
        root.addWidget(self._question)

        row = QHBoxLayout()
        self._spread = QComboBox()
        self._spread.addItems(["three-card", "celtic-cross"])
        self._spread.setCurrentText(self._settings.default_spread)
        row.addWidget(QLabel("Spread:"))
        row.addWidget(self._spread)
        row.addStretch(1)

        draw_btn = QPushButton("Draw")
        draw_btn.clicked.connect(self._on_draw)
        row.addWidget(draw_btn)
        root.addLayout(row)

        self._status = QLabel("idle")
        self._status.setAlignment(Qt.AlignLeft)
        root.addWidget(self._status)
        root.addStretch(1)

    def _on_draw(self) -> None:
        question = self._question.text().strip() or "Open reading"
        spread_id = self._spread.currentText()
        try:
            job = self._handler.run(question=question, spread_id=spread_id)
        except ValueError as exc:
            self._status.setText(f"error: {exc}")
            return
        self._status.setText(f"job {job.job_id} queued — {len(job.draws)} cards")