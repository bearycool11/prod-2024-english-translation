<template>
  <div class="flex flex-col mt-20 w-full">
    <h1
      class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
    >
      Экстренная кнопка
    </h1>
    <button @click="callEmergency" class="dark:text-white">Заблокировать отложенные посты</button>
    <button @click="recallEmergency" class="dark:text-white">Разблокировать  отложенные посты</button>
  </div>
</template>

<script setup>

import { api } from '@/logic/api.js'
const props = defineProps({
  id: {
    type: String
  },
})

function callEmergency() {
    api.callEmergency(props.id, ).then()
}

function recallEmergency() {
    api.recallEmergency(props.id, ).then()
}
</script>
