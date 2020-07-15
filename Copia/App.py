import subprocess
from Pila import Pila
import constantes
import os

simbolos          = constantes.CONSTANT_S
flecha            = constantes.CONSTANT_F
operadoresunarios = constantes.CONSTANT_U

def obtenerExpresionPostFija(expresionInfija):
    miComando = 'java App "'+expresionInfija+'"'
    tempStr = subprocess.check_output(miComando, shell=True)
    return list(tempStr.decode("utf-8").strip())

def evaluarExpresion(expresionPostFijaList):

    pila = Pila()
    
    listaFinal = []

    i = 0

    contador = 1

    for j in expresionPostFijaList:

        caracter = j

        if caracter in simbolos:

            listaDeOperandos = []
            
            operandosNecesarios = 1 if caracter in operadoresunarios  else 2

            elemento = ()

            for i in range(operandosNecesarios):

                elemento = pila.extraer()

                listaDeOperandos.append(elemento)
            
                print(listaDeOperandos)
            if operandosNecesarios == 1:
                listaDeIniciales = []
                listaDeFinales = []

                for i in listaDeOperandos:
                    inicial,final = obtenerEstadoInicialYFinal(i,caracter)
                    listaDeIniciales.append(inicial)
                    listaDeFinales.append(final)

                listaDeTuplas = obtenerInstruccionesDeOperadoresUnitarios(caracter,contador,listaDeIniciales,listaDeFinales)
                listaTemporal = unirListas(listaDeOperandos,listaDeTuplas)
                pila.incluir(listaTemporal)

            else:

                listaDeIniciales = []
                listaDeFinales = []
                
                
                for i in listaDeOperandos:
                    inicial, final = obtenerEstadoInicialYFinal(i,caracter)
                    listaDeIniciales.append(inicial)
                    listaDeFinales.append(final)

                listaDeIniciales.sort() 
                listaDeFinales.sort()


                if caracter == "|":
                    
                    listaDeTuplas = obtenerInstruccionesDeOperadoresNoUnitarios(caracter,contador,listaDeIniciales,listaDeFinales,listaDeOperandos)
                
                    contador+=2
                
                else:

                    listaDeTuplas, nodoAEliminar = obtenerInstruccionesDeOperadoresNoUnitarios(caracter,contador,listaDeIniciales,listaDeFinales,listaDeOperandos)
                    
                    for operando in listaDeOperandos:
                        for tupla in operando:
                            if nodoAEliminar in  tupla:
                                operando.remove(tupla)
                    
                    for operando in listaDeOperandos:
                        if len(operando) ==0:
                            listaDeOperandos.remove(operando)
                    
                listaTemporal =list(set(unirListas(listaDeOperandos,listaDeTuplas)))
                pila.incluir(listaTemporal)

        else:
            
            tuplaTemporal = [(str(contador), str(contador+1), caracter)]
            contador+=2
            
            pila.incluir(tuplaTemporal)


    for i in range(pila.tamano()):
        elemento = pila.extraer()
        for tupla in elemento:
            a,b = tupla[0], tupla[1]

            if int(a) != int(b):
                listaFinal.append(tupla)

    listaFinal.reverse()
    listaFinal = [listaFinal]

    return listaFinal

def unirListas(llistaUno, listaDos):
    listaF = []

    for i in llistaUno:
        for elemento in i:
            listaF.append(elemento)
    for i in listaDos:
        listaF.append(i)
    return listaF

def obtenerEstadoInicialYFinal(lista, caracter):
    inicial = 0
    final = 0

    listaAuxiliar = []

    for tupla in lista:

        for j in range(2):
            listaAuxiliar.append(int(tupla[j]))

    listaAuxiliar = sorted(set(listaAuxiliar))

    final = max(listaAuxiliar)

    listaAuxiliar.pop()

    if caracter == "*" or caracter == "+":
        inicial = max(listaAuxiliar)
    elif caracter == "|" or caracter == ".":
        inicial = min(listaAuxiliar)


    

    return inicial, final

def obtenerInstruccionesDeOperadoresNoUnitarios(operador, contador, listaDeIniciales, listaDeFinales,listaDeOperandos):

    listaDeTuplas = []

    inicial = contador
    final = contador+1

    if operador == ".":
        listaDeOperandos.reverse()
        operandoA, operandoB = listaDeOperandos[0], listaDeOperandos[1]

        inicialA, finalA = obtenerEstadoInicialYFinal(operandoA,".")
        inicialB, finalB = obtenerEstadoInicialYFinal(operandoB,".")
        nuevoNodo     = min(finalA,inicialB)
        nodoAEliminar = max(finalA, inicialB)

        for operando in listaDeOperandos:
            for tupla in operando:

                a,b,c = tupla[0], tupla[1],tupla[2]

                if str(nodoAEliminar) in tupla:

                    for i in range(len(tupla)-1):

                        a = nuevoNodo if a == str(nodoAEliminar) else a
                        b = nuevoNodo if b == str(nodoAEliminar) else b

                    listaDeTuplas.append((a,b,c))
        return listaDeTuplas, str(nodoAEliminar)

    if operador == "|":

        for i in range(2):
            
            listaDeTuplas.append((str(inicial),str(listaDeIniciales[i]),"&epsilon;"))
            
            listaDeTuplas.append((str(listaDeFinales[i]),str(final),"&epsilon;"))

        return listaDeTuplas

def obtenerInstruccionesDeOperadoresUnitarios(operador, contador,listaDeIniciales,listaDeFinales):
    listaDeTuplas = []

    inicial = contador - 2
    final = contador - 1


    if operador == "+":

        listaDeTuplas.append((str(listaDeFinales[0])       , str(listaDeIniciales[0])   ,  "&epsilon;"))
        listaDeTuplas.append((str(contador)    , str(listaDeIniciales[0])   ,  "&epsilon;"))
        listaDeTuplas.append((str(final)       , str(contador+1),  "&epsilon;"))    
    
    elif operador == "*":

        listaDeTuplas.append((str(listaDeFinales[0])       , str(listaDeIniciales[0])   ,  "&epsilon;"))
        listaDeTuplas.append((str(contador)    , str(listaDeIniciales[0])   ,  "&epsilon;"))
        listaDeTuplas.append((str(final)       , str(contador+1),  "&epsilon;"))   

        listaDeTuplas.append((str(contador)       , str(contador+1),  "&epsilon;"))   
    
    return listaDeTuplas

def obtenerEstadoInicialFinal(listaDeTuplas):
    listaTemporal = []
    for i in range(len(listaDeTuplas)):
        iTupla = listaDeTuplas[i]
        for j in range(len(iTupla)-1):
            listaTemporal.append(listaDeTuplas[i][j])

    listaTemporal = list(set(listaTemporal))

    final = max(listaTemporal)

    posicion = 0
    
    while posicion < len(listaTemporal):
        if listaTemporal[posicion] == final:
            listaTemporal.pop(posicion)

        posicion+=1

    inicial = max(listaTemporal)

    return  inicial,final

def probarApp():
    expresionInfija = input(":")
    expresionPostFijaList = obtenerExpresionPostFija(expresionInfija)
    listaDeTuplas = evaluarExpresion(expresionPostFijaList)
    obtenerArchivo(listaDeTuplas)

def obtenerArchivo(listaDeTuplas):
    str1 = "digraph AFN{"+"\n"
    str2 = "rankdir = LR;"+"\n"
    str3 = 'node[shape=circle, style="filled", fixedsize=true,width=0.2, color="#FFF7A8", fontsize=8]'+"\n"
    str4 = "edge [ fontname=Arial, fontcolor=blue, fontsize=8 ];"
    str5 = 'node [name = "1"];'+"\n"
    str6 = "}"

    lista = [str1,str2,str3,str4,str5]

    f = open("input.dot", "w")
    
    for m in lista:
        f.write(str(m))

    for elemento in listaDeTuplas:
        for tupla in elemento:
            a,b,c = str(tupla[0]),str(tupla[1]), str(tupla[2])
            nuevaStr = ''+a+' -> '+''+b+' [label = "'+c+'", color="red"]'+"\n"
            f.write(nuevaStr)
    f.write(str6)
    f.close()
    subprocess.call("dot -Tpng input.dot > output.png", shell=True)

probarApp()