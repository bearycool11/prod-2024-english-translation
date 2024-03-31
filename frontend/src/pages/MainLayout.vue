<template>
  <div class="flex">
    <RouterView />
    <nav class="bg-white border-gray-200 px-8 lg:px-6 py-2.5 dark:bg-gray-800 w-full h-16">
      <div class="flex flex-wrap justify-around items-center mx-auto max-w-screen-xl">
        <a class="flex items-center font-medium text-xl"> Username </a>
        <div class="flex items-center lg:order-2">
          <button
            @click="toggleModal()"
            class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            type="button"
          >
            Add org
          </button>
        </div>
      </div>
    </nav>
  </div>
  <ModalNewOrganization :isShown="this.isShowModal" :closeModal="closeModal"/>
</template>

<script>
import ModalNewOrganization from '../components/ModalNewOrganization.vue'
import { defineComponent } from 'vue'

export default defineComponent({
  components: {ModalNewOrganization},
  data() {
    return {
      isShowModal: false
    }
  },
  methods: {
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
