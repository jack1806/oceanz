from PyQt6.QtWidgets import QMainWindow, QListWidgetItem
from Widgets.entry_widget import EntryWidget
from Ui.main_window import Ui_MainWindow
from main import OceanzEntries, SHEET_ID
import qdarktheme


class OceanZApp(QMainWindow):

    def __init__(self):
        super(OceanZApp, self).__init__()
        qdarktheme.setup_theme()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.sheetEntries.clicked.connect(self.update_sheet_entry)
        self.ui.reportEntries.clicked.connect(self.update_report_entry)

        self.ui.reportTitle.setStyleSheet('''background-color:black;color: yellow;border: 1px solid #000000;''')
        self.ui.sheetTitle.setStyleSheet('''background-color:black;color: yellow;border: 1px solid #000000;''')

        self.oceanz = OceanzEntries(SHEET_ID)
        self.setup_entries_list()

    def update_sheet_entry(self):
        self.oceanz.set_sheet_entry()
        self.setup_entries_list()

    def update_report_entry(self):
        self.oceanz.set_report_entry()
        self.setup_entries_list()

    def setup_entries_list(self):
        self.ui.entriesListWidget.clear()
        self.ui.htmlEntriesWidget.clear()
        mismatch = 0
        sheet_total = 0
        for entry in sorted(self.oceanz.google_sheet_entries.keys()):
            entry_widget = EntryWidget()
            entry_widget.set_session(entry)
            entry_widget.set_amount(str(self.oceanz.google_sheet_entries[entry]))
            sheet_total += int(self.oceanz.google_sheet_entries[entry])
            entry_list_widget_item = QListWidgetItem(self.ui.entriesListWidget)
            entry_list_widget_item.setSizeHint(entry_widget.sizeHint())

            if entry not in self.oceanz.report_entries:
                entry_widget.text_up_label.setStyleSheet(
                    entry_widget.text_up_label.styleSheet()+'''background-color:red;color: rgb(255, 255, 255);''')
                entry_widget.text_down_label.setStyleSheet(
                    entry_widget.text_down_label.styleSheet() + '''background-color:red;color: rgb(255, 255, 255);''')
                mismatch += 1
            elif self.oceanz.report_entries[entry] != self.oceanz.google_sheet_entries[entry]:
                entry_widget.text_up_label.setStyleSheet(
                    entry_widget.text_up_label.styleSheet() + '''background-color:yellow;color: rgb(0, 0, 0);''')
                entry_widget.text_down_label.setStyleSheet(
                    entry_widget.text_down_label.styleSheet() + '''background-color:yellow;color: rgb(0, 0, 0);''')
                mismatch += 1

            self.ui.entriesListWidget.addItem(entry_list_widget_item)
            self.ui.entriesListWidget.setItemWidget(entry_list_widget_item, entry_widget)

        self.ui.sheetResult.setText(f"Entries Matched")
        self.ui.sheetResult.setStyleSheet(
            self.ui.sheetEntries.styleSheet() + '''color:green;'''
        )
        if mismatch:
            self.ui.sheetResult.setText(f"Entries mismatch : {mismatch}")
            self.ui.sheetResult.setStyleSheet(
                self.ui.sheetEntries.styleSheet() + '''color:red;'''
            )

        mismatch = 0
        report_total = 0
        for entry in sorted(self.oceanz.report_entries.keys()):
            entry_widget = EntryWidget()
            entry_widget.set_session(entry)
            entry_widget.set_amount(str(self.oceanz.report_entries[entry]))
            report_total += int(self.oceanz.report_entries[entry])
            entry_list_widget_item = QListWidgetItem(self.ui.htmlEntriesWidget)
            entry_list_widget_item.setSizeHint(entry_widget.sizeHint())

            if entry not in self.oceanz.google_sheet_entries:
                entry_widget.text_up_label.setStyleSheet(
                    entry_widget.text_up_label.styleSheet()+'''background-color:red;color: rgb(255, 255, 255);''')
                entry_widget.text_down_label.setStyleSheet(
                    entry_widget.text_down_label.styleSheet() + '''background-color:red;color: rgb(255, 255, 255);''')
                mismatch += 1
            elif self.oceanz.report_entries[entry] != self.oceanz.google_sheet_entries[entry]:
                entry_widget.text_up_label.setStyleSheet(
                    entry_widget.text_up_label.styleSheet() + '''background-color:yellow;color: rgb(0, 0, 0);''')
                entry_widget.text_down_label.setStyleSheet(
                    entry_widget.text_down_label.styleSheet() + '''background-color:yellow;color: rgb(0, 0, 0);''')
                mismatch += 1

            self.ui.htmlEntriesWidget.addItem(entry_list_widget_item)
            self.ui.htmlEntriesWidget.setItemWidget(entry_list_widget_item, entry_widget)

        self.ui.reportResult.setText(f"Entries Matched")
        self.ui.reportResult.setStyleSheet(
            self.ui.sheetEntries.styleSheet() + '''color:green;'''
        )
        if mismatch:
            self.ui.reportResult.setText(f"Entries mismatch : {mismatch}")
            self.ui.reportResult.setStyleSheet(
                self.ui.sheetEntries.styleSheet() + '''color:red;'''
            )

        self.ui.sheetTotal.setText(str(sheet_total))
        self.ui.sheetTotal.setStyleSheet(
            self.ui.sheetEntries.styleSheet() + ['''color:red;''', '''color:green;'''][sheet_total == report_total]
        )
        self.ui.reportTotal.setText(str(report_total))
        self.ui.reportTotal.setStyleSheet(
            self.ui.sheetEntries.styleSheet() + ['''color:red;''', '''color:green;'''][sheet_total == report_total]
        )
