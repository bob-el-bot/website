
document.addEventListener('DOMContentLoaded', function () {
    const statusText = document.getElementById('status-text');
    const statusIndicator = document.getElementById('status-indicator');

    fetch('/api/fetchStatus')
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text) });
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                console.error('Error detail:', data.detail);
                statusText.textContent = '⬤ Error';
                statusIndicator.classList.add('error');
                return;
            }
            const status = data.data.attributes.status;
            var label = "";
            switch (status) {
                case "up":
                    label = "⬤ Online";
                    break;
                case "down":
                    label = "⬤ Offline";
                    break;
                case "paused":
                case "error":
                case "validating":
                case "pending":
                    label = "⬤ Unknown";
                    break;
                case "maintenance":
                    label = "⬤ Maintenance";
                    break;
            }
            statusText.textContent = label;
            statusIndicator.classList.add(status);
        })
        .catch(error => {
            console.error('Error fetching status:', error);
            statusText.textContent = '⬤ Error';
            statusIndicator.classList.add('error');
        });
});