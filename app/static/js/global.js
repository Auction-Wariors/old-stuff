// Remove any alerts after 3 seconds
setTimeout(() => {
  const alert = document.getElementById("alert")
  if (alert) {
    alert.parentNode.removeChild(alert);
  }
}, 3000)

// Remove second alert after 4 seconds
setTimeout(() => {
  const alert = document.getElementById("alert")
  if (alert) {
    alert.parentNode.removeChild(alert);
  }
}, 4000)