<template>
  <div class="flex mt-20 w-full h-screen overflow-y-auto ">
    <div class="w-full px-4">
      <button
        v-if="
          store.auth.permissions.some(
            (obj) => obj.name === 'editor' || obj.name === 'admin' || obj.name === 'owner'
          )
        "
        @click="openCreateModal"
        class="block text-white mb-4 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        Добавить пост
      </button>
      <div class="grid md:grid-cols-3 max-h-80 sm:grid-cols-2 gap-2 w-full mb-4">
        <button
          v-for="(post, index) in store.data.posts"
          :key="index"
          @click="openModal(index)"
          class="p-6 min-w-sm bg-white border cursor-pointer border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 max-w-md"
        >
          <section class="flex flex-col h-full">
            <h3 class="mb-5 text-lg font-bold text-gray-500 dark:text-gray-400">
              #{{ post.id }}
            </h3>
            <div class="flex items-center justify-between">
              <h5
                class="mb-2 mr-2 text-lg text-left font-bold text-wrap max-w-md truncate tracking-tight text-gray-900 dark:text-white"
              >
                {{ post.content }}
              </h5>
            </div>
            <div class="flex gap-1 mt-auto flex-wrap">
              <div class="flex">
                <p class="text-wrap text-left dark:text-white">{{ date(post.planned_time) }}</p>
              </div>

              <div class="flex gap-1 mt-1 flex-wrap">
                <div class="p-2 bg-blue-100 rounded-md">{{ post.is_approved }}</div>
                <div class="p-2 bg-blue-100 rounded-md">{{ post.sent_status }}</div>
              </div>
            </div>
          </section>
        </button>
      </div>
    </div>
  </div>
  <ModalPost
    :isShown="state.isShowModal"
    :closeModal="closeModal"
    :content="state.targetPost"
    :creation="state.creation"
    :id="props.id"
    :post_id="state.targetPost.id"
    :channels="store.data.channels"
    v-if="state.isShowModal"
  />
</template>
<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '@/logic/api.js'
import ModalPost from '@/components/ModalPost.vue'
import { store } from '@/store/index.js'

const state = reactive({
  isShowModal: false,
  targetPost: {},
  creation: false
})

function openModal(index) {
  state.targetPost = store.data.posts[index]
  state.isShowModal = true
}

function openCreateModal() {
  state.targetPost = {}
  state.isShowModal = true
  state.creation = true
}

onMounted(() => {
  api.getPosts(props.id).then((data) => {
    store.data.posts = data
    state.targetPost = {}
  })
})

function closeModal() {
  state.isShowModal = false
  state.creation = false
}

const props = defineProps({
  id: {
    type: String
  }
})


const date = (utcIsoString) => {
  if (!utcIsoString) {
    return ''
  }

  const londonTime = new Date(utcIsoString)

  const localTimezoneOffset = new Date().getTimezoneOffset()
  const localTime = new Date(londonTime.getTime() - localTimezoneOffset * 60000)

  const formattedLocalTime = `${String(localTime.getDate()).padStart(2, '0')}.${String(localTime.getMonth() + 1).padStart(2, '0')}.${localTime.getFullYear()} ${String(localTime.getHours()).padStart(2, '0')}:${String(localTime.getMinutes()).padStart(2, '0')}`

  return 'Запланирован ' + formattedLocalTime
}
</script>
