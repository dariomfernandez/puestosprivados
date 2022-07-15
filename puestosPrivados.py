import matplotlib.pyplot as plt
import pandas as pd

apilado = True

diccDeptos = pd.read_csv("diccionario_cod_depto.csv", delimiter=",", dtype={'codigo_departamento_indec': str, 'nombre_departamento_indec': str, 'id_provincia_indec': str, 'nombre_provincia_indec': str})
#print(diccDeptos)
salir = False
codigoDepto = ""
nombreDepto = ""
nombreProvincia = ""
while (salir == False):
    departamento = input("Indique el codigo de departamento o parte de su nombre: ")
    #print(diccDeptos.query("codigo_departamento_indec == @departamento or nombre_departamento_indec == @departamento"))
    buscarDepto = diccDeptos[diccDeptos["nombre_departamento_indec"].str.lower().str.contains(departamento.lower())]
    if (buscarDepto.empty):
        buscarDepto = diccDeptos[diccDeptos["codigo_departamento_indec"].str.lower().str.contains(departamento.lower())]
        if (buscarDepto.empty):
            print("La busqueda no arroja resultados")
    if (len(buscarDepto) == 1):
        # tengo el resultado, salgo del bucle
        codigoDepto = (buscarDepto['codigo_departamento_indec']).values.tolist()[0]
        nombreDepto = (buscarDepto['nombre_departamento_indec']).values.tolist()[0]
        nombreProvincia = (buscarDepto['nombre_provincia_indec']).values.tolist()[0]
        print("Nombre del departamento: ", (buscarDepto['nombre_departamento_indec']).values.tolist()[0])
        print("Codigo INDEC del departamento: ", codigoDepto)
        salir = True
    elif (len(buscarDepto) > 1):
        print("\r\nDemasiados resultados ... mostrando los primeros 5")
        resultados = buscarDepto[['codigo_departamento_indec', 'nombre_departamento_indec', 'nombre_provincia_indec']].head()
        print(resultados.to_string(index=False))
    #print(diccDeptos[diccDeptos["nombre_departamento_indec"].str.lower().str.contains(departamento.lower())])
diccClae = pd.read_csv("diccionario_clae2.csv", delimiter=",", dtype={'clae2': str, 'clae2_desc': str, 'letra': str, 'letra_desc': str})
#diccClae.to_csv("diccclae.csv", index=False)
#print(diccClae.head())
#quit()
puestosDf = pd.read_csv("puestos_privados_depto.csv", delimiter=",", dtype={'codigo_departamento_indec': str, 'id_provincia_indec': str, 'puestos':int})
puestosDf = puestosDf [(puestosDf ["codigo_departamento_indec"] == codigoDepto)]
puestosDfClae = pd.read_csv("puestos_privados_depto_por_clae2.csv", delimiter=",", dtype={'codigo_departamento_indec': str, 'id_provincia_indec': str, 'clae2': str, 'puestos':int})
puestosDfClae = puestosDfClae [(puestosDfClae ["codigo_departamento_indec"] == codigoDepto)]
puestosDfClae = pd.merge(puestosDfClae, diccClae, on = ["clae2"], how = "left")
puestosDfClaeAgricultura = (puestosDfClae [(puestosDfClae ["letra"] == "A")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeManufacturas = (puestosDfClae [(puestosDfClae ["letra"] == "C")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeConstruccion = (puestosDfClae [(puestosDfClae ["letra"] == "F")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeComercio = (puestosDfClae [(puestosDfClae ["letra"] == "G")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeTransporte = (puestosDfClae [(puestosDfClae ["letra"] == "H")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeAlojamiento = (puestosDfClae [(puestosDfClae ["letra"] == "I")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeFinanciera = (puestosDfClae [(puestosDfClae ["letra"] == "K")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeProfesionales = (puestosDfClae [(puestosDfClae ["letra"] == "M")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeEnsenanza = (puestosDfClae [(puestosDfClae ["letra"] == "P")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeSalud = (puestosDfClae [(puestosDfClae ["letra"] == "Q")]).groupby(['fecha'], as_index=False).sum()
puestosDfClaeMinas = (puestosDfClae [(puestosDfClae ["letra"] == "B")]).groupby(['fecha'], as_index=False).sum()
total = puestosDfClaeAgricultura.append(puestosDfClaeManufacturas.append(puestosDfClaeConstruccion).append(puestosDfClaeComercio).append(puestosDfClaeTransporte).append(puestosDfClaeAlojamiento).append(puestosDfClaeFinanciera).append(puestosDfClaeProfesionales).append(puestosDfClaeEnsenanza).append(puestosDfClaeSalud).append(puestosDfClaeMinas))
#total.to_csv("todos.csv")
#print(total.groupby(['fecha']).sum())
#print(total.query("fecha == '2018-01-01'"))
#quit()
#print(puestosDfClaeAgricultura)
#puestosDfClaeAgricultura.to_csv("resultados.csv")
#puestosDfClae.to_csv("resultados2.csv")
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
ax = plt.gca()
#print(puestosDfClaeAgricultura["fecha"].values.tolist())
#print(puestosDfClaeManufacturas["puestos"].values.tolist())
#quit()
if (apilado):
    maxY = int(max(puestosDf["puestos"].values.tolist()) * 1.3)
    #print("Y maximo:", maxY)
    ejeX = puestosDfClaeAgricultura["fecha"].values.tolist()
    #print(puestosDfClaeAgricultura["puestos"].values.tolist())
    #quit()
    for i in range(len(ejeX)):
        ejeX[i] = ejeX[i][5:7] + "/" + ejeX[i][0:4]
    firstPlot = puestosDf.plot(kind='line', x='fecha', y='puestos', color='darkslateblue', ax=ax, linestyle='dashed', marker='o')
    plt.stackplot(ejeX, puestosDfClaeAgricultura["puestos"].values.tolist(), puestosDfClaeManufacturas["puestos"].values.tolist(), puestosDfClaeConstruccion["puestos"].values.tolist(), puestosDfClaeComercio["puestos"].values.tolist(), puestosDfClaeTransporte["puestos"].values.tolist(), puestosDfClaeAlojamiento["puestos"].values.tolist(), puestosDfClaeFinanciera["puestos"].values.tolist(), puestosDfClaeProfesionales["puestos"].values.tolist(), puestosDfClaeEnsenanza["puestos"].values.tolist(), puestosDfClaeSalud["puestos"].values.tolist(), puestosDfClaeMinas["puestos"].values.tolist(), colors=['dimgray', 'green', 'blue', 'purple', 'red', 'orange', 'yellow', 'rosybrown', 'indigo', 'cyan', 'darkkhaki'])
    plt.legend(["Total", "Agric. y ganadería", "Ind. manufacturera", "Construcción", "Comercio", "Transporte", "Alojamiento y comida", "Financiera y seguros", "Servicios profesionales", "Educación", "Salud humana", "Petróleo y otros minerales"], loc='upper center', ncol=4)
    plt.xticks(rotation = 45, fontsize=8)
    plt.ylim(0, maxY)
    plt.margins(0)
    plt.suptitle("Trabajadores registrados del sector privado", fontsize=18)
    plt.title(nombreDepto + ", " + nombreProvincia, fontsize=14)
    ax.set_facecolor('whitesmoke')
    ax.yaxis.grid(True)
else:
    firstPlot = puestosDf.plot(kind='line', x='fecha', y='puestos', color='red', ax=ax)
    puestosDfClaeAgricultura.plot(kind='line', x='fecha', y='puestos', color='blue', ax=firstPlot)
    puestosDfClaeManufacturas.plot(kind='line', x='fecha', y='puestos', color='green', ax = firstPlot)
    puestosDfClaeConstruccion.plot(kind='line', x='fecha', y='puestos', color='black', ax = firstPlot)
    puestosDfClaeComercio.plot(kind='line', x='fecha', y='puestos', color='brown', ax = firstPlot)
    puestosDfClaeTransporte.plot(kind='line', x='fecha', y='puestos', color='orange', ax = firstPlot)
    puestosDfClaeAlojamiento.plot(kind='line', x='fecha', y='puestos', color='lime', ax = firstPlot)
    puestosDfClaeFinanciera.plot(kind='line', x='fecha', y='puestos', color='maroon', ax = firstPlot)
    puestosDfClaeProfesionales.plot(kind='line', x='fecha', y='puestos', color='blueviolet', ax = firstPlot)
    puestosDfClaeEnsenanza.plot(kind='line', x='fecha', y='puestos', color='gray', ax = firstPlot)
    puestosDfClaeSalud.plot(kind='line', x='fecha', y='puestos', color='gold', ax = firstPlot)
    puestosDfClaeMinas.plot(kind='line', x='fecha', y='puestos', color='turquoise', ax = firstPlot)
    plt.legend(["Total", "Agric. y ganadería", "Ind. manufacturera", "Construcción", "Comercio", "Transporte", "Alojamiento y comida", "Financiera y seguros", "Servicios profesionales", "Educación", "Salud humana", "Petróleo y demás minerales"])
plt.xlabel("Mes")
plt.ylabel("Trabajadores registrados privados")
plt.show()
