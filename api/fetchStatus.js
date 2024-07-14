module.exports = async (req, res) => {
    const monitorId = '2426553'; // Replace with your actual monitor ID
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

        const contentType = response.headers.get('content-type');
        console.log('Response content-type:', contentType);

        if (contentType && contentType.includes('application/json')) {
            const data = await response.json();
            return res.status(200).json(data);
        } else {
            const text = await response.text();
            console.error('Unexpected response format:', text);
            return res.status(response.status).json({ error: 'Unexpected response format', detail: text });
        }
    } catch (error) {
        console.error('Error in fetchStatus function:', error);
        return res.status(500).json({ error: 'Failed to fetch status' });
    }
};