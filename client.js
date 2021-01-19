const helpers = require('./helpers');
const messageApi = require('./messaging_api');
const readline = require('readline');

const displayedMessages = {};

const terminal = readline.createInterface({
    input: process.stdin,
})

terminal.on('line', text=> {
    const username = process.env.NAME;
    const id = helpers.getRandomInt(1000000); // This could be changed later on for more robust application

    //Check if message has been displayed or not
    displayedMessages[id] = true;
    const message = {id, text, username};
    messageApi.sendMessage(message);
})

function displayMessages(message) {
    console.log(`> ${message.username}: ${message.text}`);
    displayedMessages[message.id] = true;
}

async function getAndDisplayMessages(){
    const messages = await messageApi.getMessages();

    for (const message of messages) {
        const messageAlreadyDisplayed = message.id in displayedMessages;
        if (!messageAlreadyDisplayed) displayMessages(message);
    }
}

function pollMessages() {
    setInterval(getAndDisplayMessages, 3000);
}

function streamMessages() {
    const messageingSocket = messageApi.createMessagingSocket();

    messageingSocket.on('message', data => {
        const message = JSON.parse(data);
        const messageAlreadyDisplayed = message.id in displayedMessages;
        if (!messageAlreadyDisplayed) displayMessages(message);
    });
}

if (process.env.MODE === 'poll'){
    getAndDisplayMessages();
    pollMessages();
}else if(process.env.MODE === 'stream'){
    getAndDisplayMessages();
    streamMessages();
}