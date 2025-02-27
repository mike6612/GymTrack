document.addEventListener("DOMContentLoaded", function () {
  // Loop through each note and process its times
  document.querySelectorAll("[data-utc]").forEach((element) => {
    const utcTime = element.getAttribute("data-utc");
    const localDate = new Date(utcTime + " UTC");
    const date = localDate.toLocaleDateString();
    const time = localDate.toLocaleTimeString();

    element.innerText = `${date} ${time}`;
  });
});
