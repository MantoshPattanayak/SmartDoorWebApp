
function getCurrentDateTime() {
    const now = new Date();
    const options = {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    const date = now.toLocaleDateString('en-US', options);
    const time = now.toLocaleTimeString('en-US', { hour12: true, hour: 'numeric', minute: 'numeric' });
    return { date, time };
  }
  
  // Display the current date and time
  function displayCurrentDateTime() {
    const { date, time } = getCurrentDateTime();
    document.getElementById('current-date').textContent = date;
    document.getElementById('current-time').textContent = time;
  }
  
  // Update the current date and time every second
  setInterval(displayCurrentDateTime, 1000);

// const form = document.getElementById("form");
// const emp_id = document.getElementById("username");
// const user_password = document.getElementById("user_password");
// const error = document.getElementById("error");

// form.addEventListener("submit", (e) => {
//   e.preventDefault();

//   if (!username.value) {
//     error.innerHTML = "Please enter a username";
//     return;
//   }

//   if (!user_password.value) {
//     error.innerHTML = "Please enter a password";
//     return;
//   }

//   if (!/^[a-zA-Z0-9]+$/.test(username.value)) {
//     error.innerHTML = "username should not contain special characters";
//     return;
//   }

//   // Validate username and password against server

//   error.innerHTML = "";
// });