<template>
  <div class="flex" v-if="profile.name">
    <RouterView class="flex" v-if="$route.name != 'AllOrganization'" />
    <nav
      class="bg-white border-gray-200 lg:px-6 sm:px-8 px-2 py-2.5 dark:bg-gray-800 w-screen shrink absolute z-50 shadow-md top-0"
    >
      <div class="flex md:content-center justify-between items-center max-w-screen">
        <div class="flex items-center mr-10">
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
          <a
            class="cursor-pointer flex text-nowrap items-center font-medium text-xl max-w-80 dark:text-neutral-200"
            href="/"
          >
            {{ profile.name }}
          </a>
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
        <div class="flex items-center" v-if="$route.name == 'AllOrganization'">
          <button
            @click="toggleModal"
            class="flex items-center justify-between text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-2 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="button"
          >
            <svg
              class="w-4 h-4 flex text-gray-800 dark:text-white"
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
        <div class="flex w-full justify-end">
          <button class="flex" @click="toggleDark()">
            <svg
              v-if="!isDark"
              class="w-6 h-6 text-gray-800 dark:text-white"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M11.675 2.015a.998.998 0 0 0-.403.011C6.09 2.4 2 6.722 2 12c0 5.523 4.477 10 10 10 4.356 0 8.058-2.784 9.43-6.667a1 1 0 0 0-1.02-1.33c-.08.006-.105.005-.127.005h-.001l-.028-.002A5.227 5.227 0 0 0 20 14a8 8 0 0 1-8-8c0-.952.121-1.752.404-2.558a.996.996 0 0 0 .096-.428V3a1 1 0 0 0-.825-.985Z"
                clip-rule="evenodd"
              />
            </svg>
            <svg
              v-else
              class="w-6 h-6 text-gray-800 dark:text-white"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M13 3a1 1 0 1 0-2 0v2a1 1 0 1 0 2 0V3ZM6.343 4.929A1 1 0 0 0 4.93 6.343l1.414 1.414a1 1 0 0 0 1.414-1.414L6.343 4.929Zm12.728 1.414a1 1 0 0 0-1.414-1.414l-1.414 1.414a1 1 0 0 0 1.414 1.414l1.414-1.414ZM12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm-9 4a1 1 0 1 0 0 2h2a1 1 0 1 0 0-2H3Zm16 0a1 1 0 1 0 0 2h2a1 1 0 1 0 0-2h-2ZM7.757 17.657a1 1 0 1 0-1.414-1.414l-1.414 1.414a1 1 0 1 0 1.414 1.414l1.414-1.414Zm9.9-1.414a1 1 0 0 0-1.414 1.414l1.414 1.414a1 1 0 0 0 1.414-1.414l-1.414-1.414ZM13 19a1 1 0 1 0-2 0v2a1 1 0 1 0 2 0v-2Z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </nav>
  </div>
  <RouterView class="flex mt-20" v-if="$route.name == 'AllOrganization'" />
  <ModalNewOrganization v-if="isShowModal" :isShown="isShowModal" :closeModal="closeModal" />
  <ModalLogout :isShown="isShowModalLogout" :closeModal="closeLogout" />
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import { api } from '@/logic/api.js' // import your API module here
import { store, toggleSidebar } from '@/store/toggleSidebar.js'
import { useDark, useToggle } from '@vueuse/core' // import your store module here
import ModalNewOrganization from '../components/ModalNewOrganization.vue'
import ModalLogout from '../components/ModalLogout.vue'

const isShowModal = ref()
const isShowModalLogout = ref()
const organizations = ref([])
const profile = ref('')

const isDark = useDark()
const toggleDark = useToggle(isDark)

const toggleModal = () => {
  isShowModal.value = !isShowModal.value
}

const toggleLogout = () => {
  isShowModalLogout.value = !isShowModalLogout.value
}

const closeModal = () => {
  isShowModal.value = false
}

const closeLogout = () => {
  isShowModalLogout.value = false
}

onBeforeMount(() => {
  api.getProfile().then((profileData) => {
    store.auth.username = profileData.name
    store.auth.id = profileData.id
    profile.value = profileData
  })
  api.getOrganizations().then((organizationsData) => {
    organizations.value = organizationsData
  })
})
</script>
