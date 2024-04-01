<template>
  <div class="flex px-4 mt-20">
    <div class="w-full">
      <!-- <button
          v-if="store.data.canAddBots === false"
          @click="toggleModal"
          class="block text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
        >
          Добавить канал
        </button> -->
      <!-- <div v-else>
          <p class="flex px-6 py-2 rounded-md bg-neutral-100 w-auto">Сначала добавьте бота</p>
        </div> -->
      <div class="flex justify-evenly flex-wrap"></div>

      <div class="flex justify-evenly flex-wrap">
        <div
          v-for="(post, index) in store.data.posts"
          :key="index"
          @click="toggleModal(index)"
          class="mt-4 p-6 bg-white border cursor-pointer border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 max-w-md"
        >
          <div class="flex items-center">
            <h5
              class="mb-2 text-xl font-bold truncate tracking-tight text-gray-900 dark:text-white"
            >
              {{ post.content }}
            </h5>
            <div class="p-2 bg-blue-100 rounded-md mb-2">{{ post.is_approved }}</div>
          </div>
          <div class="flex justify-between items-center">
            <div class="flex">
              <p class="mr-2">Запланирован в</p>
              <p class="truncate max-w-60 w-auto">{{ post.planned_time }} 00:00:00</p>
            </div>
            <div class="p-2 bg-blue-100 rounded-md">{{ post.sent_status }}</div>
          </div>
          <ModalPost
            :isShown="isShowModal[index]"
            :closeModal="closeModal[index]"
            :content="post.content"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '@/logic/api.js'
import ModalPost from '@/components/ModalPost.vue'
import { store } from '@/store/index.js'
const isShowModal = reactive([])

function toggleModal(index) {
  if (isShowModal[index]) {
    isShowModal[index] = false
  } else {
    isShowModal[index] = true
  }
}
onMounted(() => {
  api.getPosts(props.id).then((data) => {
    store.data.posts = data
  })
})

function closeModal(index) {
  isShowModal[index] = false
}

const props = defineProps({
  id: {
    type: String
  }
})
</script>
