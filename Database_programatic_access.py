import sys
import mysql.connector
from mysql.connector import errorcode


def MainMenu(): #Function to control main menu
    try:
        #Database conection and cursor creation
        cnx = mysql.connector.connect(**config)
        cnx.autocommit = True 
        cursor = cnx.cursor(buffered=True)

        #Starting Menu
        selector = input("Elija una sentencia: \n"
                        "\t1. Información General Base Datos \n"
                        "\t2. Información de los fármacos\n"
                        "\t3. Información de las enfermedades \n"
                        "\t4. Información de los efectos fenotípicos\n"
                        "\t5. Información de los targets \n"
                        "\t6. Borrados\n"
                        "\t7. Inserciones \n"
                        "\t8. Modificaciones\n")

        #Database General information selectors
        if selector == "1" :
            opcion = input ("\nElija Opción : \n"
                "a. Nº Total \n"
                "b. Primeras 10 Instancias\n"
                "c. Menu Principal\n")
            if opcion == "a" : #Total number of entries
                table = input ("\nElige Tabla: \n"
                "\t1.Drugs\n"
                "\t2.Diseases \n"
                "\t3.Phenotype effects\n"
                "\t4.Targets\n")
                if table == "1" : 
                    query = "select count(drug_id) from drug"
                elif table == "2" :
                    query = "select count(disease_id) from disease"
                elif table == "3" :
                    query = "select count(phenotype_id) from phenotype_effect"
                elif table == "4" :
                    query = "select count(target_id) from target"
                
                data = cursor.execute(query)
                row = cursor.fetchall()
                print(row)
            
            elif opcion == "b": #110 first instances
                table = input ("\nElige Tabla: \n"
                    "\t1.Drugs\n"
                    "\t2.Diseases \n"
                    "\t3.Phenotype effects\n"
                    "\t4.Targets\n")
                if table == "1" : #Drugs
                    query = ("select drug_id, drug_name, molecular_type, chemical_structure, inchi_key from drug "
                    "where drug_id is not null and drug_name is not null and molecular_type is not null and "
                    "chemical_structure is not null and inchi_key is not null")        
                elif table == "2" : #Diseases
                    query = ("select disease_id, disease_name from disease where disease_id is not null and "
                    "disease_name is not null")
                elif table == "3" : #PheEffect
                    query = ("select phenotype_id, phenotype_name from phenotype_effect where phenotype_id is not null "
                    "and phenotype_name is not null")
                elif table == "4" : #Targets
                    query = ("select target_id, target_name_pref, target_type, target_organism from target where "
                    " target_id is not null and target_name_pref is not null and target_type is not null and "
                    " target_organism is not null")
                
                data = cursor.execute(query)
                rows = cursor.fetchmany(size = 10)
                for row in rows: 
                    print(row)

            elif opcion == "c" :
                MainMenu()
    
        #Opciones for drug info
        elif selector == "2" :
            opcion = input ("\nElija Opción : \n"
                "a. Información de un fármaco\n"
                "b. Sinonimos de un fármaco\n"
                "c. Código ATC de un fármaco\n"
                "d. Menu Principal\n")
            if opcion == "a" : #IDrug info
                identif = input("Escriba el identificador ChEMBL de un fármaco: ")
                query = "select drug_name, molecular_type, chemical_structure, inchi_key from drug where drug_id=%s"  
                
                data = cursor.execute(query,(identif,))
                row = cursor.fetchall()
                print(row)


            elif opcion == "b" : #Drug Synonyms
                nombrefarm = input("Escriba el nombre de un fármaco: ")
                query = ("select synonymous.synonymous_name from synonymous, drug where drug.drug_name=%s and "
                "drug.drug_id=synonymous.drug_id")

                data = cursor.execute(query,(nombrefarm,))
                row = cursor.fetchall()
                print(row)


            elif opcion == "c" : #ATC code of drug
                identifatc = input("Escriba el identificador ChEMBL de un fármaco: ")
                query = ("select ATC_code.ATC_code_id from ATC_code, drug where drug.drug_id=%s and "
                "drug.drug_id=ATC_code.drug_id")  

                data = cursor.execute(query,(identifatc,))
                row = cursor.fetchall()
                if not row:
                    print("No existe código ATC para este Drug ID")
                else:
                    print(row)
            
            elif opcion == "d" :
                MainMenu()

         #Disease information options
        elif selector == "3" :
            opcion = input ("\nElija Opción : \n"
                "a. Fármacos para una enfermedad\n"
                "b. Fármaco y Enfermedad con el mayor Score\n"
                "c. Menu Principal\n")

            if opcion == "a" : #Drugs related to disease
                name = input("Introduzca nombre de la enfermedad: ")
                query = ("select drug.drug_id, drug.drug_name from drug, disease, drug_disease "
                "where disease.disease_name=%s and drug.drug_id=drug_disease.drug_id "
                "and drug_disease.disease_id=disease.disease_id")

                data = cursor.execute(query,(name,))
                row = cursor.fetchall()
                for rows in row: 
                    print(rows)
            
            elif opcion == "b" : #Biggest Score
                query = ("select disease.disease_name, drug.drug_name from disease, drug, drug_disease "
                "where drug.drug_id=drug_disease.drug_id and drug_disease.disease_id=disease.disease_id "
                "order by drug_disease.inferred_score desc")

                data = cursor.execute(query)
                row = cursor.fetchone()
                print(row)
            
            elif opcion == "c":
                MainMenu()
         

         #Phenotypic effects info options
        elif selector == "4" :
            opcion = input ("\nElija Opción : \n"
                "a. Indicaciones de un fármaco\n"
                "b. Efectos secundarios de un fármaco\n"
                "c. Menu Principal\n")

            if opcion == "a" : #Drug indications 
                identif = input("Escriba el identifiacdor ChEMBL de un fármaco:")
                query = ("select phenotype_effect.phenotype_id, phenotype_effect.phenotype_name "
                "from drug, phenotype_effect, drug_phenotype_effect where drug.drug_id=%s and "
                "drug.drug_id=drug_phenotype_effect.drug_id and drug_phenotype_effect.phenotype_id=phenotype_effect.phenotype_id "
                "and drug_phenotype_effect.phenotype_type='INDICATION'")
            
                data = cursor.execute(query,(identif,))
                row = cursor.fetchall()
                for rows in row: 
                    print(rows)

            elif opcion == "b" : #Secondary effects of drug
                identif = input("Escriba el identifiacdor ChEMBL de un fármaco:")
                query = ("select phenotype_effect.phenotype_id, phenotype_effect.phenotype_name from drug, "
                "phenotype_effect, drug_phenotype_effect where drug.drug_id=%s and "
                "drug_phenotype_effect.phenotype_type='SIDE EFFECT' and drug.drug_id=drug_phenotype_effect.drug_id and "
                "drug_phenotype_effect.phenotype_id=phenotype_effect.phenotype_id order by drug_phenotype_effect.score desc")

                data = cursor.execute(query,(identif,))
                row = cursor.fetchall()
                for rows in row: 
                    print(rows)

            elif opcion == "c":
                MainMenu()
               
         #Target infor options
        elif selector == "5" :
            opcion = input ("\nElija Opción : \n"
                "a. Dianas de un tipo\n"
                "b. Organismo con mayor número de dianas\n"
                "c. Menu Principal\n")

            if opcion == "a" : #Number of targets of a same type
                tipo = input("Introduzca el tipo de diana: ")
                query = ("select target_name_pref from target where target_type=%s order by target.target_name_pref asc")

                data = cursor.execute(query,(tipo,))
                rows = cursor.fetchmany(size = 20)
                for row in rows: 
                    print(row)

            elif opcion == "b" : #Organism with most targets
                query = ("select target_organism, count(target_id) from target "
                "group by target_organism order by count(target_organism) desc")

                data = cursor.execute(query)
                row = cursor.fetchone()
                print(row)

            elif opcion == "c":
                MainMenu()

        #Removing elements
        elif selector == "6" :
            #List to select
            query = ("select drug_disease.inferred_score, drug.drug_name, disease.disease_name from drug_disease, drug, disease "
            "where drug_disease.drug_id = drug.drug_id and drug_disease.disease_id = disease.disease_id and drug_disease.inferred_score "
            "is not null order by drug_disease.inferred_score asc, drug.drug_name, disease.disease_name")
            data = cursor.execute(query)
            row = cursor.fetchmany(size = 10)

            for rows in row:
                print(rows)

            #Selection
            selector = int(input("\nSeleccione que entrada desea borrar (Del 1 al 10): "))
            d_name = row[selector-1][1]
            ds_name = row[selector-1][2]

            #Delete del elemento seleccionado
            del_query = ("delete from drug_disease where drug_disease.drug_id = (select drug_id from drug where drug_name = %s) and "
            "drug_disease.disease_id = (select disease_id from disease where disease_name = %s)")
            cursor.execute(del_query,(d_name,ds_name,))
            cnx.commit()
            

        #Adding new data
        elif selector == "7" :
            #User Inputs
            preg = input("¿De qué fuente procede la nueva enfermedad? \n"
                        "\t1. OMIM\n"
                        "\t2. MeSH\n")
            idenf = input("Escriba el id de la enfermedad que quiere insertar: ")
            nombreenf = input("Escriba el nombre de dicha enfermedad: ")
            nombrefarm = input("Escriba el nombre del fármaco asociado a esta enfermedad: ")

            
            if preg == "1" :
               resource = 75
            elif preg == "2" :
               resource = 72

            #Querys insertion 
            query1 = ("insert into disease values (%s, %s, %s)")
            data = cursor.execute(query1,(resource, idenf, nombreenf,))
                        
            query2 = ("insert into drug_disease values (%s, (select drug_id from drug where "
            "drug_name=%s), 3, NULL, NULL)")
            data = cursor.execute(query2,(idenf, nombrefarm,))

        #Scores changes
        elif selector == "8" :
            valornum = float(input ("Indique valor numérico del score: "))  
            query = ("update drug_phenotype_effect set score=0 where cast(score as decimal(7,4))<%s and phenotype_type='SIDE EFFECT'")

            data = cursor.execute(query,(valornum,))
            print(cursor.rowcount, "registros se han visto modificados")

    #Error control
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("El Usuario o la Contraseña no son validos")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)
    
    else:
        cnx.close()
        cont = input ("\n¿Quiere seguir realizando consultas?[Y/n]") #Continuar consultando bd
        if cont.lower() == "y": 
            MainMenu()
        else:
            sys.exit()


user = input("Usuario: ")
pwd =  input("Contraseña: ")


config = {
 'user': user,
 'password': pwd,
 'host': '127.0.0.1',
 'database': 'disnet_drugslayer',
 'raise_on_warnings': True,
}


MainMenu()

    

        