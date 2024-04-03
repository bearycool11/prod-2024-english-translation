<template>
  <div class="flex px-4 mt-20">
    <div class="">
      <button
        v-if="
          store.data.canAddBots === false &&
          store.auth.permissions.some((obj) => obj.name === 'admin' || obj.name === 'owner')
        "
        @click="toggleModal"
        class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        Добавить канал
      </button>
      <div v-if="store.data.canAddBots === true">
        <p class="flex px-6 py-2 rounded-md bg-neutral-100 w-auto">Сначала добавьте бота</p>
      </div>
      <div class="flex justify-evenly flex-wrap"></div>

      <div class="flex justify-evenly flex-wrap">
        <div
          v-for="(channel, index) in store.data.channels"
          :key="index"
          class="mt-4 mx-2 p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
        >
          <div class="flex items-center">
            <h5
              class="mb-2 text-2xl font-bold truncate tracking-tight text-gray-900 dark:text-white"
            >
              {{ channel.name }}
            </h5>
            <button
              v-if="
                store.auth.permissions.some((obj) => obj.name === 'admin' || obj.name === 'owner')
              "
              @click="deleteChannel(channel.id)"
              class="ml-4 mb-2 p-1 text-red-600 bg-red-100 hover:bg-red-200 rounded-md font-medium flex"
            >
              Удалить
            </button>
          </div>
          <p class="truncate max-w-60 w-auto dark:text-neutral-200">{{ channel.telegram_id }}</p>
        </div>
      </div>
    </div>
  </div>
  <ModalAddChannels
  v-if="isShowModal"
    :isShown="isShowModal"
    :closeModal="closeModal"
    :id="props.id"
    :botId="store.auth.bot_id"
    :bot_token="store.data.bots[0]?.bot_token"
  />
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/logic/api.js'
import ModalAddChannels from '@/components/ModalAddChannels.vue'
import { store } from '@/store/index.js'

const isShowModal = ref()

function toggleModal() {
  if (isShowModal.value) {
    isShowModal.value = false
  } else {
    isShowModal.value = true
  }
}

onMounted(() => {
  api.getOrganizationBots(props.id).then((data) => {
    store.data.bots = data
    if (store.data.bots?.length === 0) {
      store.data.canAddBots = true
      return
    }
    store.auth.bot_id = store.data.bots[0]?.bot_id 
  })

  api.getChannels(props.id).then((channels) => {
    store.data.channels = channels
  })
 
})
function closeModal() {
  isShowModal.value = false
}

const props = defineProps({
  id: {
    type: String
  }
})

function deleteChannel(ch_id) {

  api.deleteChannels(props.id, ch_id).then(() => {
    api.getChannels(props.id).then((channels) => {
      store.data.channels = channels
    })
  })
}
</script>
