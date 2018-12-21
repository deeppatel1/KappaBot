module.exports = {
    query : async function(query) {
        const { Client } = require('pg');
        const client = new Client();
        await client.connect();
        await client.query(query)
            .then(res => console.log(res.rows[0]))
            .catch(e => console.error(e.stack));
        console.log(query);
        await client.end();
    }
 }