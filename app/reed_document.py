import pandas as pd
import pyarrow.parquet as pq
import re

class document:
    
    def consolidar_archivos_parquet(self):
        
        archivos_parquet = ['/home/ibio/Documentos/Celes/document/data_chunk000000000000.snappy.parquet',
                                '/home/ibio/Documentos/Celes/document/data_chunk000000000001.snappy.parquet',
                                '/home/ibio/Documentos/Celes/document/data_chunk000000000002.snappy.parquet',
                                '/home/ibio/Documentos/Celes/document/data_chunk000000000003.snappy.parquet']
        dfs = []
        for archivo in archivos_parquet:
            df = pq.read_table(archivo).to_pandas()
            dfs.append(df)
        df_consolidado = pd.concat(dfs, ignore_index=True)
        return df_consolidado
    
    
    def consultar_las_ventas_de_un_periodo(sel,df_consolidado,key_consulta):
        remple_key_consulta = re.sub(r'^Key', '', key_consulta+'s')        
        ventas_empleado = df_consolidado.groupby(key_consulta).agg({
            'Amount': 'sum',
            'Qty': 'sum',
            'KeyDate': ['min', 'max']     
            }).reset_index()
        ventas_empleado.columns = [key_consulta, 'TotalSales', 'TotalQuantity', 'StartDate', 'EndDate']
        df_empleados = pd.merge(ventas_empleado, df_consolidado[[key_consulta, remple_key_consulta]], on=key_consulta, how='left')
        df_empleado = df_empleados.drop_duplicates(subset=[key_consulta])
        for _, row in df_empleado.iterrows():
           doc_data = {
           key_consulta: row[key_consulta],
           "TotalSales": row["TotalSales"],
           "TotalQuantity": row["TotalQuantity"],
           "StartDate": str(row["StartDate"]),
           "EndDate": str(row["EndDate"]),
           remple_key_consulta: row[remple_key_consulta]
           }

           
    def consultar_el_promedio(self,df_consolidado):
        df_ventastienda = df_consolidado.groupby('KeyProduct')['Amount'].agg(TotalSales='sum', AverageSales='mean').reset_index()
        df_tienda = pd.merge(df_ventastienda, df_consolidado[['KeyProduct', 'Products']], on='KeyProduct', how='left')
        df_empleado = df_tienda.drop_duplicates(subset=['KeyProduct'])
        for _, row in df_empleado.iterrows():
           doc_data = {
           'KeyProduct': row['KeyProduct'],
           "TotalSales": row["TotalSales"],
           "AverageSales": row["AverageSales"],
           "Products": str(row["Products"]),
           }
				




if __name__ == "__main__":
    do = document()
    df_consolidado = do.consolidar_archivos_parquet()
    periodo_ventas = do.consultar_las_ventas_de_un_periodo(df_consolidado,'KeyStore')
    promedio = do.consultar_el_promedio(df_consolidado)
