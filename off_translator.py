from translate import Translator

s = input("entre the sentence you want to translate: ")
m = ["hi","ja","es","zh"]
while True:
    t = input("entre the code in which language you want to translate:\n1.Hindi-hi\n2.Japanese-ja\n3.spanish-es\n4.Chinese-zh\n")
    if t in m:
        translator= Translator(to_lang=t)
        break
    else:
        n = input("You putted the wrong code\nChoose 1 to put the code again\nPut anything to get it translated randomly\n")
        if n=="1":
            continue
        else:
            translator = Translator(to_lang="hi")
            break


while True:

    try:
        with open("my_f.txt",mode="r") as my_file:
            text = my_file.read()
            if text == s:
                translation = translator.translate(text)
                print(translation)
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        with open("my_f.txt", mode="w") as my_file:
            if text:
                my_file.truncate(0)
                my_file.write(s)
            else:
                my_file.write(s)
    else:
        break

