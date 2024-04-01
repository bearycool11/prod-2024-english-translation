<template>
  <div class="flex">
    <RouterView class="flex" v-if="$route.name != 'AllOrganization'" />
    <nav class="bg-white border-gray-200 lg:px-6 sm:px-8 px-2 py-2.5 dark:bg-gray-800 w-full">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <div class="flex items-center">
          <button
            @click="toggleSidebar"
            v-if="$route.name != 'AllOrganization'"
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
          <button class="cursor-pointer flex items-center font-medium text-xl">
            {{ profile.name }}
          </button>
          <button
            class="ml-3 bg-red-100 p-[2px] hover:bg-red-200 rounded flex"
            @click="toggleLogout"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
            >
              <path
                d="M16 12L4 12M16 12L12 16M16 12L12 8M15 4H17C18.6569 4 20 5.34315 20 7V17C20 18.6569 18.6569 20 17 20H15"
                stroke="#FF4A4A"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </div>
        <div class="flex items-center lg:order-2" v-if="$route.name == 'AllOrganization'">
          <button
            @click="toggleModal"
            class="flex items-center justify-between text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="button"
          >
            <svg
              class="w-6 h-6 text-gray-800 dark:text-white mr-1"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="#FFF"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 12h14m-7 7V5"
              />
            </svg>
            <p class="md:flex hidden">Организация</p>
          </button>
        </div>
        <div class="flex items-center lg:order-2" v-if="$route.name != 'AllOrganization'">
          <a
            href="/"
            class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="button"
          >
            Все организации
          </a>
        </div>
      </div>
    </nav>
  </div>
  <RouterView class="flex" v-if="$route.name == 'AllOrganization'" />
  <ModalNewOrganization :isShown="this.isShowModal" :closeModal="closeModal" />
  <ModalLogout :isShown="isShowModalLogout" :closeModal="closeLogout" />
</template>

<script>
import { store, toggleSidebar } from '@/store/toggleSidebar.js'
import ModalNewOrganization from '../components/ModalNewOrganization.vue'
import ModalLogout from '../components/ModalLogout.vue'
import { defineComponent } from 'vue'
import { api } from '@/logic/api.js'

export default defineComponent({
  components: { ModalNewOrganization, ModalLogout },
  async beforeMount() {
    api.getProfile().then((profile) => {
      this.profile = profile
    })
    api.getOrganizations().then((organizations) => {
      store.data.organizations = organizations
    })
  },
  data() {
    return {
      isShowModal: false,
      isShowModalLogout: false,
      organizations: [],
      profile: ''
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
    toggleLogout() {
      if (this.isShowModalLogout) {
        this.isShowModalLogout = false
      } else {
        this.isShowModalLogout = true
      }
    },
    closeModal() {
      this.isShowModal = false
    },
    closeLogout() {
      this.isShowModalLogout = false
    }
  }
})
</script>
