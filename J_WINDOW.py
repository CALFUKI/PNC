import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

def J_WINDOW():
    # Crear la segunda ventana
    J = tk.Tk()
    J.title("Segunda ventana")

    #%% Crear las etiquetas y los campos de entrada para los valores
    label1 = tk.Label(J, text="Ingrese el valor TVD: ")
    label1.pack()
    entry1 = tk.Entry(J)
    entry1.pack()

    label2 = tk.Label(J, text="Ingrese el valor KOP: ")
    label2.pack()
    entry2 = tk.Entry(J)
    entry2.pack()
    
    label3 = tk.Label(J, text="Ingrese el valor BUR: ")
    label3.pack()
    entry3 = tk.Entry(J)
    entry3.pack()
    
    label4 = tk.Label(J, text="Ingrese el valor AZIMUTH: ")
    label4.pack()
    entry4 = tk.Entry(J)
    entry4.pack()
    
    label5 = tk.Label(J, text="Ingrese el valor HD: ")
    label5.pack()
    entry5 = tk.Entry(J)
    entry5.pack()
    
    label6 = tk.Label(J, text="Ingrese el valor L: ")
    label6.pack()
    entry6 = tk.Entry(J)
    entry6.pack()
    #%% Función para guardar los valores ingresados en variables de tipo float
    def save_values():
        TVD = float(entry1.get())
        KOP = float(entry2.get())
        BUR = float(entry3.get())
        AZI = float(entry4.get())
        HD  = float(entry5.get())
        L   = float(entry6.get())
        return TVD, KOP , BUR, AZI, HD, L
    
    def PozoJ():
        TVD_val , KOP_val , BUR_val , AZI_val , HD_val , L_val = save_values()
        
#%%  CALCULOS TRIGONOMETRICOS     
        #OBTENCION DE RADIO
        R=(180*L_val)/(np.pi*BUR_val)
        #VARIABLES EXTRAS
        RADIANES=(180/np.pi)
        SEXA=(np.pi/180)
        #CALCULOS TRIGONOMETRICOS
        
        if R < HD_val:
            CD= HD_val - R;
        else:
            CD= R- HD_val;
            
        DO = TVD_val - KOP_val
        CO = (CD**2 + DO**2)**0.5
        BC = (CO**2 - R**2)**0.5
        GAM = np.arctan (CD/DO)*RADIANES;
        FI  = np.arccos (R/CO)*RADIANES;
        
        if R< HD_val:
            TET = 90 - (FI - GAM);
        else:
            TET = 90 - (FI + GAM);
        TETRAD=TET*SEXA
        #%%CALCULO DATOS DE TABLA
        EOB_TVD = KOP_val + R * np.sin(TETRAD);
        EOB_HD  = R * (1 - np.cos(TETRAD));
        EOB_MD  = KOP_val + (TET*L_val/BUR_val);
        #SECCION TANGENCIAL
        SOD_TVD = EOB_TVD + BC * np.cos(TETRAD);
        SOD_HD  = EOB_HD + BC * np.sin(TETRAD);
        SOD_MD  = EOB_MD + BC;
        
        Tabla= np.array([[' ','TVD', 'HD', 'MD'],['LOC', 0.0, 0.0, 0.0],['KOP', KOP_val,0.0, KOP_val],['EOB', EOB_TVD, EOB_HD, EOB_MD],['OBJ',SOD_TVD,SOD_HD,SOD_MD]]);
        #%% CALCULO DE NUM DE TUBOS EN CADA SECCION 
        # NT = NUMERO DE TUBOS
        # NTT= NUMERO TOTAL DE TUBOS
        # SECCION VERTICAL
        NT1= KOP_val/L_val; NTT1 = int( np.ceil(NT1));
        #SECCION DE CONSTRUCCION
        NT2= (EOB_MD - KOP_val)/L_val;NTT2= int( np.ceil(NT2))
        #SECCION TANGENTE
        NT3=BC/L_val; NTT3= int( np.ceil(NT3))
        #NUMERO DE TUBOS TOTALES EN TODA LA TRAYECTORIA
        NTT= NTT1 + NTT2+ NTT3;
        
        #%% SELECCION DE CUADRANTE
        
        if AZI_val<90 and AZI_val>0:
            cuadew=1.0;
            cuadns=1.0;
            BETA=AZI_val;
            ALF=BETA;
        elif AZI_val>90 and AZI_val<180:
            cuadew=1.0;
            cuadns=-1.0;
            BETA=AZI_val;
            ALF=180 - BETA;
        elif AZI_val>180 and AZI_val<270:
            cuadew=-1.0;
            cuadns=-1.0;
            BETA=AZI_val;
            ALF=BETA-180;
        else:
            cuadew=-1.0;
            cuadns=1.0;
            BETA=AZI_val;
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
            TVD[i]=L_val + TVD[i-1];
            MD[i]= L_val + MD[i-1];
        TVD[NTT1]=KOP_val; MD [NTT1]= KOP_val;
        
        #%% CALCULAMOS LA SECCION DE CONSTRUCCION 
        
        for i in range(NTT1+1, NTT1 + NTT2):
            MD[i] = L_val + MD[i-1];
            INC[i]= INC[i-1]+ BUR_val;
            AZI[i]= BETA;
            HD[i] = R*(1-np.cos(INC[i]*SEXA));
            EW[i] =cuadew*HD[i]*np.sin(ALF);
            NS[i] =cuadns*HD[i]*np.cos(ALF);
            TVD[i]= KOP_val + R* np.sin(INC[i]*SEXA);
        
        MD [NTT1+NTT2] = EOB_MD;
        INC[NTT1+NTT2] = TET
        AZI[NTT1+NTT2] = BETA;
        HD [NTT1+NTT2] = EOB_HD;
        EW [NTT1+NTT2] = cuadew*HD[NTT1+NTT2]*np.sin(ALF);
        NS [NTT1+NTT2] = cuadns*HD[NTT1+NTT2]*np.cos(ALF);
        TVD[NTT1+NTT2] = EOB_TVD;
        #%% CALCULAMOS LA SECCION TANGENTE
        
        for i in range(NTT1 + NTT2 +1,NTT):
            MD[i] = L_val + MD[i-1];
            INC[i]= TET;
            AZI[i]= BETA;
            HD[i] = L_val*(np.sin(TET*SEXA))+HD[i-1];
            EW[i] = cuadew*HD[i]*np.sin(ALF);
            NS[i] = cuadns*HD[i]*np.cos(ALF);
            TVD[i]= L_val*np.cos(TET*SEXA)+TVD[i-1];
            
        MD [NTT] = SOD_MD;
        TVD[NTT] = SOD_TVD;
        HD [NTT] = SOD_HD;
        AZI[NTT] = BETA;
        EW [NTT] = cuadew*HD[NTT]*np.sin(ALF);
        NS [NTT] = cuadns*HD[NTT]*np.cos(ALF);
        INC[NTT] = TET
        
        #%% Realizamos la grafica correspondiente
        
        mpl.rcParams['legend.fontsize']=10
        fig=plt.figure(0)
        ax = fig.add_subplot(projection='3d')
        ax.plot(EW,NS,TVD,'k',label='Pozo J',linewidth=5)
        plt.gca().invert_zaxis()
        ax.legend()
        plt.show()
        
    #%% Crear el botón para guardar los valores y cerrar la ventana
    button_save = tk.Button(J, text="Guardar", command=save_values)
    button_save.pack(pady=10)
    button_show = tk.Button(J, text="Mostrar valores", command=PozoJ)
    button_show.pack(pady=10)
    #%% Ejecutar la segunda ventana
    J.mainloop()

