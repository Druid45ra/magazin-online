---
name: Bug report
about: Imagini și butoane lipsă în pagina de produse
title: '[BUG] Probleme cu afișarea imaginilor și butoanelor în pagina de produse'
labels: bug, help wanted
assignees: ''
---

**Descrierea problemei**
Pagina de produse nu afișează imaginile produselor și butoanele "Adaugă în coș" nu sunt vizibile.

**Comportament așteptat**
- Imaginile produselor ar trebui să fie vizibile pentru fiecare produs
- Fiecare produs ar trebui să aibă un buton "Adaugă în coș"
- Layout-ul ar trebui să fie un grid responsive

**Comportament actual**
- Nu se afișează nicio imagine pentru produse
- Butoanele "Adaugă în coș" lipsesc
- Layout-ul este simplu, fără stilizare

**Cod relevant**

Template produse.html:
```html
<div class="product-grid">
    {% for produs in produse %}
    <div class="product-card">
        <img class="product-image" 
             src="{{ url_for('static', filename=produs.image) }}" 
             alt="{{ produs.name }}">
        <h2 class="product-title">{{ produs.name }}</h2>
        <p class="product-description">{{ produs.description }}</p>
        <p class="product-price">{{ "%.2f"|format(produs.price) }} RON</p>
        <form action="{{ url_for('add_to_cart', product_id=produs.id) }}" method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <button type="submit" class="add-to-cart-btn">Adaugă în coș</button>
        </form>
    </div>
    {% endfor %}
</div>
```

Ruta din app.py:
```python
@app.route('/produse')
def produse():
    produse = Product.query.all()
    return render_template('produse.html', produse=produse)
```

Model Product:
```python
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
```

**Verificări efectuate**
1. Imaginile există în directorul static/uploads/
2. Căile către imagini sunt salvate corect în baza de date
3. Template-ul a fost actualizat cu stilizare CSS
4. Am testat în mai multe browsere (Chrome, Firefox)

**Mediu de dezvoltare**
- OS: Windows
- Python: 3.13
- Flask: 3.1.0
- Browser-e testate: Chrome, Firefox

**Pași pentru reproducere**
1. Clonează repository-ul
2. Instalează dependințele: `pip install -r requirements.txt`
3. Rulează scriptul populate_db.py pentru a popula baza de date
4. Pornește serverul Flask: `flask run`
5. Accesează http://127.0.0.1:5000/produse

**Screenshots**
[Adaugă screenshot-uri cu problema]

**Întrebări pentru comunitate**
1. De ce nu se afișează imaginile deși calea pare corectă?
2. Este o problemă cu modul în care sunt servite fișierele statice?
3. Există probleme cunoscute cu Flask și servirea imaginilor?
