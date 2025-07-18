<template>
   <div class="ticket-list-container">
        <div class="header-buttons">
            <button class="nav-btn" @click="switchToUserManagement">
                👥 User Management
            </button>
        </div>
        <h1>Tickets</h1>
        <table>
            <thead>
                <tr>
                    <th>Ticket ID</th>
                    <th>Subject</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Created At</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="ticket in tickets" :key="ticket.id">
                    <td>{{ ticket.id }}</td>
                    <td>{{ ticket.subject }}</td>
                    <td>
                        <select 
                            v-model="ticket.status" 
                            @change="updateTicketStatus(ticket.id, ticket.status)"
                            :class="['status-select', ticket.status.toLowerCase()]"
                        >
                            <option value="open">Open</option>
                            <option value="in-progress">In Progress</option>
                            <option value="closed">Closed</option>
                        </select>
                    </td>
                    <td>
                        <select 
                            v-model="ticket.priority" 
                            @change="updateTicketPriority(ticket.id, ticket.priority)"
                            :class="['priority-select', ticket.priority.toLowerCase()]"
                        >
                            <option value="low">Low</option>
                            <option value="medium">Medium</option>
                            <option value="high">High</option>
                        </select>
                    </td>
                    <td>{{ formatDate(ticket.created_at) }}</td>
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

        <!-- Chat Modal -->
        <div v-if="showChat" class="chat-modal">
            <div class="chat-content">
                <div class="chat-header">
                    <h3>Ticket #{{ selectedTicketId }} Chat</h3>
                    <button class="close-btn" @click="closeChat">&times;</button>
                </div>
                <div class="chat-messages" ref="chatContainer">
                    <div v-for="(message, index) in chatMessages" 
                         :key="index" 
                         :class="['message', message.sender === currentUser ? 'sent' : 'received']">
                        <div class="message-content">
                            <p style="margin: 0;">{{ message.content }}</p>
                            <span class="message-sender">{{ message.sender }}</span>
                        </div>
                    </div>
                </div>
                <div class="chat-input">
                    <textarea 
                        v-model="newMessage" 
                        placeholder="Type your message..." 
                        @keyup.enter="sendMessage"
                        rows="2"
                    ></textarea>
                    <button @click="sendMessage">Send</button>
                </div>
            </div>
        </div>
   </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue';

export default {
    name: 'TicketList',
    setup() {
        const tickets = ref([]);
        const showChat = ref(false);
        const selectedTicketId = ref(null);
        const newMessage = ref('');
        const chatMessages = ref([]);
        const chatContainer = ref(null);
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        const currentUser = userData.email;

        const formatDate = (dateString) => {
            return new Date(dateString).toLocaleString();
        };

        const fetchTickets = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('http://localhost:8080/api/tickets', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                tickets.value = await response.json();
            } catch (error) {
                console.error('Error fetching tickets:', error);
            }
        };

        const openChat = async (ticketId) => {
            selectedTicketId.value = ticketId;
            showChat.value = true;
            await fetchMessages(ticketId);
            startMessagePolling(ticketId);
        };

        const closeChat = () => {
            showChat.value = false;
            selectedTicketId.value = null;
            newMessage.value = '';
            chatMessages.value = [];
            stopMessagePolling();
        };

        const fetchMessages = async (ticketId) => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8080/api/tickets/${ticketId}/messages`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
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
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8080/api/tickets/${selectedTicketId.value}/message`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        content: newMessage.value.trim()
                    })
                });

                if (!response.ok) throw new Error('Failed to send message');

                // Add message to chat
                chatMessages.value.push({
                    text: newMessage.value.trim(),
                    sender: 'Admin',
                    created_at: new Date().toISOString()
                });

                newMessage.value = '';

                // Scroll to bottom
                nextTick(() => {
                    const container = chatContainer.value;
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    }
                });

                // Fetch latest messages to sync with any other responses
                await fetchMessages(selectedTicketId.value);
            } catch (error) {
                console.error('Error sending message:', error);
            }
        };

        let messagePollingInterval = null;

        const startMessagePolling = (ticketId) => {
            messagePollingInterval = setInterval(() => {
                if (showChat.value) {
                    fetchMessages(ticketId);
                }
            }, 3000); // Poll every 3 seconds
        };

        const stopMessagePolling = () => {
            if (messagePollingInterval) {
                clearInterval(messagePollingInterval);
                messagePollingInterval = null;
            }
        };

        const updateTicketStatus = async (ticketId, status) => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8080/api/tickets/${ticketId}/status`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ status })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to update ticket status');
                }
                
                // Update local state
                const ticket = tickets.value.find(t => t.id === ticketId);
                if (ticket) {
                    ticket.status = status;
                }
            } catch (error) {
                console.error('Error updating ticket status:', error);
                // Revert the change on error
                await fetchTickets();
            }
        };

        const updateTicketPriority = async (ticketId, priority) => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch(`http://localhost:8080/api/tickets/${ticketId}/priority`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ priority })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to update ticket priority');
                }
                
                // Update local state
                const ticket = tickets.value.find(t => t.id === ticketId);
                if (ticket) {
                    ticket.priority = priority;
                }
            } catch (error) {
                console.error('Error updating ticket priority:', error);
                // Revert the change on error
                await fetchTickets();
            }
        };

        const switchToUserManagement = () => {
            window.location.href = '/help-desk/user-management ';
        };

        // Set up polling for updates
        onMounted(() => {
            fetchTickets();
            // Poll for updates every 30 seconds
            const pollInterval = setInterval(fetchTickets, 30000);
            
            // Clean up interval on component unmount
            return () => {
                clearInterval(pollInterval);
                stopMessagePolling();
            };
        });

        return { 
            tickets, 
            showChat, 
            selectedTicketId, 
            newMessage, 
            chatMessages, 
            chatContainer,
            openChat, 
            closeChat, 
            sendMessage,
            formatDate,
            updateTicketStatus,
            updateTicketPriority,
            currentUser,
            switchToUserManagement
        };
    }
};
</script>

<style scoped>
/* Modern Font Import - Add this at the top */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* Base Styles */
.ticket-list-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 24px;
    border: none;
    border-radius: 16px;
    background-color: #ffffff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

h1 {
    text-align: center;
    font-weight: 600;
    color: #1a1a1a;
    font-size: 1.75rem;
    margin-bottom: 24px;
}

/* Table Styles */
table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 16px 0;
}

th, td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid #edf2f7;
}

th {
    background-color: #f8fafc;
    font-weight: 500;
    color: #64748b;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

td {
    color: #334155;
    font-size: 0.9375rem;
}

/* Status Badge Updates */
.status-badge {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8125rem;
    font-weight: 500;
    display: inline-block;
}

.status-badge.open {
    background-color: #ecfdf5;
    color: #059669;
}

.status-badge.in-progress {
    background-color: #fef3c7;
    color: #d97706;
}

.status-badge.closed {
    background-color: #f1f5f9;
    color: #64748b;
}

/* Chat Modal Styles */
.chat-modal {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 360px;
    height: 480px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    z-index: 1000;
    display: flex;
    flex-direction: column;
}

.chat-content {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
    background: #f8f9fa;
}

.message {
    display: flex;
    max-width: 85%;
    margin: 4px 0;
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
    border-radius: 16px;
    position: relative;
    word-wrap: break-word;
}

.message.sent .message-content {
    background-color: #3b82f6;
    color: white;
    border-bottom-right-radius: 4px;
    margin-left: 8px;
}

.message.received .message-content {
    background-color: #f1f5f9;
    color: #1a1a1a;
    border-bottom-left-radius: 4px;
    margin-right: 8px;
}

.message-sender {
    font-size: 0.75rem;
    margin-top: 4px;
    opacity: 0.7;
}

.chat-input {
    padding: 12px;
    border-top: 1px solid #e5e7eb;
    background: white;
    display: flex;
    gap: 8px;
    align-items: flex-start;
}

.chat-input textarea {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    resize: none;
    height: 40px;
    font-family: inherit;
}

.chat-input button {
    padding: 8px 16px;
    height: 40px;
    white-space: nowrap;
}

.chat-header {
    padding: 16px;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
}

.chat-header h3 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
}

.close-btn {
    padding: 4px 8px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #6b7280;
}

.close-btn:hover {
    color: #374151;
}

/* Empty State */
.no-tickets {
    text-align: center;
    color: #64748b;
    padding: 48px 24px;
}

.no-tickets p {
    font-size: 0.9375rem;
    font-weight: 500;
}

.status-select,
.priority-select {
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 0.8125rem;
    font-weight: 500;
    border: 1px solid #e2e8f0;
    background-color: white;
    cursor: pointer;
}

.status-select.open {
    color: #059669;
    border-color: #059669;
}

.status-select.in-progress {
    color: #d97706;
    border-color: #d97706;
}

.status-select.closed {
    color: #64748b;
    border-color: #64748b;
}

.priority-select.low {
    color: #059669;
    border-color: #059669;
}

.priority-select.medium {
    color: #d97706;
    border-color: #d97706;
}

.priority-select.high {
    color: #dc2626;
    border-color: #dc2626;
}

select:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.header-buttons {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 20px;
}

.nav-btn {
    padding: 8px 16px;
    background-color: #4f46e5;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 6px;
    transition: background-color 0.2s;
}

.nav-btn:hover {
    background-color: #4338ca;
}
</style>