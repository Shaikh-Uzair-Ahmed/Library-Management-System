document.addEventListener("DOMContentLoaded", () => {
    const notificationBadge = document.querySelector("#notification-bell .notification-count");

    function updateNotificationDisplay(count) {
        // Update badge text and visibility
        if (notificationBadge) {
            notificationBadge.textContent = count;
            notificationBadge.style.display = count > 0 ? "inline" : "none";
        }
    }

    // Listen for the notification update event from any page
    document.addEventListener("notificationUpdate", (event) => {
        const newCount = event.detail;
        updateNotificationDisplay(newCount);
    });
});

/*document.addEventListener("DOMContentLoaded", () => {
    const notificationBadge = document.querySelector("#notification-bell .notification-count");

    // Function to fetch notification count from the server
    function fetchNotificationCount() {
        fetch("/api/notification-count/")
            .then(response => response.json())
            .then(data => {
                const count = data.count;
                // Update badge display
                if (notificationBadge) {
                    notificationBadge.textContent = count;
                    notificationBadge.style.display = count > 0 ? "inline" : "none";
                }
            })
            .catch(error => console.error("Error fetching notification count:", error));
    }

    // Initial fetch when the page loads
    fetchNotificationCount();
});*/


document.addEventListener("DOMContentLoaded", () => {
    const hamburgerIcon = document.getElementById("hamburger-icon");
    const menu = document.getElementById("menu");

    // Toggle the visibility of the menu with smooth sliding transition
    hamburgerIcon.addEventListener("click", () => {
        menu.classList.toggle("hidden"); // Toggle hidden class
        menu.classList.toggle("show"); // Toggle show class to trigger slide effect
    });

    // Close the menu if user clicks outside the menu
    window.addEventListener("click", (event) => {
        if (!menu.contains(event.target) && !hamburgerIcon.contains(event.target)) {
            menu.classList.add("hidden");
            menu.classList.remove("show");
        }
    });
});
