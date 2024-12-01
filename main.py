import kivy
from kivy.app import App #создание приложения
from kivy.uix.boxlayout import BoxLayout #автоматическое распределение пространства между виджетами
from kivy.uix.label import Label #текст 
from kivy.uix.textinput import TextInput #поле ввода
from kivy.uix.button import Button #кнопки
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition #слои приложения, экраны, переход между экранами(замена)

from kivy.core.clipboard import Clipboard #копирование текста
from kivy.properties import ObjectProperty, StringProperty #связывание свойств объекта

from kivy.config import Config #дизайн
Config.set('kivy', 'keyboard_mode', 'systemanddock')

# Определение русского алфавита
RUSSIAN_ALPHABET = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
# Определение английского алфавита
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def shifrovanie(text, key, alphabet):
    mytext = ''
    key_length = len(key)

    text = text.upper()  # Приводим текст к заглавным буквам
    key = key.upper()    # Приводим ключ к заглавным буквам

    j = 0

    for symb in text:
        if symb in alphabet:
            text_index = alphabet.index(symb)
            key_index = alphabet.index(key[j % key_length]) #цикличное использование ключа
            encrypted_index = (text_index + key_index) % len(alphabet)
            mytext += alphabet[encrypted_index]
        else:
            mytext += symb  # Если символ не в алфавите, добавляем его как есть
        j += 1
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
        else:
            mytext += symb
        j += 1
    return mytext.lower()


class Container(BoxLayout):
    pass


class LanguageSelectionScreen(Screen):
    pass


class CipherScreen(Screen):
    result_txt = StringProperty('Результат будет здесь')
    txt_to_copy = StringProperty('')

    def __init__(self, alphabet, **kwargs):
        super().__init__(**kwargs)
        self.alphabet = alphabet

    def encrypt(self):
        text = self.ids.txt_inpt.text
        key = self.ids.key_inpt.text
        if text and key:
            self.txt_to_copy = shifrovanie(text, key, self.alphabet)
            self.result_txt = f'Зашифрованный текст: {self.txt_to_copy}'
        else:
            self.result_txt = 'Пожалуйста, введите текст и ключ.'

    def decrypt(self):
        text = self.ids.txt_inpt.text
        key = self.ids.key_inpt.text
        if text and key:
            self.txt_to_copy = deshifrovanie(text, key, self.alphabet)
            self.result_txt = f'Расшифрованный текст: {self.txt_to_copy}'
        else:
            self.result_txt = 'Пожалуйста, введите текст и ключ.'


class CipherApp(App):
    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(LanguageSelectionScreen(name='language'))
        sm.add_widget(CipherScreen(RUSSIAN_ALPHABET, name='russian'))
        sm.add_widget(CipherScreen(ENGLISH_ALPHABET, name='english'))

        def post_build_init(ev):
            from kivy.base import EventLoop #непрерывное исполнение приложения
            EventLoop.window.bind(on_keyboard=hook_keyboard)

        def hook_keyboard(window, key, *largs):
            if key == 27:
                if sm.current == 'language':
                    App.get_running_app().stop()
                sm.current = 'language'
                return True

        self.bind(on_start=post_build_init)

        return sm


if __name__ == '__main__':
    CipherApp().run()
