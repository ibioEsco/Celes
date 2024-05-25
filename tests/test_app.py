import unittest
from fastapi.testclient import TestClient
from app.main import app, create_access_token, Connection 


class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_login_for_access_token(self):
        response = self.client.post("/token", data={"username": "ibio", "password": "secret"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertIn("token_type", response.json())

    def test_read_employee(self):
        token = create_access_token(data={"sub": "testuser"})
        headers = {"Authorization": f"Bearer {token}"}
        print(headers)
        do = "NAVARRO APARICIO ENILCE ESTHER"
        response = self.client.post(f"/sales/by_employee/{do}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre", response.json())

    def test_read_product(self):
        token = create_access_token(data={"sub": "testuser"})
        headers = {"Authorization": f"Bearer {token}"}
        prueba = 'LEVACAN NF X 2 ML'
        response = self.client.post(f"/sales/by_product/{prueba}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre", response.json())

    def test_get_sales_by_store(self):
        token = create_access_token(data={"sub": "testuser"})
        headers = {"Authorization": f"Bearer {token}"}
        prueba = 'PRADO'
        response = self.client.post(f"/sales/by_store/{prueba}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre", response.json())

    def test_get_sales_by_employee_avg(self):
        token = create_access_token(data={"sub": "testuser"})
        headers = {"Authorization": f"Bearer {token}"}
        prueba = "RAMIREZ CORREDOR DORA LIBANDY"
        response = self.client.post(f"/sales/total_avg_by_employee/{prueba}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre", response.json())

    def test_get_sales_by_product_avg(self):
        token = create_access_token(data={"sub": "testuser"})
        headers = {"Authorization": f"Bearer {token}"}
        prueba = 'LEVACAN NF X 2 ML'
        response = self.client.post(f"/sales/total_avg_by_product/{prueba}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre", response.json())

    def test_get_sales_by_store_avg(self):
        token = create_access_token(data={"sub": "testuser"})
        headers = {"Authorization": f"Bearer {token}"}
        prueba = 'CALLE79'
        response = self.client.post(f"/sales/total_avg_by_store/{prueba}", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Nombre", response.json())

if __name__ == "__main__":
    unittest.main()
