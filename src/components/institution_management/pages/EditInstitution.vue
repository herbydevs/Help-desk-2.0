<template>



    <!-- Add User Form -->
    <div class="form-container">

      <form class="add-form" @submit.prevent="handleEditInstitution">
         <h3>Edit Institution</h3>
          <div class="form-group">
          <input type="hidden" id="id" v-model="existingInstitution.id" required />
        </div>
          <div class="form-group">
          <label for="name">Name:</label>
          <input type="name" id="name" v-model="existingInstitution.name" required />
        </div>
        <div class="form-group">
          <label for="address">Address:</label>
          <input type="text" id="address" v-model="existingInstitution.address" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="existingInstitution.email" required />
        </div>
        <div class="form-group">
          <label for="phoneNumber">Telephone:</label>
          <input type="text" id="phoneNumber" v-model="existingInstitution.phoneNumber" required />
        </div>

        <div class="button-group">
        <button type="submit"><i class="pi pi-check" style="font-size: 1rem"></i>Save</button>
        <RouterLink to="/institution-management"><button><i class="pi pi-ban" style="font-size: 1rem"></i>Cancel</button></RouterLink>
      </div>
      </form>
    </div>

</template>

<script>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  //import MainTemplate from './MainTemplate.vue';
  import { useToast } from 'vue-toastification'

export default {
  name: 'InstitutionManagement',
   components: {
    //MainTemplate
  },
  setup() {
    const toast = useToast();
    const route = useRoute();
    const router = useRouter();
    const instId = route.params.id;
    const existingInstitution = ref({
      name: '',
      address: '',
      email: '',
      telephone: ''
    });





  const fetchInstitution = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/institutions/${instId}`,
        {
                    headers: {
                        "Authorization": "Bearer "+ token,
                         "Content-Type": "application/json"
                    }
                });
        if (!response.ok) throw new Error('Failed to fetch institution');
        existingInstitution.value = await response.json();

      } catch (error) {
        console.error('Error fetching institution:', error);
        toast.error('Error fetching institution')
      }
    };




   const handleEditInstitution = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/institutions/edit/${instId}`, {
          method: 'PUT',
          headers: {
             'Authorization': 'Bearer '+ token,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(existingInstitution.value)
        });
        if (!response.ok) throw new Error('Failed to edit institution');
        toast.success('Institution edited successfully');
          router.push('/institution-management');
      } catch (error) {
        console.error('Error editing institution:', error);
        toast.error('Error editing institution');
      }
    };


    onMounted(fetchInstitution);

    return {
      instId,
      existingInstitution,
      fetchInstitution ,
      handleEditInstitution
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
  margin-right: 4px;
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


.button-group{
  display: flex;
}
@media (max-width: 768px) {
.button-group {
    flex-direction: column;
  }
}

</style>
