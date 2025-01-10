<template>
  <v-container class="spacing-playground pa-16" fluid>
    <news-list />
  </v-container>
</template>
<script>
  import NewsList from '../../components/Home/News.vue'
  export default {
    name: 'HomeView',
    components: {
      NewsList,
    },
    data() {
      return {
        activeBtn: 'NewsList',
        loading: true,
      }
    },
    computed: {
      currentComponent() {
        return this.activeBtn;
      }
    },
    methods: {

    },
    watch: {
    },
    mounted() {

    }
  }
</script>
<style scoped>
  .v-bottom-navigation {
    bottom: 0;
  }
</style>