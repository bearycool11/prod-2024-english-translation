<template>
  <div class="flex mt-17 w-full">
    <div class="w-full px-4">
      <h1
        class="text-3xl mb-6 font-bold leading-tight tracking-tight text-gray-900 dark:text-white"
      >
        История постов
      </h1>
      <div class="grid grid-cols-1 gap-2 w-full mb-4 max-w-2xl">
        <history-post v-for="(post, index) in state.posts" :key="index" :post="post" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, reactive } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'
import HistoryPost from '@/components/HistoryPost.vue'

const state = reactive({
  isShowModal: false,
  targetPost: {},
  creation: false,
  posts: []
})

onMounted(() => {
  api.getHistory(props.id).then((data) => {
    state.posts = data
    state.targetPost = {}
  })
})



const props = defineProps({
  id: {
    type: String
  }
})

</script>
