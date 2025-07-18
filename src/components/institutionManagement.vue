<template>
  <div class="user-management">
    <h2>Institution Management</h2>

    <!-- Add User Form -->
    <div class="add-institution-form">
      <h3>Add New Institution</h3>
      <form @submit.prevent="handleAddInstitution">
          <div class="form-group">
          <label for="name">Name:</label>
          <input type="name" id="name" v-model="newInstitution.name" required />
        </div>
        <div class="form-group">
          <label for="address">Address:</label>
          <input type="text" id="address" v-model="newInstitution.address" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="newInstitution.email" required />
        </div>
        <div class="form-group">
          <label for="phoneNumber">Telephone:</label>
          <input type="text" id="phoneNumber" v-model="newInstitution.phoneNumber" required />
        </div>
       
        
      
        <button type="submit">Add</button>
      </form>
    </div>

    <!-- User List -->
    <div class="institution-list">
      <h3>Institutions</h3>
      <table>
        <thead>
          <tr>
             <th>Name</th>
            <th>Address</th>
            <th>Email</th>
            <th>Telephone</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="institution in institutions" :key="institution.id">
             <td>{{ institution.name }}</td>
            <td>{{ institution.address }}</td>
            <td>
             {{ institution.email }}
            </td>
            <td>
            {{ institution.phoneNumber }}
             
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
  name: 'InstitutionManagement',
  setup() {
    const users = ref([]);
    const institutions = ref([]);
    const newUser = ref({
      name: '',
      email: '',
      password: '',
      isAdmin: false,
      issueType: 'payment'
    });

     const newInstitution = ref({
      name: '',
      address: '',
      email: '',
      telephone: ''
    });


    /*const fetchUsers = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/users');
        if (!response.ok) throw new Error('Failed to fetch users');
        users.value = await response.json();
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    };*/

    const fetchInstitutions = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/institutions');
        if (!response.ok) throw new Error('Failed to fetch institutions');
        institutions.value = await response.json();
      } catch (error) {
        console.error('Error fetching institutions:', error);
      }
    };
/*
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
    */

    
    const handleAddInstitution = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/institutions/create', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(newInstitution.value)
        });
        if (!response.ok) throw new Error('Failed to add institution');
        await fetchUsers();
        // Reset form
        newInstitution.value = {
          name:'',
          address: '',
          email: '',
          phoneNumber: ''
        };
      } catch (error) {
        console.error('Error adding institution:', error);
      }
    };

    /*
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
*/
/*
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
*/
    onMounted(fetchInstitutions);

    return {
      users,
      institutions,
      newUser,
      newInstitution,
      handleAddInstitution  
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

.add-institution-form {
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