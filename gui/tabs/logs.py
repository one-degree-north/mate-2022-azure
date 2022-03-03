from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QWidget, QPlainTextEdit, QDialog, QLineEdit
from PyQt5.QtCore import Qt

import logging


class LoggerBox(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.logger = QPlainTextEdit()
        self.logger.setReadOnly(True)

    
    def emit(self, record):
        self.msg = self.format(record)
        self.logger.appendPlainText(self.msg)


class Logs(QDialog, QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.logger = LoggerBox(self)
        self.logger.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S'))

        logging.getLogger().addHandler(self.logger)
        logging.getLogger().setLevel(logging.DEBUG)
        

        self.layout = QGridLayout()
        self.layout.addWidget(self.logger.logger)

        self.setLayout(self.layout)


    def reject(self):
        pass



class CommandLine(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background: rgb(235, 235, 235);
                border-radius: 5px;
                padding: 10px
            }
        """)

        self.key_logging = False

        self.setPlaceholderText('"help" for commands')
        self.setAttribute(Qt.WA_MacShowFocusRect, False) # Mac only
        self.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)

        self.returnPressed.connect(self.command_event)

    def command_event(self):
        self.split_text = self.text().split(' ')

        self.clear()

        if self.split_text[0] == 'help':
            logging.info(f"""

                Hotkeys:
                TAB - shows/hides the tab bar (if styled)
                t - toggles between styled tabs and regular tabs (styled by default)
                1 through 3 - switches active tab


                Commands:
                help - shows this menu
                return (++) - returns text to logs
                exit - stops the program

                key - toggles logging for keyboard presses (off by default)
                controller - toggles logging for controller (off by default) -- remove maybe


                Key:
                "()" = required
                "[]" = optional
                "+" = any value
                "++" = one or more values
                """)

        elif self.split_text[0] == 'return':
            if not len(self.split_text) > 1:
                logging.error('Please provide additional argument(s)')
            else:
                logging.info(' '.join(self.split_text[1:]))

        elif self.split_text[0] == 'exit':
            print('\033[93m\033[1mAzure UI has stopped sucessfully\033[0m')
            exit()


        elif self.split_text[0] == 'key':
            if self.key_logging:
                self.key_logging = False
            else:
                self.key_logging = True

            logging.info('Toggled key logging')


        elif self.split_text[0] == 'ping':
            pass # ping to robot (maybe)
        
        elif self.split_text[0] == 'clear':
            pass # clear logs
        
        else:
            logging.error(f'Command "{self.split_text[0]}" does not exist')

class LogsTab(QWidget):
    def __init__(self):
        super().__init__()


        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(245, 245, 245);
                border-radius: 10px;
                margin: 20px
            }
        """)

        self.logs = Logs()
        self.textbox = CommandLine()


        self.layout = QVBoxLayout()


        self.layout.addWidget(self.logs)
        self.layout.addWidget(self.textbox)

        self.layout.setSpacing(0)

        self.setLayout(self.layout)

    # def keyPressEvent(self, e):
    #     if e.key() == Qt.Key_C:
    #         logging.info('ok')