<template>
  <div class="flex px-4 mt-20">
    <div class="">
      <button
      @click="toggleModal"
        class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        Добавить бота
      </button>
    </div>
  </div>
  <ModalAddBots  :isShown="isShowModal" :closeModal="closeModal" />
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/logic/api.js'
import ModalAddBots from '@/components/ModalAddBots.vue'

const bots = ref()
const isShowModal = ref()

function toggleModal() {
      if (isShowModal.value) {
        isShowModal.value = false
      } else {
        isShowModal.value = true
      }
}

function closeModal() {
      isShowModal.value = false
}

const props = defineProps({
  id: {
    type: String,
    default: '1'
  }
})
onMounted(() => {
  api.getOrganizationBots(props.id).then((data) => {
    bots.value = data
  })
})
</script>
