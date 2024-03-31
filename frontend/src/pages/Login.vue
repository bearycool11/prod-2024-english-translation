<script setup>
import { computed, reactive, watch } from 'vue'
import { api } from '@/logic/api.js'
import { store } from '@/store/index.js'
import router from '@/router.js'

const state = reactive({
  isAuthForm: false
})
const enterDate = reactive({
  login: '',
  password: '',
  name: ''
})

const toggleAuth = () => {
  state.isAuthForm = !state.isAuthForm
}

const text = computed(() => {
  if (state.isAuthForm) {
    return {
      header: 'Зайди в акканут',
      link: 'Регистрация',
      button: 'Войти'
    }
  }

  return {
    header: 'Зарегистрироваться',
    link: 'Авторизация',
    button: 'Зарегистрироваться'
  }
})

const onEnterClick = () => {
  if (!state.isAuthForm) {
    api.register(enterDate).then(() => {
      store.auth.isAuth = true
      store.auth.isLoading = false
    })
  } else {
    api.login(enterDate).then(() => {
      store.auth.isAuth = true
      store.auth.isLoading = false
    })
  }
}

watch(store.auth, async () => {
  if (store.auth.isAuth && !store.auth.isLoading) {
    await router.push('/')
  }
})
</script>

<template>
  <section class="bg-gray-50 dark:bg-gray-900">
    <div class="flex flex-col items-center justify-center px-6 py-8 mx-auto md:h-screen lg:py-0">
      <a
        href="#"
        class="flex items-center mb-6 text-2xl font-semibold text-gray-900 dark:text-white"
      >
        <img class="w-18 h-8 mr-2" src="/logo.svg" alt="logo" />
      </a>
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white"
          >
            {{ text.header }}
          </h1>
          <form :onsubmit="(e) => e.preventDefault()" class="space-y-4 md:space-y-6" action="#">
            <div v-if="!state.isAuthForm">
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Имя
              </label>
              <input
                type="name"
                name="name"
                id="name"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Имя"
                v-model="enterDate.name"
                required
              />
            </div>
            <div>
              <label
                for="email"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Твой email
              </label>
              <input
                type="login"
                name="login"
                id="login"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Твой логин"
                v-model="enterDate.login"
                required
              />
            </div>
            <div>
              <label
                for="password"
                class="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Пароль
              </label>
              <input
                type="password"
                name="password"
                id="password"
                placeholder="••••••••"
                class="bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                v-model="enterDate.password"
              />
            </div>
            <button
              @click="onEnterClick"
              type="submit"
              class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800"
            >
              {{ text.button }}
            </button>
            <div class="pt-1">
              <a
                @click="toggleAuth"
                class="font-medium cursor-pointer text-primary-600 hover:underline dark:text-primary-500"
              >
                {{ text.link }}
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped></style>
