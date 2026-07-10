import EditInstitution from "./pages/EditInstitution.vue"
import institutionManagement from './pages/institutionManagement.vue'

export default [
  {
    name: "edit-institution",
    path: "edit/:id",
    component: EditInstitution
  },
  {
    name: "institution-management",
    path: "manage",
    component:institutionManagement
  }
]
