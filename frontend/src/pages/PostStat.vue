<template>
  <div class="flex flex-col mt-20 w-full">
    <h1
      class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
    >
      Пост
    </h1>
    <div id="widget_login"></div>
  </div>
</template>

<script setup>
const props = defineProps({
  id: {
    type: String
  },
  post: {
    type: String
  }
})
</script>
