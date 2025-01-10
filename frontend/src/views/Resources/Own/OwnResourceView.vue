<template>
  <div class="table-container">
    <v-container fluid class="pa-6">
      <p class="text-h4 mt-6 mb-4">自己分享的所有资源</p>
      <p class="text-subtitle-2 mb-4">查看，修改自己的资源分享贴</p>
      <v-data-table :headers="headers" :items="ownShare" sticky>
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
      </v-data-table>
    </v-container>
  </div>
</template>

<script>
import { format } from 'date-fns';
export default {
  components: {
    format,
  },
  data() {
    return {
      dialog: false,
      curItem: null,
      headers: [
        { text: "ID", value: "post_id" },
        { text: "标题", value: "title" },
        { text: "创建时间", value: "created_at" },
        { text: "费用", value: "cost" },
        { text: "点赞数", value: "likes" },
        { text: "点踩数", value: "dislikes" },
        { text: "收藏数", value: "favorites" },
        { text: "查看", value: "view", sortable: false }, // 添加操作列
      ],
      ownShare: [],
    };
  },
  methods: {
    format,
    // 获取所有用户数据
    getOwnShare() {
      this.$store.dispatch("ownPosts")
        .then((res) => {
          this.ownShare = res.posts.map((item, index) => {
            return {
              index: index + 1,
              post_id: item.post_id,
              title: item.title,
              created_at: format(new Date(item.created_at), "yyyy-MM-dd HH:mm:ss"),
              cost: item.cost,
              likes: item.likes,
              dislikes: item.dislikes,
              favorites: item.favorites,
              view: item,
            };
          });
        })
        .catch((err) => { this.$store.commit("setAlert", { type: "error", message: err, }); });
    },
    // 查看操作
    viewItem(item) {
      window.open(`/resources/${item.post_id}`);
    },
  },
  mounted() {
    this.$store.commit("setAppTitle", "我的资源");
    this.getOwnShare();
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