<template>
  <div
    class="p-6 flex flex-col h-full w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700"
  >
    <h3 class="mb-5 text-lg font-bold text-gray-500 dark:text-gray-400">#{{ props.post.id }}</h3>
    <div
      v-if="!isPostPublic"
      class="mb-2 text-lg p-3  border-gray-300 border-[1px] rounded-md font-normal text-gray-500 dark:text-gray-400"
      role="alert"
    >
      {{ props.post.content }}
    </div>
    <div v-if="isPostPublic" class="pb-5 md:flex" :id="`${props.post.id}-post`"></div>
    <div
      v-if="!isPostPublic"
      class="mb-2 p-4 text-sm text-red-800 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400"
      role="alert"
    >
      <span class="font-medium">Пост в приватном канале</span>
    </div>
    <div class="flex gap-1 mt-auto flex-wrap flex-col">
      <div class="flex">
        <p class="text-wrap text-left dark:text-neutral-200">{{ date(post.planned_time) }}</p>
      </div>
      <div class="flex gap-1 mt-1 flex-wrap flex-col">
        <div class="p-2 bg-blue-100 rounded-md">{{ props.post.is_approved }}</div>
        <div class="p-2 bg-blue-100 rounded-md">{{ props.post.sent_status }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'

const props = defineProps({
  post: {
    type: Object,
    default: {}
  }
})

const isPostPublic = computed(
  () => !!props.post?.sent_infos?.find(({ chat_username }) => !!chat_username)
)

const load = () => {
  return new Promise((resolve) => {
    const { chat_username, telegram_message_id } = props.post?.sent_infos?.find(
      ({ chat_username }) => !!chat_username
    )

    const script = document.createElement('script')
    script.src = 'https://telegram.org/js/telegram-widget.js?22'
    script.setAttribute('data-telegram-post', `${chat_username}/${telegram_message_id}`)
    script.setAttribute('data-width', '100%')
    if (localStorage.getItem('vueuse-color-scheme') !== 'light') {
      script.setAttribute('data-dark', 1)
    }
    script.onload = resolve

    document.getElementById(`${props.post.id}-post`).append(script);
  })
}

onMounted(() => {
  if (!!props.post?.sent_infos?.find(({ chat_username }) => !!chat_username)) {
    load();
  }
});

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
  return 'Опубликован ' + dayMonthYear + ' ' + timeWithTimezone
};
</script>