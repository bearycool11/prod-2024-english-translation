<template>
  <div class="flex px-4 mt-20">
    <div class="">
      <button
        v-if="store.data.canAddBots"
        @click="toggleModal"
        class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        Добавить телеграм бота
      </button>
      <div class="flex justify-evenly flex-wrap">
        <div
          v-for="(bot, index) in store.data.bots"
          :key="index"
          class="mt-4 p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
        >
          <div class="flex items-center">
            <h5
              class="mb-2 text-2xl font-bold truncate tracking-tight text-gray-900 dark:text-white"
            >
              Телеграм бот {{ bot.bot_id }}
            </h5>
            <button
              @click="deleteBot"
              class="ml-4 mb-2 p-1 text-red-600 bg-red-100 hover:bg-red-200 rounded-md font-medium flex"
            >
              Удалить
            </button>
          </div>
          <p class="truncate max-w-60 w-auto dark:text-neutral-200">
            {{ replaceAfterColon(bot.bot_token) }}
          </p>
        </div>
      </div>
    </div>
  </div>
  <ModalAddBots :isShown="isShowModal" :closeModal="closeModal" :id="props.id" />
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/logic/api.js'
import ModalAddBots from '@/components/ModalAddBots.vue'
import { store } from '@/store/index.js'

const isShowModal = ref()
function replaceAfterColon(str) {
  const colonIndex = str.indexOf(':')

  if (colonIndex === -1) {
    return str
  }

  const beforeColon = str.substring(0, colonIndex + 1)
  const afterColon = str.substring(colonIndex + 1)

  const replacedAfterColon = afterColon.replace(/./g, '*')

  return beforeColon + replacedAfterColon
}

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

function deleteBot() {
  return
}
onMounted(() => {
  api.getOrganizationBots(props.id).then((data) => {
    store.data.bots = data
   
    if (store.data.bots.length === 0) {
      store.data.canAddBots = true
    }
  })
})
</script>
