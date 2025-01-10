<template>
  <v-container class="spacing-playground pa-16" fluid>
    <component :is="currentComponent" />
  </v-container>
</template>

<script>
import ShareHub from '../../components/Share/ShareHub.vue'

export default {
  name: 'ShareView',
  components: {
    ShareHub,
  },
  data() {
    return {
      activeBtn: 'ShareHub',
      loading: true,
    }
  },
  computed: {
    currentComponent() {
      return this.activeBtn;
    }
  },
  methods: {
    add() {
      this.$router.push('/resources/share');
    },
    own() {
      this.$router.push('/resources/own');
    }
  },
  watch: {
  }
}
</script>

<style scoped>
.v-bottom-navigation {
  bottom: 0;
}

.fixed-button1 {
  position: fixed;
  right: 4%;
  bottom: 16%;
  z-index: 5;
}

.fixed-button2 {
  position: fixed;
  right: 4%;
  bottom: 8%;
  z-index: 5;
}
</style>