<template>
  <div class="flex px-4 mt-20">
    <div class="">
      <button
        v-if="store.data.canAddBots"
        @click="toggleModal"
        class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        Пригласить в организацию
      </button>
      <div class="flex justify-evenly flex-wrap">
        <div
          v-for="(user, index) in store.data.users"
          :key="index"
          class="mt-4 p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
        >
          <div class="flex items-center">
            {{ JSON.stringify(user) }}
            <button
              @click="toggleModal"
              class="ml-4 mb-2 p-1 text-red-600 bg-red-100 hover:bg-red-200 rounded-md font-medium flex"
            >
              Редактировать
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <modal-add-user
    :isShown="isShowModal"
    :closeModal="closeModal"
    :id="props.id"
  />
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'
import ModalAddUser from "@/components/ModalAddUser.vue";

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
  api.getUsers(props.id).then((data) => {
    store.data.users = data
    if (store.data.users?.length === 0) {
      store.data.canAddBots = true
    }
  })
})
</script>
