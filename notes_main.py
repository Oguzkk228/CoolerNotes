import json
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QTextEdit, QHBoxLayout, QListWidget, QLineEdit, QInputDialog
def show_note():
    key = zametkilist.selectedItems()[0].text()
    Zametki.setText(notes[key]['текст'])
    taglist.clear()
    taglist.addItems(notes[key]['теги'])
def add_note():
    notes_name, result = QInputDialog.getText(
        main_win, 'Добавление заметки', 'Название:'
    )
    if result:
        notes[notes_name] = {
            'текст': '',
            'теги': []
        }
        zametkilist.addItem(notes_name)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
def del_note():
    if zametkilist.selectedItems():
        key = zametkilist.selectedItems()[0].text()
        del notes[key]
        zametkilist.clear()
        zametkilist.addItems(notes)
        Zametki.clear()
        taglist.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
def save_note():
    if zametkilist.selectedItems():
        key = zametkilist.selectedItems()[0].text()
        notes[key]['текст'] = Zametki.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
def add_tag():
    if zametkilist.selectedItems():
        key = zametkilist.selectedItems()[0].text()
        tag = newtag.text()
        if tag != '' and not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            taglist.addItem(tag)
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
def del_tag():
    if taglist.selectedItems():
            newtag.clear()
            key = zametkilist.selectedItems()[0].text()
            tag = taglist.selectedItems()[0].text()
            notes[key]['теги'].remove(tag)
            taglist.clear()
            taglist.addItems(notes[key]['теги'])
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
def search_tag():
    tag = newtag.text()
    if tag and findtag.text() == 'Искать заметки по тегу':
        notes_filtered = dict()
        for key in notes:
            if tag in notes[key]['теги']:
                notes_filtered[key] = notes[key]
            findtag.setText('Отменить поиск')
            zametkilist.clear()
            taglist.clear()
            Zametki.clear()
            zametkilist.addItems(notes_filtered)
    else:
        newtag.clear()
        findtag.setText('Искать заметки по тегу')
        zametkilist.clear()
        zametkilist.addItems(notes)
app = QApplication([])
main_win = QWidget()
main_win.resize(900, 600)
main_win.setWindowTitle('Умные заметки')
Zametki = QTextEdit()
text = QLabel('Список заметок')
text2 = QLabel('Список тегов')
createbtn = QPushButton('Создать заметку')
deletebtn = QPushButton('Удалить заметку')
savebtn = QPushButton('Сохранить заметку')
addtag = QPushButton('Добавить к заметке')
untag = QPushButton('Открепить заметку')
findtag = QPushButton('Искать заметки по тегу')
newtag = QLineEdit()
newtag.setPlaceholderText('Введите тег...')
zametkilist = QListWidget()
taglist = QListWidget()
v_line1 = QVBoxLayout()
v_line1.addWidget(Zametki)
v_line2 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line1.addWidget(createbtn)
h_line1.addWidget(deletebtn)
h_line2 = QHBoxLayout()
h_line2.addLayout(v_line1)
h_line2.addLayout(v_line2)
h_line3 = QHBoxLayout()
v_line2.addWidget(text)
v_line2.addWidget(zametkilist)
v_line2.addLayout(h_line1)
v_line2.addWidget(savebtn)
v_line2.addWidget(text2)
v_line2.addWidget(taglist)
h_line3.addWidget(addtag)
h_line3.addWidget(untag)
v_line2.addWidget(newtag)
v_line2.addLayout(h_line3)
v_line2.addWidget(findtag)
with open('notes_data.json', 'r') as file:
    notes = json.load(file)
zametkilist.addItems(notes)
zametkilist.itemClicked.connect(show_note)
untag.clicked.connect(del_tag)
addtag.clicked.connect(add_tag)
findtag.clicked.connect(search_tag)
savebtn.clicked.connect(save_note)
createbtn.clicked.connect(add_note)
deletebtn.clicked.connect(del_note)
main_win.setLayout(h_line2)
main_win.show()
app.exec_()