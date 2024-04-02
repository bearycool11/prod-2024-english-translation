<template>
  <div class="flex mt-20 w-full">
    <div class="w-full px-4">
      <div class="grid md:grid-cols-3 sm:grid-cols-2 gap-2 w-full mb-4">
        <div
          v-for="(post, index) in state.posts"
          :key="index"
          class="p-6 min-w-sm w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 max-w-md"
        >
          <h5
            class="mb-2 mr-2 text-lg text-left font-bold text-wrap max-w-md truncate tracking-tight text-gray-900 dark:text-white"
          >
            {{ post.content }}
          </h5>
          <div class="flex gap-1 mt-auto flex-wrap">
            <div class="flex">
              <p class="text-wrap text-left">{{ date(post.planned_time) }}</p>
            </div>

            <div class="flex gap-1 mt-1 flex-wrap">
              <div class="p-2 bg-blue-100 rounded-md">{{ post.is_approved }}</div>
              <div class="p-2 bg-blue-100 rounded-md">{{ post.sent_status }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'

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

const date = (isoString) => {
  // Check if the input is null
  if (isoString === null) {
    return ''
  }

  // Parse the ISO string into a Date object
  const date = new Date(isoString)

  // Format the date according to the current locale and timezone
  const formattedDate = new Intl.DateTimeFormat('ru-RU', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short'
  }).format(date)

  // Extract the formatted date and time parts
  const [dayMonthYear, timeWithTimezone] = formattedDate.split(', ')

  // Return the formatted date with the timezone included
  return 'Запланирован ' + dayMonthYear + ' ' + timeWithTimezone
}
</script>
