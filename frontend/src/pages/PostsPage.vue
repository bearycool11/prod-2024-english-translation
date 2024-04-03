<template>
  <div class="flex flex-col w-full h-screen overflow-x-hidden">
    <div class="w-full px-4 mt-16">
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
      <div
        class="overflow-x-hidden"
      >
        <div class="flex py-4 overflow-scroll">
          <button
            @click="() => state.targetTag = 'all'"
            type="button"
            :class="{ 'ml-1 ring-4 outline-none ring-blue-300 dark:ring-blue-800': state.targetTag === 'all' }"
            class="text-blue-700 hover:text-white border border-blue-600 bg-white hover:bg-blue-700 rounded-full text-base font-medium px-4  text-center me-3 mb-3 dark:border-blue-500 dark:text-blue-500 dark:hover:text-white dark:hover:bg-blue-500 dark:bg-gray-900"
          >
            Все
          </button>
          <button
            v-for="tag of tags"
            type="button"
            :key="tag"
            @click="() => state.targetTag = tag"
            :class="{ 'ring-4 outline-none ring-blue-300 dark:ring-gray-800': state.targetTag === tag }"
            class="text-gray-900 border border-white hover:border-gray-200 dark:border-gray-900 dark:bg-gray-900 dark:hover:border-gray-700 bg-white rounded-full text-base font-medium px-5 py-2.5 text-center me-3 mb-3 dark:text-white"
          >
            {{ tag }}
          </button>
        </div>
      </div>
      <div class="grid max-h-80 sm:grid-cols-2 gap-2 w-full mb-4">
        <button
          v-for="(post, index) in targetPosts"
          :key="index"
          @click="openModal(index)"
          class="p-6 bg-white border cursor-pointer focus:bg-neutral-100 hover:bg-neutral-100 dark:focus:bg-gray-700 dark:hover:bg-gray-700 border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 max-w-full"
        >
          <section class="flex flex-col h-full">
            <h3 class="mb-2 text-lg font-bold text-gray-500 dark:text-gray-400">#{{ post.id }}</h3>
            <div class="flex items-center justify-between">
              <h5
                class="mb-2 mr-2 text-lg text-left font-bold text-wrap max-w-md truncate tracking-tight text-gray-900 dark:text-white"
              >
                {{ post.content }}
              </h5>
            </div>
            <div class="flex">
                <p class="text-wrap text-left mb-2 dark:text-white">{{ date(post.planned_time) }}</p>
              </div>
            <div class="flex gap-1 mt-auto">
        
              <div class="flex gap-1 mt-1 flex-wrap  ">
                <div class="p-2 bg-blue-100 dark:bg-blue-400 rounded-md">{{ convertStatuses(post.is_approved) }}</div>
                <div class="p-2 bg-blue-100 dark:bg-blue-400 rounded-md">{{ convertStatuses(post.sent_status) }}</div>
              </div>
            </div>
            <div class="flex mt-2 ml-1 gap-1 max-w-full overflow-scroll">
              <span
                v-for="tag of post.tags"
                class="inline-flex items-center px-2 py-1 text-sm font-medium text-blue-800 bg-blue-200 rounded dark:bg-blue-900 dark:text-blue-600"
                :key="tag"
              >
                {{ tag }}
              </span>
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
    :tags="state.targetPost.tags"
    v-if="state.isShowModal"
  />
</template>
<script setup>
import { computed, onMounted, reactive } from 'vue'
import { api } from '@/logic/api.js'
import ModalPost from '@/components/ModalPost.vue'
import { store } from '@/store/index.js'
import convertStatuses from '../logic/statusesConverter.js'


const state = reactive({
  isShowModal: false,
  targetPost: {},
  creation: false,
  targetTag: 'all'
})

const tags = computed(() => {
  return [...new Set(store.data.posts.map(({ tags }) => tags).flat(2))]
})

const targetPosts = computed(() => {
  if (state.targetTag === 'all') {
    return store.data.posts;
  }

  return store.data.posts.filter((post) => post.tags.includes(state.targetTag))
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
