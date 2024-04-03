<template>
  <div
    class="grid md:grid-cols-3 sm:grid-cols-2 gap-2 w-full p-2 mt-10 flex-wrap"
    v-if="store.data.organizations"
  >
    <a
      v-for="(organization, index) in store.data.organizations"
      :key="index"
      :href="'/organization/' + organization.id"
      class="block overflow-hidden w-full p-6 md:w-full bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
    >
      <h5 class="mb-2 text-2xl font-bold truncate tracking-tight text-gray-900 dark:text-white">
        {{ organization.name }}
      </h5>
      <div class="flex justify-between">
        <p class="font-normal truncate text-gray-700 dark:text-gray-400">
          {{ organization.description }}
        </p>
        <p class="font-light text-sm truncate text-gray-700 dark:text-gray-400">Организация</p>
      </div>
    </a>
  </div>
  <div v-else class="flex justify-center mt-10 w-full">
    <p class="flex px-6 py-2 rounded-md bg-neutral-100 w-auto">У вас еще нет организаций</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'

onMounted(() => {
  api.getOrganizations().then((organizations) => {
    store.data.organizations = organizations
  })
})
</script>
