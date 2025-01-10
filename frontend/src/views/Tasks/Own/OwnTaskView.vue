<template>
  <div class="table-container">
    <v-container fluid class="pa-6">
      <p class="text-h4 mt-6 mb-4">自己发布的悬赏</p>
      <p class="text-subtitle-2 mb-4">查看，关闭自己的悬赏任务</p>
      <v-data-table :headers="headers" :items="ownTasks" class="elevation-0" sticky>
        <template v-slot:item.index="{ index }">
          {{ index + 1 }}
        </template>
        <!-- 操作列 -->
        <template v-slot:item.view="{ item }">
          <!-- 查看按钮 -->
          <v-btn icon color="blue" @click="viewItem(item)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
        </template>
        <!-- 添加标签列 -->
        <template v-slot:item.tags="{ item }">
          <v-chip-group column>
            <v-chip v-for="(tag, index) in item.tags" :key="index" class="ma-2" color="light-green" text-color="white">
              {{ tag }}
            </v-chip>
            </v-chip-group>
            </template>
      </v-data-table>
    </v-container>
  </div>
</template>

<script>
import { format } from 'date-fns';
export default {
  comments: {
    format,
  },
  data() {
    return {
      dialog: false,
      curItem: null,
      headers: [
        { text: "ID", value: "mission" },
        { text: "标题", value: "title" },
        { text: "创建时间", value: "created_at" },
        { text: "费用", value: "commission" },
        { text: "标签", value: "tags" },  // 新增标签列
        { text: "查看", value: "view", sortable: false }, // 添加操作列
      ],
      ownTasks: [],
    };
  },
  methods: {
    format,
    getOwnTask() {
      this.$store.dispatch("ownTasks").then((res) => {
        this.ownTasks = res.posts;
        res.posts.forEach((item, index) => {
          item.index = index + 1;
          item.created_at = format(new Date(item.created_at), "yyyy-MM-dd HH:mm:ss");
        });
      })
        .catch((err) => {
          this.$store.commit("setAlert", {
            color: "error",
            message: err
          });
        });
    },
    // 查看操作
    viewItem(item) {
      window.open(`/tasks/${item.mission}`);
    },
  },
  mounted() {
    this.$store.commit("setAppTitle", "我的任务");
    this.getOwnTask();
  },
};
</script>

<style scoped>
.table-container {
  max-width: 85%; /* 设置表格的最大宽度 */
  margin: 0 auto; /* 居中对齐 */
  display: flex; /* 启用 flexbox 布局 */
  flex-direction: column; /* 纵向排列 */
  align-items: center; /* 水平居中对齐 */
}

.fixed-button1 {
  position: fixed;
  right: 3%;
  bottom: 13%;
  z-index: 5;
}
</style>
