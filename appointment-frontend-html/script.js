const form = document.getElementById('appointment-form');
const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const dateInput = document.getElementById('date');
const list = document.getElementById('appointments-list');

const API = 'http://localhost:8000/appointments';

function renderAppointments(data) {
  list.innerHTML = '';
  data.forEach(appt => {
    const li = document.createElement('li');
    li.textContent = `${appt.name} (${appt.email}) on ${new Date(appt.appointment_date).toLocaleString()}`;
    list.appendChild(li);
  });
}

function fetchAppointments() {
  fetch(API)
    .then(res => res.json())
    .then(renderAppointments)
    .catch(console.error);
}

form.addEventListener('submit', (e) => {
  e.preventDefault();

  const newAppt = {
    name: nameInput.value,
    email: emailInput.value,
    appointment_date: dateInput.value,
  };

  fetch(API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newAppt),
  })
    .then(res => res.json())
    .then(data => {
      fetchAppointments();
      form.reset();
    })
    .catch(console.error);
});

fetchAppointments();
