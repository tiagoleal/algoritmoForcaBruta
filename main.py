#!/bin/bash/pytho3.4
# -*- coding:utf-8 -*-
import sys
import glob
import os.path
import modulo.cronometro
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

global cronometro


"""
    Mostra dados referente ao trabalho
"""
def sobre():
    popup = Toplevel()

    msg ="Para ser inteligente(Mágica),a soma de todas as linhas, colunas e diagonais devem dar o mesmo valor.\n"
    msg+="Exemplo:\n"
    msg+="Para uma matriz 3x3 temos um total de 9 casas. Neste caso os numeros de 1 a 9, de tal forma que \na soma dos elementos de cada linha, coluna e diagonais é sempre 15."

    nomes = Label(popup,text="Este programa gera matrizes Inteligentes", font = "Helvetica 14 bold",justify="left")
    nomes.grid(row=0, column=0, columnspan=3,sticky = NSEW)

    nomes = Label(popup,text=msg, font = "Helvetica 12",justify="left")
    nomes.grid(row=2, column=0, columnspan=3,sticky = NSEW)

    popup.transient(gui)
    popup.grab_set()
    gui.wait_window(popup)

"""
    gera arquivo de log do sistema
"""
def geraLogArq(numArq,strLog):

    nomeArquivo = str("log"+numArq+".txt")
    arquivo     = open(nomeArquivo,'w')
    strLinha    = ""

    for linha in strLog: 
        strLinha+=str(linha)
        strLinha+="\n"
    arquivo.write(strLinha)

"""
    ver arquivo de log do sistema
"""
def verLog(fileID):

    popupLog = Toplevel()
    popupLog.geometry("800x600") #dimensão

    log1 = Label(popupLog,text="Log:")
    log1.place(x=10, y=40)

    msglog1 = Text(popupLog,background='#FFFFFF', foreground="#000000", borderwidth=2, relief='sunken')
    msglog1.place(x=10, y=70, width=750, height=450)

    scrollBar = Scrollbar(msglog1)
    msglog1.configure(yscrollcommand=scrollBar.set)
    scrollBar.config(command=msglog1.yview)
    scrollBar.pack(side='right', fill='y')

    fileID = str(fileID)
    tmpArq = "log"+fileID+".txt"
    temp   = open(tmpArq)

    for linha in temp:
        msglog1.insert(INSERT,'%s' % linha)
    msglog1.update()
    temp.close()    

    popupLog.transient(gui)
    popupLog.grab_set()
    gui.wait_window(popupLog)

"""
  Reset formulario
"""
def limparTela():

    try:
        msglog.delete("1.0", END)
        input_matriz.delete(0, END)
        input_matriz.focus()
        msglog.delete("1.0", END)
        cronometro.Reset() 
        cronometro.Stop()
        msglog.delete("1.0", END)
        frame3.destroy()
    except:
        return "Fomulario já esta limpo!"

"""
  Função que realiza a permutação
"""
def permutacao(iterable, r=None):
    p = tuple(iterable)
    n = len(p)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    ciclos = list(range(n, n-r, -1))
    yield tuple(p[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            ciclos[i] -= 1
            if ciclos[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                ciclos[i] = n - i
            else:
                j = ciclos[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(p[i] for i in indices[:r])
                break
        else:
            return

"""
    validação da matriz
"""
def validaMatriz(matriz,dimensaoMatriz):

    #valor da dimensão da matriz exe #3x3 = 7
    qtdeVerificador = (dimensaoMatriz + dimensaoMatriz) + 1

    #numero de dimensoes da matriz ex: 7 + 1 = 8  linhas,colunas,diagonal pri, diagonal secund.
    numCasasVerificador = qtdeVerificador + 1

    #vetor com as somas dos valores de linnhas, colunas, diagonais
    verificador = [0] * numCasasVerificador

    vldigSec = qtdeVerificador #indice da diagonal secundaria
    vldigPri = qtdeVerificador - 1 #indice da diagonal primaria

    k = int(-1) #indice para popularmos o vetor verificador com as somas

    for i in range(0,dimensaoMatriz):

        k = k + 1

        for j in range(0,dimensaoMatriz):
            verificador[k] = verificador[k] + matriz[i][j] #percorre as linhas
            verificador[k + dimensaoMatriz] = verificador[k + dimensaoMatriz] + matriz[j][i] # percorre as colunas

    coluna = dimensaoMatriz #pega o valor maximo da matriz para calculo da diagonal secundaria

    for i in range(0,dimensaoMatriz):

        verificador[vldigPri] = verificador[vldigPri] + matriz[i][i] # percorre diagonal primaria
        verificador[vldigSec] = verificador[vldigSec] + matriz[i][(coluna - 1)] # percorre diagonal secundaria

        coluna = coluna - 1 #controla os indices para gerar a diagonal secundaria

    status = True #status para saber se a matriz e inteligente
    i      = 0 #contador da loop

    #laço para percorrer vetor de somas para validar matriz
    while((status) and (i < qtdeVerificador)):

        #se a soma de todas os elementos da matriz nao for igual nao é matriz inteligente
        if(verificador[i] != verificador[i + 1]):
            status = False # matriz não é inteligente

        i = i + 1 #incrementa indice do vetor

    if(status == True): #se status for true
        achou = 1 # retorna 1 matriz inteligente
    else:
        achou = 0 #matriz nao é matrizInteligente

    return achou

"""
   print matriz inteligente
"""
def printMatriz(matriz,dimensaoMatriz,numMatrizInteligente):

    #controla para imprimir os dados na tela
    if (numMatrizInteligente == 1 or numMatrizInteligente == 6):
        aux   = 0
        btnX  = 35
        btnY  = 60
        logId = 1

    elif (numMatrizInteligente == 2 or numMatrizInteligente == 7):
        aux   = 4
        btnX  = 168
        btnY  = 60
        logId = 2

        mostraMatriz1 = Label(frame3,text= "")
        mostraMatriz1.grid(column=3, padx=5)

    elif (numMatrizInteligente == 3 or numMatrizInteligente == 8):
        aux   = 8
        btnX  = 320
        btnY  = 60
        logId = 3

        mostraMatriz1 = Label(frame3,text= "")
        mostraMatriz1.grid(column=7, padx=5)

    elif (numMatrizInteligente == 4 or numMatrizInteligente == 9):
        aux   = 12
        btnX  = 460
        btnY  = 60
        logId = 4

        mostraMatriz1 = Label(frame3,text= "")
        mostraMatriz1.grid(column=11, padx=5)

    elif (numMatrizInteligente == 5 or numMatrizInteligente == 10):
        aux   = 16
        btnX  = 610
        btnY  = 60
        logId = 5

        mostraMatriz1 = Label(frame3,text= "")
        mostraMatriz1.grid(column=15, padx=5)

    for m in range(0,dimensaoMatriz):

        #controle para mostrar matrizes alinhadas
        if numMatrizInteligente <= 5:
            x = m
        else:
           x     = m + 10
           btnY  = btnY + 42

           #controle para abrir arquivos de log referente as matrizes
           if logId == 1: 
            logId = 6
           elif logId == 2:    
            logId = 7
           elif logId == 3:                 
            logId = 8
           elif logId == 4:                 
            logId = 9
           elif logId == 5:                 
            logId = 10 
           
        for n in range(0,dimensaoMatriz):

            val = matriz[m][n]
            y   = aux + n

            mostraMatriz = Label(frame3,text= "", relief=RIDGE, width=5)
            mostraMatriz.grid(row=x, column=y)
            mostraMatriz["text"] = val

    print("logId: %s" % logId)     

    btn_log = Button(frame3, text="Ver Log", command=lambda i=logId: verLog(i))
    btn_log.place(x=btnX, y=btnY)

"""
    gera matriz automatica
"""
def geraMatriz():

    try:

        dimensaoMatriz = int(input_matriz.get()) # pega o valor do campo input
        tipoVariavel   = type(dimensaoMatriz)
        tipoAlgoritmo  = box_value.get() #retorna o valor que foi selecionado

        if dimensaoMatriz == 0:
            messagebox.showinfo("ERRO", "Informe um numero maior > 0!")
            sys.exit(0)

        #limpa os arquivos de log do sistema
        for arq in sorted(glob.glob('*.txt')): os.remove(arq)
        
        if(tipoAlgoritmo == "Força Bruta"):

            #=====================
            #matriz inteligente
            #=====================
            matrizInteligente = Label(gui,text="Matriz Inteligente:")
            matrizInteligente.place(x=15, y=230)

            if (tipoVariavel is int):

                global frame3
                frame3 = Frame(gui)
                frame3.place(x=10, y=250, width=750, height=220)
                tam                  = (dimensaoMatriz * dimensaoMatriz) + 1 # ex: 3x3 = 9  range de 1 - 9
                listaNumeros         = [] #retorno da permutação
                numMatrizInteligente = 0; #contador com numero de matrizes inteligentes
                strLog               = [] #armazena registro de logs
                cronometro.Start() #start do cronometro

                #realiza a permutação de acordo com a range
                for listaNumeros in permutacao(reversed(range(1,tam))):

                    lin    = 0;#linha da matriz
                    col    = dimensaoMatriz; #coluna da matriz recebe o valor da dimensao da matriz informada
                    matriz = [] #matriz popula de acordo com a permutação
                        
                    strLog.append(listaNumeros);                    
                    msglog.insert(INSERT,'%s \n' % [listaNumeros]) #mostra o log
                    msglog.update() #atualiza o log na tela

                    #monta a matriz para realizarmos a validação
                    for index in range(0,dimensaoMatriz):

                        val = listaNumeros[lin:col] #separa a lista de acordo com a formatação exemplo: 3x3

                        matriz.append(val) #adicionamos a os elementos a matriz

                        lin = col #atualiza o valor da linha
                        col = col + dimensaoMatriz #atualiza o valor da coluna

                    #função que realiza a validação da matriz
                    # statusMatInteligente=1 matriz inteligente
                    # statusMatInteligente=0 nao é inteligente
                    statusMatInteligente = validaMatriz(matriz,dimensaoMatriz)

                    if statusMatInteligente == 1: # matriz é inteligente
                       numMatrizInteligente = numMatrizInteligente + 1 #contador de matriz inteligente
                       
                       numArqLog = str(numMatrizInteligente)
                       geraLogArq(numArqLog,strLog) #gera arquivo de log

                       printMatriz(matriz,dimensaoMatriz,numMatrizInteligente) #printa a matriz na tela

                       strLog = []

                       if numMatrizInteligente == 10: #se numMatrizInteligente = 10 para o relogio
                            cronometro.Stop() #para o relogio
                            cronometro.update() #atualiza os dados na tela

                       if dimensaoMatriz == 3: #caso for matriz 3x3 somente gera 8 matrizes

                           if numMatrizInteligente == 8: #se numMatrizInteligente = 8 para o relogio
                                cronometro.Stop() #para o relogio
                                cronometro.update()#atualiza os dados na tela
        
        else:    
            messagebox.showinfo("ERRO", "Selecione o Tipo de Algoritmo!")                        

    except ValueError:
       messagebox.showinfo("ERRO", "Informe somente numeros inteiros!")

#=====================
# interface
#=====================
gui = Tk()
gui.title("Este programa gera matrizes Inteligentes (mágica)")
gui.geometry("800x500") #dimensão

#=====================
#menu
#=====================
menu = Menu(gui)
gui.config(menu=menu)

#=====================
#submenu
#=====================
editMenu = Menu(menu)
menu.add_cascade(label="Menu", menu=editMenu)
editMenu.add_command(label="Sobre",command=sobre)
editMenu.add_command(label="Exit",command=gui.destroy)

#=====================
#formulario
#=====================
frame = Frame(gui)
frame.place(x=10, y=10)

label_tipo_alg = Label(frame, text="Tipo de Algoritmo:")
label_tipo_alg.place(x=10, y=10)
label_tipo_alg.grid(column=0, row=0)

box_value = StringVar()
box = ttk.Combobox(frame, textvariable=box_value)
box['values'] = ('<-- Selecione -->', 'Força Bruta', 'Genético')
box.current(0)
box.grid(column=1, row=0)

matrizQuadrada = IntVar()
label_matriz   = Label(gui, text="Matriz Quadrada:")
label_matriz.place(x=15, y=40)

input_matriz   = Entry(gui, textvariable=matrizQuadrada, width=10)
input_matriz.place(x=122, y=40)

#=====================
#log do sistema
#=====================
log = Label (gui,text="Log:")
log.place(x=15, y=70)

msglog = Text(gui,background='#FFFFFF', foreground="#000000", borderwidth=2, relief='sunken')
msglog.place(x=15, y=90, width=750, height=140)

scrollBar = Scrollbar(msglog)
msglog.configure(yscrollcommand=scrollBar.set)
scrollBar.config(command=msglog.yview)
scrollBar.pack(side='right', fill='y')

#=====================
#botao
#=====================
btn_gerar = Button(gui, text="Start", command = geraMatriz)
btn_gerar.place(x=210, y=39)

btn_reset = Button(gui, text="Reset", command = limparTela)
btn_reset.place(x=280, y=39)

#=====================
#cronometro
#=====================
cronometro      = modulo.cronometro.StopWatch(gui)
cronometroLabel = Label(gui, text="Cronômetro:").place(x=350, y=10)
cronometro.place(x=430, y=9)
cronometroMask  = Label(gui, text="(hh:mm:ss:hs)").place(x=520, y=10)

#=====================
#log do sistema
#=====================
log = Label (gui,text="Log:")
log.place(x=15, y=70)

msglog = Text(gui,background='#FFFFFF', foreground="#000000", borderwidth=2, relief='sunken')
msglog.place(x=15, y=90, width=750, height=140)

scrollBar = Scrollbar(msglog)
msglog.configure(yscrollcommand=scrollBar.set)
scrollBar.config(command=msglog.yview)
scrollBar.pack(side='right', fill='y')

gui.mainloop()