from app import app, db, Product

# Populates the database with products if it is empty
with app.app_context():
    if not Product.query.first():
        products = [
            Product(
                name="Laptop",
                price=3000,
                description="Laptop performant cu ecran de 15.6 inch.",
                image_path="uploads/laptop.jpg"
            ),
            Product(
                name="Smartphone",
                price=2000,
                description="Telefon inteligent cu cameră de 108 MP.",
                image_path="uploads/smartphone.jpg"
            ),
            Product(
                name="Televizor",
                price=4000,
                description="Televizor UHD cu diagonala de 55 inch.",
                image_path="uploads/televizor.jpg"
            )
        ]
        db.session.add_all(products)
        db.session.commit()
        print("Produse adăugate cu succes în baza de date!")
    else:
        print("Baza de date este deja populată.")