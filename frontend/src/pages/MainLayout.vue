<template>
  <div class="flex">
    <RouterView />
    <nav class="bg-white border-gray-200 px-8 lg:px-6 py-2.5 dark:bg-gray-800 w-full ">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <a class="flex items-center font-medium text-xl"> Username </a>
        <div class="flex items-center lg:order-2">
          <button type="submit" class="w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800">
            Add org
          </button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script></script>
