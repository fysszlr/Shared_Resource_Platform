<template>
  <v-alert
    elevation="11"
    v-show="$store.state._alert_.show != 0"
    :type="['success', 'info', 'warning', 'error'].includes($store.state._alert_.type) ? $store.state._alert_.type : 'info'"
    transition="scroll-y-transition"
    dense
    prominent
  >
    {{ $store.state._alert_.message }}
  </v-alert>
</template>

<style scoped>
  .v-alert {
    z-index: 999;
    position: fixed;
    bottom: 0;
    width: 105%;
    margin-bottom: 0;
    height: fit-content;
  }
</style>