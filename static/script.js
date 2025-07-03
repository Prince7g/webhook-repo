async function fetchEvents() {
    const response = await fetch('/events');
    const data = await response.json();
    const list = document.getElementById('event-list');
    list.innerHTML = '';
    data.forEach(event => {
        const li = document.createElement('li');
        li.textContent = event;
        list.appendChild(li);
    });
}

setInterval(fetchEvents, 15000);
window.onload = fetchEvents;
