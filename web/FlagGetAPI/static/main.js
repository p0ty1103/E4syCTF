// TODO: Implement /api/get_admin_info for admins. -
// This endpoint seems to be the real deal.

document.getElementById('infoButton').addEventListener('click', () => {
    fetch('/api/get_info')
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').innerText = data.error;
        });
});