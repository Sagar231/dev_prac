from translate import Translator

s = input("entre the sentence you want to translate: ")
translator= Translator(to_lang="zh")

try:
    with open("/my_f.txt",mode="r") as my_file:
        text = 
