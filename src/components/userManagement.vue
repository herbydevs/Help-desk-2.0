<template>
  <div class="user-management">
    <h2>User Management</h2>

    <!-- Add User Form -->
    <div class="add-user-form">
      <h3>Add New User</h3>
      <form @submit.prevent="handleAddUser">
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="newUser.email" required />
        </div>
            <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="newUser.name" required />
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="newUser.password" required />
        </div>
        <div class="form-group">
          <label for="role">Role:</label>
          <select id="role" v-model="newUser.isAdmin">
            <option :value="false">User</option>
            <option :value="true">Admin</option>
          </select>
        </div>
        <div class="form-group" v-if="newUser.isAdmin">
          <label for="issueType">Issue Type:</label>
          <select id="issueType" v-model="newUser.issueType">
            <option value="payment">Payment</option>
            <option value="service">Service</option>
            <option value="account">Account</option>
          </select>
        </div>
        <button type="submit">Add User</button>
      </form>
    </div>

    <!-- User List -->
    <div class="user-list">
      <h3>Users</h3>
      <table>
        <thead>
          <tr>
             <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Issue Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
             <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>
              <select v-model="user.isAdmin" @change="handleRoleChange(user)">
                <option :value="false">User</option>
                <option :value="true">Admin</option>
              </select>
            </td>
            <td>
              <select 
                v-if="user.isAdmin" 
                v-model="user.issueType" 
                @change="handleIssueTypeChange(user)"
              >
                <option value="payment">Payment</option>
                <option value="service">Service</option>
                <option value="account">Account</option>
              </select>
              <span v-else>-</span>
            </td>
            <td>
              <button class="delete-btn" @click="handleDeleteUser(user.id)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'UserManagement',
  setup() {
    const users = ref([]);
    const newUser = ref({
      name: '',
      email: '',
      password: '',
      isAdmin: false,
      issueType: 'payment'
    });

    const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/users');
        if (!response.ok) throw new Error('Failed to fetch users');
        users.value = await response.json();
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };

    const handleAddUser = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/users/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newUser.value)
        });
        if (!response.ok) throw new Error('Failed to add user');
        await fetchUsers();
        // Reset form
        newUser.value = {
          name:'',
          email: '',
          password: '',
          isAdmin: false,
          issueType: 'payment'
        };
      } catch (error) {
        console.error('Error adding user:', error);
      }
    };

    const handleDeleteUser = async (userId) => {
      if (!confirm('Are you sure you want to delete this user?')) return;
      try {
        const response = await fetch(`http://localhost:8080/api/users/${userId}`, {
          method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete user');
        await fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    };

    const handleRoleChange = async (user) => {
      try {
        const response = await fetch(`http://localhost:8000/api/users/${user.id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            isAdmin: user.isAdmin,
            issueType: user.issueType
          })
        });
        if (!response.ok) throw new Error('Failed to update user role');
        await fetchUsers();
      } catch (error) {
        console.error('Error updating user role:', error);
      }
    };

    const handleIssueTypeChange = async (user) => {
      try {
        const response = await fetch(`http://localhost:8000/api/users/${user.id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            issueType: user.issueType
          })
        });
        if (!response.ok) throw new Error('Failed to update issue type');
        await fetchUsers();
      } catch (error) {
        console.error('Error updating issue type:', error);
      }
    };

    onMounted(fetchUsers);

    return {
      users,
      newUser,
      handleAddUser,
      handleDeleteUser,
      handleRoleChange,
      handleIssueTypeChange
    };
  }
};
</script>

<style scoped>
.user-management {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.add-user-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.delete-btn {
  background: #dc3545;
}

.delete-btn:hover {
  background: #c82333;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f8f9fa;
}
</style>