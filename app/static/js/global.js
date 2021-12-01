// Remove any alerts after 3 seconds
setTimeout(() => {
  const alert = document.getElementById("alert")
  if (alert) {
    alert.parentNode.removeChild(alert);
  }
}, 3000)