document.addEventListener("DOMContentLoaded", function () {
    const notificationCounter = document.getElementById("notification-counter");
    const checkboxes = document.querySelectorAll(".notification-checkbox");

    if (!notificationCounter) return; // Exit if counter doesn't exist on the page

    // Function to count unchecked notifications
    function updateCounter() {
        const uncheckedCount = Array.from(checkboxes).filter(checkbox => !checkbox.checked).length;
        notificationCounter.textContent = uncheckedCount;

        // Dispatch a custom event with the updated count
        const event = new CustomEvent("notificationUpdate", { detail: uncheckedCount });
        document.dispatchEvent(event);
    }

    // Initialize counter and add checkbox listeners if checkboxes are found
    if (checkboxes.length) {
        updateCounter();
        checkboxes.forEach(checkbox => checkbox.addEventListener("change", updateCounter));
    }
});

/*document.addEventListener("DOMContentLoaded", function () {
    const notificationCounter = document.getElementById("notification-counter");
    const checkboxes = document.querySelectorAll(".notification-checkbox");

    function updateCounter() {
        const uncheckedCount = Array.from(checkboxes).filter(checkbox => !checkbox.checked).length;
        if (notificationCounter) {
            notificationCounter.textContent = uncheckedCount;
        }
    }

    function markNotificationAsChecked(notificationId) {
        fetch("/api/update-notification/", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrftoken  // Use the global CSRF token variable
            },
            body: `notification_id=${notificationId}`
        })
        .then(response => response.json())
        .then(data => {
            notificationCounter.textContent = data.count;
        })
        .catch(error => console.error("Error updating notification status:", error));
    }

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function () {
            if (checkbox.checked) {
                const notificationId = checkbox.dataset.notificationId;
                markNotificationAsChecked(notificationId);
            }
        });
    });
});*/