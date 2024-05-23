from google.cloud import firestore
from firebase_admin import credentials
from firebase_admin import firestore

class Connection:
    
    def __init__(self) -> None:
        self.db = firestore.Client()
    

    def fire_store(self,key):
        
        self.db.collection(key).add()
        
    def select_fire_store(self, name_collection,obje_name,fich_name,name):
        db = self.db
        collection_name = name_collection
        docs = db.collection(collection_name).stream()
        for doc in docs:
            data = doc.to_dict()  
            employee_details = data.get(obje_name, {})  
            employee_name = employee_details.get(fich_name+"Name") 
            if employee_name == name:
                data = {
                    'Nombre':name,
                    'total_venta':data['TotalSales'],
                    'fecha_inicio_periodo':data['StartDate'],
                    'fecha_fin_periodo':data['EndDate']
                }
                print(f"Documento ID: {doc.id}")  
                print(f"Datos: {data}")  
                print(f"Nombre del Empleado: {employee_name}") 
                return data
    

        
        
        
        
if __name__ == "__main__":
    co = Connection()
    co.select_fire_store('keyStore_sales','Stores','Store','CENTRO')
