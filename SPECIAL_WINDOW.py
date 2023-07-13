import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

def SPECIAL_WINDOW():
    SPECIAL = tk.Tk()
    #%% Crear las etiquetas y los campos de entrada para los valores
    label1 = tk.Label(SPECIAL, text="Ingrese el valor TVD: ")
    label1.pack()
    entry1 = tk.Entry(SPECIAL)
    entry1.pack()

    label2 = tk.Label(SPECIAL, text="Ingrese el valor KOP: ")
    label2.pack()
    entry2 = tk.Entry(SPECIAL)
    entry2.pack()
    
    label3 = tk.Label(SPECIAL, text="Ingrese el primer valor BUR: ")
    label3.pack()
    entry3 = tk.Entry(SPECIAL)
    entry3.pack()
    
    label4 = tk.Label(SPECIAL, text="Ingrese el segundo valor DOR: ")
    label4.pack()
    entry4 = tk.Entry(SPECIAL)
    entry4.pack()
    
    label5 = tk.Label(SPECIAL, text="Ingrese el valor AZIMUTH: ")
    label5.pack()
    entry5 = tk.Entry(SPECIAL)
    entry5.pack()
    
    label6 = tk.Label(SPECIAL, text="Ingrese el valor HD: ")
    label6.pack()
    entry6 = tk.Entry(SPECIAL)
    entry6.pack()
    
    label7 = tk.Label(SPECIAL, text="Ingrese el valor de la SECCIÓN HORIZONTAL: ")
    label7.pack()
    entry7 = tk.Entry(SPECIAL)
    entry7.pack()
    
    label8 = tk.Label(SPECIAL, text="Ingrese el valor L: ")
    label8.pack()
    entry8 = tk.Entry(SPECIAL)
    entry8.pack()
    #%%
    def save_values():
        # Función para guardar los valores ingresados en variables de tipo float
        TVD = float(entry1.get())
        KOP = float(entry2.get())
        BUR1 = float(entry3.get())
        BUR2 = float(entry4.get())
        AZI  = float(entry5.get())
        HD_EOB  = float(entry6.get())
        HD_SOD  = float(entry7.get())
        L   = float(entry8.get())
        return TVD , KOP , BUR1 , BUR2 , AZI, HD_EOB , HD_SOD , L
    
    def PozoS():
        TVD , KOP , BUR1 , BUR2 , AZI, HD_EOB , HD_SOD , L = save_values()
                
        #OBTENCION DE RADIOS
        R1=(180*L)/(np.pi*BUR1)
        R2=(180*L)/(np.pi*BUR2)
        #VARIABLES EXTRAS
        RADIANES=(180/np.pi)
        SEXA=(np.pi/180)
        #CALCULOS TRIGONOMETRICOS
        GE = TVD-R2-KOP
        EO = HD_EOB-R1
        GO = (GE**2+EO**2)**0.5
        FO = R1-R2
        
        GAM = np.arctan (GE/EO)*RADIANES;
        FI  = np.arccos (FO/GO)*RADIANES;
        TET1 = 180 - FI - GAM
        TET2 = 90 - TET1
        #%%CALCULO DATOS DE TABLA
        #SECCION DE CONSTRUCCION 1
        EOB_TVD = KOP + R1 * np.sin(TET1*SEXA);
        EOB_HD  = R1 * (1 - np.cos(TET1*SEXA));
        EOB_MD  = KOP + (TET1*L/BUR1);
        #SECCION TANGENCIAL
        SOD_TVD = EOB_TVD + GO * np.cos(TET1*SEXA);
        SOD_HD  = EOB_HD + GO * np.sin(TET1*SEXA);
        SOD_MD  = EOB_MD + GO;
        #SECCION DE CONSTRUCCION 2
        
        EOD_TVD = R2*(1-np.cos(TET2*SEXA)) + SOD_TVD
        EOD_HD  = R2 * np.sin(TET2*SEXA) + SOD_HD
        EOD_MD  = SOD_MD + (TET2*L/BUR2)
        #SECCION HORIZONTAL
        OBJ_TVD = EOD_TVD
        OBJ_HD  = EOD_HD + HD_SOD
        OBJ_MD  = EOD_MD + HD_SOD
        
        #%% CALCULO DE NUM DE TUBOS EN CADA SECCION 
        #np. ceil realiza redondeo hacia arriba
        # NT# = NUMERO DE TUBOS POR SECCION
        # NTT= NUMERO TOTAL DE TUBOS
        # SECCION VERTICAL
        NT1 = KOP/L; 
        NTT1 = int( np.ceil(NT1));
        # PRIMERA SECCION DE CONSTRUCCION
        NT2 = (EOB_MD- KOP)/L;
        NTT2 = int( np.ceil(NT2))
        # SECCION TANGENTE
        NT3 = (GO/L); 
        NTT3 = int( np.ceil(NT3))
        # SEGUNDA SECCION DE CONSTRUCCION
        NT4 = (EOD_MD-SOD_MD)/L;
        NTT4 = int( np.ceil(NT4))
        #SECCION HORIZONTAL
        NT5 = HD_SOD / L
        NTT5 = int( np.ceil(NT5))
        # NUMERO DE TUBOS TOTALES EN TODA LA TRAYECTORIA
        NTT = NTT1 + NTT2 + NTT3 + NTT4 + NTT5;
        
        #%% SELECCION DE CUADRANTE
        AZI= 45
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
            TVD[i]=L + TVD[i-1];
            MD[i]= L + MD[i-1];
        TVD[NTT1]=KOP; MD [NTT1]= KOP;
        
        #%% CALCULAMOS LA SECCION DE CONSTRUCCION 
        
        for i in range(NTT1+1, NTT1 + NTT2):
            MD[i] = L + MD[i-1];
            INC[i]= INC[i-1]+ BUR1;
            AZI[i]= BETA;
            HD[i] = R1*(1-np.cos(INC[i]*SEXA));
            EW[i] =cuadew*HD[i]*np.sin(ALF);
            NS[i] =cuadns*HD[i]*np.cos(ALF);
            TVD[i]= KOP + R1* np.sin(INC[i]*SEXA);
        
        MD [NTT1+NTT2] = EOB_MD;
        INC[NTT1+NTT2] = TET1
        AZI[NTT1+NTT2] = BETA;
        HD [NTT1+NTT2] = EOB_HD;
        EW [NTT1+NTT2] = cuadew*HD[NTT1+NTT2]*np.sin(ALF);
        NS [NTT1+NTT2] = cuadns*HD[NTT1+NTT2]*np.cos(ALF);
        TVD[NTT1+NTT2] = EOB_TVD;
        #%% CALCULAMOS LA SECCION TANGENTE
        
        for i in range(NTT1 + NTT2 +1,NTT1+NTT2+NTT3):
            MD[i] = L + MD[i-1];
            INC[i]= TET1;
            AZI[i]= BETA;
            HD[i] = L*(np.sin(TET1*SEXA))+HD[i-1];
            EW[i] = cuadew*HD[i]*np.sin(ALF);
            NS[i] = cuadns*HD[i]*np.cos(ALF);
            TVD[i]= L*np.cos(TET1*SEXA)+TVD[i-1];
         
        MD [NTT1+NTT2+NTT3] = SOD_MD;
        TVD[NTT1+NTT2+NTT3] = SOD_TVD;
        HD [NTT1+NTT2+NTT3] = SOD_HD;
        AZI[NTT1+NTT2+NTT3] = BETA;
        EW [NTT1+NTT2+NTT3] = cuadew*HD[NTT1+NTT2+NTT3]*np.sin(ALF);
        NS [NTT1+NTT2+NTT3] = cuadns*HD[NTT1+NTT2+NTT3]*np.cos(ALF);
        INC[NTT1+NTT2+NTT3] = TET1
        
        #%% SEGUNDO INCREMENTO
        
        for i in range(NTT1+NTT2+NTT3+1, NTT-NTT5):
            MD[i]  = L + MD[i-1];
            INC[i] = INC[i-1] + BUR2;
            AZI[i] = BETA;
            HD[i]  = HD[i-1] + (L * np.sin(TET2*SEXA));
            EW[i]  = cuadew*HD[i]*np.sin(ALF);
            NS[i]  = cuadns*HD[i]*np.cos(ALF);
            TVD[i] = TVD[i-1] + (L * (1 - np.cos(TET2*SEXA)));
        
        MD [NTT1+NTT2+NTT3+NTT4] = EOD_MD;
        TVD[NTT1+NTT2+NTT3+NTT4] = EOD_TVD;
        HD [NTT1+NTT2+NTT3+NTT4] = EOD_HD;
        AZI[NTT1+NTT2+NTT3+NTT4] = BETA;
        EW [NTT1+NTT2+NTT3+NTT4] = cuadew*HD[NTT1+NTT2+NTT3+NTT4]*np.sin(ALF);
        NS [NTT1+NTT2+NTT3+NTT4] = cuadns*HD[NTT1+NTT2+NTT3+NTT4]*np.cos(ALF);
        INC[NTT1+NTT2+NTT3+NTT4] = 90
        
        #%%SECCION HORIZONTAL
        
        for i in range (NTT1+NTT2+NTT3+NTT4+1, NTT):
            MD[i]  = L + MD[i-1];
            INC[i] = INC[i-1];
            AZI[i] = BETA;
            HD[i]  = HD[i-1] + L;
            EW[i]  = cuadew*HD[i]*np.sin(ALF);
            NS[i]  = cuadns*HD[i]*np.cos(ALF);
            TVD[i] = TVD[i-1];
            
        MD[NTT]  = OBJ_MD;
        TVD[NTT] = OBJ_TVD;
        HD[NTT]  = OBJ_HD;
        AZI[NTT] = BETA;
        EW[NTT]  = cuadew*HD[NTT]*np.sin(ALF);
        NS[NTT]  = cuadns*HD[NTT]*np.cos(ALF);
        INC[NTT] = 90;
        #%%% GRAFICA
        
        mpl.rcParams['legend.fontsize']=10
        fig=plt.figure(0)
        ax = fig.add_subplot(projection='3d')
        ax.plot(EW,NS,TVD,'k',label='Pozo DOBLE',linewidth=5)
        plt.gca().invert_zaxis()
        ax.legend()
        plt.show()
    
    # Crear el botón para guardar los valores y cerrar la ventana
    button_save = tk.Button(SPECIAL, text="Guardar", command=save_values)
    button_save.pack(pady=10)
    button_show = tk.Button(SPECIAL, text="Mostrar valores", command=SPECIAL_WINDOW)
    button_show.pack(pady=10)
    SPECIAL.mainloop()