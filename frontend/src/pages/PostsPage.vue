<template>
  <div class="flex px-4 mt-20">
    <div class="w-full">
      <button
        v-if="store.auth.permissions.some(obj => obj.name === 'editor' || obj.name === 'admin' || obj.name === 'owner')"
        @click="openCreateModal"
        class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        Добавить пост
      </button>
      <div class="flex justify-evenly flex-wrap"></div>

      <div class="flex justify-evenly flex-wrap">
        <button
          v-for="(post, index) in store.data.posts"
          :key="index"
          @click="openModal(index)"
          class="mt-4 p-6 mx-2 min-w-sm w-80 bg-white border cursor-pointer border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 max-w-md"
        >
          <div class="flex items-center justify-between">
            <h5
              class="mb-2 mr-2 text-lg font-bold text-wrap max-w-md truncate tracking-tight text-gray-900 dark:text-white"
            >
              {{ post.content }}
            </h5>
            <div class="p-2 bg-blue-100 rounded-md mb-2">{{ post.is_approved }}</div>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex">
              <p class="mr-2 text-wrap">{{ date(post.planned_time) }}</p>
            </div>
            <div class="p-2 bg-blue-100 rounded-md">{{ post.sent_status }}</div>
          </div>
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

const date = (isoString) => {
  {
    // Check if the input is null
    if (isoString === null) {
      return ''
    }

    // Parse the ISO string into a Date object
    const date = new Date(isoString)

    // Extract the day, month, year, hours, and minutes
    const day = date.getDate()
    const month = date.getMonth() + 1 // Months are 0-based in JavaScript
    const year = date.getFullYear()
    const hours = date.getHours()
    const minutes = date.getMinutes()

    // Format the values into DD.MM.YYYY HH:MM
    const formattedDate = `${day < 10 ? '0' + day : day}.${month < 10 ? '0' + month : month}.${year} ${hours < 10 ? '0' + hours : hours}:${minutes < 10 ? '0' + minutes : minutes}`

    return 'Запланирован ' + formattedDate
  }
}
</script>