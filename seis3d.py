import numpy as np
import segysak as sg
import pathlib
import matplotlib.pyplot as plt
from segysak.segy import get_segy_texthead, segy_loader, well_known_byte_locs
from scipy.signal import hilbert
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkinter.ttk import Combobox
import xarray as xr 

cubo = None
cubo_atr = None

def read_sismica(cubo_path):
    global cubo  
    cubo_path = pathlib.Path(cubo_path)
    print('3D Seismic Data-', cubo_path, cubo_path.exists())
    print(get_segy_texthead(cubo_path))
    cubo = segy_loader(cubo_path, iline=5, xline=21, cdpx=73, cdpy=77, vert_domain='DEPTH')
    segy_file = cubo_path
    print('Las dimensiones del cubo son: ', np.shape(cubo.data))
    return cubo

def plot_section(cubo, xspa, yspa, i_inicio, i_fin, x_inicio, x_fin, cmap1, folder):

    lenx = x_fin - x_inicio
    leni = i_fin - i_inicio

    y_lines = []
    x_lines = []

    numberi = leni // yspa
    numberx = lenx // xspa
    
    for i in range(numberi):
        iline_sel = 2113 + (yspa * i)
        y_lines.append(iline_sel)
        
    for i in range(numberx):
        xline_sel = 1 + (xspa * i)
        x_lines.append(xline_sel)

    def create_and_save_profiles(lines, direction):
        for i, line in enumerate(lines):
            fig, ax = plt.subplots(ncols=1, figsize=(15, 8), dpi=300)
            cubo.data.transpose('depth', 'iline', 'xline', transpose_coords=True).sel(**{direction: line}, method='nearest').plot(yincrease=False, cmap=cmap1)
            plt.grid('grey')
            plt.ylabel('DEPTH')
            plt.xlabel('XLINE' if direction == 'iline' else 'ILINE')
            plt.savefig(f'{folder}/{direction}{line}.png', bbox_inches='tight')
            plt.close()

    create_and_save_profiles(y_lines, 'iline')
    create_and_save_profiles(x_lines, 'xline')

    print('Perfiles salvados exitosamente\n'
          'En dirección NW-SE hay {} secciones\n'
          'En dirección NE-SW hay {} secciones'.format(len(y_lines), len(x_lines)))

    return [x_lines, y_lines]

def plot_atr(cubo_atr, atributo, xspa, yspa, i_inicio, i_fin, x_inicio, x_fin, cmap2, folder):

    lenx = x_fin - x_inicio
    leni = i_fin - i_inicio

    y_lines = []
    x_lines = []

    numberi = leni // yspa
    numberx = lenx // xspa
    
    for i in range(numberi):
        iline_sel = 2113 + (yspa * i)
        y_lines.append(iline_sel)
        
    for i in range(numberx):
        xline_sel = 1 + (xspa * i)
        x_lines.append(xline_sel)

    def create_and_save_profiles(lines, direction):
        for i, line in enumerate(lines):
            fig, ax = plt.subplots(ncols=1, figsize=(15, 8), dpi=300)
            cubo_atr.transpose('depth', 'iline', 'xline', transpose_coords=True).sel(**{direction: line}, method='nearest').plot(yincrease=False, cmap=cmap2)
            plt.grid('grey')
            plt.ylabel('DEPTH')
            plt.xlabel('XLINE' if direction == 'iline' else 'ILINE')
            plt.savefig('{}/{}{}{}.png'.format(folder, direction, line, atributo), bbox_inches='tight')
            plt.close()

    create_and_save_profiles(y_lines, 'iline')
    create_and_save_profiles(x_lines, 'xline')

    print('Perfiles salvados exitosamente\n'
          'En dirección NW-SE hay {} secciones\n'
          'En dirección NE-SW hay {} secciones'.format(len(y_lines), len(x_lines)))

    return [x_lines, y_lines]   

def atributos(cubo, atributo):
    global cubo_atr
    if atributo == 'RMS':
        cubo_atr = np.sqrt(cubo.data**2)
    elif atributo == 'AI':  # Amplitud Instantánea
        analytic_signal = hilbert(cubo.data)
        cubo_atr = np.abs(analytic_signal)
    elif atributo == 'FI':  # Frecuencia Instantánea
        analytic_signal = hilbert(cubo.data)
        instantaneous_phase = np.unwrap(np.angle(analytic_signal))
        cubo_atr = np.diff(instantaneous_phase) / (2.0*np.pi) 
    elif atributo == 'PI':  # Fase Instantánea
        analytic_signal = hilbert(cubo.data)
        cubo_atr = np.unwrap(np.angle(analytic_signal))
    else:
        print("Atributo no reconocido")
        return None

    # Convertir el resultado a xarray.DataArray
    cubo_atr = xr.DataArray(cubo_atr, coords=cubo.coords, dims=cubo.dims)
    print('Cálculo exitoso')
    print(type(cubo_atr))
    print(type(cubo.data))
    return cubo_atr



def main_window():
    window = tk.Tk()
    window.title("SIS3D")

    # Crear los widgets
    tk.Label(window, text="Cubo sísmico: ").grid(row=0, column=0)
    cubo_entry = tk.Entry(window)
    cubo_entry.grid(row=0, column=1)
    tk.Button(window, text="Buscar", command=lambda: cubo_entry.insert(0, filedialog.askopenfilename())).grid(row=0, column=2)
    tk.Button(window, text="Cargar", command=lambda: read_sismica(cubo_entry.get())).grid(row=0, column=3)

    # Espaciamiento en X
    tk.Label(window, text="Espaciamiento en X").grid(row=1, column=0)
    xspa_entry = tk.Entry(window)
    xspa_entry.grid(row=1, column=1)

    # Espaciamiento en Y
    tk.Label(window, text="Espaciamiento en Y").grid(row=2, column=0)
    yspa_entry = tk.Entry(window)
    yspa_entry.grid(row=2, column=1)

    # Primera iline
    tk.Label(window, text="Primera iline: ").grid(row=3, column=0)
    i_inicio_entry = tk.Entry(window)
    i_inicio_entry.grid(row=3, column=1)

    # Última iline
    tk.Label(window, text="Última iline: ").grid(row=4, column=0)
    i_fin_entry = tk.Entry(window)
    i_fin_entry.grid(row=4, column=1)

    # Primera xline
    tk.Label(window, text="Primera xline: ").grid(row=5, column=0)
    x_inicio_entry = tk.Entry(window)
    x_inicio_entry.grid(row=5, column=1)

    # Última xline
    tk.Label(window, text="Última xline: ").grid(row=6, column=0)
    x_fin_entry = tk.Entry(window)
    x_fin_entry.grid(row=6, column=1)

    # Carpeta destino
    tk.Label(window, text="Carpeta destino: ").grid(row=7, column=0)
    folder_entry = tk.Entry(window)
    folder_entry.grid(row=7, column=1)
    tk.Button(window, text="Buscar", command=lambda: folder_entry.insert(0, filedialog.askdirectory())).grid(row=7, column=2)

    # Diverging color maps
    colores1 = ['BrBG', 'PRGn', 'PiYG', 'PuOr', 'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
    cmap1_combo = ttk.Combobox(window, values=colores1)  
    cmap1_combo.grid(row=8, column=1)  

    # Botón para guardar perfiles
    tk.Button(window, text="Guardar perfiles", command=lambda: plot_section(cubo, int(xspa_entry.get()), int(yspa_entry.get()), int(i_inicio_entry.get()), int(i_fin_entry.get()), int(x_inicio_entry.get()), int(x_fin_entry.get()), cmap1_combo.get(), folder_entry.get())).grid(row=9, column=0)

    # Atributos
    lista_atributos = ['RMS', 'AI', 'FI', 'PI']  
    tk.Label(window, text="Atributos").grid(row=10, column=0)
    atributo_combo = ttk.Combobox(window, values=lista_atributos) 
    atributo_combo.grid(row=10, column=1)

    # Botón para calcular atributos
    tk.Button(window, text="Calcular", command=lambda: atributos(cubo, atributo_combo.get())).grid(row=11, column=0) 


    # Qualitative color maps
    colores2 = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']

    cmap2_combo = ttk.Combobox(window, values=colores2)  # Usa ttk.Combobox en lugar de Combobox
    cmap2_combo.grid(row=12, column=1)  

    # Botón para guardar perfiles con atributo
    tk.Button(window, text="Guardar perfiles con atributo", command=lambda: plot_atr(cubo_atr, atributo_combo.get(), int(xspa_entry.get()), int(yspa_entry.get()), int(i_inicio_entry.get()), int(i_fin_entry.get()), int(x_inicio_entry.get()), int(x_fin_entry.get()), cmap2_combo.get(), folder_entry.get())).grid(row=13, column=0)

    window.mainloop()

if __name__ == '__main__':
    main_window()
