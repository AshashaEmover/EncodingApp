import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.properties import ObjectProperty, StringProperty

### Настройки ###
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemanddock')  # Активация клавы на Андройде

LabelBase.register(name='NadejdaBold', fn_regular='NadejdaBold.ttf')  # Добавление шрифтов
LabelBase.register(name='TimesNewRoman', fn_regular='TimesNewRoman.ttf')

# Window.size = (1080 / 2.8, 2048 / 2.8) # Стартовое размер окна на компе (закомментить для Андройда)

RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'  # Определение русского алфавита
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Определение английского алфавита


### Движок ###
def shifrovanie(text, key, alphabet):
    mytext = ''
    key_length = len(key)

    text = text.upper()  # Приводим текст к заглавным буквам
    key = key.upper()    # Приводим ключ к заглавным буквам

    j = 0

    for symb in text:
        if symb in alphabet:
            text_index = alphabet.index(symb)
            key_index = alphabet.index(key[j % key_length])
            encrypted_index = (text_index + key_index) % len(alphabet)
            mytext += alphabet[encrypted_index]
            j += 1
        else:
            mytext += symb  # Если символ не в алфавите, добавляем его как есть
    return mytext.lower()  # Возвращаем зашифрованный текст в нижнем регистре


def deshifrovanie(text, key, alphabet):
    mytext = ''
    key_length = len(key)

    text = text.upper()
    key = key.upper()

    j = 0

    for symb in text:
        if symb in alphabet:
            text_index = alphabet.index(symb)
            key_index = alphabet.index(key[j % key_length])
            encrypted_index = (text_index - key_index) % len(alphabet)
            mytext += alphabet[encrypted_index]
            j += 1
        else:
            mytext += symb
    return mytext.lower()


class SimpleTextInput(TextInput):
    def on_double_tap(self):
        pass

    def on_triple_tap(self):
        pass


class ImageButton(ButtonBehavior, Image):
    pass

### Конструктор ###
Builder.load_string('''
#:import Clipboard kivy.core.clipboard.Clipboard

# Экран выбора языка
<LanguageSelectionScreen>: 

    BoxLayout:  # Основная рабочая область
        orientation: 'vertical'
        padding: 50
        spacing: 50

        Label:
            text: 'Шифрование на каком языке?'
            font_size: '30sp'
            font_name: 'NadejdaBold'

        ImageButton:  # Картинка с поведением кнопки
            size_hint: 1, 1
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_press: root.manager.current = 'english'  # На вызове: меняет в Менеджере Экранов текущий экран 
            text: 'English'
            # Код с картинкой 
            canvas:            
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: 'en_flag.png'
            # Конец кода с картинкой 

        ImageButton:  # Картинка с поведением кнопки
            size_hint: 1, 1
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            on_press: root.manager.current = 'russian'  # Нажатие: меняет в Менеджере Экранов текущий экран 
            text: ''
            # Код с картинкой 
            canvas:     
                Rectangle:
                    pos: self.pos
                    size: self.size
                    source: 'ru_flag.png'
            # Конец кода с картинкой 

# Экран шифра
<CipherScreen>:

    BoxLayout:  # Основная рабочая область
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        SimpleTextInput:  # Вывод текста с множеством строк с отключенным выделением
            text: root.result_txt
            size_hint: 1, 1
            font_size: '32sp'
            font_name: 'TimesNewRoman'
            multiline: True  # много строк
            background_color: [0,0,0,0]
            cursor_color: [1,1,1,1]
            readonly: True
            allow_copy: False
            on_focus: cancel_selection: True
            scroll_from_swipe: True
            foreground_color: [1,1,1,1]         
        
        BoxLayout:  # Доп горизонтальная рабочая область
            orientation: 'horizontal'
            padding: 0
            spacing: 10
            size_hint: 1, 0.8

            TextInput:  # Ввод текста
                id: txt_inpt
                multiline: True
                hint_text: 'Введите текст'
                size_hint: 1, 1
                font_name: 'TimesNewRoman'
                font_size: '24sp'
                
            Button:  # Кнопка удалить
                size: 40, 40
                size_hint: None, None
                pos_hint: {'center_y': 0.5}
                on_press: root.del_text_inpt('txt_inpt')  # Нажатие: удалить текст у виджета с id txt_inpt
                text: 'Del'
                font_size: '14sp'
                font_name: 'TimesNewRoman'             
        
        BoxLayout:  # Доп горизонтальная рабочая область
            orientation: 'horizontal'
            padding: 0
            spacing: 10
            size_hint: 1, 0.2
        
            TextInput:  # Ввод текста
                id: key_inpt
                multiline: False
                hint_text: 'Введите ключ'
                size_hint: 1, 1
                font_name: 'TimesNewRoman'
                font_size: '24sp'
                
            Button:  # Кнопка удалить
                size: 40, 40
                size_hint: None, None
                pos_hint: {'center_y': 0.5}
                on_press: root.del_text_inpt('key_inpt')  # Нажатие: удалить текст у виджета с id txt_inpt
                text: 'Del'
                font_size: '14sp'
                font_name: 'TimesNewRoman' 
            
        BoxLayout:  # Доп горизонтальная рабочая область
            orientation: 'horizontal'
            padding: 0
            spacing: 20
            size_hint: 1, 0.25
            
            Button:  # Кнопка Шифровать
                size_hint: 1, 1
                on_press: root.encrypt()  # Нажатие: запуск функции движка через функцию родителя
                text: 'Шифровать'
                font_size: '30sp'
                font_name: 'NadejdaBold'
    
            Button:  # Кнопка Дешифровать
                size_hint: 1, 1
                on_press: root.decrypt()  # Нажатие: запуск функции движка через функцию родителя
                text: 'Дешифровать'
                font_size: '30sp'
                font_name: 'NadejdaBold'

        Button:  # Кнопка Копировать
            size_hint: 1, 0.25
            on_release: Clipboard.copy(root.txt_to_copy)  # Нажатие: копировать результат в переменной родителя
            text: 'Копировать результат'
            font_size: '30sp'
            font_name: 'NadejdaBold'
''')


### Kivy ###
class LanguageSelectionScreen(Screen):  # Экран выбора языка
    pass


class CipherScreen(Screen):  # Экран шифра
    result_txt = StringProperty('Результат будет здесь')
    txt_to_copy = StringProperty('')

    def __init__(self, alphabet, **kwargs):
        super().__init__(**kwargs)
        self.alphabet = alphabet

    def encrypt(self):  # Вызов функции движка
        text = self.ids.txt_inpt.text
        key = self.ids.key_inpt.text
        try:  # Проверка на посторонние символы в ключе
            if text and key:
                self.txt_to_copy = shifrovanie(text, key, self.alphabet)  # Вызов функции движка
                self.result_txt = f'{self.txt_to_copy}'  # Сохранение текста для копирования
            else:
                self.result_txt = 'Пожалуйста, введите текст и ключ.'
        except ValueError:  # Посторонние символы в ключе
            self.result_txt = 'Пожалуйста, введите ключ без символов.'

    def decrypt(self):  # Вызов функции движка
        text = self.ids.txt_inpt.text
        key = self.ids.key_inpt.text
        try:  # Проверка на посторонние символы в ключе
            if text and key:
                self.txt_to_copy = deshifrovanie(text, key, self.alphabet)  # Вызов функции движка
                self.result_txt = f'{self.txt_to_copy}'  # Сохранение текста для копирования
            else:
                self.result_txt = 'Пожалуйста, введите текст и ключ.'
        except ValueError:  # Посторонние символы в ключе
            self.result_txt = 'Пожалуйста, введите ключ без символов.'

    def del_text_inpt(self, id):  # Функциия удаления текста
        if id == 'txt_inpt':
            self.ids.txt_inpt.text = ''
        else:
            self.ids.key_inpt.text = ''


class CipherApp(App):  # Основной класс приложения
    def build(self):
        sm = ScreenManager(transition=SwapTransition())  # Создание Менеджера Экрана
        sm.add_widget(LanguageSelectionScreen(name='language'))
        sm.add_widget(CipherScreen(RUSSIAN_ALPHABET, name='russian'))
        sm.add_widget(CipherScreen(ENGLISH_ALPHABET, name='english'))

        # Код для шага назад при нажатии кнопки назад Андроида или esc Windows
        def post_build_init(ev):
            from kivy.base import EventLoop
            EventLoop.window.bind(on_keyboard=hook_keyboard)

        def hook_keyboard(window, key, *largs):
            if key == 27:
                if sm.current == 'language':
                    App.get_running_app().stop()
                sm.current = 'language'
                return True

        self.bind(on_start=post_build_init)
        # Конец кода для шага назад при нажатии кнопки назад Андроида или esc Windows

        return sm


if __name__ == '__main__':
    CipherApp().run()  # Запуск приложения
