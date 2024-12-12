document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.product button');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            alert('Produs adăugat în coș!');
        });
    });
});

fetch('/add_product', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': '{{ csrf_token }}'  // Asigură-te că este inclus tokenul
    },
    body: JSON.stringify(data)
});
