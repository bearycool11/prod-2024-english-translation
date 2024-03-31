<template>
  <div class="flex">
    <RouterView />
    <nav class="bg-white border-gray-200 px-8 lg:px-6 py-2.5 dark:bg-gray-800 w-full ">
      <div class="flex flex-wrap justify-between items-center mx-auto max-w-screen-xl">
        <a class="flex items-center font-medium text-xl"> Username </a>
        <div class="flex items-center lg:order-2">
          <button
            class="text-gray-800 dark:text-white hover:bg-gray-50 focus:ring-4 focus:ring-gray-300 font-medium rounded-lg text-sm px-4 lg:px-5 py-2 lg:py-2.5 mr-2 dark:hover:bg-gray-700 focus:outline-none dark:focus:ring-gray-800"
          >
            Add org
          </button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script></script>
