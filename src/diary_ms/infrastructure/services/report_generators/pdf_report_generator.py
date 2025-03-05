from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.diary_ms.application.diary_card.dto.diary_cards_report import DiaryCardsReportDTO
from src.diary_ms.application.diary_card.interfaces.report_generator import ReportGenerator


class PDFReportGenerator(ReportGenerator):
    async def generate(self, report_data: DiaryCardsReportDTO) -> bytes:
        """
        Генерирует PDF-отчет на основе данных отчета из БД.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        # Заголовок отчета
        title = Paragraph("Weekly DBT Diary Card Report", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        # Данные отчета
        data = [
            ["Beginning of the week", report_data.start_date.strftime("%Y-%m-%d")],
            ["End of the week", report_data.end_date.strftime("%Y-%m-%d")],
            ["Total entries", report_data.total_entries],
            ["Average mood", f"{report_data.average_mood:.2f}"],
        ]

        # Таблица с данными
        table = Table(data, colWidths=[200, 200])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        story.append(table)
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
