<template>
  <div class="flex flex-col px-4 mt-20 w-full">
    <button
      @click="toggleModal"
      class="block mb-3 w-60 max-w-full text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
    >
      Пригласить в организацию
    </button>
    <div class="grid md:grid-cols-3 sm:grid-cols-2 gap-2 w-full">
      <div
        v-for="(user, index) in store.data.users"
        :key="index"
        class="w-full flex flex-col p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="flex flex-col h-full">
          <div class="flex justify-between">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ user.user.name }}
          </h3>
          <h3 class="text-lg mb-2 font-semibold text-gray-500 dark:text-neutral-400">
            {{ user.user.id }}
          </h3>
        </div>
        <div class="flex flex-wrap mb-4">
          <h3
            v-for="(right, index) in user.rights"
            class="text-md mx-2 font-normal text-gray-900 dark:text-white"
            :key="index"
          >
            {{ convertPermissions(right.name) || convertPermissions(right) }}
          </h3>
        </div>
          <button
            v-if="allowEdit(user)"
            @click="() => toggleModal(user)"
            class="block mt-auto text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
          >
            Редактировать
          </button>
          <div
            class="text-lg mt-auto font-semibold text-blue-400 dark:text-white"
            v-if="store.auth.id === user.user.id"
          >
            Это вы!
          </div>
        </div>
      </div>
    </div>
  </div>
  <modal-add-user
    v-if="isShowModal"
    :isShown="isShowModal"
    :closeModal="closeModal"
    :id="props.id"
    :initial-user="state.targetUser"
  />
</template>
<script setup>
import { onMounted, reactive, ref, computed } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'
import ModalAddUser from '@/components/ModalAddUser.vue'
import convertPermissions  from '../logic/converter.js'

const isShowModal = ref()
const allowEdit = computed(
  () => (user) =>
    (store.auth.id !== user.user.id &&
      user.rights.some((obj) => obj.name !== 'admin' && obj.name !== 'owner')) ||
    (store.auth.permissions.some((obj) => obj.name === 'owner') && store.auth.id !== user.user.id)
)

const state = reactive({
  targetUser: {}
})

function toggleModal(user) {
  if (isShowModal.value) {
    state.targetUser = {}
    isShowModal.value = false
  } else {
    if (user) {
      state.targetUser = user
    }
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
    store.data.users = data.users
  })
})
</script>
