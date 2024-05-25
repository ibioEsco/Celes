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
            employee_name = employee_details.get(fich_name+'Name') 
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
    

    def select_fire_store_average_sales(self, name_collection,obje_name,fich_name,name):
        db = self.db
        collection_name = name_collection
        docs = db.collection(collection_name).stream()
        for doc in docs:
            data = doc.to_dict()  
            employee_details = data.get(obje_name, {})
            employee_name = employee_details.get(fich_name+'Name') 
            if employee_name == name:
                data = {
                    'Nombre':name,
                    'venta_promedio':data['AverageSales'],
                    'venta_totales':data['TotalSales'],
                }
                print(f"Documento ID: {doc.id}")  
                print(f"Datos: {data}")  
                print(f"Nombre del Empleado: {employee_name}") 
                return data

    def user_fire(self, username , password):
        db = self.db
        collection_name=  db.collection('user')
        query = collection_name.where('user', '==', username).where('pass', '==', password)
        results = query.stream()
        for doc in results:
            print(f'Document ID: {doc.id}')
            print(f'Data: {doc.to_dict()}')
            if doc:
                return True
        return False

        

if __name__ == "__main__":
    co = Connection()
    co.select_fire_store('keyStore_sales','Stores','Store','CENTRO')
    co.select_fire_store_average_sales('promedio_products_sales','Products','Product','VITAMINA C 1000MG 100 CAPS HEALTHY')
    co.user_fire('aa','admin')
    
