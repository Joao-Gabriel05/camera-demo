import camera
import os
from pathlib import Path
from rich.console import Console
import typer
import cv2 as cv
import numpy as np
import math

app = typer.Typer(no_args_is_help=True)
console = Console()
def criar_indices(min_i, max_i, min_j, max_j):
    import itertools
    L = list(itertools.product(range(min_i, max_i), range(min_j, max_j)))
    idx_i = np.array([e[0] for e in L])
    idx_j = np.array([e[1] for e in L])
    idx = np.vstack( (idx_i, idx_j) )
    return idx
@app.command('info')
def print_info(custom_message : str = ""):
    """
    Print information about the module
    """
    console.print("Hello! I am camera")
    console.print(f"Author: { camera.__author__}")
    console.print(f"Version: { camera.__version__}")
    if custom_message != "":
        console.print(f"Custom message: {custom_message}")

@app.command() # Defines a default action
def run():
    """
    Probably run the main function of the module
    """
    cap = cv.VideoCapture(0)

    width = 320
    height = 240
    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    theta = 0
    aumento = 0
    expansao=1
    while True:
        tecla = cv.waitKey(10)
        if tecla == ord('w'):
            aumento += 0.1
        if tecla == ord('s'):
            aumento -= 0.075
        if tecla == ord('e'):
            aumento_expansao = 0.05
            expansao += aumento_expansao
        if tecla == ord('d'):
            diminuicao_expansao = 0.05
            expansao -= diminuicao_expansao
        if tecla == ord('r'):
            theta = 0
            aumento = 0
            expansao = 1

        theta += aumento

        ret, frame = cap.read()
        if not ret:
            print("Não consegui capturar frame!")
            break

        frame = cv.resize(frame, (width,height), interpolation =cv.INTER_AREA)
        image = np.array(frame).astype(float)/255
        image_ = np.zeros_like(image)
        Xd = criar_indices(0, height, 0, width)
        Xd = np.vstack ( (Xd, np.ones( Xd.shape[1]) ) )

        T = np.array([[1, 0, -(height//2)], 
                    [0, 1, -(width//2)], 
                    [0, 0,1]])
        R = np.array([[np.cos(theta), -np.sin(theta), 0], 
                      [np.sin(theta), np.cos(theta), 0],
                        [0, 0, 1]])
        E = np.array([[expansao, 0, 0], 
                      [0, expansao, 0], 
                      [0, 0, 1]])
        T_inv = np.linalg.inv(T)
        Tr = T_inv@R@E@T
        X  = np.linalg.inv(Tr)@Xd #pegando os pixeis da origem para garantir que todos tenham orgiem 
        Xd = Xd.astype(int)
        X = X.astype(int)

        Xd[0,:] = np.clip(Xd[0,:], 0, height)
        Xd[1,:] = np.clip(Xd[1,:], 0, width)
        filtro = (X[0,:] < height) & (X[1,:] < width) & (X[0,:] >= 0) & (X[1,:] >= 0)
        Xd = Xd[:, filtro] 
        X = X[:, filtro] 

        image_[Xd[0,:], Xd[1,:], :] = image[X[0,:], X[1,:], :]

        # Agora, mostrar a imagem na tela!
        cv.imshow('Minha Imagem!', image_)
        
        # Se aperto 'q', encerro o loop
        if tecla == ord('q'):
            break

    # Ao sair do loop, vamos devolver cuidadosamente os recursos ao sistema!
    cap.release()
    cv.destroyAllWindows()

