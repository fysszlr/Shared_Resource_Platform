<template>
  <loading v-if="loading" />
  <div v-else>
    <TaskPostForAsker v-if="this.task.created_by.user_id == this.$store.state._user_id_ || this.$store.state._role_ === 'Administrator'" :task="task" />
    <TaskPostForOther :task="task" v-else/>
  </div>
</template>

<script>
import TaskPostForAsker from './TaskPostForAsker.vue';
import TaskPostForOther from './TaskPostForOther.vue';
import Loading from '../Loading.vue';
export default({
  components: {
    TaskPostForAsker,
    TaskPostForOther,
    Loading,
  },
  data() {
    return {
      taskId: this.$route.params.id,
      task: null,
      loading: true,
    };
  },
  mounted() {
    this.$store.dispatch("getTaskDetail", { id: this.taskId })
      .then((res) => {
        this.task = res
        this.loading = false
      })
      .catch((err) => {
        this.$store.commit("setAlert", {
          type: "error",
          message: err,
        });
      });
  }
})
</script>
