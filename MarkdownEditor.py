import sqlite3
from PyQt5.QtWidgets import QMainWindow, QAction,\
        QPushButton, QTreeView, QFileSystemModel, \
        QFileDialog, QTextEdit

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QDir, pyqtSlot
import markdown

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        # turn off resizing
        self.setFixedSize(1200, 900)
        # initialize vars
        self.isEditing = True
        self.switcherText = ['Edit', 'Preview']
        self.markdownText = ''
        self.fileName = ''
        
        # Создание пунктов меню
        file_menu = self.menuBar().addMenu('File')
        open_action = QAction('Open', self)
        open_action.setShortcut(QKeySequence('Ctrl+O'))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Save', self)
        save_action.setShortcut(QKeySequence('Ctrl+S'))
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save As', self)
        save_as_action.setShortcut(QKeySequence('Ctrl+Shift+S'))
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)

        create_file_action = QAction('Create file', self)
        create_file_action.setShortcut(QKeySequence('Ctrl+N'))
        create_file_action.triggered.connect(self.create_file)
        file_menu.addAction(create_file_action)
        
        # Поле для ввода текста
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(330, 30, 855, 810)
        self.text_edit.setStyleSheet("border: 1px solid black;")
        # TODO: сделать сохранение и render
        self.text_edit.textChanged.connect(self.update_markdown)
        
        # Кнопка для переключения режима
        self.mode_button = QPushButton(self.switcherText[self.isEditing], self)
        self.mode_button.setGeometry(10, 810, 300, 30)
        self.mode_button.clicked.connect(self.switch_mode)
        self.mode_button.setStyleSheet("background-color: #CECECE; border: 1px solid black;")

        # Проводник файловой структуры
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.currentPath())
        self.file_model.setNameFilters(['*.md'])
        self.file_model.setNameFilterDisables(False)

        self.file_tree = QTreeView(self)
        self.file_tree.setModel(self.file_model)
        self.file_tree.setHeaderHidden(True)
        self.file_tree.setColumnWidth(0, 300)
        self.file_tree.setRootIndex(self.file_model.index(QDir.currentPath()))
        self.file_tree.setGeometry(10, 30, 300, 750)
        self.file_tree.doubleClicked.connect(lambda index: self.open_file_from_tree(index))
        self.file_tree.setStyleSheet("background-color: #CECECE; border: 1px solid black;")
        
        # open last opened file
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT last_file FROM users WHERE login='admin';")
        result = cursor.fetchall()[0][0]
        print(result)
        if result != '':
            with open(result) as f:
                self.markdownText = f.read()
                if self.isEditing:
                    self.text_edit.setPlainText(self.markdownText)
                else:
                    html = markdown.markdown(self.markdownText, extras=["task_list"])
                    self.text_edit.setHtml(html)
            
    
    # функция для создания пустого файла (зануляет имя и содержание)
    def create_file(self):
        self.fileName = ''
        self.markdownText = ''
        self.text_edit.setPlainText(self.markdownText)

    # обновляет текст, только если мы в редакторе, на превью изменения не сохраняются
    def update_markdown(self):
        if self.isEditing:
            self.markdownText = self.text_edit.toPlainText()
    
    def update_file_tree(self, path = QDir.currentPath()):
        # Обновляем список файлов и папок в QTreeView
        self.file_tree.setRootIndex(self.file_model.index(path))
    
    @pyqtSlot()
    def open_file(self):
        # Логика открытия файла
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Markdown Files (*.md)", options=options)
        if self.fileName:
            print(self.fileName)
        with open(self.fileName) as f:
            self.markdownText = f.read()
            if self.isEditing:
                self.text_edit.setPlainText(self.markdownText)
            else:
                html = markdown.markdown(self.markdownText, extras=["task_list"])
                self.text_edit.setHtml(html)
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET last_file = '{self.fileName}' WHERE login = 'admin';")
        result = cursor.fetchall()
        print(result)
        conn.commit()
            

    @pyqtSlot()
    def save_file(self):
        # Логика сохранения файла
        if self.fileName == '':
            self.save_as_file()
        else:
            with open(self.fileName, 'w') as f:
                f.write(self.markdownText)
                print(self.fileName)
        self.update_file_tree()
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET last_file = '{self.fileName}' WHERE login = 'admin';")
        result = cursor.fetchall()
        print(result)
        conn.commit()

    @pyqtSlot()
    def save_as_file(self):
        # Логика сохранения файла как
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Markdown Files (*.md)", options=options)
        
        with open(self.fileName, 'w') as f:
            f.write(self.markdownText)
            print(self.fileName)
        self.update_file_tree()
        
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET last_file = '{self.fileName}' WHERE login = 'admin';")
        result = cursor.fetchall()
        print(result)
        conn.commit()
        
    @pyqtSlot()
    def switch_mode(self):
        # Логика переключения режима отображения
        self.isEditing = not self.isEditing
        
        if self.isEditing:    
            self.text_edit.setPlainText(self.markdownText)
        else:
            html = markdown.markdown(self.markdownText, extras=["task_list"])
            self.text_edit.setHtml(html)
        self.mode_button.setText(self.switcherText[self.isEditing])

    @pyqtSlot()
    def open_file_from_tree(self, index):
        fileName = self.file_model.fileInfo(index).absoluteFilePath()
        if '.md' not in fileName:
            print('Not Markdown file')
            return
        else:
            self.fileName = fileName
        # Логика открытия файла из проводника
        print(self.fileName)
        with open(self.fileName) as f:
            self.markdownText = f.read()
            if self.isEditing:
                self.text_edit.setPlainText(self.markdownText)
            else:
                html = markdown.markdown(self.markdownText, extras=["task_list"])
                self.text_edit.setHtml(html)
        conn = sqlite3.connect('DataBase.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE users SET last_file = '{self.fileName}' WHERE login = 'admin';")
        result = cursor.fetchall()
        print(result)
        conn.commit()