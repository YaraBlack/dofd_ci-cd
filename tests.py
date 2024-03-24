import unittest
from app import app as flask_app
from db import db, ProductModel, create_product


class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the Flask app for testing"""
        flask_app.config["TESTING"] = True
        cls.app = flask_app.test_client()

    def setUp(self):
        """Create the in-memory SQLite database for testing"""
        db.create_tables([ProductModel])

    def tearDown(self):
        """Clean up after each test"""
        db.drop_tables([ProductModel])

    def test_create_product_endpoint(self):
        """Test creating a product"""
        response = self.app.post(
            "/api/products", json={"name": "Test Product", "price": 10}
        )
        self.assertEqual(response.status_code, 201)

    def test_get_product_by_id_endpoint(self):
        """Test getting a product by ID"""
        product = create_product("Test Product", 10)

        response = self.app.get(f"/api/products/{product.id}")
        self.assertEqual(response.status_code, 200)

    def test_get_all_products(self):
        """Test getting all products"""
        product1 = create_product("Test Product 1", 10)
        product2 = create_product("Test Product 2", 5)
        expected_data = [
            {
                "id": product1.id,
                "name": product1.name,
                "price": product1.price,
            },
            {
                "id": product2.id,
                "name": product2.name,
                "price": product2.price,
            },
        ]
        response = self.app.get("/api/products")
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertEqual(expected_data, response_data)

    def test_edit_product(self):
        """Test updating a product by ID"""
        product = create_product("Test Product 1", 10)

        updated_product = {"name": "Test Product Updated", "price": 5}

        response = self.app.patch(
            f"api/products/{product.id}",
            json=updated_product,
        )

        self.assertEqual(response.status_code, 200)

        response = self.app.get(f"api/products/{product.id}")
        self.assertEqual(
            {
                "id": product.id,
                "name": updated_product["name"],
                "price": updated_product["price"],
            },
            response.get_json(),
        )

    def test_delete_product(self):
        """Test deleting a product by ID"""
        product = create_product("Test Product 1", 10)

        response = self.app.delete(f"api/products/{product.id}")

        self.assertEqual(response.status_code, 200)

        response = self.app.get("api/products")
        self.assertEqual(response.get_json(), [])


if __name__ == "__main__":
    unittest.main()
