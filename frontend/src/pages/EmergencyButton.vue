<template>
  <div
    class="flex flex-col mt-10 p-10 w-full"
    v-if="store.auth.permissions.some((obj) => obj.name === 'admin' || obj.name === 'owner')"
  >
    <h1
      class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
    >
      Экстренная кнопка
    </h1>
    <div class="flex mt-8 flex-wrap items-center">
      <button
        @click="callEmergency"
        class=" mx-4 mt-2 bg-red-200 text-red-600 p-2 rounded-md hover:bg-red-300"
      >
        Заблокировать отложенные посты
      </button>
      <button
        @click="recallEmergency"
        class="mx-4 mt-2 bg-red-200 text-red-600 p-2 rounded-md hover:bg-red-300"
      >
        Разблокировать отложенные посты
      </button>
    </div>
    <p class="mt-4 ml-4 dark:text-white">{{ text.error }}</p>
  </div>
</template>

<script setup>
import { api } from '@/logic/api.js'
import { reactive } from 'vue'
import { store } from '../store/index.js'
const props = defineProps({
  id: {
    type: String
  }
})

const text = reactive({ error: '' })
function callEmergency() {
  api
    .callEmergency(props.id)
    .then((text.error = ''))
    .catch(() => {
      text.error = 'Посты уже заблокированы'
    })
}

function recallEmergency() {
  api
    .recallEmergency(props.id)
    .then((text.error = ''))
    .catch(() => {
      text.error = 'Посты уже разблокированы'
    })
}
</script>
