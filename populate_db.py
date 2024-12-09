from app import app, db, Product

# Populează baza de date cu produse
with app.app_context():
    # Creează obiecte de tip Product
    produs1 = Product(name="Laptop", price=3000, description="Laptop performant cu ecran de 15.6 inch.")
    produs2 = Product(name="Smartphone", price=2000, description="Telefon inteligent cu cameră de 108 MP.")
    produs3 = Product(name="Televizor", price=4000, description="Televizor UHD cu diagonala de 55 inch.")
    produs4 = Product(name="Televizor LG", price=4000, description="Televizor UHD cu diagonala de 45 inch.")
    
    # Adaugă produsele în sesiune
    db.session.add_all([produs1, produs2, produs3])
    
    # Salvează în baza de date
    db.session.commit()

    print("Produse adăugate cu succes în baza de date!")
