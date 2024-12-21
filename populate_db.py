from app import app, db, Product
import requests
import os
import shutil

# Curăță directorul uploads
uploads_dir = 'static/uploads'
if os.path.exists(uploads_dir):
    for filename in os.listdir(uploads_dir):
        file_path = os.path.join(uploads_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Error: {e}')

def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(os.path.join('static/uploads', filename), 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return True
        return False
    except Exception as e:
        print(f'Error downloading {url}: {e}')
        return False

# Lista de produse cu detalii
produse = [
    {
        "name": "Laptop Gaming ASUS ROG",
        "price": 4999.99,
        "description": "Laptop gaming cu procesor Intel i7, 16GB RAM, 1TB SSD, placă video RTX 3060",
        "image": "laptop-asus.jpg",
        "placeholder": "https://picsum.photos/800/600?random=1"
    },
    {
        "name": "iPhone 15 Pro",
        "price": 5499.99,
        "description": "Smartphone Apple cu cameră triplă, 256GB stocare, iOS 17",
        "image": "iphone15.jpg",
        "placeholder": "https://picsum.photos/800/600?random=2"
    },
    {
        "name": "Samsung QLED TV",
        "price": 3999.99,
        "description": "Televizor Smart TV 65 inch, 4K UHD, HDR, procesor AI",
        "image": "samsung-tv.jpg",
        "placeholder": "https://picsum.photos/800/600?random=3"
    },
    {
        "name": "PlayStation 5",
        "price": 2499.99,
        "description": "Consolă de gaming next-gen, include controller DualSense",
        "image": "ps5.jpg",
        "placeholder": "https://picsum.photos/800/600?random=4"
    },
    {
        "name": "Apple MacBook Air M2",
        "price": 5999.99,
        "description": "Laptop ultraportabil cu chip M2, 8GB RAM, 512GB SSD",
        "image": "macbook-air.jpg",
        "placeholder": "https://picsum.photos/800/600?random=5"
    },
    {
        "name": "Căști Sony WH-1000XM4",
        "price": 1499.99,
        "description": "Căști wireless cu anulare activă a zgomotului, autonomie 30 ore",
        "image": "sony-headphones.jpg",
        "placeholder": "https://picsum.photos/800/600?random=6"
    },
    {
        "name": "iPad Pro 12.9",
        "price": 4999.99,
        "description": "Tabletă Apple cu display Liquid Retina XDR, chip M2, 256GB",
        "image": "ipad-pro.jpg",
        "placeholder": "https://picsum.photos/800/600?random=7"
    },
    {
        "name": "Monitor Gaming LG",
        "price": 1999.99,
        "description": "Monitor 27 inch, 165Hz, 1ms, QHD, HDR400, FreeSync Premium",
        "image": "lg-monitor.jpg",
        "placeholder": "https://picsum.photos/800/600?random=8"
    }
]

# Asigură-te că directorul uploads există
os.makedirs('static/uploads', exist_ok=True)

# Populează baza de date cu produse
with app.app_context():
    # Șterge toate produsele existente
    Product.query.delete()
    
    # Descarcă imaginile și adaugă produsele
    for produs in produse:
        # Descarcă imaginea placeholder
        if download_image(produs["placeholder"], produs["image"]):
            new_product = Product(
                name=produs["name"],
                price=produs["price"],
                description=produs["description"],
                image=f"uploads/{produs['image']}"  # Calea corectă pentru imagini
            )
            db.session.add(new_product)
            print(f"Produs adăugat: {produs['name']}")
        else:
            print(f"Eroare la descărcarea imaginii pentru {produs['name']}")
    
    # Salvează în baza de date
    db.session.commit()
    print("Produse și imagini adăugate cu succes în baza de date!")
