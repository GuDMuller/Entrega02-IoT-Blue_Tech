import random
import cv2
import webbrowser
from numpy import *
import speech_recognition as sr 
from datetime import datetime
import playsound
import os
import time
from gtts import gTTS
from mal import *




#Inicializar o reconhecedor!
r = sr.Recognizer()
agora = datetime.now()
data = agora.strftime("%d/%m/%Y")
hora = agora.strftime("%H:%M")


def gravar_audio(rqr = False):
    with sr.Microphone() as source: #Usando o microfone como source
        if rqr:
            st_fala(rqr)
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit = 5)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio,language='pt-br')
            print(voice_data)
        except sr.UnknownValueError:
            st_fala("Não compreendi")
        except sr.RequestError:
            st_fala("Infelizmente vivemos no Brasil e o serviço caiu")
        return voice_data

def st_fala(audio_string):
    tts = gTTS(text = audio_string, lang ='pt')
    r = random.randint(1,100000000)
    arq_audio = "audio-"+ str(r) + ".mp3"
    tts.save (arq_audio)
    playsound.playsound (arq_audio)
    print(audio_string)
    os.remove(arq_audio)

def respostas(voice_data):
    if "nome" in voice_data:
        st_fala("Me chamo Strix!")

    if "data" in voice_data:
        st_fala("hoje é dia: " + data + "e o horário é:" + hora)

    if "assistir" in voice_data:
        pesquisa = gravar_audio("O que você quer assistir?")
        url = "https://youtube.com/results?search_query=" + pesquisa
        webbrowser.get().open(url)
        st_fala("Isso foi o que encontrei para " + pesquisa)

    if "anime" in voice_data:
        anime = gravar_audio("Qual anime deseja pesquisar?")
        search = AnimeSearch(anime)
        st_fala(search.results[0].title)
        url = "https://myanimelist.net/search/all?q=" + anime +"&cat=all"
        webbrowser.get().open(url)
        st_fala("A nota do anime é: " + str(search.results[0].score))

    if "pesquisar" in voice_data:
        pesquisa = gravar_audio("O que você quer pesquisar?")
        url = "https://google.com/search?q=" + pesquisa
        webbrowser.get().open(url) 
        st_fala("Isso foi o que encontrei para "+ pesquisa)

    if "sair" in voice_data:
        st_fala("Saindo...")
        camera.release()
        cv2.destroyAllWindows() 
        exit()




camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')



while 1:
    ret, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x +w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y +h, x:x + w]


        camera.release()
        cv2.destroyAllWindows() 
        st_fala("Rosto detectado! Olá, como posso ajudar?")
        time.sleep(1)
        while 1:
            voice_data = gravar_audio()
            respostas(voice_data)

    
    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break







            

