<template>
  <div class="flex mt-24 w-full">
    <div class="fixed dark:bg-gray-800 w-screen"></div>
    <div class="w-full px-4 dark:bg-gray-800 shrink flex">
      <div class="flex dark:bg-gray-800">
        <div class="flex flex-col items-center justify-between">
          <h1
            class="text-3xl mb-6 font-bold leading-tight tracking-tight text-gray-900 dark:text-white"
          >
            История постов
          </h1>
          <div class="grid grid-cols-1 gap-2 w-full mb-4 max-w-2xl lg:w-screen">
            <history-post v-for="(post, index) in state.posts" :key="index" :post="post" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '@/logic/api.js'
//import { store } from '@/store/index.js'
import HistoryPost from '@/components/HistoryPost.vue'

const state = reactive({
  isShowModal: false,
  targetPost: {},
  creation: false,
  posts: []
})

onMounted(() => {
  api.getHistory(props.id).then((data) => {
    state.posts = data.reverse()
    state.targetPost = {}
  })
})

const props = defineProps({
  id: {
    type: String
  }
})

// const date = (isoString) => {
//   // Check if the input is null
//   if (isoString === null) {
//     return ''
//   }

//   // Parse the ISO string into a Date object
//   const date = new Date(isoString)

//   // Format the date according to the current locale and timezone
//   const formattedDate = new Intl.DateTimeFormat('ru-RU', {
//     year: 'numeric',
//     month: '2-digit',
//     day: '2-digit',
//     hour: '2-digit',
//     minute: '2-digit',
//     timeZoneName: 'short'
//   }).format(date)

//   // Extract the formatted date and time parts
//   const [dayMonthYear, timeWithTimezone] = formattedDate.split(', ')

//   // Return the formatted date with the timezone included
//   return 'Запланирован ' + dayMonthYear + ' ' + timeWithTimezone
// }
</script>
