document.getElementById("appointment-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;
  const date = document.getElementById("date").value;

  const appointment = {
    name: name,
    email: email,
    appointment_date: new Date(date).toISOString()
  };

  try {
    const response = await fetch("/appointments/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(appointment)
    });

    if (response.ok) {
      alert("Appointment booked!");
      document.getElementById("appointment-form").reset();
    } else {
      alert("Error booking appointment.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Network error.");
  }
});
