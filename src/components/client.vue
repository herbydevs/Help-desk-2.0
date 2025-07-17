<template>
    <div class="header">
        <h1>Help Desk</h1>
       
    </div>
    <div class="SubmitTicket">
        <h2> Submit A Ticket</h2>
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="subject">Subject:</label>
                <input type="text" id="subject" v-model="subject" required />
            </div>
            <div class="form-group
">
                <label for="description">Description:</label>
                <textarea id="description" v-model="description" required></textarea>
            </div>
            <div class="form-group">
                <label for="priority">Priority:</label>
                <select id="priority" v-model="priority" required>
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                </select>

                <label for="type">Type:</label>
                <select id="type" v-model="type" required>
                    <option value="payment">payment</option>
                    <option value="service">service</option>
                    <option value="account">account</option>
                </select>

            </div>
            <button type="submit">Submit Ticket</button>
        </form>
        <div v-if="successMessage" class="success">{{ successMessage }}</div>
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div> 
    </div>

    <div class="my-tickets">
        <h2>My Tickets</h2>
        <table>
            <thead>
                <tr>
                    <th>Ticket ID</th>
                    <th>Subject</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Created At</th>
                    <th>Actions</th>  <!-- New column -->
                </tr>
            </thead>
            <tbody>
                <tr v-for="ticket in tickets" :key="ticket.id">
                    <td>{{ ticket.id }}</td>
                    <td>{{ ticket.subject }}</td>
                    <td>{{ ticket.status }}</td>
                    <td>{{ ticket.priority }}</td>
                    <td>{{ new Date(ticket.created_at).toLocaleDateString() }}</td>
                    <td>
                        <button class="chat-btn" @click="openChat(ticket.id)">
                            💬 Chat
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="tickets.length === 0" class="no-tickets">
            <p>No tickets available.</p>
        </div>
    </div>
    <div v-if="showChat" class="chat-modal">
        <div class="chat-content">
            <div class="chat-header">
                <h3>Ticket #{{ selectedTicketId }} Chat</h3>
                <button class="close-button" @click="closeChat">&times;</button>
            </div>
            <div class="chat-messages">
                <div v-for="(message, index) in chatMessages" 
                     :key="index" 
                     :class="['message', message.sender === 'You' ? 'sent' : 'received']">
                    <div class="message-content">
                        <p>{{ message.text }}</p>
                        <span class="message-sender">{{ message.sender }}</span>
                    </div>
                </div>
            </div>
            <div class="chat-input">
                <textarea 
                    v-model="newMessage" 
                    placeholder="Type your message..." 
                    rows="2"
                    @keyup.enter="sendMessage"
                ></textarea>
                <button @click="sendMessage">Send</button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';

export default {
    name: 'SubmitTicket',
    setup() {
        const subject = ref('');
        const description = ref('');
        const priority = ref('low');
        const type = ref('payment'); // Add this line with default value
        const successMessage = ref('');
        const errorMessage = ref('');
        const tickets = ref([]);
        const showChat = ref(false);
        const selectedTicketId = ref(null);
        const newMessage = ref('');
        const chatMessages = ref([
            { sender: 'You', text: 'Hi, I need help with my ticket.' },
            { sender: 'Support', text: 'How can we assist you today?' },
            { sender: 'You', text: 'I have a question about my ticket.' },
            { sender: 'Support', text: 'Please provide your ticket ID for reference.' },
            { sender: 'You', text: 'My ticket ID is 12345.' },
            { sender: 'Support', text: 'Thank you! We will look into it and get back to you shortly.' }
        ]);

        const handleSubmit = async () => {  // Remove event parameter
            try {
                const response = await fetch('http://localhost:8000/api/tickets', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        subject: subject.value,
                        description: description.value,
                        priority: priority.value,
                        type: type.value
                    })
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                successMessage.value = 'Ticket submitted successfully!';
                errorMessage.value = '';
                subject.value = '';
                description.value = '';
                priority.value = 'low';
                type.value = 'payment';  // Reset type to default
                fetchTickets(); // Refresh the ticket list
            } catch (error) {
                errorMessage.value = `Error submitting ticket: ${error.message}`;
                successMessage.value = '';
            }
        };

        const fetchTickets = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/tickets');
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                tickets.value = await response.json();
            } catch (error) {
                console.error('Error fetching tickets:', error);
            }
        };

        // Add polling interval ref
        let messagePollingInterval = null;

        const startMessagePolling = (ticketId) => {
            // Poll every 2 seconds
            messagePollingInterval = setInterval(async () => {
                if (showChat.value) {
                    await fetchMessages(ticketId);
                }
            }, 2000);
        };

        const stopMessagePolling = () => {
            if (messagePollingInterval) {
                clearInterval(messagePollingInterval);
                messagePollingInterval = null;
            }
        };

        // Update openChat to start polling
        const openChat = async (ticketId) => {
            selectedTicketId.value = ticketId;
            showChat.value = true;
            await fetchMessages(ticketId);
            startMessagePolling(ticketId);
        };

        // Update closeChat to stop polling
        const closeChat = () => {
            showChat.value = false;
            selectedTicketId.value = null;
            newMessage.value = '';
            chatMessages.value = [];
            stopMessagePolling();
        };

        const fetchMessages = async (ticketId) => {
            try {
                const response = await fetch(`http://localhost:8000/api/tickets/${ticketId}/messages`);
                if (!response.ok) throw new Error('Failed to fetch messages');
                chatMessages.value = await response.json();
            } catch (error) {
                console.error('Error fetching messages:', error);
                chatMessages.value = [];
            }
        };

        const sendMessage = async () => {
            if (!newMessage.value.trim()) return;

            try {
                const response = await fetch(`http://localhost:8000/api/tickets/${selectedTicketId.value}/messages`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        content: newMessage.value.trim()
                    })
                });

                if (!response.ok) throw new Error('Failed to send message');

                // Add message to chat
                chatMessages.value.push({
                    sender: 'You',
                    text: newMessage.value.trim(),
                    created_at: new Date().toISOString()
                });

                newMessage.value = '';

                // Scroll to bottom
                nextTick(() => {
                    const chatContainer = document.querySelector('.chat-messages');
                    if (chatContainer) {
                        chatContainer.scrollTop = chatContainer.scrollHeight;
                    }
                });
            } catch (error) {
                console.error('Error sending message:', error);
            }
        };

        const handleLogout = () => {
            localStorage.removeItem('token');
            window.location.href = '/login';
        };

        onMounted(() => {
            fetchTickets();
            
            // Return cleanup function
            return () => {
                stopMessagePolling();
            };
        });

        return { 
            subject, description, priority, type, // Add type here
            successMessage, errorMessage, 
            tickets, handleSubmit, showChat, 
            selectedTicketId, newMessage, 
            chatMessages, sendMessage, handleLogout, 
            openChat, closeChat 
        };
    }
};
</script>

<style scoped>
/* Main container classes */
.SubmitTicket,
.my-tickets,
.ticket-chatbox {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}

/* Form styling */
.form-group {
    margin-bottom: 15px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input, textarea, select {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
    border: 1px solid #ddd;
    border-radius: 4px;
}

/* Table styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}

th, td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}

th {
    background-color: #f2f2f2;
}

/* Button styling */
button {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin: 10px 0;
}

button:hover {
    background-color: #0056b3;
}

/* Messages */
.success {
    color: green;
    text-align: center;
    margin: 10px 0;
}

.error {
    color: red;
    text-align: center;
    margin: 10px 0;
}

/* Chat messages */
.chat-messages {
    margin-top: 10px;
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.chat-messages p {
    margin: 5px 0;
    padding: 5px;
}

.chat-messages strong {
    color: #333;
}

/* Headings */
h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

/* No tickets message */
.no-tickets {
    text-align: center;
    color: #888;
    padding: 20px;
    font-style: italic;
}

/* Chat Bubbles Styling */
.message {
    display: flex;
    margin: 8px 0;
    max-width: 85%;
}

.message.sent {
    margin-left: auto;
    flex-direction: row-reverse;
}

.message.received {
    margin-right: auto;
    flex-direction: row;
}

.message-content {
    padding: 8px 12px;
    border-radius: 15px;
    position: relative;
    max-width: 100%;
    word-wrap: break-word;
}

.message.sent .message-content {
    background-color: #007bff;
    color: white;
    margin-right: 8px;
    border-top-right-radius: 2px;
}

.message.received .message-content {
    background-color: #e9ecef;
    color: #333;
    margin-left: 8px;
    border-top-left-radius: 2px;
}

.message-sender {
    font-size: 0.75rem;
    margin-top: 4px;
    opacity: 0.7;
}

.message.sent .message-sender {
    text-align: right;
}

.message.received .message-sender {
    text-align: left;
}

.chat-messages {
    padding: 15px;
    height: 300px;
    overflow-y: auto;
    background: #fff;
    scroll-behavior: smooth;
    display: flex;
    flex-direction: column;
}

/* Headings */
h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

/* No tickets message */
.no-tickets {
    text-align: center;
    color: #888;
    padding: 20px;
    font-style: italic;
}

/* Chat modal positioning */
.chat-modal {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 360px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    z-index: 1000;
}
</style>