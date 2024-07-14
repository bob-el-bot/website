const fetch = require('node-fetch');

module.exports = async (req, res) => {
    const monitorId = '2426553';
    const apiKey = process.env.BETTERSTACK_TOKEN;

    const targetUrl = `https://uptime.betterstack.com/api/v2/monitors/${monitorId}`;

    try {
        const response = await fetch(targetUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${apiKey}`
            }
        });

        if (!response.ok) {
            return res.status(response.status).json({ error: 'Network response was not ok' });
        }

        const data = await response.json();
        return res.status(200).json(data);
    } catch (error) {
        return res.status(500).json({ error: 'Failed to fetch status' });
    }
};
