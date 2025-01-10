<template>
  <v-container class="spacing-playground pa-16" fluid>
    <component :is="currentComponent" />
  </v-container>
</template>
<script>
import TaskHub from '../../components/Task/TaskHub.vue'

  export default {
    name: 'TasksView',
    components: {
      TaskHub,
    },
    data() {
      return {
        activeBtn: 'TaskHub',
      }
    },
    computed: {
      currentComponent() {
        return this.activeBtn;
      }
    },
    methods: {
      add() {
        this.$router.push('/tasks/add');
      },
      own() {
        this.$router.push('/tasks/own');
      },
    },
    watch: {
    },
    mounted() {
      this.$store.commit("setAppTitle", "任务悬赏站");
    },
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