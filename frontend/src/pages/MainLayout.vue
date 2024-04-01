<template>
  <div class="flex">
    <RouterView />
    <nav class="bg-white border-gray-200 lg:px-6 sm:px-8 px-2 py-2.5 dark:bg-gray-800 w-full">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <div class="flex items-center">
          <button
            @click="toggleSidebar"
            v-if="$route.name === 'OrganizationPage'"
            type="button"
            class="text-gray-400 sm:hidden bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 ms-auto inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white"
            data-modal-toggle="crud-modal"
          >
            <svg
              class="w-6 h-6 text-gray-800 dark:text-white"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-width="2"
                d="M5 7h14M5 12h14M5 17h14"
              />
            </svg>
          </button>
          <a class="flex items-center font-medium text-xl"> Username </a>
        </div>
        <div class="flex items-center lg:order-2">
          <button
            @click="toggleModal"
            class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="button"
          >
            Добавить организацию
          </button>
        </div>
      </div>
    </nav>
  </div>
  <div class="flex justify-evenly mt-10 flex-wrap" v-if="organizations">
    <a
      v-for="(organization, index) in organizations"
      :key="index"
      :href="'/organization/' + organization.id"
      class="block max-w-sm mt-4 p-6 md:w-full w-52 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
    >
      <h5 class="mb-2 text-2xl font-bold truncate tracking-tight text-gray-900 dark:text-white">
        {{ organization.name }}
      </h5>
      <p class="font-normal truncate text-gray-700 dark:text-gray-400">
        {{ organization.description }}
      </p>
    </a>
  </div>
  <div v-else class="flex justify-center mt-10 w-full">
    <p class="flex px-6 py-2 rounded-md bg-neutral-100 w-auto">У вас еще нет организаций</p>
  </div>
  <ModalNewOrganization :isShown="this.isShowModal" :closeModal="closeModal" />
</template>

<script>
import { toggleSidebar } from '@/store/toggleSidebar.js'
import ModalNewOrganization from '../components/ModalNewOrganization.vue'
import { defineComponent } from 'vue'
import { api } from '@/logic/api.js'

export default defineComponent({
  components: { ModalNewOrganization },
  async beforeMount() {
    api.getOrganizations().then((organizations) => {
      this.organizations = organizations
    })
  },
  data() {
    return {
      isShowModal: false,
      organizations: []
    }
  },
  methods: {
    toggleSidebar,
    toggleModal() {
      if (this.isShowModal) {
        this.isShowModal = false
      } else {
        this.isShowModal = true
      }
    },
    closeModal() {
      this.isShowModal = false
    }
  }
})
</script>
