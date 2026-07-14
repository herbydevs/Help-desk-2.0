<template>
        <div>
    <div class="SubmitTicket">
        <form class="add-ticket-form" @submit.prevent="handleSubmit">
                    <h2> Submit A Ticket</h2>

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
                    <option disabled value="">-- Select Type --</option>
                    <option v-for="issue in issueTypes" :key="issue.id" :value="issue.name">
                        {{ issue.name }}
                    </option>
                 </select>

            </div>
            <button type="submit"><i class="pi pi-check" style="font-size: 1rem"></i>Submit Ticket</button>
        </form>
        <div v-if="successMessage" class="success">{{ successMessage }}</div>
        <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
    </div>

    <div class="tickets-list">
        <h2>My Tickets</h2>
        <table>
            <thead>
                <tr>
                    <th>Ticket ID</th>
                    <th>Subject</th>
                    <th>Status</th>
                    <th>Priority</th>
                    <th>Assignee</th>
                    <th>Created At</th>
                    <th>Actions</th>  <!-- New column -->
                </tr>
            </thead>
            <tbody>
                <tr v-for="ticket in tickets" :key="ticket.id">
                    <td>{{ ticket.id }}</td>
                    <td><RouterLink :to="`/tickets/view/${ticket.id}`">{{ ticket.subject }}</RouterLink></td>
                    <td>{{ ticket.status }}</td>
                    <td>{{ ticket.priority }}</td>
                     <td>{{ ticket.assignedTo }}</td>
                    <td>{{ formatDate(ticket.createdAt) }}</td>


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
                     :class="['message', message.sender === currentUser ? 'sent' : 'received']">
                    <div class="message-content">
                        <p>{{ message.content }}</p>
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

    </div>

</template>

<script>
import { ref, onMounted, nextTick ,computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../../stores/auth';
//import MainTemplate from './MainTemplate.vue';
import { useToast } from 'vue-toastification'

export default {
    name: 'SubmitTicket',

     components: {
   //MainTemplate
  },
    setup() {
        const auth = useAuthStore();
        const currentUser = computed(() => auth.user?.email);

          function formatDate(dateString) {
            if (!dateString) return '';
            // Convert to valid ISO if using space instead of T
            const cleaned = dateString.replace(' ', 'T');
            const date = new Date(cleaned);
            if (isNaN(date.getTime())) {
                return 'Invalid Date';
            }
        return date.toLocaleString(); // e.g., "7/15/2025, 9:44 AM"
        }

        const toast = useToast()
        const router = useRouter();
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
        const issueTypes = ref([]);



        const handleSubmit = async () => {
            try {
                const token = localStorage.getItem('token');
                const response = await fetch('/api/tickets/create', {
                    method: 'POST',
                    headers: {
                        "Authorization": "Bearer "+ token,
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

                toast.success('Ticket submitted successfully!')


                fetchMyTickets(); // Refresh the ticket list
            } catch (error) {
                errorMessage.value = `Error submitting ticket: ${error.message}`;
                successMessage.value = '';
                toast.error('Something went wrong!')

            }
        };


        const fetchMyTickets = async () => {
            try {
                const token = localStorage.getItem('token');

                const response = await fetch('/api/myTickets',
                     {
                    headers: {
                        "Authorization": "Bearer "+ token,
                         "Content-Type": "application/json"
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
                const token = localStorage.getItem('token');
                const response = await fetch(`/api/tickets/${ticketId}/messages`,
                 {
                    headers: {
                        "Authorization": "Bearer "+ token,
                         "Content-Type": "application/json"
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
                const response = await fetch(`/api/tickets/${selectedTicketId.value}/message`, {
                    method: 'POST',
                    headers: {
                         'Authorization': 'Bearer '+ token,
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
            auth.logout();
            router.push('/login');
        };



    const fetchIssueTypes = async () => {
      try {
        const token = localStorage.getItem('token');
           if (!token) return;

        const response = await fetch('/api/issue-types',
        {
                    headers: {
                        "Authorization": "Bearer "+ token,
                         "Content-Type": "application/json"
                    }
                });
        if (!response.ok) throw new Error('Failed to fetch Issues');
        issueTypes.value = await response.json();
      } catch (error) {
        console.error('Error fetching issue types:', error);
        toast.error('Error fetching issue types');
      }
    };

        onMounted(() => {
            const token = auth.token;
            if(!token){
                handleLogout()
            }
            fetchMyTickets();
            fetchIssueTypes()
            // Return cleanup function
            return () => {
                stopMessagePolling();
            };
        });

        return {
            subject, description, priority,
            type, // Add type here
            successMessage,
            errorMessage,
            tickets,
            handleSubmit,
            showChat,
            selectedTicketId,
            newMessage,
            chatMessages,
            sendMessage,
            handleLogout,
            openChat,
            closeChat ,
            formatDate,
            fetchMyTickets,
            issueTypes,
            fetchIssueTypes,currentUser

        };
    }
};
</script>

<style scoped>
/* Main container classes */
/*.SubmitTicket,*/
.my-tickets,
.ticket-chatbox {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}


.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: bold;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}



.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
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
    box-sizing: border-box;
}


.SubmitTicket {
  width: 100%;
  max-width: 500px;
  padding: 10px;
  display: flex;
  margin: auto;
  box-sizing: border-box;

}

.add-ticket-form {
  background-color: #f9f9f9;
  border-radius: 10px;
  padding: 30px;
  border: #DDD solid thin;
/* box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);*/
  width: 100%;
}


/* Table styling */
.tickets-list ,table {
  width: 100%;
  border-collapse: collapse;


}
.tickets-list th,
.tickets-list td {
  /*border: 1px solid #ddd;*/
   border-collapse: collapse;
  padding: 8px;
}

/* Responsive table for mobile */
@media (max-width: 768px) {
  .tickets-list table,
  .tickets-list thead,
  .tickets-list tbody,
  .tickets-list th,
  .tickets-list td,
  .tickets-list tr {
    display: block;
  }
  .tickets-list thead tr {
    display: none;
  }
  .tickets-list tr {
    margin-bottom: 20px;
    border-bottom: 2px solid #ddd;
  }
  .tickets-list td {
    padding-left: 20px;
    position: relative;
    text-align: left;
  }
  .tickets-list td::before {
    content: attr(data-label);
    position: absolute;
    left: 15px;
    font-weight: bold;
  }

   .chat-modal {
    bottom: 8px;
    right: 8px;
    width: 95%;
    height: 75%;
    box-sizing: border-box;
  }
}
</style>
