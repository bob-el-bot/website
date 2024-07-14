const fetch = require('node-fetch');

module.exports = async (req, res) => {
    const monitorId = '2426553';
    const apiKey = process.env.BETTERSTACK_TOKEN;
   
    if (!apiKey) {
        console.error('API key is missing');
        return res.status(500).json({ error: 'API key is missing' });
    }

    const targetUrl = `https://uptime.betterstack.com/api/v2/monitors/${monitorId}`;

    try {
        const response = await fetch(targetUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${apiKey}`
            }
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error fetching from BetterStack API:', errorText);
            return res.status(response.status).json({ error: 'Network response was not ok' });
        }

        const data = await response.json();
        return res.status(200).json(data);
    } catch (error) {
        console.error('Error in fetchStatus function:', error);
        return res.status(500).json({ error: 'Failed to fetch status' });
    }
};
