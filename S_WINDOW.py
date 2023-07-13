import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

def S_WINDOW():
    # Crear la tercer ventana
    S = tk.Tk()
    S.title("Tercera ventana")
    #%% Crear las etiquetas y los campos de entrada para los valores
    label1 = tk.Label(S, text="Ingrese el valor TVD: ")
    label1.pack()
    entry1 = tk.Entry(S)
    entry1.pack()

    label2 = tk.Label(S, text="Ingrese el valor KOP: ")
    label2.pack()
    entry2 = tk.Entry(S)
    entry2.pack()
    
    label3 = tk.Label(S, text="Ingrese el valor BUR: ")
    label3.pack()
    entry3 = tk.Entry(S)
    entry3.pack()
    
    label4 = tk.Label(S, text="Ingrese el valor DOR: ")
    label4.pack()
    entry4 = tk.Entry(S)
    entry4.pack()
    
    label5 = tk.Label(S, text="Ingrese el valor AZIMUTH: ")
    label5.pack()
    entry5 = tk.Entry(S)
    entry5.pack()
    
    label6 = tk.Label(S, text="Ingrese el valor HD: ")
    label6.pack()
    entry6 = tk.Entry(S)
    entry6.pack()
    
    
    label7 = tk.Label(S, text="Ingrese el valor L: ")
    label7.pack()
    entry7 = tk.Entry(S)
    entry7.pack()
    #%%
    def save_values():
        # Función para guardar los valores ingresados en variables de tipo float
        TVD = float(entry1.get())
        KOP = float(entry2.get())
        BUR = float(entry3.get())
        DOR = float(entry4.get())
        AZI  = float(entry5.get())
        HD   = float(entry6.get())
        L   = float(entry7.get())
        return TVD , KOP , BUR , DOR , AZI, HD , L
    
    def PozoS():
        TVD , KOP , BUR , DOR , AZI , HD , L = save_values()  
        #OBTENCION DE RADIOS
        R1=(180*L)/(np.pi*BUR)
        R2=(180*L)/(np.pi*DOR)
        #VARIABLES EXTRAS
        RADIANES=(180/np.pi)
        SEXA=(np.pi/180)
        #CALCULOS TRIGONOMETRICOS
        FO = TVD-KOP
        GE = R1+R2
        FE = GE-HD
        EO = (FE**2+FO**2)**0.5
        OG = (EO**2-GE**2)**0.5

        if GE < HD:
            FE= HD-GE;
        else:
            FE= GE-HD;
            
        GAM=np.arcsin (GE/EO)*RADIANES;
        FI= np.arcsin (FE/EO)*RADIANES;

        if GE < HD:
            TET=GAM+FI;
        else:
            TET=GAM-FI;
            
        TETRAD=TET*SEXA
        #%%CALCULO DATOS DE TABLA
        EOB_TVD = KOP + R1 * np.sin(TETRAD);
        EOB_HD  = R1 * (1 - np.cos(TETRAD));
        EOB_MD  = KOP + (TET*L/BUR);
        #SECCION TANGENCIAL
        SOD_TVD = EOB_TVD + OG * np.cos(TETRAD);
        SOD_HD  = EOB_HD + OG * np.sin(TETRAD);
        SOD_MD  = EOB_MD + OG;
        #SECCION DE CONSTRUCCION 2
        EOD_TVD = SOD_TVD + R2 * np.sin(TETRAD);
        EOD_HD  = SOD_HD + R2 * (1-np.cos(TETRAD));
        EOD_MD  = SOD_MD + (TET*L/DOR);


        #%% CALCULO DE NUM DE TUBOS EN CADA SECCION 
        #np. ceil realiza redondeo hacia arriba
        # NT# = NUMERO DE TUBOS POR SECCION
        # NTT= NUMERO TOTAL DE TUBOS
        #%% SECCION VERTICAL
        NT1 = KOP/L; 
        NTT1 = int( np.ceil(NT1));
        # PRIMERA SECCION DE CONSTRUCCION
        NT2 = (EOB_MD- KOP)/L;
        NTT2 = int( np.ceil(NT2))
        # SECCION TANGENTE
        NT3 = (OG/L); 
        NTT3 = int( np.ceil(NT3))
        # SEGUNDA SECCION DE CONSTRUCCION
        NT4 = (EOD_MD-SOD_MD)/L;
        NTT4 = int( np.ceil(NT4))
        # NUMERO DE TUBOS TOTALES EN TODA LA TRAYECTORIA
        NTT = NTT1 + NTT2 + NTT3 + NTT4;

        #%% SELECCION DE CUADRANTE

        if AZI<90 and AZI>0:
            cuadew=1.0;
            cuadns=1.0;
            BETA=AZI;
            ALF=BETA;
        elif AZI>90 and AZI<180:
            cuadew=1.0;
            cuadns=-1.0;
            BETA=AZI;
            ALF=180 - BETA;
        elif AZI>180 and AZI<270:
            cuadew=-1.0;
            cuadns=-1.0;
            BETA=AZI;
            ALF=BETA-180;
        else:
            cuadew=-1.0;
            cuadns=1.0;
            BETA=AZI;
            ALF= 360- BETA;
            
        #%% CREAMOS LOS ARREGLOS DONDE LOS GUARDAREMOS 
        MD=  np.zeros(NTT+1);
        INC= np.zeros(NTT+1);
        AZI= np.zeros(NTT+1);
        HD=  np.zeros(NTT+1);
        EW=  np.zeros(NTT+1);
        NS=  np.zeros(NTT+1);
        TVD= np.zeros(NTT+1);

        #%% CALCULO DE SECCION VERTICAL

        for i in range(1,NTT1):
            TVD[i] = L + TVD[i-1];
            MD[i]  = L + MD[i-1];
        TVD[NTT1] = KOP; MD [NTT1]= KOP;

        #%% CALCULAMOS LA SECCION DE CONSTRUCCION 

        for i in range(NTT1+1, NTT1 + NTT2):
            MD[i] = L + MD[i-1];
            INC[i]= INC[i-1]+ BUR;
            AZI[i]= BETA;
            HD[i] = R1*(1-np.cos(INC[i]*SEXA));
            EW[i] =cuadew*HD[i]*np.sin(ALF);
            NS[i] =cuadns*HD[i]*np.cos(ALF);
            TVD[i]= KOP + R1* np.sin(INC[i]*SEXA);

        MD [NTT1+NTT2] = EOB_MD;
        INC[NTT1+NTT2] = TET
        AZI[NTT1+NTT2] = BETA;
        HD [NTT1+NTT2] = EOB_HD;
        EW [NTT1+NTT2] = cuadew*HD[NTT1+NTT2]*np.sin(ALF);
        NS [NTT1+NTT2] = cuadns*HD[NTT1+NTT2]*np.cos(ALF);
        TVD[NTT1+NTT2] = EOB_TVD;

        #%% CALCULAMOS LA SECCION TANGENTE

        for i in range(NTT1+NTT2+1,NTT1+NTT2+NTT3):
            MD[i] = L + MD[i-1];
            INC[i]= TET;
            AZI[i]= BETA;
            HD[i] = L*(np.sin(TET*SEXA))+HD[i-1];
            EW[i] = cuadew*HD[i]*np.sin(ALF);
            NS[i] = cuadns*HD[i]*np.cos(ALF);
            TVD[i]= L*np.cos(TET*SEXA)+TVD[i-1];
            
        MD [NTT1+NTT2+NTT3] = SOD_MD;
        TVD[NTT1+NTT2+NTT3] = SOD_TVD;
        HD [NTT1+NTT2+NTT3] = SOD_HD;
        AZI[NTT1+NTT2+NTT3] = BETA;
        EW [NTT1+NTT2+NTT3] = cuadew*HD[NTT1+NTT2+NTT3]*np.sin(ALF);
        NS [NTT1+NTT2+NTT3] = cuadns*HD[NTT1+NTT2+NTT3]*np.cos(ALF);
        INC[NTT1+NTT2+NTT3] = TET

        #%% TIRAR ANGULO

        for i in range(NTT1+NTT2+NTT3+1, NTT):
            MD[i]  = L + MD[i-1];
            INC[i] = INC[i-1]- DOR;
            AZI[i] = BETA;
            HD[i]  = R2*(np.cos(INC[i]*SEXA)-np.cos(INC[i-1]*SEXA))+HD[i-1];
            EW[i]  = cuadew*HD[i]*np.sin(ALF);
            NS[i]  = cuadns*HD[i]*np.cos(ALF);
            TVD[i] = R2*(np.sin(INC[i-1]*SEXA)-np.sin(INC[i]*SEXA))+TVD[i-1];

        MD[NTT]  = EOD_MD;
        TVD[NTT] = EOD_TVD;
        HD[NTT]  = EOD_HD;
        AZI[NTT] = BETA;
        EW[NTT]  = cuadew*HD[NTT]*np.sin(ALF);
        NS[NTT]  = cuadns*HD[NTT]*np.cos(ALF);
        INC[NTT] = 0;
        #%%% GRAFICA

        mpl.rcParams['legend.fontsize']=10
        fig=plt.figure(0)
        ax = fig.add_subplot(projection='3d')
        ax.plot(EW,NS,TVD,'k',label='Pozo S',linewidth=5)
        plt.gca().invert_zaxis()
        ax.legend()
        plt.show()
    
    # Crear el botón para guardar los valores y cerrar la ventana
    button_save = tk.Button(S, text="Guardar", command=save_values)
    button_save.pack(pady=10)
    button_show = tk.Button(S, text="Mostrar valores", command=PozoS)
    button_show.pack(pady=10)
    #%% Ejecutar la tercera ventana
    S.mainloop()
