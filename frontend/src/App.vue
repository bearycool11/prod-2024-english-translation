<script setup>
import { useAuth } from '@/logic/useAuth.js'

useAuth()
</script>

<template>
  <main class="dark:bg-gray-800 shrink h-screen overflow-scroll transform"><RouterView /></main>
</template>

<style scoped></style>
